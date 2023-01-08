from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import date, datetime
import os
import json
import requests

class Scraper:
    def __init__(self):
        '''
        This class is used to scrape a given website and extract
        text data and images.

        Attributes:
            driver: firefox web driver
            url: link of the website's homepage
            get_request: opens the website link
            load_and_accept_cookies: loads the webpage and accepts the cookies statement
            downward_scroller: scrolls to a specific set of coordinates when called
            get_products_page: finds the page element corresponding to the specific products section and clicks on it to go to the section
        '''
        self.driver = webdriver.Firefox()
        self.url = "https://urushop.co.uk/"
        self.get_request = self.driver.get(self.url)
        self._load_and_accept_cookies()
        #self._downward_scroller()
        #self._get_products_page()
        #self.url_list = []
        #self._get_links()
        #self.product_list = []
        
        
        #self.links = self.get_links()
        #self.get_product_data()
        #self.products_dict_list = self.get_product_data()
        # self.save_data_to_json()
        # self.download_images()
        
    def _load_and_accept_cookies(self):
        '''A method that loads the cookie statement and accepts it'''
        consent_button = self.driver.find_element(By.XPATH, '//*[@id = "cookie_action_close_header"]')
        time.sleep(5)
        accept_cookies = consent_button.click()
        return accept_cookies
    
    def _downward_scroller(self):
        '''A method that scrolls to a given set of coordinates when called'''
        time.sleep(5)
        scroll_down = self.driver.execute_script("window.scrollTo(0, 300);")
        return scroll_down

    def _get_products_page(self):
        '''A method that finds the page element corresponding to the specific products section and clicks on it to go to the section'''
        products_page_link = self.driver.find_element(By.XPATH, '//*[@class = "perfmatters-lazy entered pmloaded"]')
        time.sleep(5)
        click_page = products_page_link.click()
        return click_page
    
    def _get_next_page(self):
        '''A method that goes to the next page of products'''
        next_page = self.driver.find_element(By.XPATH, '//*[@class = "next page-number"]')
        self.driver.execute_script("window.scrollTo(0, 1700);")
        time.sleep(5)
        click_next_page = next_page.click()
        return click_next_page

    def _get_links(self) -> list:
        '''A method that retrieves the url's corresponding to the pages of each product in the product section, putting them in a list'''
        
        url_list = []
        page = 0
        for i in range(1,7):
            page += i
            try:
                urls = self.driver.find_elements(By.XPATH, '//*[@class = "woocommerce-LoopProduct-link woocommerce-loop-product__link"]')
                for url in urls:
                    url_list.append(url.get_attribute('href'))
                    #time.sleep(5)
            except StaleElementReferenceException:
                break

            try:
                self._get_next_page()
            except NoSuchElementException:
                break
        
        print(url_list)
        print(len(url_list)) 
        return url_list  

    def _retrieve_product_data(self, product_link):
        '''A method that goes onto each product's webpage and retrives the relevant data'''
        #product_list = []
        #property_list = ['id', 'name', 'price', 'weight', 'brand', 'rating', 'image']
        #products = {key: None for key in property_list}
        # url_list = self._get_links() 
        # for product_link in url_list:  
        #     self.driver.get(link)
        #     time.sleep(5)
        driver = self.driver
        driver.get(product_link)
    
        try:
            id = self.driver.find_element(By.XPATH, '//*[@class = "yith-wcwl-add-button"]/a')
            id = id.get_attribute('data-product-id')
        except NoSuchElementException:
            id = "N/A"
        
        try:
            name = self.driver.find_element(By.XPATH, '//*[@class = "product-info summary col-fit col entry-summary product-summary text-left"]/h1').text
        except NoSuchElementException:
            name = "N/A"    
            
        try:
            price = self.driver.find_element(By.XPATH, '//*[@class = "woocommerce-Price-amount amount"]/bdi').text
        except NoSuchElementException:
            price = "N/A"
                
        try:
            weight = self.driver.find_element(By.XPATH, '//*[@class = "woocommerce-product-attributes-item__value"]')
            weight = weight.get_attribute('innerHTML')
        except NoSuchElementException:
            weight = "N/A"
            
        try:
            brand = self.driver.find_element(By.XPATH, '//*[@itemprop = "brand"]/a').text
        except NoSuchElementException:
            brand = "N/A"
            
        try:
            rating = self.driver.find_element(By.XPATH, '//*[@class = "jdgm-prev-badge__stars"]')
            rating = rating.get_attribute('data-score')
        except NoSuchElementException:
            rating = "N/A"
        
        try:    
            image = self.driver.find_element(By.XPATH, '//*[@class = "wp-post-image skip-lazy entered pmloaded"]')
            image = image.get_attribute('src')
        except NoSuchElementException:
            image = "N/A"
            
        t = time.time()
        dt = datetime.fromtimestamp(t)
        Timestamp = dt.strftime("%d-%m-%Y, %H:%M:%S")

        time.sleep(2)

        return id, name, price, weight, brand, rating, image, Timestamp

    def _update_data_dictionary(self, link) -> dict:
        
        property_list = ['id', 'name', 'price', 'weight', 'brand', 'rating', 'image']
        product_dict = {key: None for key in property_list}
        id, name, price, weight, brand, rating, image, Timestamp = self._retrieve_product_data(link)
        
        product_dict['id'] = id
        product_dict['name'] = name
        product_dict['price'] = price
        product_dict['weight'] = weight
        product_dict['brand'] = brand
        product_dict['rating'] = rating
        product_dict['image'] = image
        product_dict['timestamp'] = Timestamp  
            
        product_dict_copy = product_dict.copy()
        print(product_dict_copy)
        filename = product_dict_copy['id']
        self._create_folder_json(filename)
        self._write_json(product_dict_copy, filename)
        #self.product_list.append(products_copy)
        return product_dict_copy
            
        # print(product_list)
        # print(len(product_list))
        return self.product_list

    def _get_product_properties(self):
        # first_product = self.url_list[0]
        # for link in self.url_list:
        #     while link == first_product:
        #         self.driver.get(link)
        #         time.sleep(5)
        #         self._update_dictionary_list()
        #         break
        list_of_links = []
        item_info = []
        # self._downward_scroller()
        # self._get_products_page()
        #while True:
        item_list = self._get_links()
        # print(item_list)
        list_of_links.extend(item_list)
        print(list_of_links)
        print(len(list_of_links))

        #try:
            
        for item_link in list_of_links:
            item_info.append(self._update_data_dictionary(item_link))
        print(item_info)
        print(len(item_info)) 
            
        index = 0
        for dictionary in item_info:
            index += 1
            image = dictionary['image']
            self._download_image(index, image)
                
        # except NoSuchElementException:
        #     break

        return item_info

    def _get_product_info_from_each_page(self):
        self._downward_scroller()
        self._get_products_page()
        self._get_product_properties()
        
            
            
    # def _get_products_from_each_page(self):

    #     self._downward_scroller()
    #     self._get_products_page()
    #     page = 0
    #     for i in range(1,7):
    #         page += i
    #         self._get_products()
            # url = f"https://urushop.co.uk/pc/yerba-mate-from-south-america/page/{i}/"
            # self.driver.get

        # print(self.product_list)
        # return self.product_list
    
    # def _get_remaining_products(self):
    #     remaining_products = self.url_list[1:]
    #     for link in remaining_products:
    #         self.driver.get(link)
    #         time.sleep(5)
    #         self._update_dictionary_list()
    #     print(self.product_list)
    #     return self.product_list
    @staticmethod
    def _create_folder_json(filename): #destination_folder = 'raw_data/data'):
        '''A method that converts product_list into a .json file and stored it within the designated directory'''
        if not os.path.exists('raw_data'):
            os.makedirs('raw_data')
        if not os.path.exists(f'raw_data/{filename}'):
            os.makedirs(f'raw_data/{filename}')
    
    @staticmethod
    def _write_json(data, filename):
        '''Saves the data in a json file'''
        folder_path = f'raw_data/{filename}/data.json'
        with open(folder_path, 'w', encoding = 'utf-8') as f:
            json.dump(data, f, ensure_ascii = False, indent = 4)
    
    # def _create_image_folder():
    #     if not os.path.exists('images'):
    #         os.makedirs('images')
    
    def _download_image(self, index, link):
        # self._create_image_folder()
        if not os.path.exists('raw_data'):
            os.makedirs('raw_data')
        
        if not os.path.exists('raw_data/images'):
            os.makedirs('raw_data/images')
        
        # dict_list = self._get_product_properties()
        # for index, dict in dict_list:
        # index =+ 1
        #image_name = f'{str(date.today())}_{str(datetime.now())}_{str(index)}.jpg'
        t = datetime.now()
        scrape_time = t.strftime("%H%M%S")
        image_path =  f'raw_data/images/{str(date.today())}_{str(scrape_time)}_{str(index)}.jpg' #os.path.join(destination_folder, image_name)
        # file_name = f'{str(date.today())}_{str(scrape_time)}_{str(index)}.jpg'
        # image_path = os.path.join('raw_data/images', file_name)
        #image_url = dict['image']
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': 'https://urushop.co.uk/',
        'DNT': '1'
        }
        image_data = requests.get(link, headers = headers, stream = True)
        if image_data.status_code == 200:

            with open(image_path, 'wb') as handler:
                handler.write(image_data.content)
            print("Image downloaded successfully", handler)
        else:
            print(image_data.status_code)
        
    def quit(self):
        self.driver.quit()



        # file_name = 'data.json'
        # folder_path = os.path.join(destination_folder, file_name)
    
        # with open(folder_path, 'w', encoding = 'utf-8') as f:
        #     json.dump(self.product_list, f, ensure_ascii= False, indent = 4)
    
    # def _download_images(self, destination_folder = 'raw_data/scraped_images'):
    #     '''A method that downloads the images corresponding to each product under the 'image' key of product_list'''
    #     if not os.path.exists(destination_folder):
    #         os.makedirs(destination_folder)
        
    #     dict_list = 
    #     for index, dict in enumerate(self.product_list):
    #         index += 1
    #         image_name = f'{str(date.today())}_{datetime.now()}_{str(index)}.jpg'
    #         image_path = os.path.join(destination_folder, image_name)
    #         image_url = dict['image']

    #         image_data = requests.get(image_url)
    #         with open(image_path, 'wb') as handler:
    #             handler.write(image_data.content)
            
            #requests.get(dict['image']) 

if __name__ == "__main__":
    scraper = Scraper()
    scraper._get_product_info_from_each_page()
    scraper.quit()
    
    