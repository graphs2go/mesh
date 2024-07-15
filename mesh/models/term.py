from graphs2go.models import rdf
from rdflib import Literal

from mesh.namespaces import MESHV


class Term(rdf.NamedModel):
    """
    A MeSH term.

    https://hhs.github.io/meshrdf/terms
    """

    @property
    def pref_label(self) -> Literal:
        return self.resource.required_value(
            MESHV.prefLabel, rdf.Resource.ValueMappers.literal
        )
