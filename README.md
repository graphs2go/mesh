# Graphs2go: Medical Subject Headings (MeSH)

Transform the [Medical Subject Headings (MeSH)](https://www.nlm.nih.gov/mesh/meshhome.html) into Cypher and SKOS RDF.

## Getting started

### Prerequisites

* [Python](https://www.python.org/)
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

Transform MeSH into Cypher and RDF and serialize them as files in `data/output`:

    jobs/files

Due to a limitation in Dagster, the script will not exit when all the files have been generated. You will have to terminate it with ^C after you see the message:

    Shutting down Dagster code server
