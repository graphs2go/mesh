from collections.abc import Iterable
from multiprocessing import JoinableQueue, Queue

from graphs2go.models import interchange
from graphs2go.models.label_type import LabelType
from graphs2go.transformers import parallel_transform
from rdflib import SKOS, Literal, URIRef
from returns.maybe import Some

from mesh.models import Category, Descriptor, Term, Thesaurus

_DESCRIPTOR_BATCH_SIZE = 100
_IN_PROCESS = True


def __transform_category(
    *, category: Category, concept_scheme_iri: URIRef
) -> Iterable[interchange.Model]:
    # See note in Thesaurus about what categories are.

    yield interchange.Node.builder(category.iri).add_type(SKOS.Concept).build()

    yield interchange.Label.builder(
        literal_form=Literal(category.pref_label),
        subject=category.iri,
        type_=Some(LabelType.PREFERRED),
    ).build()

    yield interchange.Relationship.builder(
        category.iri, SKOS.topConceptOf, concept_scheme_iri
    ).build()

    yield interchange.Relationship.builder(
        concept_scheme_iri, SKOS.hasTopConcept, category.iri
    ).build()


def __transform_descriptor(
    *, concept_scheme_iri: URIRef, descriptor: Descriptor
) -> Iterable[interchange.Model]:
    yield interchange.Node.builder(descriptor.iri).add_type(SKOS.Concept).build()

    yield from __transform_descriptor_labels(descriptor)

    yield from __transform_descriptor_properties(descriptor)

    yield from __transform_descriptor_relationships(
        concept_scheme_iri=concept_scheme_iri, descriptor=descriptor
    )


def _transform_descriptor_consumer(
    input_: Thesaurus.Descriptor,
    output_queue: Queue,
    work_queue: JoinableQueue,
) -> None:
    with Thesaurus.open(input_, read_only=True) as thesaurus:
        while True:
            descriptor_iris: tuple[URIRef, ...] | None = work_queue.get()

            if descriptor_iris is None:
                work_queue.task_done()
                break  # Signal from the producer there's no more work

            interchange_models: list[interchange.Model] = []  # type: ignore
            for descriptor_iri in descriptor_iris:
                interchange_models.extend(
                    __transform_descriptor(
                        concept_scheme_iri=thesaurus.iri,
                        descriptor=thesaurus.descriptor_by_iri(descriptor_iri),
                    )
                )
            output_queue.put(tuple(interchange_models))
            work_queue.task_done()


def __transform_descriptor_labels(
    descriptor: Descriptor,
) -> Iterable[interchange.Model]:
    def transform_mesh_term_to_interchange_label(
        *, term_: Term, type_: LabelType
    ) -> interchange.Label:
        return interchange.Label.builder(
            literal_form=Literal(term_.pref_label),
            subject=descriptor.iri,
            type_=Some(type_),
        ).build()

    yield transform_mesh_term_to_interchange_label(
        term_=descriptor.preferred_concept.preferred_term, type_=LabelType.PREFERRED
    )

    for concept in descriptor.concepts():
        yield transform_mesh_term_to_interchange_label(
            term_=concept.preferred_term, type_=LabelType.ALTERNATIVE
        )

        for term in concept.terms():
            yield transform_mesh_term_to_interchange_label(
                term_=term, type_=LabelType.ALTERNATIVE
            )


def __transform_descriptor_properties(
    descriptor: Descriptor,
) -> Iterable[interchange.Model]:
    for property_predicate, property_value in (
        (SKOS.scopeNote, descriptor.preferred_concept.scope_note.value_or(None)),
    ):
        if property_value is None:
            continue
        yield interchange.Property.builder(
            descriptor.iri, property_predicate, property_value
        ).build()


def __transform_descriptor_relationships(
    *, concept_scheme_iri: URIRef, descriptor: Descriptor
) -> Iterable[interchange.Model]:
    has_broader_descriptor = False
    for broader_descriptor_iri in descriptor.broader_descriptor_iris():
        yield interchange.Relationship.builder(
            descriptor.iri, SKOS.broader, broader_descriptor_iri
        ).build()
        yield interchange.Relationship.builder(
            broader_descriptor_iri, SKOS.narrower, descriptor.iri
        ).build()
        has_broader_descriptor = True

    if has_broader_descriptor:
        yield interchange.Relationship.builder(
            descriptor.iri, SKOS.inScheme, concept_scheme_iri
        ).build()
    else:
        # A top-level descriptor. Yield the categories this descriptor belongs to.
        for tree_number in descriptor.tree_numbers:
            category = tree_number.category
            yield interchange.Relationship.builder(
                descriptor.iri, SKOS.broader, category.iri
            ).build()
            yield interchange.Relationship.builder(
                category.iri, SKOS.narrower, descriptor.iri
            ).build()


def _transform_descriptor_producer(
    input_: Thesaurus.Descriptor, work_queue: JoinableQueue
) -> None:
    descriptor_iris_batch: list[URIRef] = []
    with Thesaurus.open(input_, read_only=True) as thesaurus:
        for descriptor_iri in thesaurus.descriptor_iris():
            descriptor_iris_batch.append(descriptor_iri)
            if len(descriptor_iris_batch) == _DESCRIPTOR_BATCH_SIZE:
                work_queue.put(tuple(descriptor_iris_batch))
                descriptor_iris_batch = []

    if descriptor_iris_batch:
        work_queue.put(tuple(descriptor_iris_batch))


def transform_thesaurus_to_interchange_models(
    thesaurus_descriptor: Thesaurus.Descriptor,
) -> Iterable[interchange.Model]:
    with Thesaurus.open(thesaurus_descriptor, read_only=True) as thesaurus:
        yield (
            interchange.Node.builder(iri=thesaurus.iri)
            .add_type(SKOS.ConceptScheme)
            .build()
        )

        yield interchange.Label.builder(
            literal_form=Literal("Medical Subject Headings (MeSH)"),
            subject=thesaurus.iri,
            type_=Some(LabelType.PREFERRED),
        ).build()

        if _IN_PROCESS:
            for category in thesaurus.categories:
                yield from __transform_category(
                    category=category, concept_scheme_iri=thesaurus.iri
                )

            for descriptor in thesaurus.descriptors():
                yield from __transform_descriptor(
                    concept_scheme_iri=thesaurus.iri, descriptor=descriptor
                )
            return

    yield from parallel_transform(
        consumer=_transform_descriptor_consumer,
        consumer_input=thesaurus_descriptor,
        producer=_transform_descriptor_producer,
        producer_input=thesaurus_descriptor,
    )
