from ssc_codegen import DictSchema, ItemSchema, ListSchema, D, N, R


class AniboomPage(ItemSchema):
    """Extract MPD and M3U8 urls

    Required `referer="https://animego.org/` HEADER

    USAGE:
        1. GET <PLAYER_LINK> (e.g. https://aniboom.one/embed/6BmMbB7MxWO?episode=1&translation=30)
        2. PARSE. If pre-unescape response before parse - css selector may not find attribute
        3. For video playing, url required next headers:

        - Referer="https://aniboom.one/"
        - Accept-Language="ru-RU"  # INCREASE DOWNLOAD SPEED with this static value
        - Origin="https://aniboom.one"
    ISSUES:
        - 403 Forbidden if request sent not from CIS region
        - KEYS SHOULD BE STARTED IN Title case else hls/mpd links returns 403 error
        - Sometimes, aniboom backend missing MPD key and returns M3U8 url. Check this value before usage:

        https://github.com/vypivshiy/ani-cli-ru/issues/29

        Expected json signature (LOOK at dash.src and hls.src keys):

        { ...
        "dash":"{\"src\":\"https:.../abcdef.mpd\",\
        "type\":\"application\\\/dash+xml\"}",
        "hls":"{\"src\":\"https:...\\\/master_device.m3u8\",
        \"type\":\"application\\\/x-mpegURL\"}"

        ... }

        MAYBE returns this:

         { ...
        "dash":"{\"src\":\"https:...master_device.m3u8\",\
        "type\":\"application\\\/dash+xml\"}",
        "hls":"{\"src\":\"https:...master_device.m3u8\",
        \"type\":\"application\\\/x-mpegURL\"}"

        ... }



    """

    # can be json unmarshal
    # eg signature:
    # {"id":"WlmXYpNLMK0",
    # "error":"/video-error/WlmXYpNLMK0",
    # "domain":"animego.org",
    # "cdn":"/cdn/WlmXYpNLMK0",
    # "counter":"/counter/WlmXYpNLMK0",
    # "duration":"1437",
    # "poster":"https://i1.boom-img.com/wl/WlmXYpNLMK0/mqdefault.webp",
    # "thumbnails":"https://i1.boom-img.com/wl/WlmXYpNLMK0/thumbnails/thumbnails.vtt",
    #
    # YES, THIS KEYS contains STRING
    # "dash":"{
    #   "src":"https://lily.yagami-light.com/wl/WlmXYpNLMK0/qqppjxsz6fvkf.mpd",
    #   "type":"application/dash+xml"
    #   }",
    # "hls":"{
    #   "src":"https://lily.yagami-light.com/wl/WlmXYpNLMK0/master_device.m3u8",
    #   "type":"application/x-mpegURL"}",
    #
    # "quality":true, "qualityVideo":1080, "vast":true, "country":"RU",
    # "platform":"Linux","rating":"16+","nshowbl":false,"limitRate":false,
    # "aBlocklimitRate":false}
    data_parameters = (D().css('#video').attr('data-parameters')
                       .replace('\\', '').replace('&quot;', '"')  # json unescape
                       )
    hls = (D().css('#video').attr('data-parameters')
            .replace('\\', '').replace('&quot;', '"')
            .re('"hls":"{"src":"(https?.*?\.m3u8)"')
            )

    dash = (D().css('#video').attr('data-parameters')
           .replace('\\', '').replace('&quot;', '"')
           .re('"dash":"{"src":"(https?.*?\.(?:mpd|m3u8))"')
           )


