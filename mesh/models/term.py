from rdflib import Literal

from graphs2go.models import akos, rdf
from mesh.namespaces import MESHV


class Term(rdf.NamedModel, akos.Label):
    """
    A MeSH term.

    https://hhs.github.io/meshrdf/terms
    """

    @property
    def literal_form(self) -> Literal:
        return self.resource.required_value(
            MESHV.prefLabel, rdf.Resource.ValueMappers.literal
        )
