from dagster import define_asset_job

from mesh.assets import skos_file

files_job = define_asset_job(
    "files_job",
    selection=[
        "*" + skos_file.key.path[0],
    ],
)
