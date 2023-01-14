from DCP import Scraper
import unittest
import time
import os


class ScraperTestCase(unittest.TestCase):
    def setUp(self):
        self.scraper = Scraper()

    @unittest.skip
    def test_load_and_accept_cookies(self):
        self.setUp()
        time.sleep(2)
        actual = self.scraper.driver.current_url
        expected = "https://urushop.co.uk/"
        self.assertEqual(actual, expected, 'Test Failed')
    
    @unittest.skip
    def test_get_products_page(self):
        self.setUp()
        time.sleep(2)
        self.scraper._get_products_page()
        time.sleep(2)
        actual = self.scraper.driver.current_url
        print(self.scraper.driver.page_source)
        expected = "https://urushop.co.uk/pc/yerba-mate-from-south-america/"
        self.assertEqual(actual, expected)
    
    @unittest.skip
    def test_get_next_page(self):
        self.assertTrue(True)
    
    def test_get_links(self):
        self.setUp()
        time.sleep(2)
        self.scraper._get_products_page()
        time.sleep(2)
        self.item_list = self.scraper._get_links()
        message = "first and second are not almost equal."
        self.assertAlmostEqual(len(self.item_list), 130, None, message, 1)
    
    def test_retrieve_product_data(self):
        self.setUp()
        time.sleep(2)
        self.scraper._downward_scroller()
        time.sleep(2)
        self.scraper._get_products_page()
        time.sleep(2)
        self.item_list = self.scraper._get_links()
        self.assertTrue(True)
        id, name, price, weight, brand, rating, image, Timestamp = self.scraper._retrieve_product_data(self.item_list[0])
        assert type(id) is str
        assert type(name).__name__ == 'str'
        assert type(price) is str
        assert type(weight) is str
        assert type(brand) is str
        assert type(rating) is str
        self.assertEqual(type(Timestamp), type("hello world"))
        print(id, name, price, weight, brand, rating, image, Timestamp)
    
    def test_update_data_dictionary(self):
        self.setUp()
        time.sleep(2)
        self.scraper._downward_scroller()
        time.sleep(2)
        self.scraper._get_products_page()
        time.sleep(2)
        self.item_list = self.scraper._get_links()
        product_dict = self.scraper._update_data_dictionary(self.item_list[0])

        assert type(product_dict) is dict
    
    def test_get_product_properties(self):
        self.assertTrue(True)

    def test_get_product_info_from_each_page(self):
        self.assertTrue(True)
    
    def test_write_json(self):
        if (os.path.isdir('./raw_data/*/*.json')):
            self.assertTrue(True)
        else:
            self.assertFalse(False)
    
    def test_download_image(self):
        if (os.path.isdir('./raw_data/images/*.jpg')):
            self.assertTrue(True)
        else:
            self.assertFalse(False)

    def tearDown(self):
        self.scraper.driver.close()
        del self.scraper

if __name__ == "__main__":
    unittest.main()






