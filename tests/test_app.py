"""The entry point configures compatible GL contexts before Qt starts."""

import os
import subprocess
import sys

import pytest

pytest.importorskip("PyQt6")


def test_core_profile_and_sharing_are_configured_before_qapplication(tmp_path):
    (tmp_path / "paragliders").mkdir()
    code = """
import sys
from types import ModuleType
from PyQt6 import QtWidgets
from PyQt6.QtCore import QCoreApplication, QTimer, Qt
from PyQt6.QtGui import QSurfaceFormat
from xc_thermal_viewer.app import main

import truststore

original = QtWidgets.QApplication
events = []
truststore.inject_into_ssl = lambda: events.append("certificates")

class CheckedApplication(original):
    def __init__(self, argv):
        assert QCoreApplication.instance() is None
        fmt = QSurfaceFormat.defaultFormat()
        assert (fmt.majorVersion(), fmt.minorVersion()) >= (3, 3)
        assert fmt.profile() == QSurfaceFormat.OpenGLContextProfile.CoreProfile
        assert fmt.depthBufferSize() >= 24
        assert fmt.stencilBufferSize() >= 8
        assert QCoreApplication.testAttribute(
            Qt.ApplicationAttribute.AA_ShareOpenGLContexts
        )
        events.append("application")
        super().__init__(argv)

class Window:
    def __init__(self):
        assert QCoreApplication.instance() is not None
        events.append("window")

    def show(self):
        QTimer.singleShot(0, QCoreApplication.instance().quit)

QtWidgets.QApplication = CheckedApplication
module = ModuleType("xc_thermal_viewer.main_window")
module.MainWindow = Window
sys.modules[module.__name__] = module
assert main() == 0
assert events == ["certificates", "application", "window"]
"""
    result = subprocess.run(
        [sys.executable, "-c", code],
        env={
            **os.environ,
            "QT_QPA_PLATFORM": "offscreen",
            "PYTHONPATH": os.pathsep.join(sys.path),
            "XC_THERMAL_VIEWER_DATA": str(tmp_path),
        },
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stdout + result.stderr
