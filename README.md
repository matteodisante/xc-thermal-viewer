# XC Thermal Viewer

Interactive viewer of cross-country paraglider and hang-glider flights from the French
FFVL contest archive (CFD), and of the thermals they climbed. It shows single tracks
with their flight phases (Vilpellet segmentation), launch maps, thermal planes over
5 km cells, regional thermal-time maps, route comparisons and group flights.

## Run it

You need [uv](https://docs.astral.sh/uv/getting-started/installation/). It fetches
Python 3.12 and every dependency by itself; nothing else has to be installed.

```bash
uvx --from git+https://github.com/matteodisante/xc-thermal-viewer xc-thermal-viewer
```

Or from a clone of this repository:

```bash
uv run xc-thermal-viewer
```

Works on macOS, Linux and Windows. The 3D views need OpenGL 3.3.

## The data folder

The viewer reads everything from one local folder, which is not part of this
repository. On first launch a dialog asks for it; the choice is remembered. You can
also pass it on the command line, or switch it from **File → Choose data folder…**.

```bash
uvx --from git+https://github.com/matteodisante/xc-thermal-viewer xc-thermal-viewer /path/to/data
```

The folder holds one archive per discipline, either or both:

```text
data/
├── manifest.json            what was packed, and when
├── paragliders/
│   ├── raw/igc/<season>/    the .igc tracks
│   ├── catalog/catalog.csv  flight metadata
│   └── derived/
│       ├── fixes.parquet, flights_meta.parquet   cleaned tracks
│       ├── segmentation/vilpellet/               saved flight phases
│       └── viewer/thermal-planes/                prepared maps, indexes and caches
└── hang_gliders/            the same layout
```

A tab whose files are missing still opens and says what it needs. Map backgrounds
(IGN Géoplateforme, Esri hillshade) are downloaded when shown, so they need an
internet connection; everything saved in the folder works offline.

The folder can be moved or copied to another computer as is: saved products identify
their inputs by their place inside the folder and their content, never by absolute
path or file date.

## Building a data folder (maintainers)

`scripts/pack_data_folder.py` builds the folder from the thesis archive
([soaring-anomalous-transport](https://github.com/matteodisante/soaring-anomalous-transport)),
copying only what the viewer reads and checking each saved product against the thesis
code before marking it valid here:

```bash
uv run python scripts/pack_data_folder.py --dry-run \
    --para /Volumes/SSD/paragliders/ffvl_cfd_igc \
    --hang /Volumes/SSD/hang_gliders/delta_cfd_igc \
    --to /Volumes/Other/xc-data
```

Drop `--dry-run` to copy. Never point the viewer at the thesis archive itself: its
preparation steps rewrite saved products in place.

The `scripts/prepare_*.py` scripts rebuild the saved products of a data folder from its
tracks and tables. Set `XC_THERMAL_VIEWER_DATA` to the folder first; each script's
`--help` says what it prepares.

## Development

```bash
uv sync
QT_QPA_PLATFORM=offscreen uv run pytest
uv run ruff check src tests scripts
```

Tests run without a display. Those needing a real GPU are skipped unless
`XC_THERMAL_VIEWER_NATIVE_OPENGL=1`.

## Origin and licences

The viewer and the flight-processing code (IGC parsing, cleaning, Vilpellet
segmentation) come from the master's thesis repository linked above. Code: MIT.
Bundled terrain extracts: IGN, Licence Ouverte 2.0 (see
`src/xc_thermal_viewer/assets/thermal_orography/README.md`). Basemap: Natural Earth,
public domain.
