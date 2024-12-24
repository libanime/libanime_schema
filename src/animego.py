from typing import List, Optional, Sequence

from ssc_codegen import D, N, DictSchema, ItemSchema, ListSchema

# old domain - animego.org
URL_FMT = "https://animego.me" + "{{}}"


class OngoingPage(ListSchema):
    """Get all available ongoings from the main page

    GET https://animego.me
    """

    __SPLIT_DOC__ = D().css_all(".border-bottom-0.cursor-pointer")

    url = D().attr("onclick").ltrim("location.href=").trim("'").format(URL_FMT)
    title = D().css(".last-update-title").text()
    thumbnail = D().css(".lazy").attr("style").ltrim("background-image: url(").rtrim(");")
    episode = D().css(".text-truncate").text().re("(\d+)\s")
    dub = D().css(".text-gray-dark-6").text().replace(")", "").replace("(", "")


class SearchPage(ListSchema):
    """Get all search results by query

    USAGE:

        GET https://animego.me/search/anime
        q={QUERY}

    EXAMPLE:

        GET https://animego.me/search/anime?q=LAIN
    """

    __SPLIT_DOC__ = D().css_all(".row > .col-ul-2")

    title = D().css(".text-truncate a").attr("title")
    thumbnail = D().css(".lazy").attr("data-original")
    url = D().css(".text-truncate a").attr("href")


class AnimePage(ItemSchema):
    """Anime page information. anime path contains in SearchView.url or Ongoing.url

    - id needed for next API requests
    - raw_json used for extract extra metadata (unescape required)

    USAGE:

        GET https://animego.me/anime/<ANIME_PATH>

    EXAMPLE:

        GET https://animego.me/anime/eksperimenty-leyn-1114
    """

    title = D().css(".anime-title h1").text()
    # maybe missing description eg:
    # https://animego.org/anime/chelovek-muskul-2589
    description = D().default('').css_all(".description").text().join('').re_sub(r"^\s+|\s+$", "")
    thumbnail = D().css("#content img").attr("src")
    # anime id required for next requests (for DubberView, Source schemas)
    id = D().css(".br-2 .my-list-anime").attr("id").ltrim("my-list-")

    # DEV key: for parse extra metadata can be json unmarshal.
    # unescape required
    raw_json = D().css("script[type='application/ld+json']").text()


class EpisodeDubbersView(DictSchema):
    __SPLIT_DOC__ = D().css_all("#video-dubbing .mb-1")
    __SIGNATURE__ = {"<dubber_id>": "<dubber_name>", "<id>": "..."}

    __KEY__ = D().attr("data-dubbing")
    __VALUE__ = D().css("span").text().re_sub(r"^\s+|\s+$", "")


class EpisodesView(ListSchema):
    __SPLIT_DOC__ = D().css_all("#video-carousel .mb-0")

    num = D().attr("data-episode")
    title = D().attr("data-episode-title")
    id = D().attr("data-id")


class EpisodePage(ItemSchema):
    """Representation episodes

    Prepare:
      1. get id from Anime object
      2. GET 'https://animego.me/anime/{Anime.id}/player?_allow=true'
      3. extract html from json by ['content'] key
      4. OPTIONAL: unescape HTML

    EXAMPLE:

        GET https://animego.me/anime/anime/1114//player?_allow=true
    """

    dubbers = N().sub_parser(EpisodeDubbersView)
    episodes = N().sub_parser(EpisodesView)


class SourceVideoView(ListSchema):
    __SPLIT_DOC__ = D().css_all("#video-players > span")

    title = D().text()
    url = D().attr("data-player").format("https:{{}}")
    data_provider = D().attr("data-provider")
    data_provide_dubbing = D().attr("data-provide-dubbing")


class SourceDubbersView(DictSchema):
    __SPLIT_DOC__ = D().css_all("#video-dubbing > span")
    __SIGNATURE__ = {"<dubber_id>": "<dubber_name>", "...": "..."}

    __KEY__ = D().attr("data-dubbing")
    __VALUE__ = D().text().re_sub(r"^\s+", "").re_sub(r"\s+$", "")


class SourcePage(ItemSchema):
    """representation player urls

    Prepare:
      1. get num and id from Episode

      2.

      GET https://animego.me/anime/series
      dubbing=2&provider=24&episode={Episode.num}id={Episode.id}

      3. extract html from json by ["content"] key

      4. OPTIONAL: unescape document

    EXAMPLE:

        GET https://animego.me/anime/series?dubbing=2&provider=24&episode=2&id=15837
    """

    dubbers = N().sub_parser(SourceDubbersView)
    videos = N().sub_parser(SourceVideoView)
