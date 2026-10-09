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



## Development

```bash
uv sync
QT_QPA_PLATFORM=offscreen uv run pytest



## Origin and licences

The viewer and the flight-processing code (IGC parsing, cleaning, Vilpellet
segmentation) come from the master's thesis repository linked above. Code: MIT.
Bundled terrain extracts: IGN, Licence Ouverte 2.0 (see
`src/xc_thermal_viewer/assets/thermal_orography/README.md`). Basemap: Natural Earth,
public domain.
