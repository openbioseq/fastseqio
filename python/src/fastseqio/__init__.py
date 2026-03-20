from typing import Literal

from .fastseqio import seqioFile, Record

__all__ = ["seqioFile", "Record", "open"]


def open(
    path: str, mode: Literal["w", "r"] = "r", compressed: bool = False
) -> seqioFile:
    return seqioFile(path, mode, compressed)

