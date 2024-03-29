from typing import Optional, Sequence

from ssc_codegen import DictSchema, Document, ItemSchema, ListSchema, assert_

__all__ = ["AnimeView", "OngoingView", "VideoView", "SearchView", "DubbersView"]


class OngoingView(ListSchema):
    """Send to main page request

    GET https://animania.online/
    """

    def __pre_validate_document__(self, doc: Document) -> Optional[Document]:
        pass

    def __split_document_entrypoint__(self, doc: Document) -> Document:
        return doc.css_all(".short-tablet")

    def url(self, doc: Document):
        return doc.css(".st-poster").attr("href")

    def title(self, doc: Document):
        return doc.css("h5").text()

    def thumbnail(self, doc: Document):
        return doc.css("img").attr("data-src").format("https://animania.online{{}}")


class SearchView(ListSchema):
    """Send search request

    GET https://animania.online/index.php
    story={QUERY}&do=search&subaction=search
    """

    def __split_document_entrypoint__(self, doc: Document) -> Document:
        return doc.css_all("#short")

    def title(self, doc: Document):
        return doc.css("img").attr("alt")

    def thumbnail(self, doc: Document):
        return doc.css("img").attr("src").format("https://animania.online{{}}")

    def url(self, doc: Document):
        return doc.css("a").attr("href")


class AnimeView(ItemSchema):
    """send request to anime page

    GET https://animania.online/9403-jeksperimenty-ljejn-serial-experiments-lain-1998-smotret-onlajn.html
    """

    def title(self, doc: Document):
        return doc.css("h1").text()

    def description(self, doc: Document):
        return doc.css("#fdesc").text()

    def thumbnail(self, doc: Document):
        return doc.css(".fposter img").attr("data-src").format("https://animania.online{{}}")


class DubbersView(DictSchema):
    """send to anime page request

    GET https://animania.online/9403-jeksperimenty-ljejn-serial-experiments-lain-1998-smotret-onlajn.html
    """

    def __split_document_entrypoint__(self, doc: Document) -> Sequence[Document]:
        return doc.css_all("#ks-translations > span")

    def key(self, doc: Document) -> Document:
        """get dubber id

        attr signature kodikSlider.season('1', this)
        """
        return doc.attr("onclick").re("(\d+)")

    def value(self, doc: Document) -> Document:
        return doc.text()


class VideoView(ListSchema):
    """send request to anime page

    GET https://animania.online/9403-jeksperimenty-ljejn-serial-experiments-lain-1998-smotret-onlajn.html
    """

    def __split_document_entrypoint__(self, doc: Document) -> Sequence[Document]:
        return doc.css_all("#ks-episodes > li")

    def id(self, doc: Document) -> Document:
        """get dubber id

        attr signature <li id="season1" ...>
        """
        return doc.attr("id").lstrip("season")

    def names(self, doc: Document) -> Document:
        return doc.css_all("span").text()

    def urls(self, doc: Document):
        return doc.raw().re_all("'(//.*?)'").format("https:{{}}")
