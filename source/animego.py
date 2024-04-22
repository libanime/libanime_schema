from typing import Optional, Sequence

from ssc_codegen import DictSchema, Document, ItemSchema, ListSchema, assert_

__all__ = [
    "OngoingView",
    "SearchView",
    "AnimeView",
    "DubbersView",
    "EpisodeView",
    "SourceView",
]


class OngoingView(ListSchema):
    """Get all available ongoings from main page

    GET https://animego.org
    """

    def __split_document_entrypoint__(self, doc: Document) -> Document:
        return doc.css_all(".border-bottom-0.cursor-pointer")

    def url(self, doc: Document):
        """ongoing page"""
        return doc.attr("onclick").lstrip("location.href=").strip("'").format("https://animego.org{{}}")

    def title(self, doc: Document):
        return doc.css(".last-update-title").text()

    def thumbnail(self, doc: Document):
        return doc.css(".lazy").attr("style").lstrip("background-image: url(").rstrip(");")

    def episode(self, doc: Document):
        return doc.css(".text-truncate").text().re("(\d+)\s")

    def dub(self, doc: Document):
        return doc.css(".text-gray-dark-6").text().replace(")", "").replace("(", "")


class SearchView(ListSchema):
    """Get all search results by query

    GET https://animego.org/search/anime
    q={QUERY}

    EXAMPLE:

        GET https://animego.org/search/anime?q=LAIN
    """

    def __split_document_entrypoint__(self, doc: Document) -> Document:
        return doc.css_all(".row > .col-ul-2")

    def title(self, doc: Document):
        return doc.css(".text-truncate a").attr("title")

    def thumbnail(self, doc: Document):
        return doc.css(".lazy").attr("data-original")

    def url(self, doc: Document):
        return doc.css(".text-truncate a").attr("href")


class AnimeView(ItemSchema):
    """Anime page information. anime path contains in SearchView.url or Ongoing.urk

    GET https://animego.org/anime/<ANIME_PATH>

    EXAMPLE:

        GET https://animego.org/anime/eksperimenty-leyn-1114
    """

    def title(self, doc: Document):
        return doc.css(".anime-title h1").text()

    def description(self, doc: Document):
        return doc.css_all(".description").text().join(" ")

    def thumbnail(self, doc: Document):
        return doc.css("#content img").attr("src")

    def id(self, doc: Document):
        """anime id required for next requests (for DubberView, Source schemas)"""
        return doc.css(".br-2 .my-list-anime").attr("id").lstrip("my-list-")

    def raw_json(self, doc: Document):
        """DEV key: for parse extra metadata"""
        return doc.css("script[type='application/ld+json']").text()


class DubbersView(DictSchema):
    """Representation dubbers in {id: 'dubber_id', name: 'dubber_name'}

    Prepare:
      1. get id from Anime object
      2. GET 'https://animego.org/anime/{Anime.id}/player?_allow=true'
      3. extract html from json by ['content'] key
      4. OPTIONAL: unescape HTML

    EXAMPLE:
        GET https://animego.org/anime/anime/1114//player?_allow=true
    """

    def __pre_validate_document__(self, doc: Document) -> Optional[Document]:
        return assert_.css(doc, "#video-dubbing .mb-1")

    def __split_document_entrypoint__(self, doc: Document) -> Sequence[Document]:
        return doc.css_all("#video-dubbing .mb-1")

    def key(self, doc: Document) -> Document:
        """dubber id"""
        return doc.attr("data-dubbing")

    def value(self, doc: Document) -> Document:
        return doc.css("span").text().strip("\n").strip(" ").rstrip("\n")


class EpisodeView(ListSchema):
    """Representation episodes

    Prepare:
      1. get id from Anime object
      2. GET 'https://animego.org/anime/{Anime.id}/player?_allow=true'
      3. extract html from json by ['content'] key
      4. OPTIONAL: unescape HTML

    EXAMPLE:
        GET https://animego.org/anime/anime/1114//player?_allow=true
    """

    def __split_document_entrypoint__(self, doc: Document) -> Document:
        return doc.css_all("#video-carousel .mb-0")

    def __pre_validate_document__(self, doc: Document) -> Optional[Document]:
        return assert_.css(doc, "#video-carousel .mb-0")

    def num(self, doc: Document):
        return doc.attr("data-episode")

    def title(self, doc: Document):
        return doc.attr("data-episode-title")

    def id(self, doc: Document):
        return doc.attr("data-id")


class SourceView(ListSchema):
    """representation videos

    Prepare:
      1. get num and id from Episode

      2.

      GET https://animego.org/anime/series
      dubbing=2&provider=24&episode={Episode.num}id={Episode.id}

      3. extract html from json by ["content"] key

      4. OPTIONAL: unescape document

    EXAMPLE:

        GET https://animego.org/anime/series?dubbing=2&provider=24&episode=2&id=15837
    """

    def __split_document_entrypoint__(self, doc: Document) -> Document:
        return doc.css_all("#video-players > span")

    def title(self, doc: Document):
        return doc.text()

    def url(self, doc: Document):
        return doc.attr("data-player").format("https:{{}}")

    def data_provider(self, doc: Document):
        """player id"""
        return doc.attr("data-provider")

    def data_provide_dubbing(self, doc: Document):
        """dubber id"""
        return doc.attr("data-provide-dubbing")
