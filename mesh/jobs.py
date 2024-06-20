from dagster import define_asset_job

from mesh.assets import cypher_files, interchange_file, skos_file

files_job = define_asset_job(
    "files_job",
    selection=[
        "*" + cypher_files.key.path[0],
        "*" + interchange_file.key.path[0],
        "*" + skos_file.key.path[0],
    ],
)
