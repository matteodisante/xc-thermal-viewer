# XC Thermal Viewer

Interactive viewer of cross-country paraglider and hang-glider flights from the French
FFVL contest archive (CFD), and of the thermals they climbed. It shows single tracks
with their flight phases (Vilpellet segmentation), launch maps, thermal planes over
5 km cells, regional thermal-time maps, route comparisons and group flights.

## Requirements

**[uv](https://docs.astral.sh/uv/)** and **git**. You do not need to install Python
or any library yourself. Works on macOS, Linux and Windows; the 3D views need
OpenGL 3.3. On Windows, use **Git Bash** as your terminal: it comes with
[Git for Windows](https://git-scm.com/downloads/win), and every command below works
there as on macOS and Linux.

Check what you have; each command prints a version number, or an error if the tool is
missing:

```bash
uv --version
git --version
```

Install git if it is missing:

```bash
# macOS
xcode-select --install
# Linux (Debian, Ubuntu)
sudo apt install git
# Windows: install Git for Windows from https://git-scm.com/downloads/win
```

Install uv if it is missing, then open a new terminal:

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows (Git Bash)
winget install --id=astral-sh.uv -e
```

### On a company or university network

If uv stops with `invalid peer certificate: UnknownIssuer`, the network inspects HTTPS
with its own certificate. Your IT department has installed it in the system, but uv
does not look there by default. Tell uv to use the system certificates, once:

```bash
# uv 0.11 or newer (check with: uv --version)
echo 'export UV_SYSTEM_CERTS=1' >> ~/.bashrc
# uv older than 0.11
echo 'export UV_NATIVE_TLS=1' >> ~/.bashrc
```

On macOS, write to `~/.zshrc` instead of `~/.bashrc`. Then open a new terminal: the
launch command stays the same. The viewer itself always uses the system certificates
for its map downloads.

If the error persists, the company certificate is not in the system. Ask your IT
department for it as a `.pem` file and add, the same way,
`export SSL_CERT_FILE=/path/to/company-certificate.pem`.

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

1. Launch the viewer (same command on every system):

   ```bash
   uvx --from git+https://github.com/matteodisante/xc-thermal-viewer xc-thermal-viewer
   ```

2. On first launch a dialog asks for the data folder. Select the folder named
   **`xc-thermal-viewer-data`** itself, the one holding `paragliders/` and
   `hang_gliders/`, not one of its subfolders. The viewer remembers it, so later
   launches open straight away. To switch folders, click **Choose data folder…** at
   the top of the left panel.

You can also give the data folder on the command line; it is remembered the same way:

```bash
# macOS and Linux
uvx --from git+https://github.com/matteodisante/xc-thermal-viewer xc-thermal-viewer /path/to/xc-thermal-viewer-data
```

```bash
# Windows (Git Bash)
uvx --from git+https://github.com/matteodisante/xc-thermal-viewer xc-thermal-viewer D:/xc-thermal-viewer-data
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
