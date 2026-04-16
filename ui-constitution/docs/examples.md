# Examples (Valid vs Invalid)

## Valid
```json
{
  "version": "0.1.0",
  "typography": {
    "font_size_scale": [12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72],
    "line_height_bounds": { "min": 1.2, "max": 1.6 },
    "max_distinct_sizes_per_page": 8,
    "heading_sizes": [24, 30, 36, 48, 60, 72],
    "body_sizes": [12, 14, 16, 18, 20]
  },
  "spacing": {
    "spacing_scale": [4, 8, 12, 16, 24, 32, 40, 48, 64],
    "min_spacing": 4,
    "max_spacing": 64,
    "vertical_rhythm_unit": 4,
    "vertical_rhythm_strict": true
  },
  "color": {
    "color_roles": [
      "primary",
      "secondary",
      "background",
      "surface",
      "text",
      "text-muted",
      "border",
      "success",
      "warning",
      "danger",
      "info"
    ],
    "allow_arbitrary_colors": false,
    "contrast_floor": 4.5,
    "contrast_pairs": [
      { "foreground_role": "text", "background_role": "background", "min_ratio": 4.5 },
      { "foreground_role": "text", "background_role": "surface", "min_ratio": 4.5 }
    ]
  },
  "elevation": {
    "elevation_levels": [0, 1, 2, 3, 4],
    "max_elevation_level": 4,
    "shadow_styles": ["none", "ambient", "direct"],
    "max_shadows_per_surface": 1,
    "prohibited_combinations": [
      { "elevation_level": 0, "shadow_style": "ambient" },
      { "elevation_level": 0, "shadow_style": "direct" }
    ]
  },
  "radius": {
    "radius_values": [0, 2, 4, 6, 8, 12, 16],
    "max_radius_variants_per_surface": 2,
    "surface_type_variance": {
      "container": { "max_radius_variance": 8 },
      "control": { "max_radius_variance": 6 },
      "overlay": { "max_radius_variance": 8 }
    }
  },
  "motion": {
    "allowed_states": ["enter", "exit", "state-change", "feedback", "progress"],
    "disallowed_states": ["decorative-loop", "ambient-loop", "auto-play"],
    "duration_ms_bounds": { "min": 80, "max": 600 },
    "easing_functions": ["linear", "ease", "ease-in", "ease-out", "ease-in-out"],
    "motion_off_switch_required": true,
    "reduced_motion_behavior": "disable"
  },
  "assets": {
    "icon_set": {
      "name": "core-icons",
      "version": "1.0.0",
      "source": "local",
      "license": "MIT"
    },
    "image_usage": {
      "allowed_types": ["photo", "illustration", "diagram", "screenshot"],
      "allowed_formats": ["jpg", "png", "webp", "svg"],
      "max_images_per_page": 6
    },
    "aspect_ratios_allowed": ["1:1", "4:3", "3:2", "16:9", "2:3", "9:16"],
    "aspect_ratio_enforced": true,
    "decorative_assets_allowed": false
  }
}
```

## Invalid (arbitrary color allowed)
```json
{
  "version": "0.1.0",
  "typography": {
    "font_size_scale": [12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72],
    "line_height_bounds": { "min": 1.2, "max": 1.6 },
    "max_distinct_sizes_per_page": 8,
    "heading_sizes": [24, 30, 36, 48, 60, 72],
    "body_sizes": [12, 14, 16, 18, 20]
  },
  "spacing": {
    "spacing_scale": [4, 8, 12, 16, 24, 32, 40, 48, 64],
    "min_spacing": 4,
    "max_spacing": 64,
    "vertical_rhythm_unit": 4,
    "vertical_rhythm_strict": true
  },
  "color": {
    "color_roles": [
      "primary",
      "secondary",
      "background",
      "surface",
      "text",
      "text-muted",
      "border",
      "success",
      "warning",
      "danger",
      "info"
    ],
    "allow_arbitrary_colors": true,
    "contrast_floor": 4.5,
    "contrast_pairs": [
      { "foreground_role": "text", "background_role": "background", "min_ratio": 4.5 }
    ]
  },
  "elevation": {
    "elevation_levels": [0, 1, 2, 3, 4],
    "max_elevation_level": 4,
    "shadow_styles": ["none", "ambient", "direct"],
    "max_shadows_per_surface": 1,
    "prohibited_combinations": [
      { "elevation_level": 0, "shadow_style": "ambient" },
      { "elevation_level": 0, "shadow_style": "direct" }
    ]
  },
  "radius": {
    "radius_values": [0, 2, 4, 6, 8, 12, 16],
    "max_radius_variants_per_surface": 2,
    "surface_type_variance": {
      "container": { "max_radius_variance": 8 },
      "control": { "max_radius_variance": 6 },
      "overlay": { "max_radius_variance": 8 }
    }
  },
  "motion": {
    "allowed_states": ["enter", "exit", "state-change", "feedback", "progress"],
    "disallowed_states": ["decorative-loop", "ambient-loop", "auto-play"],
    "duration_ms_bounds": { "min": 80, "max": 600 },
    "easing_functions": ["linear", "ease", "ease-in", "ease-out", "ease-in-out"],
    "motion_off_switch_required": true,
    "reduced_motion_behavior": "disable"
  },
  "assets": {
    "icon_set": {
      "name": "core-icons",
      "version": "1.0.0",
      "source": "local",
      "license": "MIT"
    },
    "image_usage": {
      "allowed_types": ["photo", "illustration", "diagram", "screenshot"],
      "allowed_formats": ["jpg", "png", "webp", "svg"],
      "max_images_per_page": 6
    },
    "aspect_ratios_allowed": ["1:1", "4:3", "3:2", "16:9", "2:3", "9:16"],
    "aspect_ratio_enforced": true,
    "decorative_assets_allowed": false
  }
}
```

## Invalid (spacing scale contains a non-allowed value)
```json
{
  "version": "0.1.0",
  "typography": {
    "font_size_scale": [12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72],
    "line_height_bounds": { "min": 1.2, "max": 1.6 },
    "max_distinct_sizes_per_page": 8,
    "heading_sizes": [24, 30, 36, 48, 60, 72],
    "body_sizes": [12, 14, 16, 18, 20]
  },
  "spacing": {
    "spacing_scale": [4, 6, 12, 16, 24, 32, 40, 48, 64],
    "min_spacing": 4,
    "max_spacing": 64,
    "vertical_rhythm_unit": 4,
    "vertical_rhythm_strict": true
  },
  "color": {
    "color_roles": [
      "primary",
      "secondary",
      "background",
      "surface",
      "text",
      "text-muted",
      "border",
      "success",
      "warning",
      "danger",
      "info"
    ],
    "allow_arbitrary_colors": false,
    "contrast_floor": 4.5,
    "contrast_pairs": [
      { "foreground_role": "text", "background_role": "background", "min_ratio": 4.5 }
    ]
  },
  "elevation": {
    "elevation_levels": [0, 1, 2, 3, 4],
    "max_elevation_level": 4,
    "shadow_styles": ["none", "ambient", "direct"],
    "max_shadows_per_surface": 1,
    "prohibited_combinations": [
      { "elevation_level": 0, "shadow_style": "ambient" },
      { "elevation_level": 0, "shadow_style": "direct" }
    ]
  },
  "radius": {
    "radius_values": [0, 2, 4, 6, 8, 12, 16],
    "max_radius_variants_per_surface": 2,
    "surface_type_variance": {
      "container": { "max_radius_variance": 8 },
      "control": { "max_radius_variance": 6 },
      "overlay": { "max_radius_variance": 8 }
    }
  },
  "motion": {
    "allowed_states": ["enter", "exit", "state-change", "feedback", "progress"],
    "disallowed_states": ["decorative-loop", "ambient-loop", "auto-play"],
    "duration_ms_bounds": { "min": 80, "max": 600 },
    "easing_functions": ["linear", "ease", "ease-in", "ease-out", "ease-in-out"],
    "motion_off_switch_required": true,
    "reduced_motion_behavior": "disable"
  },
  "assets": {
    "icon_set": {
      "name": "core-icons",
      "version": "1.0.0",
      "source": "local",
      "license": "MIT"
    },
    "image_usage": {
      "allowed_types": ["photo", "illustration", "diagram", "screenshot"],
      "allowed_formats": ["jpg", "png", "webp", "svg"],
      "max_images_per_page": 6
    },
    "aspect_ratios_allowed": ["1:1", "4:3", "3:2", "16:9", "2:3", "9:16"],
    "aspect_ratio_enforced": true,
    "decorative_assets_allowed": false
  }
}
```
