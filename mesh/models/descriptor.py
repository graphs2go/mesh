from __future__ import annotations

from typing import TYPE_CHECKING

from graphs2go.models import rdf

from mesh.models.concept import Concept
from mesh.models.tree_number import TreeNumber
from mesh.namespaces import MESHV

if TYPE_CHECKING:
    from collections.abc import Iterable

    from rdflib import URIRef

    from mesh.models.thesaurus import Thesaurus


class Descriptor(rdf.NamedModel):
    """
    A MeSH descriptor, treated as equivalent to an akos.Concept.

    https://hhs.github.io/meshrdf/descriptors
    """

    RDF_TYPES = frozenset(
        (
            MESHV.CheckTag,
            MESHV.GeographicalDescriptor,
            MESHV.PublicationType,
            MESHV.TopicalDescriptor,
        )
    )

    def __init__(self, resource: rdf.NamedResource, thesaurus: Thesaurus):
        super().__init__(resource)
        self.__thesaurus = thesaurus

    def broader_descriptor_iris(self) -> Iterable[URIRef]:
        return self.resource.values(
            MESHV.broaderDescriptor, rdf.Resource.ValueMappers.iri
        )

    def concepts(self) -> Iterable[Concept]:
        """
        Non-preferred MeSH concepts
        """

        concept_resource: rdf.NamedResource
        for concept_resource in self.resource.values(
            MESHV.concept, rdf.Resource.ValueMappers.named_resource
        ):
            yield Concept(concept_resource)

    @property
    def preferred_concept(self) -> Concept:
        return Concept(
            self.resource.required_value(
                MESHV.preferredConcept, rdf.Resource.ValueMappers.named_resource
            )
        )

    @property
    def tree_numbers(self) -> tuple[TreeNumber, ...]:
        return tuple(  # type: ignore
            TreeNumber(resource=resource, thesaurus=self.__thesaurus)
            for resource in self.resource.values(
                MESHV.treeNumber, rdf.Resource.ValueMappers.named_resource
            )
        )
