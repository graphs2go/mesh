from dagster import get_dagster_logger
from graphs2go.resources import DirectoryInputConfig
from graphs2go.utils import find_file_releases

from mesh.models import Release


def find_releases(input_config: DirectoryInputConfig) -> tuple[Release, ...]:
    return find_file_releases(
        logger=get_dagster_logger(),
        release_directory_path=input_config.parse().directory_path,
        release_factory=Release,
    )
