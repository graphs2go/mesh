# MeSH

Medical Subject Heading (MeSH) Thesaurus transformation pipelines.

## Prerequisites

* [Python](https://www.python.org/)
* [Python Poetry](https://python-poetry.org/)

## One-time setup

### Install Python dependencies

    script/bootstrap

### Download the MeSH thesaurus

1. [Download the MeSH thesaurus in RDF](https://nlmpubs.nlm.nih.gov/projects/mesh/rdf/).
2. Move the `.nt.gz` file to `data/input`.

The resulting directory tree should resemble:

* `data/`
  * `input/`
    * `mesh2024.nt.gz`

or similar, depending on the release date.

## Running

### From an installed Poetry virtual environment (recommended for OS X)

#### Run a Dagster pipeline

The code includes multiple [Dagster](https://dagster.io/) pipelines. Each pipeline (a Dagster "job") has a corresponding shell script in `jobs/`.

For example, to transform the MeSH thesaurus into multiple representations and serialize them as files in `data/output`, run:

    jobs/files

## Structure of this project

* `data/input/`: directory containing a MeSH thesaurus .nt file
* `data/output/`: transformed/output data such as RDF versions of the MeSH thesaurus
* `mesh`: Python code
* `script`: scripts following the [Scripts To Rule Them All](https://github.com/github/scripts-to-rule-them-all) normalized script pattern
* `tests`: unit tests
