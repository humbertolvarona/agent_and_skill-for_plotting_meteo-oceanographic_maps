from __future__ import annotations

import argparse
import ssl
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

ssl._create_default_https_context = ssl._create_unverified_context

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter
from matplotlib.colors import Colormap


@dataclass(frozen=True)
class MapConfig:
    extent: tuple[float, float, float, float]
    output_path: Path
    title: str
    colorbar_label: str
    colorbar_location: Literal["right", "bottom"] = "right"
    show: bool = False
    include_state_boundaries: bool = False
    overwrite: bool = False


def validate_config(config: MapConfig, project_root: Path) -> MapConfig:
    west, east, south, north = config.extent
    if not all(np.isfinite([west, east, south, north])):
        raise ValueError("Map extent contains nonfinite values")
    if west >= east or south >= north:
        raise ValueError("Map extent must satisfy west < east and south < north")
    resolved_root = project_root.resolve()
    resolved_output = config.output_path.resolve()
    if resolved_root not in resolved_output.parents:
        raise ValueError(f"Output path must remain under the project root: {resolved_output}")
    if resolved_output.suffix.lower() != ".png":
        raise ValueError("Output path must use the .png suffix")
    if resolved_output.exists() and not config.overwrite:
        raise FileExistsError(f"Output already exists: {resolved_output}")
    resolved_output.parent.mkdir(parents=True, exist_ok=True)
    return MapConfig(
        extent=config.extent,
        output_path=resolved_output,
        title=config.title,
        colorbar_label=config.colorbar_label,
        colorbar_location=config.colorbar_location,
        show=config.show,
        include_state_boundaries=config.include_state_boundaries,
        overwrite=config.overwrite,
    )


def validate_data(longitude: np.ndarray, latitude: np.ndarray, field: np.ndarray) -> None:
    if longitude.ndim != 1 or latitude.ndim != 1:
        raise ValueError("Longitude and latitude must be one-dimensional arrays")
    if field.shape != (latitude.size, longitude.size):
        raise ValueError(
            f"Field shape {field.shape} does not match coordinates {(latitude.size, longitude.size)}"
        )
    if longitude.size < 2 or latitude.size < 2:
        raise ValueError("Longitude and latitude must each contain at least two values")
    if not np.all(np.isfinite(longitude)) or not np.all(np.isfinite(latitude)):
        raise ValueError("Coordinate arrays contain nonfinite values")
    if not np.any(np.isfinite(field)):
        raise ValueError("Field contains no finite values")


def upper_end_is_darker(colormap: Colormap) -> bool:
    low = np.asarray(colormap(0.05)[:3], dtype=float)
    high = np.asarray(colormap(0.95)[:3], dtype=float)
    low_luminance = float(np.dot(low, [0.2126, 0.7152, 0.0722]))
    high_luminance = float(np.dot(high, [0.2126, 0.7152, 0.0722]))
    return high_luminance < low_luminance


def select_colormap(name: str = "Blues") -> Colormap:
    colormap = plt.get_cmap(name)
    if upper_end_is_darker(colormap):
        return colormap
    reversed_colormap = colormap.reversed()
    if not upper_end_is_darker(reversed_colormap):
        raise ValueError(f"Colormap does not provide a darker upper range: {name}")
    return reversed_colormap


def geographic_ticks(start: float, stop: float, target_count: int = 6) -> np.ndarray:
    span = stop - start
    raw_step = span / max(target_count - 1, 1)
    candidates = np.asarray([1, 2, 5, 10, 15, 20, 30, 45, 60, 90], dtype=float)
    step = float(candidates[np.argmin(np.abs(candidates - raw_step))])
    first = np.ceil(start / step) * step
    return np.arange(first, stop + step * 0.5, step)


def create_map(
    longitude: np.ndarray,
    latitude: np.ndarray,
    field: np.ndarray,
    config: MapConfig,
) -> Path:
    validate_data(longitude, latitude, field)
    data_crs = ccrs.PlateCarree()
    figure = plt.figure(figsize=(12, 9), constrained_layout=True)
    ax = figure.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent(config.extent, crs=data_crs)
    land = cfeature.LAND.with_scale("10m")
    rivers = cfeature.RIVERS.with_scale("10m")
    ax.add_feature(land, facecolor="whitesmoke", edgecolor="none", alpha=0.55, zorder=1)
    ax.add_feature(rivers, edgecolor="steelblue", linewidth=0.6, alpha=0.8, zorder=4)
    if config.include_state_boundaries:
        states = cfeature.NaturalEarthFeature(
            category="cultural",
            name="admin_1_states_provinces_lines",
            scale="10m",
            facecolor="none",
        )
        ax.add_feature(states, edgecolor="dimgray", linewidth=0.6, zorder=5)
    colormap = select_colormap("Blues")
    levels = np.linspace(float(np.nanmin(field)), float(np.nanmax(field)), 16)
    if np.unique(levels).size < 2:
        raise ValueError("Field range is insufficient for filled contours")
    mappable = ax.contourf(
        longitude,
        latitude,
        field,
        levels=levels,
        cmap=colormap,
        extend="both",
        transform=data_crs,
        zorder=2,
    )
    ax.coastlines(resolution="10m", color="black", linewidth=1.0, zorder=6)
    west, east, south, north = config.extent
    ax.set_xticks(geographic_ticks(west, east), crs=data_crs)
    ax.set_yticks(geographic_ticks(south, north), crs=data_crs)
    ax.xaxis.set_major_formatter(LongitudeFormatter(number_format=".0f", degree_symbol="°"))
    ax.yaxis.set_major_formatter(LatitudeFormatter(number_format=".0f", degree_symbol="°"))
    ax.tick_params(axis="both", labelsize=14)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontweight("bold")
    ax.gridlines(
        crs=data_crs,
        draw_labels=False,
        linewidth=0.7,
        color="lightgray",
        alpha=0.9,
        linestyle="--",
        zorder=3,
    )
    ax.set_title(config.title, fontsize=14, fontweight="bold", pad=12)
    colorbar = figure.colorbar(
        mappable,
        ax=ax,
        location=config.colorbar_location,
        orientation="horizontal" if config.colorbar_location == "bottom" else "vertical",
        pad=0.08 if config.colorbar_location == "bottom" else 0.03,
        shrink=0.9,
    )
    colorbar.set_label(config.colorbar_label, fontsize=14, fontweight="bold")
    colorbar.ax.tick_params(labelsize=14)
    for label in colorbar.ax.get_xticklabels() + colorbar.ax.get_yticklabels():
        label.set_fontweight("bold")
    figure.savefig(config.output_path, dpi=500, format="png", bbox_inches="tight")
    if config.show:
        plt.show()
    else:
        plt.close(figure)
    return config.output_path


def build_demo_data() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    longitude = np.linspace(-54.0, -30.0, 121)
    latitude = np.linspace(-35.0, 7.0, 141)
    lon_grid, lat_grid = np.meshgrid(longitude, latitude)
    field = 20.0 + 10.0 * np.cos(np.deg2rad(lat_grid)) * np.sin(np.deg2rad(lon_grid * 3.0))
    return longitude, latitude, field


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("outputs/maps/cartopy_map.png"))
    parser.add_argument("--show", action="store_true")
    parser.add_argument("--states", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--colorbar-location", choices=("right", "bottom"), default="right")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = Path.cwd()
    config = validate_config(
        MapConfig(
            extent=(-54.0, -30.0, -35.0, 7.0),
            output_path=args.output,
            title="Scientific Cartopy Map",
            colorbar_label="Field units",
            colorbar_location=args.colorbar_location,
            show=args.show,
            include_state_boundaries=args.states,
            overwrite=args.overwrite,
        ),
        project_root,
    )
    longitude, latitude, field = build_demo_data()
    output_path = create_map(longitude, latitude, field, config)
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
