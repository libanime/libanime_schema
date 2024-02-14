from typing import Optional, Sequence

from ssc_codegen import Document, DictSchema, ListSchema, ItemSchema, assert_


__all__ = ["OngoingView", "SearchView", "AnimeView", "EpisodeView"]


class OngoingView(ListSchema):
    """
     Prepare:
      1. GET https://sovetromantica.com/anime
    """

    def __pre_validate_document__(self, doc: Document) -> Optional[Document]:
        return assert_.re(doc.css('title').text(), "Аниме / SovetRomantica")

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
    """ Get all search results by query

    Prepare:
      1. GET https://sovetromantica.com/anime?query=<QUERY>"""
    def __split_document_entrypoint__(self, doc: Document) -> Document:
        return doc.css_all(".anime--block__desu")

    def __pre_validate_document__(self, doc: Document) -> Optional[Document]:
        return assert_.re(doc.css("title").text(), "Аниме / SovetRomantica")

    def title(self, doc: Document):
        # TODO rewrite
        return doc.css(".anime--block__name > span + span").text()

    def thumbnail(self, doc: Document):
        return doc.css(".anime--poster--loading > img").attr('src')

    def alt_title(self, doc: Document):
        return doc.css(".anime--block__name > span").text()

    def url(self, doc: Document):
        return doc.css(".anime--block__desu a").attr('href')


class AnimeView(ItemSchema):
    # TODO add example
    """Anime page information

    Prepare:
      1. GET to anime URL page"""
    def __pre_validate_document__(self, doc: Document) -> Optional[Document]:
        return assert_.re(doc.css('title').text(), "/ SovetRomantica")

    def title(self, doc: Document):
        return doc.css(".anime-name .block--container").text()

    def description(self, doc: Document):
        return doc.css(".block--full anime-description").text()

    def thumbnail(self, doc: Document):
        return doc.css("#poster").attr('src')

    def video(self, doc: Document):
        """WARNING!

        in main page give first episode video contains in <meta> tag and maybe does not exist

        EG:

          https://sovetromantica.com/anime/1398-tsundere-akuyaku-reijou-liselotte-to-jikkyou-no-endou-kun-to-kaisetsu-no-kobayashi-san
        """
        with doc.default(None):
            return doc.raw().re(r'content=\"(https://.*\.m3u8)\"')


class EpisodeView(ListSchema):
    """ WARNING!

    target page maybe does not contain video!

    Prepare:
      1. GET https://sovetromantica.com/anime?query=<QUERY>
      """

    def __split_document_entrypoint__(self, doc: Document) -> Document:
        return doc.css_all(".episodes-slick_item")

    def __pre_validate_document__(self, doc: Document) -> Optional[Document]:
        return assert_.re(doc.css('title').text(), "/ SovetRomantica")

    def url(self, doc: Document):
        return doc.css("a").attr("href").format("https://sovetromantica.com/anime{{}}")

    def thumbnail(self, doc: Document):
        return doc.css("img").attr("src")

    def title(self, doc: Document):
        return doc.css("img").attr("alt")