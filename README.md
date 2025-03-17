# Graphs2go: Medical Subject Headings (MeSH)

Transform the [Medical Subject Headings (MeSH)](https://www.nlm.nih.gov/mesh/meshhome.html) into Cypher and SKOS RDF.

## Download transformed data

See the [Releases page](https://github.com/graphs2go/mesh/releases).

## Getting started

### Prerequisites

* [Python 3.12](https://www.python.org/)
* [Python Poetry](https://python-poetry.org/)

### Install Python dependencies

    script/bootstrap

### Download MeSH RDF

[Download the MeSH RDF (.nt) file](https://nlmpubs.nlm.nih.gov/projects/mesh/rdf/) to `data/input`.

The resulting directory tree should resemble:

* `data/`
  * `input/`
    * `mesh2024.nt`

or similar, depending on the release year.

## Usage

Start the Dagster daemon:

    script/dagster-daemon

Launch a Dagster job to transform MeSH into Cypher and RDF and serialize them as files in `data/output`:

    jobs/files

## Credits

MeSH is provided by the [National Library of Medicine](https://www.nlm.nih.gov/databases/download/terms_and_conditions_mesh.html).
