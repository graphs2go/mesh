from __future__ import annotations

import logging
from functools import cache
from typing import TYPE_CHECKING

from rdflib import RDF, URIRef

from graphs2go.models import rdf
from mesh.models.category import Category
from mesh.models.descriptor import Descriptor

if TYPE_CHECKING:
    from collections.abc import Iterable

logger = logging.getLogger(__name__)


class Thesaurus(rdf.Graph[rdf.Model]):
    @property
    @cache
    def categories(self) -> tuple[Category, ...]:
        # Synthesize categories from their representations in the browser, since they aren't represented in the RDF.
        # https://meshb.nlm.nih.gov/treeView
        # https://hhs.github.io/meshrdf/tree-numbers

        return tuple(
            Category(letter=letter, pref_label=pref_label, thesaurus=self)
            for letter, pref_label in (
                ("A", "Anatomy"),
                ("B", "Organisms"),
                ("C", "Diseases"),
                ("D", "Chemicals and Drugs"),
                (
                    "E",
                    "Analytical, Diagnostic and Therapeutic Techniques, and Equipment",
                ),
                ("F", "Psychiatry and Psychology"),
                ("G", "Phenomena and Processes"),
                ("H", "Disciplines and Occupations"),
                ("I", "Anthropology, Education, Sociology, and Social Phenomena"),
                ("J", "Technology, Industry, and Agriculture"),
                ("K", "Humanities"),
                ("L", "Information Science"),
                ("M", "Named Groups"),
                ("N", "Health Care"),
                ("V", "Publication Characteristics"),
                ("Z", "Geographicals"),
            )
        )

    def descriptor_by_iri(self, iri: URIRef) -> Descriptor:
        return Descriptor(
            resource=rdf.NamedResource(graph=self.rdflib_graph, iri=iri),
            thesaurus=self,
        )

    def descriptors(self) -> Iterable[Descriptor]:
        for descriptor_iri in self.descriptor_iris():
            yield self.descriptor_by_iri(descriptor_iri)

    def descriptor_iris(self) -> Iterable[URIRef]:
        # The MeSH RDF doesn't have rdfs:subClassOf mesh:Descriptor statements in it, so we have to check the subclasses individually.
        for descriptor_rdf_type in Descriptor.RDF_TYPES:
            for descriptor_iri in self.rdflib_graph.subjects(
                predicate=RDF.type, object=descriptor_rdf_type
            ):
                if not isinstance(descriptor_iri, URIRef):
                    continue
                yield descriptor_iri

    @property
    @cache
    def iri(self) -> URIRef:
        return URIRef(f"http://id.nlm.nih.gov/mesh/{self.year}/")

    @property
    @cache
    def year(self) -> int:
        return int(self.identifier.rsplit(":", 1)[-1])
