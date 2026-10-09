# XC Thermal Viewer

Interactive viewer of cross-country paraglider and hang-glider flights from the French
FFVL contest archive (CFD), and of the thermals they climbed. It shows single tracks
with their flight phases (Vilpellet segmentation), launch maps, thermal planes over
5 km cells, regional thermal-time maps, route comparisons and group flights.

## Requirements

- **Python 3.12 or newer**
- **[uv](https://docs.astral.sh/uv/)**, which installs the viewer and its libraries

Works on macOS, Linux and Windows; the 3D views need OpenGL 3.3.

Check what you have:

```bash
uv --version
python3 --version        # Windows: py --version
```

Install uv if it is missing:

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```powershell
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then open a new terminal. If Python is missing or older than 3.12, let uv install it:

```bash
uv python install 3.12
```

## Run it

1. Launch the viewer:

   ```bash
   uvx --from git+https://github.com/matteodisante/xc-thermal-viewer xc-thermal-viewer
   ```

2. On first launch a dialog asks for the data folder. Select the folder named
   **`xc-thermal-viewer-data`** itself, the one holding `paragliders/` and
   `hang_gliders/`, not one of its subfolders. The viewer remembers it, so later
   launches open straight away. To switch folders, use **File → Choose data folder…**.

You can also give the data folder on the command line; it is remembered the same way:

```bash
uvx --from git+https://github.com/matteodisante/xc-thermal-viewer xc-thermal-viewer /path/to/xc-thermal-viewer-data
```

From a clone of this repository, `uv run xc-thermal-viewer` does the same.

### Updates, and what stays on your computer

Each `uvx` launch checks this repository and runs its latest version; it downloads
and rebuilds only when the code has changed. Nothing is installed system-wide and no
command is added to your PATH: uv keeps the code, its environment and Python in its
own folders (`uv cache dir` and `uv python dir` print where). `uv cache clean` empties
uv's cache, viewer included.

## The data folder

The viewer reads everything from the `xc-thermal-viewer-data` folder, which is not
part of this repository. The folder holds one archive per discipline, either or both:

```text
xc-thermal-viewer-data/
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
```

## Origin and licences

The viewer and the flight-processing code (IGC parsing, cleaning, Vilpellet
segmentation) come from the master's thesis repository
[soaring-anomalous-transport](https://github.com/matteodisante/soaring-anomalous-transport). Code: MIT.
Bundled terrain extracts: IGN, Licence Ouverte 2.0 (see
`src/xc_thermal_viewer/assets/thermal_orography/README.md`). Basemap: Natural Earth,
public domain.
