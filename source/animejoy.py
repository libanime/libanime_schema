from typing import Optional, Sequence

from ssc_codegen import Document, DictSchema, ListSchema, ItemSchema, assert_

# NOTE: this source have CLOUDFLARE, sometimes maybe not works
__all__ = ["OngoingView", "SearchView", "AnimeView", "PlayerView", "PlayerUrls"]


class OngoingView(ListSchema):
    """
    Prepare:
      1. GET https://animejoy.ru
    """

    def __pre_validate_document__(self, doc: Document) -> Optional[Document]:
        return assert_.re(doc.css("title").text(), "AnimeJoy.Ru аниме с субтитрами")

    def __split_document_entrypoint__(self, doc: Document) -> Document:
        return doc.css_all(".shortstory")

    def url(self, doc: Document):
        return doc.css(".ntitle > a").attr("href")

    def title(self, doc: Document):
        return doc.css(".ntitle > a").text()

    def alt_title(self, doc: Document):
        return doc.css(".romanji").text()

    def thumbnail(self, doc: Document):
        return doc.css(".fr-fil").attr("src").format("https://animejoy.ru{{}}")


class SearchView(ListSchema):
    """
    Prepare:

      1. POST https://animejoy.ru/

      2. payload:
        story: <QUERY>, do: search, subaction: search
    """

    def __split_document_entrypoint__(self, doc: Document) -> Document:
        return doc.css_all(".shortstory")

    def __pre_validate_document__(self, doc: Document) -> Optional[Document]:
        return assert_.re(doc.css("title").text(), "Поиск по сайту")

    def title(self, doc: Document):
        return doc.css(".ntitle > a").text()

    def alt_title(self, doc: Document):
        return doc.css(".romanji").text()

    def thumbnail(self, doc: Document):
        return doc.css(".fr-fil").attr("src")

    def url(self, doc: Document):
        return doc.css(".ntitle > a").attr("href").format("https://animejoy.ru{{}}")


class AnimeView(ItemSchema):
    """
    Prepare:
      1. GET anime page
    """

    def __pre_validate_document__(self, doc: Document) -> Optional[Document]:
        return assert_.re(doc.css("title").text(), "Поиск по сайту")

    def title(self, doc: Document):
        return doc.css(".ntitle > a").text()

    def alt_title(self, doc: Document):
        return doc.css(".romanji").text()

    def url(self, doc: Document):
        return doc.css(".ntitle > a").attr("href")

    def description(self, doc: Document):
        return doc.css(".pcdescrf p").text()

    def thumbnail(self, doc: Document):
        return doc.css(".fr-fil").attr("src").format("https://animejoy.ru{{}}")

    def news_id(self, doc: Document):
        """required for extract episodes and videos"""
        return doc.css("div.playlists-ajax").attr("data-news_id")


class PlayerView(DictSchema):
    """Represent player name and player id

    Prepare:
      1. get news_id from Anime

      2. GET https://animejoy.ru/engine/ajax/playlists.php?news_id={Anime.news_id}&xfield=playlist

      3. get json, get HTML by "response" key

      4. OPTIONAL: Unescape document
    """

    def __split_document_entrypoint__(self, doc: Document) -> Sequence[Document]:
        return doc.css_all(".playlists-player > .playlists-lists ul > li")

    def __pre_validate_document__(self, doc: Document) -> Optional[Document]:
        return assert_.css(doc, ".playlists-player > .playlists-lists ul > li")

    def key(self, doc: Document) -> Document:
        return doc.attr("data-id")

    def value(self, doc: Document) -> Document:
        return doc.text()


class PlayerUrls(DictSchema):
    """Represent player url and player id

    Prepare:
      1. get news_id from Anime
      2. GET https://animejoy.ru/engine/ajax/playlists.php?news_id={Anime.news_id}&xfield=playlist
      3. get json, get HTML by "response" key
      4. OPTIONAL: Unescape document
    """

    def __split_document_entrypoint__(self, doc: Document) -> Sequence[Document]:
        return doc.css_all(".playlists-videos > .playlists-items ul > li")

    def __pre_validate_document__(self, doc: Document) -> Optional[Document]:
        return assert_.css(doc, ".playlists-videos > .playlists-items ul > li")

    def key(self, doc: Document) -> Document:
        return doc.attr("data-id")

    def value(self, doc: Document) -> Document:
        return doc.attr("data-file")
