# Map Specification

## Resolved defaults

The detailed task specification takes precedence over the earlier general sentence when they conflict.

| Property | Default |
|---|---|
| Python version | 3.12 |
| Mapping library | Cartopy |
| SSL behavior | Disable certificate verification within the plotting process before Cartopy resource access |
| Label size | 14 points |
| Label weight | Bold |
| Coastline | Black, 10 m resolution |
| Geographic labels | Longitude and latitude with hemisphere indicators, zero decimal places |
| Gridlines | Light gray |
| Rivers | Enabled |
| State boundaries | Disabled unless requested |
| Land | Light neutral fill, alpha 0.55, distinct from the scalar colormap |
| Scalar output | Darker colors indicate larger values |
| Colorbar | Outside map, right side by default, bottom when requested |
| Image format | PNG |
| Resolution | 500 dpi |
| Display | Disabled unless explicitly requested |

## Supported scientific layers

Use at least one of the following when requested:

- `Axes.contour`
- `Axes.contourf`
- `Axes.quiver`
- `Axes.barbs`
- `Axes.streamplot`

Every data layer must use an explicit `transform` appropriate to the data CRS.

## Geographic formatting

Use Cartopy formatters:

- `LongitudeFormatter(number_format=".0f", degree_symbol="°")`
- `LatitudeFormatter(number_format=".0f", degree_symbol="°")`

Use fixed longitude and latitude tick locations derived from the requested extent. Avoid decimal labels. Keep top and right labels disabled unless the user explicitly requests them.

## Natural Earth features

Use:

- `ax.coastlines(resolution="10m", color="black")`
- `cfeature.RIVERS.with_scale("10m")`
- `cfeature.LAND.with_scale("10m")`

For first-order administrative boundaries, use:

`cfeature.NaturalEarthFeature("cultural", "admin_1_states_provinces_lines", "10m", facecolor="none")`

Do not add state boundaries when the user requests no boundaries.

## Color rules

Before selecting a colormap, verify visually and programmatically that the upper end is darker than the lower end. Prefer sequential colormaps for ordered scalar fields. Do not use land colors that appear in the scalar colormap's dominant range.

Use `matplotlib.colors.Normalize`, `BoundaryNorm`, `LogNorm`, or `TwoSlopeNorm` only when scientifically justified by the data and user request.

## Colorbar placement

Create a dedicated colorbar axis outside the map. Do not allow the colorbar to overlap the map, labels, or title.

Right-side default:

`figure.colorbar(mappable, ax=ax, location="right", pad=0.03, shrink=0.9)`

Bottom option:

`figure.colorbar(mappable, ax=ax, location="bottom", pad=0.08, shrink=0.9, orientation="horizontal")`

## Output safety

Resolve paths with `Path.resolve()`. Require output paths to remain under the project root unless the user explicitly approves an external path. Reject unsupported suffixes. Create parent directories. Refuse silent overwrite by default.

Save using:

`figure.savefig(output_path, dpi=500, format="png", bbox_inches="tight")`

Call `plt.show()` only after saving and only when explicitly requested.
