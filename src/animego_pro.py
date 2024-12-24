from ssc_codegen import D, N, DictSchema, ItemSchema, ListSchema


class OngoingPage(ListSchema):
    """Get all available ongoings from main page

    GET https://animego.pro/ongoing
    """

    __SPLIT_DOC__ = D().css_all(".card")

    url = D().css(".card .card__title > a").attr("href")
    title = D().css(".card .card__title > a").text()
    # maybe returns `animego-online.org` src link - path this"""
    thumbnail = D().css(".card img").attr("src").ltrim("https://animego-online.org").format("https://animego.pro{{}}")


class SearchPage(OngoingPage):
    """Get all search results by query

    POST https://animego.pro
    do=search&subaction=search&story=QUERY
    """
    pass


class AnimePage(ItemSchema):
    """Anime page information. anime path contains in SearchView.url or Ongoing.url

    GET https://animego.pro/<ANIME_PATH>

    EXAMPLE:

        GET https://animego.pro/3374-serial-experiments-lain.html
    """

    title = D().css(".page__header h1").text()
    description = D().css_all(".clearfix").text().join(" ")
    # maybe returns `animego-online.org` src link - path this
    thumbnail = (
        D()
        .css(".pmovie__poster > img")
        .attr("src")
        .ltrim("https://animego-online.org")
        .format("https://animego.pro{{}}")
    )
    # id required for next requests (for EpisodesView)
    news_id = D().css("#kodik_player_ajax").attr("data-news_id")


class EpisodeDubbersView(DictSchema):
    __SPLIT_DOC__ = D().css_all("#translators-list > li")

    __KEY__ = D().attr("data-this_translator")
    __VALUE__ = D().text()


class EpisodesPage(ItemSchema):
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

    dubbers = N().sub_parser(EpisodeDubbersView)
    #  first player url. Required for extract episodes"
    #
    #     Eg LINK signature:
    #               data-id vvvv       data-hash                                                          dubber_id
    #                       vvvv       vvvvv                                                                vvvv
    # '//kodik.info/serial/56520/fd227df3f52d477c793a58f4c99ee4f2/720p?translations=false&only_translations=28220'
    player_url = D().css("#player_kodik > iframe").attr("src").format("https:{{}}")


class SourceKodikEpisodesView(ListSchema):
    __SPLIT_DOC__ = D().css_all(".serial-series-box > select > option")

    value = D().attr("value")
    data_id = D().attr("data-id")
    data_hash = D().attr("data-hash")
    data_title = D().attr("data-title").trim(" ")


class SourceKodikTranslationsView(ListSchema):
    __SPLIT_DOC__ = D().css_all(".serial-translations-box > select > option")

    value = D().attr("value")
    data_id = D().attr("data-id")
    data_translation_type = D().attr("data-translation-type")
    data_media_id = D().attr("data-media-id")
    data_media_hash = D().attr("data-media-hash")
    data_media_type = D().attr("data-media-type")
    data_title = D().attr("data-title")
    data_episode_count = D().attr("data-episode-count")


class SourceKodikSerialPage(ItemSchema):
    """extract videos from kodik serial path. this values helps create video player link

    Example:
         SERIAL, bot SERIA path====vvvvv
        - GET 'https://kodik.info/serial/58496/d2a8737db86989de0863bac5c14ce18b/720p?translations=false&only_translations=1895'
    """

    episodes = N().sub_parser(SourceKodikEpisodesView)
    translations = N().sub_parser(SourceKodikTranslationsView)
