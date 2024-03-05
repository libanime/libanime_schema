from typing import Optional, Sequence

from ssc_codegen import DictSchema, Document, ItemSchema, ListSchema, assert_


class OngoingView(ListSchema):
    def __pre_validate_document__(self, doc: Document) -> Optional[Document]:
        pass

    def __split_document_entrypoint__(self, doc: Document) -> Document:
        pass

    def url(self, doc: Document):
        pass

    def title(self, doc: Document):
        pass

    def thumbnail(self, doc: Document):
        pass


class SearchView(ListSchema):
    def __split_document_entrypoint__(self, doc: Document) -> Document:
        pass

    def title(self, doc: Document):
        pass

    def thumbnail(self, doc: Document):
        pass

    def url(self, doc: Document):
        pass


class AnimeView(ItemSchema):
    def title(self, doc: Document):
        pass

    def description(self, doc: Document):
        pass

    def thumbnail(self, doc: Document):
        pass


class DubbersView(DictSchema):
    def __split_document_entrypoint__(self, doc: Document) -> Sequence[Document]:
        pass

    def key(self, doc: Document) -> Document:
        pass

    def value(self, doc: Document) -> Document:
        pass


class EpisodeView(ListSchema):
    def __split_document_entrypoint__(self, doc: Document) -> Document:
        pass

    def title(self, doc: Document):
        pass


class SourceView(ListSchema):
    def __split_document_entrypoint__(self, doc: Document) -> Document:
        pass

    def title(self, doc: Document):
        pass

    def url(self, doc: Document):
        pass
