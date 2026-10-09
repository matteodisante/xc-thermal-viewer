# XC Thermal Viewer

Interactive viewer of cross-country paraglider and hang-glider flights from the French
FFVL contest archive (CFD), and of the thermals they climbed. It shows single tracks
with their flight phases (Vilpellet segmentation), launch maps, thermal planes over
5 km cells, regional thermal-time maps, route comparisons and group flights.

## Requirements

**[uv](https://docs.astral.sh/uv/)** and **git**. You do not need to install Python
or any library yourself. Works on macOS, Linux and Windows; the 3D views need
OpenGL 3.3. Every command below works in a macOS or Linux terminal, in Git Bash and
in PowerShell on Windows, unless a block says otherwise.

Check what you have:

```bash
uv --version
git --version
```

Install uv if it is missing, then open a new terminal:

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```powershell
# Windows (in PowerShell, also if you then use Git Bash)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Install git if it is missing:

```bash
# macOS
xcode-select --install
# Linux (Debian, Ubuntu)
sudo apt install git
```

```powershell
# Windows (PowerShell)
winget install --id Git.Git -e --source winget
```

### What uv does on the first launch

The first launch downloads, into uv's own folders in your user directory:

- **Python 3.12**, only if your computer has no Python 3.12 or newer. A Python already
  on your system is left untouched, and other programs do not see this one.
- **the viewer and its libraries**, in a private environment used only by the viewer.

Nothing is installed system-wide and nothing is added to your PATH. On macOS and Linux
these folders are `~/.cache/uv` and `~/.local/share/uv/python`; on any system,
including Windows, `uv cache dir` and `uv python dir` print them. Later launches reuse
them and start quickly. `uv cache clean` deletes the viewer and its libraries;
`uv python uninstall 3.12` deletes the Python that uv downloaded.

## Run it

1. Launch the viewer (same command in every terminal, Git Bash and PowerShell
   included):

   ```bash
   uvx --from git+https://github.com/matteodisante/xc-thermal-viewer xc-thermal-viewer
   ```

2. On first launch a dialog asks for the data folder. Select the folder named
   **`xc-thermal-viewer-data`** itself, the one holding `paragliders/` and
   `hang_gliders/`, not one of its subfolders. The viewer remembers it, so later
   launches open straight away. To switch folders, use **File → Choose data folder…**.

You can also give the data folder on the command line; it is remembered the same way:

```bash
# macOS and Linux
uvx --from git+https://github.com/matteodisante/xc-thermal-viewer xc-thermal-viewer /path/to/xc-thermal-viewer-data
```

```bash
# Windows (Git Bash)
uvx --from git+https://github.com/matteodisante/xc-thermal-viewer xc-thermal-viewer D:/xc-thermal-viewer-data
```

```powershell
# Windows (PowerShell)
uvx --from git+https://github.com/matteodisante/xc-thermal-viewer xc-thermal-viewer D:\xc-thermal-viewer-data
```

From a clone of this repository, `uv run xc-thermal-viewer` does the same.

### Updates

Each launch checks this repository and runs its latest version; it downloads and
rebuilds only when the code has changed.

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
uv run pytest
```

Tests run without a display.

## Origin and licences

The viewer and the flight-processing code (IGC parsing, cleaning, Vilpellet
segmentation) come from the master's thesis repository
[soaring-anomalous-transport](https://github.com/matteodisante/soaring-anomalous-transport). Code: MIT.
Bundled terrain extracts: IGN, Licence Ouverte 2.0 (see
`src/xc_thermal_viewer/assets/thermal_orography/README.md`). Basemap: Natural Earth,
public domain.
