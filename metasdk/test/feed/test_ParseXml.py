from unittest import TestCase

from metasdk.feed.FeedColumn import FeedColumn
from metasdk.feed.ParseXml import parse_xml
from metasdk.test.feed import get_sample_fn


class TestParseXml(TestCase):
    def test_startElement(self):
        fn = get_sample_fn('books.xml')
        actual = parse_xml(fn)
        self.assertEquals(9, len(actual))
        first = FeedColumn(
            type="TEXT",
            search_path="/catalog",
            path=["catalog"],
            name="catalog",
            display_name="catalog"
        )
        self.assertEquals(first.__dict__, actual[0].__dict__)

        second = FeedColumn(
            type="TEXT",
            search_path="/catalog/@shop-name",
            path=["catalog"],
            name="shop-name",
            display_name="catalog_shop-name"
        )
        self.assertEquals(second.__dict__, actual[1].__dict__)
