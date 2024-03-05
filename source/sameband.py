from typing import Optional, Sequence

from ssc_codegen import DictSchema, Document, ItemSchema, ListSchema, assert_

__all__ = ["OngoingView", "SearchView", "AnimeView", "PlaylistURLView"]


class OngoingView(ListSchema):
    """GET https://sameband.studio"""

    def __pre_validate_document__(self, doc: Document) -> Optional[Document]:
        pass

    def __split_document_entrypoint__(self, doc: Document) -> Document:
        # [0] - ongoings
        # [1] - new
        # [2] - already watch
        # [3] - most rated
        # [4] - now discussion
        # [5] - Coming soon element
        # parsel index issues
        # TODO add to tests in ssc-gen package
        return doc.css(".container-fluid > .swiper").css_all(".poster")

    def url(self, doc: Document):
        return doc.css("a").attr("href")

    def title(self, doc: Document):
        return doc.attr("title")

    def thumbnail(self, doc: Document):
        return doc.css("img.swiper-lazy").attr("src").format("https://sameband.studio{{}}")


class SearchView(ListSchema):
    """
    POST https://sameband.studio/index.php?do=search
    do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=<QUERY>
    """

    def __split_document_entrypoint__(self, doc: Document) -> Document:
        return doc.css_all(".col-auto")

    def title(self, doc: Document):
        return doc.css(".col-auto .poster").attr("title")

    def thumbnail(self, doc: Document):
        return doc.css("img.swiper-lazy").attr("src").format("https://sameband.studio{{}}")

    def url(self, doc: Document):
        return doc.css(".image").attr("href")


class AnimeView(ItemSchema):
    def title(self, doc: Document):
        return doc.css("h1.m-0").text()

    def alt_title(self, doc: Document):
        return doc.css(".help").text()

    def description(self, doc: Document):
        return doc.css_all(".limiter span").text().join(" ")

    def thumbnail(self, doc: Document):
        return doc.css(".image > img").attr("src").format("https://sameband.studio{{}}")

    def player_url(self, doc: Document):
        """dev value for access playlist

        playlist tag signature:

        <body>
            <div id="player"></div>
         <script>var player = new Playerjs({id:"player",file:"/v/list/....txt"});
        </script>
        </body>
        """
        return doc.css(".player > .player-content > iframe").attr("src").format("https://sameband.studio{{}}")


class PlaylistURLView(ItemSchema):
    """GET https://sameband.studio/pl/a/Mashle_2nd_Season.html

      NOTE: url contains in AnimeView.player_url key

      playlist items signature (need manually provide json marshall logic):

      [
    {
      "title": "<img src='/v/anime/...01 RUS_snapshot.jpg' class=playlist_poster><div class=playlist_duration>23:37</div>... 01",
      ### delimiter - ','
      "file": "[480p]/v/anime/... - 01 RUS_480p/... - 01 RUS_r480p.m3u8,[720p]/v/anime/.../... - 01 RUS_720p/... - 01 RUS_r720p.m3u8,[1080p]/v/anime/.../... -
      01 RUS_1080p/... - 01 RUS_r1080p.m3u8",
      ### thumbnails images for video
      "thumbnails": "/v/anime/.../thumbnails/... - 01 RUS.txt"  # contains
    },
    {
    ...
    },
    ...
    ]
    """

    def playlist_url(self, doc: Document):
        # player script signature:
        # ...
        # <script>var player = new Playerjs({id:"player",file:"/v/list/....txt"});
        # ...
        # extract URL PATH -----------------------------------vvvvv
        return doc.raw().re(r"var\s*player\s*=[^>]+file:[\"']([^>]+)[\"']").format("https://sameband.studio{{}}")
