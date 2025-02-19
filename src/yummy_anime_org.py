from ssc_codegen import ItemSchema, D, ListSchema


FMT_URL = 'https://yummy-anime.org{{}}'

class OngoingPage(ListSchema):
    """Get all available ongoings from the main page

    USAGE:

        GET https://yummy-anime.org/

    """
    __SPLIT_DOC__ = D().css_all('.ksupdate_block a')

    thumbnail = D().css('.xfieldimage').attr('src').fmt(FMT_URL)
    url = D().attr('href').fmt(FMT_URL)
    episode = D().css('.cell-2').text().re("(\d+)\s").to_int()
    title = D().css('.xfieldimage').attr('alt')


class SearchPage(ListSchema):
    """Get search results

    USAGE:

        POST https://yummy-anime.org
        do=search&subaction=search&story=<QUERY>

    EXAMPLE:

        POST https://yummy-anime.org/index.php
        do=search&subaction=search=from_page=0story=ван-пис
    """

    __SPLIT_DOC__ = D().css_all("a.has-overlay")

    title = D().css(".poster__title").text()
    thumbnail = D().css(".xfieldimage").attr('data-src').fmt(FMT_URL)
    url = D().attr("href")


class AnimePage(ItemSchema):
    """get anime page

    USAGE:

        GET https://yummy-anime.org/<...>.html

    EXAMPLE:

        GET https://yummy-anime.org/4790-vedma-i-chudovische.html

    """

    title = D().css(".anime__title h1").text()
    alt_title = D().default(None).css('.anime__title .pmovie__original-title').text()

    description = D().default('').css_all(".page__text p").text().join('')
    thumbnail = D().css(".pmovie__poster .xfieldimage").attr("data-src").fmt(FMT_URL)
    player_url = D().default(None).css('.pmovie__player iframe').attr('src').fmt('https:{{}}')
