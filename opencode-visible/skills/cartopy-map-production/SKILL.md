---
name: cartopy-map-production
description: Generate, revise, or review production-ready Python 3.12 Cartopy map code with deterministic geographic formatting, disabled SSL certificate verification for Cartopy resource downloads, 10 m black coastlines, bold geographic labels, light-gray grids, optional rivers and state boundaries, safe colorbars, 500 dpi PNG output, validation, and explicit display behavior.
license: MIT
compatibility: opencode
metadata:
  audience: scientific-python-users
  language: python-3.12
  domain: geospatial-visualization
  workflow: plan-build-review-validate
---

# Cartopy Map Production

## Purpose

Create or modify reproducible Python 3.12 code for scientific geographic maps using Cartopy. Produce code that follows the map specification in `references/map-specification.md`, validates user inputs before plotting, writes only to approved project paths, and reports measurable completion checks.

## Activation rules

Load this skill when the user asks to create, generate, plot, draw, revise, debug, standardize, or review a geographic map in Python and any of the following applies:

- Cartopy is requested or appropriate.
- The prompt mentions coastlines, rivers, state boundaries, geographic ticks, contours, filled contours, current vectors, wind vectors, or streamlines.
- The output must be a high-resolution scientific map.
- The user asks for Python map code compatible with Python 3.12.

Do not activate for non-geographic charts, browser-based maps, GIS desktop instructions, or maps explicitly required in a library other than Cartopy.

## Scope

The skill may:

- Inspect project-local Python, NetCDF, CSV, GeoJSON, Shapefile, and configuration files.
- Create or edit project-local Python scripts, tests, and map configuration files.
- Generate code for `contour`, `contourf`, `quiver`, `barbs`, or `streamplot` layers.
- Add coastlines, land, rivers, graticules, geographic labels, colorbars, titles, legends, and optional administrative boundaries.
- Run safe syntax, import, static, and output checks when dependencies and input data are available.

The skill must not:

- Read secrets, credentials, `.env` files, browser stores, SSH keys, or unrelated home-directory files.
- Modify files outside the current project.
- Install packages, access remote data, or overwrite existing outputs without user approval.
- Suppress validation failures or claim that a map was rendered when it was not.
- Disable SSL globally outside the generated Python process.

## Inputs

Required inputs:

- The requested map type or scientific layer.
- An explicit project-relative output script path or a safe default under `./src/`.
- An explicit project-relative image path or a safe default under `./outputs/maps/`.

Inputs required when applicable:

- Longitude and latitude arrays or coordinate variable names.
- Scalar field for contours or filled contours.
- Zonal and meridional components for current or wind vectors.
- Map extent as `[west, east, south, north]`.
- Projection and data coordinate reference system.
- Color limits, contour levels, colormap, units, and colorbar orientation.
- State-boundary source when boundaries are requested and Natural Earth administrative boundaries are insufficient.
- Whether `plt.show()` is explicitly required.

Use the defaults in `references/map-specification.md` only when the user does not provide a conflicting value.

## Outputs

Produce:

1. A Python 3.12-compatible map script.
2. A project-relative image path ending in `.png` unless the user explicitly requests another supported format.
3. A validation report containing pass, fail, or not-run status for every completion check.
4. A concise assumptions section for defaults applied because the prompt omitted details.

When requested, also produce:

- A JSON configuration file.
- A minimal test file.
- A dependency file.

## Deterministic workflow

### Phase 1: Inspect

1. Read the user request exactly once and extract explicit requirements.
2. Inspect only project-local files needed to identify coordinate names, variable shapes, units, masks, and existing plotting conventions.
3. Record contradictions. Resolve them by this precedence order:
   1. The latest explicit user instruction.
   2. The current task-specific instruction.
   3. `references/map-specification.md`.
   4. Existing project conventions that do not conflict with items 1 through 3.
4. Do not infer unseen variable names or dimensions.

### Phase 2: Plan

1. Select one primary layer type: `contour`, `contourf`, `quiver`, `barbs`, or `streamplot`.
2. Select an explicit Cartopy projection and use `ccrs.PlateCarree()` as the data transform unless the data use another documented CRS.
3. Define all input paths and output paths with `pathlib.Path`.
4. Define validation rules before writing plotting code.
5. For nontrivial tasks, invoke `@cartopy-map-reviewer` after implementation.

### Phase 3: Build

1. Start from `templates/cartopy_map.py` when creating a new script.
2. Keep identifiers, messages, configuration keys, and generated documentation in American English.
3. Disable SSL verification only inside the Python process before Cartopy may download Natural Earth resources.
4. Validate dimensions, finite coordinate values, monotonic extents, output suffix, and output directory.
5. Create the output directory with `parents=True` and `exist_ok=True`.
6. Use explicit figure size, projection, transforms, z-order values, and plotting parameters.
7. Apply all required styling from `references/map-specification.md`.
8. Place the colorbar outside the map. Use the right side by default; use the bottom when requested.
9. Save before any optional display call.
10. Call `plt.show()` only when the user explicitly requests on-screen display.
11. Close the figure when display is not requested.

### Phase 4: Review

Invoke `@cartopy-map-reviewer` with the generated script path and the exact user requirements. The reviewer must check:

- Python 3.12 compatibility.
- Cartopy usage and explicit transforms.
- Process-local SSL override placement.
- Required coastlines, rivers, labels, grids, land styling, colorbar behavior, output format, and DPI.
- Input validation and failure messages.
- Least-privilege file access.
- No unrequested display call.

Apply only reviewer changes that are directly supported by the user request or this skill.

### Phase 5: Validate

Run these checks in order when available:

1. `python3.12 -m py_compile <script>`.
2. `python3.12 -c "import cartopy, matplotlib, numpy"`.
3. Run the script with a noninteractive backend when valid local input data exist.
4. Confirm the output file exists.
5. Confirm the output suffix is `.png` unless overridden.
6. Confirm output DPI metadata or script configuration is 500.
7. Confirm output size is greater than 10 KiB.
8. Confirm the script contains no absolute path outside the project unless explicitly supplied and approved.

Do not execute the rendering step when required data are unavailable. Mark it `not run` and state the missing prerequisite.

## Constraints

- Target Python version: 3.12.
- Required mapping library: Cartopy.
- Default output: PNG at 500 dpi.
- Default label size: 14 points, bold.
- Coastline: black, Natural Earth 10 m resolution.
- Geographic axis labels: degrees with hemisphere indicators and zero decimal places.
- Gridlines: light gray.
- Rivers: enabled by default.
- Land: light, partially transparent, and visually distinct from the scalar colormap.
- Darker scalar colors must represent larger values. Reverse a colormap only when necessary to satisfy this rule.
- State or first-order administrative boundaries are optional and controlled by the user request.
- Colorbar must be outside the map when a scalar color scale is present.
- Never mutate source datasets.
- Never overwrite an existing image unless the user requested replacement or the output path is versioned.

## Dependencies

Runtime:

- Python `>=3.12,<3.13`
- `cartopy>=0.23`
- `matplotlib>=3.8`
- `numpy>=1.26`

Optional by input format:

- `xarray>=2024.1`
- `netCDF4>=1.6`
- `geopandas>=0.14`
- `shapely>=2.0`

System libraries may be required by binary distributions or source builds, including PROJ and GEOS. Prefer prebuilt wheels and do not install dependencies without approval.

## Error handling

- Raise `FileNotFoundError` for missing local inputs and include the resolved path.
- Raise `ValueError` for invalid extents, incompatible array shapes, empty fields, invalid contour levels, unsupported output suffixes, or nonfinite coordinates.
- Raise `RuntimeError` when Cartopy features cannot be loaded or the output cannot be written.
- Preserve the original exception as the cause when wrapping failures.
- Never catch `Exception` without re-raising a typed error or returning a nonzero exit status.
- Never continue after a failed shape, CRS, or output-path validation.
- Report unavailable optional layers separately from failures in the primary scientific layer.

## Completion criteria

The task is complete only when all applicable checks pass:

- The script compiles with Python 3.12.
- The script imports Cartopy and uses an explicit projection.
- SSL verification is disabled only for the generated process.
- Every plotted data layer has an explicit `transform` when required.
- Coastline is black and uses 10 m resolution.
- Labels are bold and use the resolved point size.
- Longitude and latitude labels use geographic formatting with zero decimal places.
- Gridlines are light gray.
- Rivers are included unless explicitly disabled.
- Land is light, partially transparent, and distinct from the color scale.
- A scalar colorbar is outside the map and follows the requested orientation.
- Higher scalar values map to darker colors.
- The file is saved at 500 dpi.
- `plt.show()` appears only when explicitly requested.
- Existing outputs are not silently overwritten.
- The final report distinguishes validated, not-run, and failed checks.

## Required references

Read `references/map-specification.md` before generating or reviewing code. Use `templates/cartopy_map.py` as the baseline for new scripts. Use `scripts/validate_skill.py` to validate this skill package.
