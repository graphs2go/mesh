from dagster import Definitions
from returns.maybe import Some

from graphs2go.resources import DirectoryInputConfig, OutputConfig, RdfStoreConfig
from graphs2go.utils import configure_markus, load_dotenv
from mesh.assets import (
    interchange_graph,
    release,
    thesaurus,
    skos_file,
    skos_graph,
)
from mesh.jobs import files_job
from mesh.paths import (
    INPUT_DIRECTORY_PATH,
    OUTPUT_DIRECTORY_PATH,
    RDF_STORE_DIRECTORY_PATH,
)

configure_markus()
load_dotenv()


definitions = Definitions(
    assets=[
        interchange_graph,
        release,
        thesaurus,
        skos_file,
        skos_graph,
    ],
    jobs=[files_job],
    resources={
        "input_config": DirectoryInputConfig.from_env_vars(
            directory_path_default=INPUT_DIRECTORY_PATH
        ),
        "output_config": OutputConfig.from_env_vars(
            directory_path_default=OUTPUT_DIRECTORY_PATH
        ),
        "rdf_store_config": RdfStoreConfig.from_env_vars(
            directory_path_default=Some(RDF_STORE_DIRECTORY_PATH)
        ),
    },
)
