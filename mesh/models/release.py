from __future__ import annotations

import os.path
from base64 import b64decode, b64encode
from pathlib import Path

from rdflib import URIRef


class Release:
    """
    Picklable descriptor of a MeSH release.
    """

    def __init__(self, file_path: Path):
        file_stem, file_ext = os.path.splitext(file_path.name.lower())
        file_stem_prefix = "mesh"
        if not file_stem.startswith("mesh"):
            raise ValueError(
                f"{file_path} file name does not start with {file_stem_prefix}"
            )
        if file_ext != ".nt":
            raise ValueError(f"{file_path} does not have .nt extension")
        self.__nt_file_path = file_path

        self.__version = int(file_stem[len(file_stem_prefix) :])

    @classmethod
    def from_partition_key(cls, partition_key: str) -> Release:
        return Release(Path(b64decode(partition_key).decode("utf-8")))

    @property
    def identifier(self) -> URIRef:
        return URIRef("urn:mesh-release:" + str(self.version))

    @property
    def nt_file_path(self) -> Path:
        return self.__nt_file_path

    def to_partition_key(self) -> str:
        # Getting around https://github.com/dagster-io/dagster/issues/16064
        return b64encode(str(self.__nt_file_path).encode("utf-8")).decode("ascii")

    @property
    def version(self) -> int:
        return self.__version
