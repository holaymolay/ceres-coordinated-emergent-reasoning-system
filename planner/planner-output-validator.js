#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');

function usage() {
  console.error('Usage: node planner/planner-output-validator.js --dir <planner-output-dir>');
  console.error('Optional: --task-graph <path> --concept-map <path> --required-syncs <path>');
}

function readJson(filePath, errors) {
  if (!fs.existsSync(filePath)) {
    errors.push(`Missing file: ${filePath}`);
    return null;
  }
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (err) {
    errors.push(`Invalid JSON in ${filePath}: ${err.message}`);
    return null;
  }
}

function isNonEmptyString(value) {
  return typeof value === 'string' && value.trim() !== '';
}

function ensureArray(value) {
  return Array.isArray(value) ? value : null;
}

function validateTaskGraph(taskGraph, filePath, errors) {
  if (!taskGraph || typeof taskGraph !== 'object' || Array.isArray(taskGraph)) {
    errors.push(`task_graph.json must be an object (${filePath}).`);
    return { taskIds: new Set(), edges: [] };
  }

  const tasks = ensureArray(taskGraph.tasks);
  const edges = ensureArray(taskGraph.edges);

  if (!tasks) {
    errors.push(`task_graph.json must include a tasks array (${filePath}).`);
  }
  if (!edges) {
    errors.push(`task_graph.json must include an edges array (${filePath}).`);
  }

  const taskIds = new Set();
  if (tasks) {
    tasks.forEach((task, index) => {
      if (!task || typeof task !== 'object' || Array.isArray(task)) {
        errors.push(`task_graph.json tasks[${index}] must be an object (${filePath}).`);
        return;
      }
      if (!isNonEmptyString(task.task_id)) {
        errors.push(`task_graph.json tasks[${index}] missing task_id (${filePath}).`);
      }
      if (!isNonEmptyString(task.description)) {
        errors.push(`task_graph.json tasks[${index}] missing description (${filePath}).`);
      }
      if (isNonEmptyString(task.task_id)) {
        if (taskIds.has(task.task_id)) {
          errors.push(`Duplicate task_id '${task.task_id}' in task_graph.json (${filePath}).`);
        }
        taskIds.add(task.task_id);
      }
      if (task.depends_on !== undefined) {
        if (!Array.isArray(task.depends_on)) {
          errors.push(`task_graph.json tasks[${index}].depends_on must be an array (${filePath}).`);
        }
      }
    });
  }

  const normalizedEdges = [];
  const edgeKeys = new Set();
  if (edges) {
    edges.forEach((edge, index) => {
      if (!edge || typeof edge !== 'object' || Array.isArray(edge)) {
        errors.push(`task_graph.json edges[${index}] must be an object (${filePath}).`);
        return;
      }
      if (!isNonEmptyString(edge.from) || !isNonEmptyString(edge.to)) {
        errors.push(`task_graph.json edges[${index}] must include from/to (${filePath}).`);
        return;
      }
      const key = `${edge.from}::${edge.to}`;
      if (edgeKeys.has(key)) {
        errors.push(`Duplicate edge '${edge.from}' -> '${edge.to}' in task_graph.json (${filePath}).`);
      }
      edgeKeys.add(key);
      if (taskIds.size && !taskIds.has(edge.from)) {
        errors.push(`Edge references unknown task '${edge.from}' (${filePath}).`);
      }
      if (taskIds.size && !taskIds.has(edge.to)) {
        errors.push(`Edge references unknown task '${edge.to}' (${filePath}).`);
      }
      normalizedEdges.push({ from: edge.from, to: edge.to });
    });
  }

  const dependsOnEdges = new Set(normalizedEdges.map((edge) => `${edge.from}::${edge.to}`));
  if (tasks) {
    tasks.forEach((task) => {
      if (!task || !isNonEmptyString(task.task_id) || !Array.isArray(task.depends_on)) {
        return;
      }
      task.depends_on.forEach((dep) => {
        if (!isNonEmptyString(dep)) {
          errors.push(`Task '${task.task_id}' has an empty dependency entry (${filePath}).`);
          return;
        }
        if (!taskIds.has(dep)) {
          errors.push(`Task '${task.task_id}' depends_on unknown task '${dep}' (${filePath}).`);
          return;
        }
        const key = `${dep}::${task.task_id}`;
        if (!dependsOnEdges.has(key)) {
          errors.push(
            `Implicit dependency for task '${task.task_id}': depends_on '${dep}' not declared in edges (${filePath}).`
          );
        }
      });
    });
  }

  if (taskIds.size && normalizedEdges.length) {
    const adjacency = new Map();
    for (const id of taskIds) {
      adjacency.set(id, []);
    }
    normalizedEdges.forEach((edge) => {
      if (!adjacency.has(edge.from)) {
        adjacency.set(edge.from, []);
      }
      adjacency.get(edge.from).push(edge.to);
    });

    const visiting = new Set();
    const visited = new Set();
    let cyclePath = null;

    function dfs(node, stack) {
      if (cyclePath) {
        return;
      }
      if (visiting.has(node)) {
        const cycleStart = stack.indexOf(node);
        if (cycleStart !== -1) {
          cyclePath = stack.slice(cycleStart).concat(node);
        } else {
          cyclePath = stack.concat(node);
        }
        return;
      }
      if (visited.has(node)) {
        return;
      }
      visiting.add(node);
      stack.push(node);
      for (const next of adjacency.get(node) || []) {
        dfs(next, stack);
      }
      stack.pop();
      visiting.delete(node);
      visited.add(node);
    }

    for (const id of taskIds) {
      if (!visited.has(id)) {
        dfs(id, []);
      }
      if (cyclePath) {
        break;
      }
    }

    if (cyclePath) {
      errors.push(`Task graph contains a cycle: ${cyclePath.join(' -> ')} (${filePath}).`);
    }
  }

  return { taskIds, edges: normalizedEdges };
}

function validateConceptMap(conceptMap, filePath, taskIds, errors) {
  if (!conceptMap || typeof conceptMap !== 'object' || Array.isArray(conceptMap)) {
    errors.push(`concept_map.json must be an object (${filePath}).`);
    return { taskConcept: new Map(), concepts: new Set() };
  }

  const tasks = ensureArray(conceptMap.tasks);
  if (!tasks) {
    errors.push(`concept_map.json must include a tasks array (${filePath}).`);
    return { taskConcept: new Map(), concepts: new Set() };
  }

  const taskConcept = new Map();
  const concepts = new Set();

  tasks.forEach((entry, index) => {
    if (!entry || typeof entry !== 'object' || Array.isArray(entry)) {
      errors.push(`concept_map.json tasks[${index}] must be an object (${filePath}).`);
      return;
    }
    if (!isNonEmptyString(entry.task_id)) {
      errors.push(`concept_map.json tasks[${index}] missing task_id (${filePath}).`);
      return;
    }
    if (!isNonEmptyString(entry.concept)) {
      errors.push(`concept_map.json tasks[${index}] missing concept (${filePath}).`);
      return;
    }
    if (taskConcept.has(entry.task_id)) {
      errors.push(`Task '${entry.task_id}' mapped to multiple concepts in concept_map.json (${filePath}).`);
      return;
    }
    taskConcept.set(entry.task_id, entry.concept);
    concepts.add(entry.concept);
  });

  if (taskIds.size) {
    for (const taskId of taskIds) {
      if (!taskConcept.has(taskId)) {
        errors.push(`Task '${taskId}' missing concept mapping in concept_map.json (${filePath}).`);
      }
    }
    for (const taskId of taskConcept.keys()) {
      if (!taskIds.has(taskId)) {
        errors.push(`concept_map.json references unknown task '${taskId}' (${filePath}).`);
      }
    }
  }

  return { taskConcept, concepts };
}

function validateRequiredSyncs(requiredSyncs, filePath, conceptSet, errors) {
  if (!requiredSyncs || typeof requiredSyncs !== 'object' || Array.isArray(requiredSyncs)) {
    errors.push(`required_syncs.json must be an object (${filePath}).`);
    return [];
  }
  const syncs = ensureArray(requiredSyncs.synchronizations);
  if (!syncs) {
    errors.push(`required_syncs.json must include a synchronizations array (${filePath}).`);
    return [];
  }

  const syncIds = new Set();
  const normalized = [];

  syncs.forEach((sync, index) => {
    if (!sync || typeof sync !== 'object' || Array.isArray(sync)) {
      errors.push(`required_syncs.json synchronizations[${index}] must be an object (${filePath}).`);
      return;
    }
    if (!isNonEmptyString(sync.sync_id)) {
      errors.push(`required_syncs.json synchronizations[${index}] missing sync_id (${filePath}).`);
      return;
    }
    if (!isNonEmptyString(sync.from_concept) || !isNonEmptyString(sync.to_concept)) {
      errors.push(`required_syncs.json synchronizations[${index}] missing from_concept/to_concept (${filePath}).`);
      return;
    }
    if (!isNonEmptyString(sync.status) || !['existing', 'new'].includes(sync.status)) {
      errors.push(`required_syncs.json synchronizations[${index}] status must be 'existing' or 'new' (${filePath}).`);
      return;
    }
    if (syncIds.has(sync.sync_id)) {
      errors.push(`Duplicate sync_id '${sync.sync_id}' in required_syncs.json (${filePath}).`);
      return;
    }
    syncIds.add(sync.sync_id);

    if (conceptSet.size) {
      if (!conceptSet.has(sync.from_concept)) {
        errors.push(
          `required_syncs.json sync '${sync.sync_id}' references unknown concept '${sync.from_concept}' (${filePath}).`
        );
      }
      if (!conceptSet.has(sync.to_concept)) {
        errors.push(
          `required_syncs.json sync '${sync.sync_id}' references unknown concept '${sync.to_concept}' (${filePath}).`
        );
      }
    }

    normalized.push({
      sync_id: sync.sync_id,
      from_concept: sync.from_concept,
      to_concept: sync.to_concept,
      status: sync.status,
    });
  });

  return normalized;
}

function validateCrossConceptDeps(edges, taskConcept, requiredSyncs, errors, filePath) {
  const requiredPairs = new Set(
    requiredSyncs.map((sync) => `${sync.from_concept}::${sync.to_concept}`)
  );

  edges.forEach((edge) => {
    const fromConcept = taskConcept.get(edge.from);
    const toConcept = taskConcept.get(edge.to);
    if (!fromConcept || !toConcept) {
      return;
    }
    if (fromConcept === toConcept) {
      return;
    }
    const key = `${fromConcept}::${toConcept}`;
    if (!requiredPairs.has(key)) {
      errors.push(
        `Missing required synchronization for dependency ${edge.from}(${fromConcept}) -> ${edge.to}(${toConcept}) (${filePath}).`
      );
    }
  });
}

function main() {
  const args = process.argv.slice(2);
  let outputDir = process.cwd();
  let taskGraphPath = null;
  let conceptMapPath = null;
  let requiredSyncsPath = null;

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === '--dir' && args[i + 1]) {
      outputDir = path.resolve(args[i + 1]);
      i += 1;
    } else if (arg === '--task-graph' && args[i + 1]) {
      taskGraphPath = path.resolve(args[i + 1]);
      i += 1;
    } else if (arg === '--concept-map' && args[i + 1]) {
      conceptMapPath = path.resolve(args[i + 1]);
      i += 1;
    } else if (arg === '--required-syncs' && args[i + 1]) {
      requiredSyncsPath = path.resolve(args[i + 1]);
      i += 1;
    } else if (arg === '--help' || arg === '-h') {
      usage();
      return;
    }
  }

  const taskGraphFile = taskGraphPath ?? path.join(outputDir, 'task_graph.json');
  const conceptMapFile = conceptMapPath ?? path.join(outputDir, 'concept_map.json');
  const requiredSyncsFile = requiredSyncsPath ?? path.join(outputDir, 'required_syncs.json');

  const errors = [];

  const taskGraph = readJson(taskGraphFile, errors);
  const conceptMap = readJson(conceptMapFile, errors);
  const requiredSyncs = readJson(requiredSyncsFile, errors);

  const taskGraphValidation = validateTaskGraph(taskGraph, taskGraphFile, errors);
  const conceptValidation = validateConceptMap(
    conceptMap,
    conceptMapFile,
    taskGraphValidation.taskIds,
    errors
  );
  const requiredSyncsValidation = validateRequiredSyncs(
    requiredSyncs,
    requiredSyncsFile,
    conceptValidation.concepts,
    errors
  );

  validateCrossConceptDeps(
    taskGraphValidation.edges,
    conceptValidation.taskConcept,
    requiredSyncsValidation,
    errors,
    requiredSyncsFile
  );

  if (errors.length) {
    const unique = [...new Set(errors)];
    console.error(`Planner output validation failed with ${unique.length} error(s):`);
    unique.forEach((error) => console.error(`- ${error}`));
    process.exit(1);
  }

  console.log('Planner output validation passed.');
}

main();
