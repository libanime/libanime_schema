from typing import Optional, Sequence

from ssc_codegen import DictSchema, Document, ItemSchema, ListSchema, assert_

__all__ = ["OngoingView", "SearchView", "AnimeView", "EpisodeView"]


class OngoingView(ListSchema):
    """
    GET https://sovetromantica.com/anime
    """

    def __split_document_entrypoint__(self, doc: Document) -> Document:
        return doc.css_all(".anime--block__desu")

    def url(self, doc: Document):
        """ongoing page"""
        return doc.css(".anime--block__desu a").attr("href")

    def title(self, doc: Document):
        # TODO simplify css without `+`
        return doc.css(".anime--block__name > span + span").text()

    def thumbnail(self, doc: Document):
        return doc.css(".anime--poster--loading > img").attr("src")

    def alt_title(self, doc: Document):
        return doc.css(".anime--block__name > span").text()


class SearchView(ListSchema):
    """Get all search results by query

    GET https://sovetromantica.com/anime
    query=<QUERY>

    EXAMPLE:
        GET https://sovetromantica.com/anime
        query=LAIN
    """

    def __split_document_entrypoint__(self, doc: Document) -> Document:
        return doc.css_all(".anime--block__desu")

    def __pre_validate_document__(self, doc: Document) -> Optional[Document]:
        return assert_.re(doc.css("title").text(), "Аниме / SovetRomantica")

    def title(self, doc: Document):
        # TODO rewrite
        return doc.css(".anime--block__name > span + span").text()

    def thumbnail(self, doc: Document):
        return doc.css(".anime--poster--loading > img").attr("src")

    def alt_title(self, doc: Document):
        return doc.css(".anime--block__name > span").text()

    def url(self, doc: Document):
        return doc.css(".anime--block__desu a").attr("href")


class AnimeView(ItemSchema):
    # TODO add example
    """Anime page information

    GET https://sovetromantica.com/anime/<ANIME PATH>

    EXAMPLE:
        GET https://sovetromantica.com/anime/1459-sousou-no-frieren
    """

    def title(self, doc: Document):
        return doc.css(".anime-name .block--container").text()

    def description(self, doc: Document):
        with doc.default(""):
            return doc.css("#js-description_open-full").text()

    def thumbnail(self, doc: Document):
        return doc.css("#poster").attr("src").format("https://sovetromantica.com{{}}")

    def video(self, doc: Document):
        """WARNING!

        in main page give first episode video contains in <meta> tag and maybe does not exist

        EG:

          https://sovetromantica.com/anime/1398-tsundere-akuyaku-reijou-liselotte-to-jikkyou-no-endou-kun-to-kaisetsu-no-kobayashi-san
        """
        # video signature:
        # var config={  "id":"sovetromantica_player",
        # "file":[ { "title":"123", "file":"https://.../subtitles/episode_1/episode_1.m3u8" } ,
        with doc.default(None):
            return doc.raw().re(r'"file":"([^>]+\.m3u8)"\s*}')


class EpisodeView(ListSchema):
    """WARNING!

    target page maybe does not contain video!

    GET https://sovetromantica.com/anime/<ANIME PATH>

    EXAMPLE:
        GET https://sovetromantica.com/anime/1459-sousou-no-frieren

    """

    def __split_document_entrypoint__(self, doc: Document) -> Document:
        return doc.css_all(".episodes-slick_item")

    def __pre_validate_document__(self, doc: Document) -> Optional[Document]:
        return assert_.re(doc.css("title").text(), "/ SovetRomantica")

    def url(self, doc: Document):
        return doc.css("a").attr("href").format("https://sovetromantica.com{{}}")

    def thumbnail(self, doc: Document):
        return doc.css("img").attr("src")

    def title(self, doc: Document):
        return doc.css("img").attr("alt")
