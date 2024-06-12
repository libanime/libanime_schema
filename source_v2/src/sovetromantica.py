from ssc_codegen.schema import DictSchema, ItemSchema, ListSchema
from ssc_codegen.document import D, N



class OngoingPage(ListSchema):
    """
    GET https://sovetromantica.com/anime
    """

    __SPLIT_DOC__ = D().css_all(".anime--block__desu")

    # TODO rewrite
    # several css selectors not support next query:
    # .anime--block__name > span + span
    # extract by last index
    title = D().css_all(".anime--block__name > span").last().text()
    thumbnail = D().css(".anime--poster--loading > img").attr("src")
    alt_title = D().css(".anime--block__name > span").text()
    url = D().css(".anime--block__desu a").attr("href")


class SearchPage(OngoingPage):
    """Get all search results by query

    GET https://sovetromantica.com/anime
    query=<QUERY>

    EXAMPLE:
        GET https://sovetromantica.com/anime
        query=LAIN
    """
    pass


class EpisodeView(ListSchema):
    """WARNING!

    target page maybe does not contain video!

    GET https://sovetromantica.com/anime/<ANIME PATH>

    EXAMPLE:
        GET https://sovetromantica.com/anime/1459-sousou-no-frieren

    """
    __SPLIT_DOC__ = D().css_all(".episodes-slick_item")

    url = D().css("a").attr("href").format("https://sovetromantica.com{{}}")
    thumbnail = D().css("img").attr("src")
    title = D().css("img").attr("alt")


class AnimePage(ItemSchema):
    # TODO add example
    """Anime page information

    GET https://sovetromantica.com/anime/<ANIME PATH>

    EXAMPLE:
        GET https://sovetromantica.com/anime/1459-sousou-no-frieren

    ISSUES:
        - description maybe does not exist and return null (CHECK IT)
        - video key maybe returns null (not available)
    """

    title = D().css(".anime-name .block--container").text()
    description = D().default(None).css("#js-description_open-full").text()
    thumbnail = D().css("#poster").attr("src").format("https://sovetromantica.com{{}}")
    # video signature:
    # var config={ "id":"sovetromantica_player",
    # "file":[ { "title":"123", "file":"https://.../subtitles/episode_1/episode_1.m3u8" } ,
    # WARNING!
    #
    #  in main page give first episode video contains in <meta> tag and maybe does not exist
    #
    # EG:
    #
    #  https://sovetromantica.com/anime/1398-tsundere-akuyaku-reijou-liselotte-to-jikkyou-no-endou-kun-to-kaisetsu-no-kobayashi-san
    video_url = D().default(None).raw().re('"file":"([^>]+\.m3u8)"\s*}')
    episodes: EpisodeView = N().sub_parser(EpisodeView)
