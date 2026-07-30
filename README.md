# Cartopy Map Production Skill for OpenCode

This project-local OpenCode skill generates and reviews production-ready Python 3.12 Cartopy map scripts. It implements deterministic geographic formatting, process-local SSL certificate verification disabling for Cartopy downloads, 10 m black coastlines, bold geographic labels, light-gray grids, rivers, optional state boundaries, safe external colorbars, darker colors for larger values, 500 dpi PNG output, and explicit display behavior.

## Installation

Copy the `.opencode` directory and `opencode.json` into the root of the target Git project:

```text
/path/to/project/.opencode/skills/cartopy-map-production/SKILL.md
/path/to/project/.opencode/agents/cartopy-map-reviewer.md
/path/to/project/opencode.json
```

OpenCode discovers project-local skills from `.opencode/skills/<name>/SKILL.md`. The skill directory name and the `name` frontmatter field must both be `cartopy-map-production`.

## Validation

Run:

```bash
python3.12 .opencode/skills/cartopy-map-production/scripts/validate_skill.py
python3.12 -m py_compile .opencode/skills/cartopy-map-production/templates/cartopy_map.py
```

A successful package validation prints:

```text
PASS: skill structure and required content are valid
```

## Usage examples

### Example 1: Filled contour map

```text
Create `src/plot_sst.py` using the cartopy-map-production skill. Read longitude, latitude, and SST from `data/monthly_sst.nc`. Plot SST with contourf over 54°W–30°W and 35°S–7°N. Put the colorbar to the right, include rivers, omit state boundaries, and save `outputs/maps/monthly_sst.png`. Do not display the figure.
```

Expected behavior: the skill creates Python 3.12 Cartopy code, validates coordinate and field shapes, uses a darker-high-value colormap, saves a 500 dpi PNG, and does not call `plt.show()`.

### Example 2: Current vectors and state boundaries

```text
Use cartopy-map-production to create `src/plot_currents.py` from `data/currents.nc`. Draw current-speed contourf plus subsampled quiver vectors. Add Brazilian state boundaries, place the horizontal colorbar below the map, and save `outputs/maps/currents.png`. Do not overwrite an existing file.
```

Expected behavior: the skill uses explicit transforms for both scalar and vector layers, enables 10 m administrative boundaries, places the colorbar outside below the map, and refuses silent overwrite.

### Example 3: Streamlines with explicit display

```text
Revise `src/plot_wind.py` using cartopy-map-production. Replace wind arrows with streamlines, retain the existing extent, save `outputs/maps/wind_streamlines.png` at 500 dpi, and show the figure after saving.
```

Expected behavior: the skill preserves unrelated code, saves before calling `plt.show()`, invokes the review subagent, and reports compilation and rendering checks separately.

## Compatibility checklist

- [ ] OpenCode recognizes `.opencode/skills/cartopy-map-production/SKILL.md`.
- [ ] `name` matches the skill directory and satisfies `^[a-z0-9]+(-[a-z0-9]+)*$`.
- [ ] `description` is present and no longer than 1024 characters.
- [ ] OpenCode supports project-local `.opencode/agents/` Markdown agents.
- [ ] OpenCode uses `permission` rather than legacy `tools` configuration.
- [ ] Python 3.12 is installed as `python3.12`.
- [ ] Cartopy 0.23 or newer is installed.
- [ ] Matplotlib 3.8 or newer is installed.
- [ ] NumPy 1.26 or newer is installed.
- [ ] Required input datasets are project-local and readable.
- [ ] The output directory is project-local and writable.
- [ ] Natural Earth 10 m resources are locally cached or network access is available to the plotting process.
- [ ] The project accepts the security implications of process-local SSL verification disabling.
- [ ] `python3.12 .opencode/skills/cartopy-map-production/scripts/validate_skill.py` passes.
- [ ] `python3.12 -m py_compile` passes for generated scripts.
- [ ] A rendered PNG is at least 10 KiB and is configured for 500 dpi.

## Security model

The supplied `opencode.json` starts from approval-required behavior, denies external-directory access, denies secret-like files, denies package installation and download commands, allows the skill by exact name, and permits edits only in project-local source, test, and map configuration paths. Rendering remains approval-gated because scripts may read scientific datasets and create output files.

## Why This Project Includes Both an Agent and a Skill

This project includes both an OpenCode skill and a specialized agent because they perform different but complementary functions.

The **skill** defines how the work must be performed. It contains the mapping requirements, activation rules, accepted inputs, expected outputs, technical constraints, validation steps, error-handling procedures, and completion criteria. When a user requests a scientific map, the skill guides OpenCode through a consistent and deterministic workflow.

The **agent** acts as an independent reviewer. It examines the generated Python code and verifies that the implementation follows the requirements established by the skill. For example, it can check Python compatibility, Cartopy usage, coastline resolution, geographic labels, colorbar placement, image resolution, output format, and whether the figure is displayed only when explicitly requested.

In simple terms:

```text
Skill = defines how the map must be created
Agent = verifies that the map was created correctly
```

Using both components creates a clearer separation of responsibilities. The skill focuses on implementation, while the agent focuses on quality control. This reduces inconsistencies, makes validation easier, and provides a more reliable workflow for producing publication-ready scientific maps.

The agent is not strictly required for the skill to function. The skill can operate independently. However, including a reviewer agent is useful in production environments where reproducibility, compliance, and measurable validation are important.

