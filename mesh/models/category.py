from collections.abc import Iterable
from typing import TYPE_CHECKING

from rdflib import RDF, RDFS, Graph, URIRef, Variable

from graphs2go.models import rdf
from mesh.models.descriptor import Descriptor
from mesh.namespaces import MESHV

if TYPE_CHECKING:
    from mesh.models.thesaurus import Thesaurus


class Category:
    """
    A MeSH category (A-N, V, Z) that is the root of a tree.

    These aren't represented in the RDF but are shown in the browser, and are implied by tree numbers.
    We have to synthesize them.

    https://hhs.github.io/meshrdf/tree-numbers
    """

    def __init__(
        self,
        *,
        graph: Graph,
        letter: str,
        pref_label: str,
        thesaurus: "Thesaurus",
    ):
        self.__graph = graph
        self.__iri = URIRef(
            f"http://id.nlm.nih.gov/mesh/{thesaurus.year}/category/{letter}"
        )
        self.__letter = letter
        self.__pref_label = pref_label
        self.__thesaurus = thesaurus

    def _narrower_concepts(self, *, transitive: bool) -> Iterable[Descriptor]:
        result = self.__graph.query(
            f"""\
SELECT ?descriptor
WHERE {{
    VALUES ?descriptorRdfType {{ {' '.join(f'<{rdf_type}>' for rdf_type in Descriptor.RDF_TYPES)} }}
    ?descriptor <{RDF.type}> ?descriptorRdfType .
    ?descriptor <{MESHV.treeNumber}> ?treeNumber .
    ?treeNumber <{RDFS.label}> ?treeNumberLabel .
    FILTER (strStarts(?treeNumberLabel, "{self.letter}") && !contains(?treeNumberLabel, "."))
}}"""
        )

        for binding in result.bindings:
            descriptor_iri = binding[Variable("descriptor")]
            if not isinstance(descriptor_iri, URIRef):
                continue
            descriptor = Descriptor(
                resource=rdf.NamedResource(graph=self.__graph, iri=descriptor_iri),
                thesaurus=self.__thesaurus,
            )
            yield descriptor
            if transitive:
                yield from descriptor._narrower_concepts(transitive=True)

    @property
    def iri(self) -> URIRef:
        return self.__iri

    @property
    def letter(self) -> str:
        return self.__letter

    @property
    def pref_label(self) -> str:
        return self.__pref_label
