"""Entry point for the ``xc-thermal-viewer`` console script."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import datafolder


def configure_graphics() -> None:
    """Choose a shared core profile before Qt creates any internal contexts.

    macOS cannot share the terrain widget's core-profile textures with Qt's
    default legacy context. Configure all windows before QApplication exists,
    including the backing-store compositor used by modeless 3D dialogs.
    """
    from PyQt6.QtCore import QCoreApplication, Qt
    from PyQt6.QtGui import QSurfaceFormat

    fmt = QSurfaceFormat()
    fmt.setRenderableType(QSurfaceFormat.RenderableType.OpenGL)
    fmt.setVersion(3, 3)
    fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
    fmt.setDepthBufferSize(24)
    fmt.setStencilBufferSize(8)
    fmt.setSamples(4)
    QSurfaceFormat.setDefaultFormat(fmt)
    QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    """The command line: an optional data folder."""
    parser = argparse.ArgumentParser(
        prog="xc-thermal-viewer",
        description="Interactive viewer of cross-country soaring flights and thermals.",
    )
    parser.add_argument(
        "data_folder",
        nargs="?",
        type=Path,
        help=(
            "Folder holding paragliders/ and/or hang_gliders/. Remembered for the "
            "next launch; without it the last folder is reused, or a dialog asks."
        ),
    )
    return parser.parse_args(argv)


def choose_data_folder(parent=None, start: str | Path = "") -> Path | None:
    """Ask for a data folder until a usable one is chosen or the user cancels.

    Args:
        parent: The dialog's parent widget, if any.
        start: The folder the dialog opens in.

    Returns:
        The chosen folder, or ``None`` if the user cancelled.
    """
    from PyQt6.QtWidgets import QFileDialog, QMessageBox

    while True:
        chosen = QFileDialog.getExistingDirectory(
            parent, "Choose the XC Thermal Viewer data folder", str(start)
        )
        if not chosen:
            return None
        problems = datafolder.missing_parts(chosen)
        if not problems:
            return Path(chosen)
        QMessageBox.warning(parent, "Not a data folder", "\n".join(problems))
        start = chosen


def _initial_data_folder(argument: Path | None, settings) -> tuple[Path | None, bool]:
    """The data folder to start with, and whether to remember it.

    The command-line argument wins, then the environment variable (used for this run
    only), then the folder used last time, then a dialog.
    """
    if argument is not None:
        problems = datafolder.missing_parts(argument)
        if problems:
            raise SystemExit("\n".join(problems))
        return argument, True
    if datafolder.current() is not None:
        return datafolder.current(), False
    remembered = settings.value(datafolder.SETTINGS_KEY, "", type=str)
    if remembered and not datafolder.missing_parts(remembered):
        return Path(remembered), False
    return choose_data_folder(start=remembered), True


def main(argv: list[str] | None = None) -> int:
    """Launch the viewer. Returns the process exit code."""
    args = _parse_args(argv)
    configure_graphics()

    from PyQt6.QtCore import QSettings
    from PyQt6.QtWidgets import QApplication

    from .main_window import MainWindow

    app = QApplication(sys.argv[:1])
    app.setOrganizationName("xc-thermal-viewer")
    app.setApplicationName("xc-thermal-viewer")
    settings = QSettings()
    folder, remember = _initial_data_folder(args.data_folder, settings)
    if folder is not None:
        folder = datafolder.use(folder)
        if remember:
            settings.setValue(datafolder.SETTINGS_KEY, str(folder))
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
