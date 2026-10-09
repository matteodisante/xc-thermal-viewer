"""Portable identities of the files a saved product was built from.

A saved product (a census, an index, a raster) records a fingerprint of its inputs and
is reused only while that fingerprint still matches. The data folder can move to
another disk or computer, so a fingerprint never contains an absolute path or a
modification time: only where a file sits inside its archive root and what it holds
(its bytes when the file is small, its size otherwise). Code changes are tracked by an
explicit version constant in each module, bumped on purpose, never by hashing source
files.

No Qt import (see the package docstring).
"""

from __future__ import annotations

import hashlib
from functools import lru_cache
from pathlib import Path

#: Files up to this size are identified by their bytes, larger ones by their size.
SMALL_FILE_BYTES = 16 * 2**20


def file_identity(path: str | Path, root: str | Path | None = None) -> list:
    """Name, size and, for a small file, content hash of ``path``.

    Args:
        path: An input file.
        root: The folder the name is taken relative to (a discipline's archive
            root); the bare file name when omitted.

    Returns:
        A JSON-serialisable list that is the same on every computer holding the
        same file at the same place inside the data folder.
    """
    path = Path(path)
    name = path.relative_to(root).as_posix() if root is not None else path.name
    stat = path.stat()
    if stat.st_size > SMALL_FILE_BYTES:
        return [name, stat.st_size]
    return [name, stat.st_size, _sha256(str(path), stat.st_size, stat.st_mtime_ns)]


@lru_cache(maxsize=256)
def _sha256(path: str, size: int, mtime_ns: int) -> str:
    """Hash a small file once per version of it seen by this process."""
    del size, mtime_ns  # cache key only: a rewritten file is hashed again
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
