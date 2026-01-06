/* global fetch, document */

const plannerCandidates = [
  '../planner-output',
  '../artifacts/planner-output',
  '../logs/planner-output',
  '..',
];

const dataSources = {
  arbitration: '../logs/arbitration-decision.json',
  conceptGraph: '../logs/concept-graph.json',
  enforcementEvents: '../logs/events.jsonl',
};

function qs(id) {
  return document.getElementById(id);
}

function setStatus(id, message) {
  const el = qs(id);
  if (el) {
    el.textContent = message;
  }
}

function escapeHtml(value) {
  const span = document.createElement('span');
  span.textContent = value === undefined || value === null ? '' : String(value);
  return span.innerHTML;
}

async function fetchJson(path) {
  try {
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) {
      return null;
    }
    return await response.json();
  } catch (err) {
    return null;
  }
}

async function fetchJsonl(path) {
  try {
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) {
      return null;
    }
    const text = await response.text();
    if (!text.trim()) {
      return [];
    }
    return text
      .trim()
      .split('\n')
      .map((line) => {
        try {
          return JSON.parse(line);
        } catch (err) {
          return null;
        }
      })
      .filter(Boolean);
  } catch (err) {
    return null;
  }
}

async function loadPlannerArtifacts() {
  for (const candidate of plannerCandidates) {
    const taskGraph = await fetchJson(`${candidate}/task_graph.json`);
    if (!taskGraph) {
      continue;
    }
    const conceptMap = await fetchJson(`${candidate}/concept_map.json`);
    const requiredSyncs = await fetchJson(`${candidate}/required_syncs.json`);
    if (conceptMap && requiredSyncs) {
      return {
        base: candidate,
        taskGraph,
        conceptMap,
        requiredSyncs,
      };
    }
  }
  return null;
}

function renderPlanning(data) {
  const tasksEl = qs('planning-tasks');
  const syncsEl = qs('planning-syncs');
  if (!tasksEl || !syncsEl) {
    return;
  }

  if (!data) {
    tasksEl.innerHTML = '<p class="status">Planner artifacts not found.</p>';
    syncsEl.innerHTML = '<p class="status">No required syncs loaded.</p>';
    return;
  }

  const taskRows = (data.taskGraph.tasks || []).map((task) => {
    const taskId = task.task_id || '';
    const conceptEntry = (data.conceptMap.tasks || []).find((entry) => entry.task_id === taskId);
    const concept = conceptEntry ? conceptEntry.concept : 'unmapped';
    return {
      task_id: taskId,
      description: task.description || '',
      concept,
      depends_on: Array.isArray(task.depends_on) ? task.depends_on.join(', ') : '',
    };
  });

  if (!taskRows.length) {
    tasksEl.innerHTML = '<p class="status">No tasks in task_graph.json.</p>';
  } else {
    const rows = taskRows
      .map(
        (row) =>
          `<tr><td>${escapeHtml(row.task_id)}</td><td>${escapeHtml(row.description)}</td><td>${escapeHtml(
            row.concept
          )}</td><td>${escapeHtml(row.depends_on)}</td></tr>`
      )
      .join('');
    tasksEl.innerHTML = `
      <table>
        <thead><tr><th>Task</th><th>Description</th><th>Concept</th><th>Depends On</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>
    `;
  }

  const syncs = (data.requiredSyncs.synchronizations || []).map((sync) => {
    return `${sync.sync_id} (${sync.from_concept} -> ${sync.to_concept}, ${sync.status})`;
  });

  if (!syncs.length) {
    syncsEl.innerHTML = '<p class="status">No required synchronizations declared.</p>';
  } else {
    syncsEl.innerHTML = `<div class="list">${syncs.map((item) => `<div>${escapeHtml(item)}</div>`).join('')}</div>`;
  }
}

function renderArbitration(data) {
  const orderEl = qs('arbitration-order');
  const blockedEl = qs('arbitration-blocked');
  if (!orderEl || !blockedEl) {
    return;
  }

  if (!data) {
    orderEl.innerHTML = '<p class="status">No arbitration log found.</p>';
    blockedEl.innerHTML = '<p class="status">No blocked tasks to show.</p>';
    return;
  }

  const order = Array.isArray(data.order) ? data.order : [];
  if (!order.length) {
    orderEl.innerHTML = '<p class="status">No ordered tasks in arbitration log.</p>';
  } else {
    orderEl.innerHTML = `<ol>${order.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ol>`;
  }

  const blocked = Array.isArray(data.blocked) ? data.blocked : [];
  if (!blocked.length) {
    blockedEl.innerHTML = '<p class="status">No blocked tasks.</p>';
  } else {
    blockedEl.innerHTML = blocked
      .map((item) => {
        const reasons = Array.isArray(item.reasons) ? item.reasons.join(', ') : '';
        return `<div><span class="badge">${escapeHtml(item.task_id)}</span>${escapeHtml(reasons)}</div>`;
      })
      .join('');
  }
}

function renderConcepts(data) {
  const listEl = qs('concepts-list');
  const depsEl = qs('concepts-deps');
  if (!listEl || !depsEl) {
    return;
  }

  if (!data || !Array.isArray(data.concepts)) {
    listEl.innerHTML = '<p class="status">No concept graph artifact found.</p>';
    depsEl.innerHTML = '<p class="status">Dependencies unavailable.</p>';
    return;
  }

  listEl.innerHTML = `<div class="list">${data.concepts
    .map((concept) => `<div>${escapeHtml(concept.name || concept)}</div>`)
    .join('')}</div>`;

  const edges = Array.isArray(data.edges) ? data.edges : [];
  if (!edges.length) {
    depsEl.innerHTML = '<p class="status">No dependency edges available.</p>';
    return;
  }

  depsEl.innerHTML = `<div class="list">${edges
    .map((edge) => `${escapeHtml(edge.from)} -> ${escapeHtml(edge.to)}`)
    .map((line) => `<div>${line}</div>`)
    .join('')}</div>`;
}

function renderEnforcement(events) {
  const eventsEl = qs('enforcement-events');
  if (!eventsEl) {
    return;
  }

  if (!events || !events.length) {
    eventsEl.innerHTML = '<p class="status">No enforcement events found.</p>';
    return;
  }

  const sorted = events.slice().sort((a, b) => {
    const aTime = Date.parse(a.timestamp || 0);
    const bTime = Date.parse(b.timestamp || 0);
    return bTime - aTime;
  });

  const rows = sorted.slice(0, 12).map((event) => {
    const meta = `${event.type || 'event'}:${event.status || 'unknown'}`;
    const message = event.message || '';
    return `<div><span class="badge">${escapeHtml(meta)}</span>${escapeHtml(message)}</div>`;
  });

  eventsEl.innerHTML = `<div class="list">${rows.join('')}</div>`;
}

async function init() {
  const planner = await loadPlannerArtifacts();
  setStatus('planning-status', planner ? `Planner artifacts loaded from ${planner.base}.` : 'Planner artifacts not found.');
  renderPlanning(planner);

  const arbitration = await fetchJson(dataSources.arbitration);
  setStatus('arbitration-status', arbitration ? 'Arbitration log loaded.' : 'Arbitration log missing.');
  renderArbitration(arbitration);

  const concepts = await fetchJson(dataSources.conceptGraph);
  setStatus('concepts-status', concepts ? 'Concept graph loaded.' : 'Concept graph missing.');
  renderConcepts(concepts);

  const events = await fetchJsonl(dataSources.enforcementEvents);
  setStatus('enforcement-status', events ? 'Enforcement events loaded.' : 'Enforcement events missing.');
  renderEnforcement(events);
}

init();
