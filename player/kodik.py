from ssc_codegen import D, DictSchema, ItemSchema, ListSchema, N, R


class MovieTranslationsPanel(ListSchema):
    """Representation available dubbers and params. Useful for switch dubber"""

    # element signature eg:
    # < option
    # value = "1291"
    # data - id = "1291"
    # data - translation - type = "subtitles"
    # data - media - id = "1132855"
    # data - media - hash = "00c597737850b65972d22c112ddec73a"
    # data - media - type = "seria"
    # data - title = "Crunchyroll.Subtitles"
    # > Crunchyroll.Subtitles < / option >

    __SPLIT_DOC__ = D().css(".movie-translations-box").css_all("option")

    name = D().text().trim(" ")
    value = D().attr("value")
    data_id = D().attr("data-id")
    data_translation_type = D().attr("data-translation-type")
    data_media_hash = D().attr("data-media-hash")
    data_media_type = D().attr("data-media-type")
    data_title = D().attr("data-title")


class KodikAPIPayload(ItemSchema):
    """payload for Kodik API request"""

    # single params pairs
    d = R().re("var\s*domain\s+=\s+['\"](.*?)['\"];")
    d_sign = R().re("var\s*d_sign\s+=\s+['\"](.*?)['\"];")
    pd = R().re("var\s*pd\s+=\s+['\"](.*?)['\"];")
    pd_sign = R().re("var\s*pd_sign\s+=\s+['\"](.*?)['\"];")
    ref = R().re("var\s*ref\s+=\s+['\"](.*?)['\"];")
    ref_sign = R().re("var\s*ref_sign\s+=\s+['\"](.*?)['\"];")
    type = R().re("videoInfo\.type\s*=\s*['\"](.*?)['\"];")
    hash = R().re("videoInfo\.hash\s*=\s*['\"](.*?)['\"];")
    id = R().re("videoInfo\.id\s*=\s*['\"](.*?)['\"];")


class KodikPage(ItemSchema):
    """this schema used to extract params for next API request

    required next keys for API request:
        - contain in `api_payload` key
    constants:
        - cdn_is_working: true
        - bad_user: false (or true)
        - info: {}

    USAGE:
        1. GET <PLAYER_LINK> (e.g.: https://kodik.info/seria/1133512/04d5f7824ba3563bd78e44a22451bb45/720p)
        2. parse payload (see required pairs upper) (<PAYLOAD>)
        3. extract the API path from player_js_path (<API_PATH>) (encoded in BASE64)
        4. POST https://kodik.info/ + <API_PATH>; data=<PAYLOAD> (<JSON>). next HEADERS required:
            - origin="https://<NETLOC>" // player page
            - referer=<PLAYER_LINK> // FIRST URL player entrypoint
            - accept= "application/json, text/javascript, */*; q=0.01"
        5. extract data from ['links'] key from <JSON> response
        6. urls encoded in ROT_13 + BASE64 ciphers
    ISSUES:
        - kodik maybe have another netloc (e.g.: anivod)
        - 403 Forbidden if request sent not from CIS region
        - 404 DELETED: eg: https://kodik.info/seria/310427/09985563d891b56b1e9b01142ae11872/720p
        - 500 Internal server error: eg: https://kodik.info/seria/1051016/af405efc5e061f5ac344d4811de3bc16/720p ('Cyberpunk: Edgerunners' ep5 Anilibria dub)

    """

    # original player decode signature:
    # function (e) {
    #   var t;
    #   e.src = (
    #     t = e.src,
    #     atob(
    #       t.replace(
    #         /[a-zA-Z]/g,
    #         function (e) {
    #           return String.fromCharCode((e <= 'Z' ? 90 : 122) >= (e = e.charCodeAt(0) + 13) ? e : e - 26)
    #         }
    #       )
    #     )
    #   )
    # }

    # can be json unmarshal
    # contains keys:
    # ['d', 'd_sign', 'pd', 'pd_sign', 'ref', 'ref_sign', 'advert_debug', 'first_url']
    url_params = R().re("var\s*urlParams\s*=\s*['\"](\{.*\})['\"]")
    api_payload: KodikAPIPayload = N().sub_parser(KodikAPIPayload)

    # kodik sometimes changes the API path. It must be extracted from the player source code
    # (netloc excluded)
    # api path - base64 encoded string
    player_js_path = R().re('<script\s*type="text/javascript"\s*src="(/assets/js/app\.player_single.*?)">')

    # TODO: maybe add extra information?
    movie_translations: MovieTranslationsPanel = N().default(None).sub_parser(MovieTranslationsPanel)


# TODO create function signature
class KodikApiPath(ItemSchema):
    """Extract the API path from js player source"""

    # js api path signature examples:
    # ... $.ajax({type:"POST",url:atob("L2Z0b3I="),cache:! ...
    # ... $.ajax({type: 'POST', url:atob('L3RyaQ=='),cache: !1 ...
    path = R().re("\$\.ajax\([^>]+,url:\s*atob\([\"']([\w=]+)[\"']\)")
