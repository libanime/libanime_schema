from ssc_codegen import ItemSchema, D, ListSchema

FMT_URL = 'https://yummyanime.in{{}}'

class OngoingPage(ListSchema):
    """Get all available ongoings from the main page

    USAGE:

        GET https://yummyanime.in/

    """
    __SPLIT_DOC__ = D().css_all('.ksupdate_block a')

    thumbnail = D().css('.xfieldimage[src]').attr('src').fmt(FMT_URL)
    url = D().attr('href').fmt(FMT_URL)
    # maybe not exist episode number in element, set 1 as default
    episode = D().default(1).css('.cell-2').text().re(r"(\d+)\s").to_int()
    title = D().css('.xfieldimage[alt]').attr('alt')


class SearchPage(ListSchema):
    """Get search results

    USAGE:

        POST https://yummyanime.in
        do=search&subaction=search&story=<QUERY>

    EXAMPLE:

        POST https://yummyanime.in/index.php
        do=search&subaction=search=from_page=0story=ван-пис
    """

    __SPLIT_DOC__ = D().css_all("a.has-overlay")

    title = D().css(".poster__title").text()
    thumbnail = D().css(".xfieldimage[data-src]").attr('data-src').fmt(FMT_URL)
    url = D().attr("href")


class AnimePage(ItemSchema):
    """get anime page

    USAGE:

        GET https://yummyanime.in/<...>.html

    EXAMPLE:

        GET https://yummyanime.in/4790-vedma-i-chudovische.html

    """

    title = D().css(".anime__title h1").text()
    alt_title = D().default(None).css('.anime__title .pmovie__original-title').text()

    description = D().default('').css_all(".page__text p").text().join('')
    thumbnail = D().css(".pmovie__poster .xfieldimage[data-src]").attr("data-src").fmt(FMT_URL)
    player_url = D().default(None).css('.pmovie__player iframe[src]').attr('src').fmt('https:{{}}')
