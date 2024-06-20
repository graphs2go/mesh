from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace


class MESHV(DefinedNamespace):
    """
    Vocabulary for the Medical Subject Headings (MeSH) thesaurus.

    Adapted from https://nlmpubs.nlm.nih.gov/projects/mesh/rdf/2024/vocabulary_1.0.0.ttl
    """

    _NS = Namespace("http://id.nlm.nih.gov/mesh/vocab#")

    _fail = True

    # Classes
    AllowedDescriptorQualifierPair: URIRef
    CheckTag: URIRef
    Concept: URIRef
    Descriptor: URIRef
    DescriptorQualifierPair: URIRef
    DisallowedDescriptorQualifierPair: URIRef
    GeographicalDescriptor: URIRef
    PublicationType: URIRef
    Qualifier: URIRef
    SCR_Chemical: URIRef
    SCR_Disease: URIRef
    SCR_Protocol: URIRef
    SCR_Organism: URIRef
    SupplementaryConceptRecord: URIRef
    Term: URIRef
    TopicalDescriptor: URIRef
    TreeNumber: URIRef

    # Data properties
    abbreviation: URIRef
    active: URIRef
    altLabel: URIRef
    annotation: URIRef
    casn1_label: URIRef
    considerAlso: URIRef
    dateCreated: URIRef
    dateRevised: URIRef
    entryVersion: URIRef
    frequency: URIRef
    historyNote: URIRef
    identifier: URIRef
    lastActiveYear: URIRef
    nlmClassificationNumber: URIRef
    note: URIRef
    prefLabel: URIRef
    previousIndexing: URIRef
    publishMeSHNote: URIRef
    registryNumber: URIRef
    relatedRegistryNumber: URIRef
    scopeNote: URIRef
    sortVersion: URIRef
    source: URIRef
    thesaurusID: URIRef

    # Object properties
    allowableQualifier: URIRef
    broader: URIRef
    broaderConcept: URIRef
    broaderDescriptor: URIRef
    broaderQualifier: URIRef
    concept: URIRef
    hasDescriptor: URIRef
    hasQualifier: URIRef
    indexerConsideredAlso: URIRef
    mappedTo: URIRef
    narrowerConcept: URIRef
    parentTreeNumber: URIRef
    pharmacologicalAction: URIRef
    preferredConcept: URIRef
    preferredMappedTo: URIRef
    preferredTerm: URIRef
    relatedConcept: URIRef
    seeAlso: URIRef
    term: URIRef
    treeNumber: URIRef
    useInstead: URIRef
