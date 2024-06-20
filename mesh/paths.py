from pathlib import Path

DATA_DIRECTORY_PATH = (Path(__file__).parent.parent / "data").absolute()
INPUT_DIRECTORY_PATH = DATA_DIRECTORY_PATH / "input"
RDF_STORE_DIRECTORY_PATH = DATA_DIRECTORY_PATH / "oxigraph"
OUTPUT_DIRECTORY_PATH = DATA_DIRECTORY_PATH / "output"
