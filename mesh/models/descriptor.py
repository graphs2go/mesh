from __future__ import annotations

from typing import TYPE_CHECKING

from rdflib import URIRef

from graphs2go.models import rdf
from mesh.models.concept import Concept
from mesh.models.tree_number import TreeNumber
from mesh.namespaces import MESHV

if TYPE_CHECKING:
    from collections.abc import Iterable

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

    # @property
    # @cache
    # def alt_labels(self) -> tuple[akos.Label, ...]:
    #     alt_labels: list[akos.Label] = []
    #     for concept in self.__concepts():
    #         alt_labels.append(concept.preferred_term)
    #         alt_labels.extend(concept.terms())
    #     return tuple(alt_labels)

    def broader_descriptors(self, *, transitive: bool) -> Iterable[Descriptor]:
        """
        Yield broader concepts in the SKOS sense of "concept" i.e., MeSH descriptors, not MeSH concepts.
        """
        yielded_broader_descriptor = False
        broader_descriptor_resource: rdf.NamedResource
        for broader_descriptor_resource in self.resource.values(
            MESHV.broaderDescriptor, rdf.Resource.ValueMappers.named_resource
        ):
            broader_descriptor = Descriptor(
                resource=broader_descriptor_resource, thesaurus=self.__thesaurus
            )
            yield broader_descriptor
            yielded_broader_descriptor = True
            if transitive:
                yield from broader_descriptor.broader_descriptors(transitive=True)

        if yielded_broader_descriptor:
            return

        # This is a top-level descriptor. Yield the categories this descriptor belongs to.
        for tree_number in self.tree_numbers:
            yield tree_number.category

    def concepts(self) -> Iterable[Concept]:
        """
        Non-preferred MeSH concepts
        """

        concept_resource: rdf.NamedResource
        for concept_resource in self.resource.values(
            MESHV.concept, rdf.Resource.ValueMappers.named_resource
        ):
            yield Concept(concept_resource)

    # @property
    # def scope_notes(self) -> tuple[Literal, ...]:
    #     # scope_notes: list[Literal] = []
    #     return self.__preferred_concept.scope_note.map(
    #         lambda scope_note: (scope_note,)
    #     ).value_or(())
    #     # Other concepts do have scope notes, but don't use them.
    #     # if scope_note is not None:
    #     #     scope_notes.append(scope_note)
    #     # for concept in self.__concepts():
    #     #     scope_note = concept.scope_note
    #     #     if scope_note is not None:
    #     #         scope_notes.append(scope_note)
    #     # return tuple(scope_notes)

    def narrower_descriptors(self, *, transitive: bool) -> Iterable[Descriptor]:
        # MeSH has no inverse of mesh:broaderConcept, so we infer it here.
        for narrower_descriptor_iri in self.resource.graph.subjects(
            predicate=MESHV.broaderDescriptor, object=self.identifier
        ):
            if not isinstance(narrower_descriptor_iri, URIRef):
                continue
            narrower_descriptor = Descriptor(
                resource=rdf.NamedResource(
                    graph=self.resource.graph, iri=narrower_descriptor_iri
                ),
                thesaurus=self.__thesaurus,
            )
            yield narrower_descriptor
            if transitive:
                yield from narrower_descriptor.narrower_descriptors(transitive=True)

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
