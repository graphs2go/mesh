from collections.abc import Iterable

from rdflib import Literal
from returns.maybe import Maybe

from graphs2go.models import rdf
from mesh.models.term import Term
from mesh.namespaces import MESHV


class Concept(rdf.NamedModel):
    """
    A MeSH concept, not equivalent to an akos.Concept.

    https://hhs.github.io/meshrdf/concepts
    """

    @property
    def preferred_term(self) -> Term:
        return Term(
            self.resource.required_value(
                MESHV.preferredTerm, rdf.Resource.ValueMappers.named_resource
            )
        )

    @property
    def scope_note(self) -> Maybe[Literal]:
        return self.resource.optional_value(
            MESHV.scopeNote, rdf.Resource.ValueMappers.literal
        )

    def terms(self) -> Iterable[Term]:
        """
        Non-preferred MeSH terms.
        """

        term_resource: rdf.NamedResource
        for term_resource in self.resource.values(
            MESHV.term, rdf.Resource.ValueMappers.named_resource
        ):
            yield Term(term_resource)
