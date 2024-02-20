from typing import Optional, Sequence

from ssc_codegen import Document, DictSchema, ListSchema, ItemSchema, assert_

__all__ = ["OngoingView", "SearchView", "SourceView", "AnimeView", "EpisodeView"]


class OngoingView(ListSchema):
    """usage:

    POST https://jut.su/anime/ongoing/
    ajax_load=yes&start_from_page=1&show_search=&anime_of_user=

    """
    def __pre_validate_document__(self, doc: Document) -> Optional[Document]:
        return assert_.css(doc, '.all_anime_global')

    def __split_document_entrypoint__(self, doc: Document) -> Document:
        return doc.css_all('.all_anime_global')

    def url(self, doc: Document):
        return doc.css('a').attr('href').format('https://jut.su{{}}')

    def title(self, doc: Document):
        return doc.css('.aaname').text()

    def thumbnail(self, doc: Document):
        """signature:

        background: url('https://gen.jut.su/uploads/animethumbs/aaaa.jpg')  no-repeat;
        """
        return doc.css('.all_anime_image').attr('style').re("'(https?://.*?)'")

    def counts(self, doc: Document):
        """signature:

        <div class="aailines">
                1094 серии
                <br>
                14 фильмов
        </div>
        """
        return doc.css_all('.aailines').text().strip('\r\n').join(' ')


class SearchView(ListSchema):
    """
    POST https://jut.su/anime/
    ajax_load=yes&start_from_page=1&show_search=<QUERY>&anime_of_user=
    """

    def __pre_validate_document__(self, doc: Document) -> Optional[Document]:
        return assert_.css(doc, '.all_anime_global')

    def __split_document_entrypoint__(self, doc: Document) -> Document:
        return doc.css_all('.all_anime_global')

    def url(self, doc: Document):
        return doc.css('a').attr('href').format('https://jut.su{{}}')

    def title(self, doc: Document):
        return doc.css('.aaname').text()

    def thumbnail(self, doc: Document):
        """signature:

        background: url('https://gen.jut.su/uploads/animethumbs/aaaa.jpg')  no-repeat;
        """
        return doc.css('.all_anime_image').attr('style').re("'(https?://.*?)'")

    def counts(self, doc: Document):
        """signature:

        <div class="aailines">
                1094 серии
                <br>
                14 фильмов
        </div>
        """
        return doc.css_all('.aailines').text().strip('\r\n').join(' ')


class AnimeView(ItemSchema):
    """
    GET https://jut.su/toradora/
    """
    def title(self, doc: Document):
        # test cases:
        # Смотреть Клинок, рассекающий демонов все серии и сезоны
        # Смотреть ТораДора все серии
        return doc.css('.anime_padding_for_title').text().re('Смотреть (.*?) все')

    def description(self, doc: Document):
        return doc.css_all('.uv_rounded_bottom span').text().join(' ')

    def thumbnail(self, doc: Document):
        # background: url('https://gen.jut.su/uploads/animethumbs/anime_toradora.jpg') no-repeat; background-size: 104px auto;
        return doc.css('.all_anime_title').attr('style').re("'(https?://.*?)'")


class EpisodeView(ListSchema):
    """
    GET https://jut.su/toradora/
    """
    def __split_document_entrypoint__(self, doc: Document) -> Document:
        return doc.css_all('.video')

    def title(self, doc: Document):
        return doc.text().strip(' ')

    def url(self, doc: Document):
        return doc.attr('href').format('https://jut.su{{}}')


class SourceView(ItemSchema):
    """
    GET https://jut.su/toradora/episode-1.html

    NOTE: VIDEO REQUEST SHOULD HAVE SAME USER-AGENT AS CLIENT

    need set user-agent same as send HTTP request in API

    eg:

    cl = Client(headers={"user-agent": "X"})

    s = SourceView(doc).parse().view()

    mpv s["url_1080"]  # 403, FORBIDDEN

    mpv s["url_1080"] --user-agent="Y"  # 403, FORBIDDEN

    mpv s["url_1080"] --user-agent="X"  # 200, OK
    """
    def url_1080(self, doc: Document):
        with doc.default(None):
            return doc.css('.watch_additional_players .wap_player').attr('data-player-1080')

    def url_720(self, doc: Document):
        with doc.default(None):
            return doc.css('.watch_additional_players .wap_player').attr('data-player-720')

    def url_480(self, doc: Document):
        with doc.default(None):
            return doc.css('.watch_additional_players .wap_player').attr('data-player-480')

    def url_360(self, doc: Document):
        with doc.default(None):
            return doc.css('.watch_additional_players .wap_player').attr('data-player-360')
