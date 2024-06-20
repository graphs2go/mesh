from typing import TYPE_CHECKING

from rdflib import URIRef

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
        letter: str,
        pref_label: str,
        thesaurus: "Thesaurus",
    ):
        self.__iri = URIRef(
            f"http://id.nlm.nih.gov/mesh/{thesaurus.year}/category/{letter}"
        )
        self.__letter = letter
        self.__pref_label = pref_label

    @property
    def iri(self) -> URIRef:
        return self.__iri

    @property
    def letter(self) -> str:
        return self.__letter

    @property
    def pref_label(self) -> str:
        return self.__pref_label
