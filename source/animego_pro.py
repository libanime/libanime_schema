from typing import Optional, Sequence

from ssc_codegen import DictSchema, Document, ItemSchema, ListSchema, assert_

__all__ = [
    "OngoingView",
    "SearchView",
    "AnimeView",
    "EpisodesView",
    "FirstPlayerUrlView",
    "SourceKodikView"
]


class OngoingView(ListSchema):
    """Get all available ongoings from main page

    GET https://animego.pro/ongoing
    """

    def __split_document_entrypoint__(self, doc: Document) -> Document:
        return doc.css_all(".card")

    def url(self, doc: Document):
        """ongoing page"""
        return doc.css('.card .card__title > a').attr('href')

    def title(self, doc: Document):
        return doc.css(".card .card__title > a").text()

    def thumbnail(self, doc: Document):
        """maybe returns `animego-online.org` src link - path this"""
        return doc.css(".card img").attr("src").lstrip('https://animego-online.org').format('https://animego.pro{{}}')


class SearchView(ListSchema):
    """Get all search results by query

    POST https://animego.pro
    do=search&subaction=search&story=QUERY
    """

    def __split_document_entrypoint__(self, doc: Document) -> Document:
        return doc.css_all(".card")

    def url(self, doc: Document):
        """ongoing page"""
        return doc.css('.card .card__title > a').attr('href')

    def title(self, doc: Document):
        return doc.css(".card .card__title > a").text()

    def thumbnail(self, doc: Document):
        """maybe returns `animego-online.org` src link - path this"""
        return doc.css(".card img").attr("src").lstrip('https://animego-online.org').format('https://animego.pro{{}}')


class AnimeView(ItemSchema):
    """Anime page information. anime path contains in SearchView.url or Ongoing.url

    GET https://animego.pro/<ANIME_PATH>

    EXAMPLE:

        GET https://animego.pro/3374-serial-experiments-lain.html
    """

    def title(self, doc: Document):
        return doc.css(".page__header h1").text()

    def description(self, doc: Document):
        return doc.css_all(".clearfix").text().join(" ")

    def thumbnail(self, doc: Document):
        """maybe returns `animego-online.org` src link - path this"""
        return (doc.css(".pmovie__poster > img").attr("src").lstrip('https://animego-online.org')
                .format('https://animego.pro{{}}'))

    def news_id(self, doc: Document):
        """id required for next requests (for EpisodesView)"""
        return doc.css("#kodik_player_ajax").attr("data-news_id")


class EpisodesView(ListSchema):
    """Representation dubbers, and video url data

    Prepare:
      1. get news_id from Anime object
      2. POST 'https://animego.pro/engine/ajax/controller.php?mod=kodik_playlist_ajax'
        news_id=<AnimeView.news_id>&action=load_player
      3. send request to /serial/ link, DROP param only_translations
    EXAMPLE:

        # SOURCE:
            https://animego.pro/6240-loop-7-kaime-no-akuyaku-reijou-wa-moto-tekikoku-de-jiyuukimama-na-hanayome-seikatsu-o-mankitsu-suru.html

        POST https://animego.pro/engine/ajax/controller.php?mod=kodik_playlist_ajax
        news_id=6240&action=load_player
    """

    def __split_document_entrypoint__(self, doc: Document) -> Sequence[Document]:
        return doc.css_all(".serial-translations-box > select > option")

    def value(self, doc: Document) -> Document:
        return doc.attr("value")

    def id(self, doc: Document) -> Document:
        return doc.attr('data-id')

    def media_id(self, doc: Document) -> Document:
        """video id"""
        return doc.attr('data-media-id')

    def media_hash(self, doc: Document) -> Document:
        """video hash"""
        return doc.attr('data-media-hash')

    def media_type(self, doc: Document) -> Document:
        """video type"""
        return doc.attr('data-media-type')

    def title(self, doc: Document) -> Document:
        """dubber name"""
        return doc.attr('data-title')

    def episode_count(self, doc: Document) -> Document:
        """episodes count for dubber"""
        return doc.attr('data-episode-count')


class FirstPlayerUrlView(ItemSchema):
    """Prepare:
      1. get news_id from Anime object
      2. POST 'https://animego.pro/engine/ajax/controller.php?mod=kodik_playlist_ajax'
        news_id=<AnimeView.news_id>&action=load_player

    EXAMPLE:

        # SOURCE:
            https://animego.pro/6240-loop-7-kaime-no-akuyaku-reijou-wa-moto-tekikoku-de-jiyuukimama-na-hanayome-seikatsu-o-mankitsu-suru.html

        POST https://animego.pro/engine/ajax/controller.php?mod=kodik_playlist_ajax
        news_id=6240&action=load_player
        """

    def url(self, doc: Document):
        """return first player url. Required for extract episodes"

        Eg LINK signature:
                  data-id vvvv       data-hash                                                          dubber_id
                          vvvv       vvvvv                                                                vvvv
    '//kodik.info/serial/56520/fd227df3f52d477c793a58f4c99ee4f2/720p?translations=false&only_translations=28220'
        """
        return doc.css('#player_kodik > iframe').attr('src').format("https:{{}}")


class SourceKodikView(ListSchema):
    """extract videos from kodik serial path. this values helps create video player link

    Example:
         SERIAL, NOT SERIA path====vvvvv
        - GET 'https://kodik.info/serial/58496/d2a8737db86989de0863bac5c14ce18b/720p?translations=false&only_translations=1895'
    """
    def __split_document_entrypoint__(self, doc: Document) -> Document:
        return doc.css_all('.series-options > div > option')

    def value(self, doc: Document):
        return doc.attr('value')

    def id(self, doc: Document):
        return doc.attr('data-id')

    def hash(self, doc: Document):
        return doc.attr('data-hash')

    def title(self, doc: Document):
        return doc.attr('data-title')

