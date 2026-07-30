# Natural-Language Usage Examples

This file provides practical examples of how to invoke the Cartopy Map Production skill in OpenCode using natural language. The prompts can be copied directly into an OpenCode session and adapted to a specific dataset, region, variable, or output path.

## Basic Contour Map

Create a Python 3.12 script that plots a filled contour map with Cartopy using the data in `data/sea_surface_temperature.nc`. Use longitude, latitude, and the variable `sst`. Plot the region from 60°W to 30°W and from 35°S to 10°N. Save the result as `outputs/maps/sst_map.png` at 500 dpi. Use bold 14-point labels, black 10 m coastlines, light-gray gridlines, rivers, geographic coordinate labels without decimal places, and a light transparent land color. Do not display the figure after saving it.

## Map With the Colorbar Below

Generate a Cartopy filled contour map from `data/wave_height.nc` using the variable `VHM0`. Place the horizontal colorbar below the map. Use a color scale in which higher values are represented by darker colors. Save the figure as `outputs/maps/significant_wave_height.png` at 500 dpi. Use Python 3.12 and disable SSL certificate verification for Cartopy data downloads.

## Current Vector Map

Create a Python 3.12 Cartopy script that reads `u` and `v` surface-current components from `data/ocean_currents.nc`. Plot current vectors over a filled contour map of current speed. Reduce the vector density so the arrows remain readable. Add black coastlines at 10 m resolution, rivers, geographic labels without decimal places, bold 14-point text, and light-gray gridlines. Save the figure to `outputs/maps/surface_currents.png` at 500 dpi.

## Wind Vector Map

Using `data/atmospheric_fields.nc`, create a map of wind speed calculated from `u10` and `v10`, with wind vectors overlaid on the filled contour field. Use Cartopy and Python 3.12. Plot the South Atlantic region, include rivers and national borders, and omit state boundaries. Place the colorbar on the right side of the map. Save the image as `outputs/maps/wind_speed.png` at 500 dpi.

## Streamline Map

Create a Cartopy map that displays ocean-current streamlines from the `uo` and `vo` variables in `data/currents_monthly.nc`. Use current speed as the streamline color field and ensure that larger values use darker colors. Add a separate colorbar on the right. Save the map as `outputs/maps/current_streamlines.png` at 500 dpi and display it after saving.

## Map With State Boundaries

Generate a filled contour map of accumulated precipitation from `data/precipitation.nc`. Include coastlines, rivers, national borders, and state boundaries. Use a light land color that does not appear in the data color scale. Plot geographic axis labels without decimal places and use bold 14-point labels throughout. Save the result as `outputs/maps/precipitation_states.png` at 500 dpi.

## Map Without State Boundaries

Create a Cartopy contour map of sea-level pressure from `data/pressure.nc`. Include rivers and national borders, but do not plot state boundaries. Use black coastlines at 10 m resolution, light-gray gridlines, and geographic coordinate labels without decimal places. Save the output as `outputs/maps/sea_level_pressure.png` at 500 dpi.

## Contour Lines Over a Filled Field

Create a map from `data/ocean_temperature.nc` with filled contours of sea-surface temperature and black contour lines at intervals of 1 °C. Label the contour lines without unnecessary decimal places. Use Cartopy, Python 3.12, bold 14-point labels, black 10 m coastlines, rivers, light-gray gridlines, and a colorbar on the right. Save the figure as `outputs/maps/sst_contours.png` at 500 dpi.

## Map From a NetCDF Monthly Climatology

Read the monthly climatology file `data/wave_climatology.nc` and create a map for January using the variable `VHM0_SW1`. Select the first time index, preserve masked values, and validate that longitude and latitude dimensions match the plotted field. Save the figure as `outputs/maps/january_primary_swell.png` at 500 dpi. Do not overwrite an existing file unless explicitly authorized.

## Map With a Custom Geographic Extent

Create a filled contour map for the Brazilian continental margin using `data/wave_power.nc` and the variable `wave_power_flux`. Use the geographic extent 54°W to 30°W and 35°S to 7°N. Add black coastlines at 10 m resolution, rivers, state boundaries, bold 14-point geographic labels without decimals, and light-gray gridlines. Put the colorbar below the map and save the figure as `outputs/maps/brazil_wave_power.png` at 500 dpi.

## Review an Existing Mapping Script

Review `scripts/plot_wave_energy.py` with the Cartopy map reviewer agent. Check its compatibility with Python 3.12, Cartopy usage, SSL handling, coastline resolution, label size and weight, geographic coordinate formatting, gridline styling, river and boundary layers, colorbar placement, color ordering, output format, 500 dpi resolution, and conditional use of `plt.show()`. Report every failed requirement with the relevant file location and a specific correction.

## Correct an Existing Script

Update `scripts/plot_currents.py` so that it complies with the Cartopy Map Production skill. Preserve the existing scientific calculations and variable names. Change only the mapping, validation, output, and display logic required for compliance. Save the corrected script without executing it, and summarize the modifications.

## Generate and Validate a Complete Map

Create a Python 3.12 Cartopy script from `data/wave_fields.nc` that plots significant wave height with primary-swell direction vectors. Save the script as `scripts/plot_wave_fields.py` and the expected figure as `outputs/maps/wave_fields.png`. Then run the available validation checks and use the reviewer agent to verify compliance. Do not declare the task complete unless all measurable checks pass or any unverified checks are clearly reported.

## Reusable Prompt Pattern

Use the following general prompt pattern when creating new requests:

```text
Create a Python 3.12 Cartopy map using [input file] and [variable names].
Plot [map type] for [geographic region or extent].
Include [contours, filled contours, vectors, or streamlines].
Use [boundary and feature requirements].
Place the colorbar [right or below].
Save the figure as [explicit output path] at 500 dpi.
[Display or do not display] the figure after saving.
Validate [dimensions, coordinates, missing values, and output path].
```

## Notes

Natural-language prompts should identify the input file, required variables, geographic extent, plot type, output path, colorbar position, administrative boundaries, and display behavior whenever those details are known.

When a request omits an optional setting, the skill applies its documented defaults. Explicit user instructions take precedence unless they conflict with safety requirements, unavailable data, or technical constraints.
