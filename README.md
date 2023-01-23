# Data-Collection-Pipeline
A repository showcasing the work I did to build a data collection pipeline

Despite having previous Python experience prior to completing this project, this was my first experience building a webscraper, therefore all tools mentioned throughout were learnt whilst doing the project.

## Project Goals

 - Develop a webscraper that collects data from a chosen website primarily with the help of Selenium and Requests;

 - perform unit testing on the webscraper to ensure it works as expected;

 - using Docker to containerise the application and if running successfully, deploying the image to Dockerhub;

 - setting up a CI/CD pipeline using GitHub Actions to automate the deployment of a new Docker image to Dockerhub.

## Milestones 1-2: Setting up the environment and choosing the website

This project was completed with the help of VS Code as the code editor, as well as Git and Github, which provided a means to implement version control. A separate environment was created for this project with conda, and it was named `DCPenv`.

The choice of website was based on personal interest. As an enthusiast of Yerba Mate, a caffeinous hot beverage with numerous health benefits consumed primarily in Argentina and Uruguay, as well as southern parts of Brazil, I wanted to explore it further by looking into the types of brands out there that sell this product, as well as the different flavours that exist. Therefore, the natural choice in terms of websites to scrape was [Urushop](https://urushop.co.uk/). Given that the products that they sell aren't solely limited to Yerba Mate, I decided to limit the scope of the project to only include Yerba Mate products.

![yerbamatepage](https://user-images.githubusercontent.com/67421468/213881590-7241cdc6-f664-419e-ba74-1b78d46945ed.png)

## Milestone 3: Finding all the pages from which the data will be scraped

The webscrper has been written in Python, utilising the concept of Object Orientated Programming. In this milestone, I created a `Scraper()` class within a file named `DCP.py`, creating different methods within it with the help of Selenium that would bypass cookies (`_load_and_accept_cookies()`), navigate the webpage (`_downward_scroller()`), go to the Yerba Mate products page (`_get_products_page()`), and get the links to each page from which the product data would be extracted, storing them in a list (`_get_links()`). I created an `if __name__ == '__main__':` block, so that the class would be initialised only if the file is run directly rather than on any import. 

The method,  `_get_links()`, iterates through each page with the help of a for-loop, within which a `try-except` syntax is used to find the link and append it to the designated list; once all the links from the page are collected, another `try-except` syntax is used to navigate to the next page of products via the previously created method `_get_next_page()`.

## Milestone 4: Retrieving the data from the details page

In this milestone, I created a method that would retrieve the data from each product's page (`_retrieve_product_data()`) as well as another one that then puts the data obtained by the previous method into a dictionary and writes the dictionary into a JSON file so that it is stored locally (`_update_data_dictionary()`). A method was then created that integrates `_get_links()` as well as `_update_data_dictionary()`. The dictionary created has the following structure:

```python

{'id':, 'name':, 'price':, 'weight':, 'brand':, 'rating':, 'image':, 'timestamp': }

```
The JSON file in which the dictionary is written looks as such:

```python

{
    "id": "0bb449b8-7c1a-431e-94cc-7c1f65fb920b",
    "name": "Yerba Mate Canarias 500g",
    "price": "£5.50",
    "weight": "0.5 kg",
    "brand": "Canarias",
    "rating": "4.84",
    "image": "https://urushop.co.uk/wp-content/uploads/y2.jpg",
    "timestamp": "14-01-2023, 17:58:27"
}
```
The value corresponding to the 'image' key is the URL associated with the product image. The image was downloaded using `_download_image()`, which was also integrated into `_get_product_properties()`. Within `_download_image()`, I integrated a HTTP header when using `requests` in order to pass additional information about the request, therefore minimising the chances of the server thinking that I am a bot.

The header looks like this:

```python

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0', 
        'Accept-Language': 'en-GB,en;q=0.5', 
        'Referer': 'https://urushop.co.uk/', 
        'DNT': '1' 
        }
```

The JSON file was stored in a local directory called `raw_data`, while the image was stored in a local directory called `images`.

`_get_product_properties()` was then integrated into another method, called `_get_product_info_from_each_page()`, along with `_downward_scroller()` and `_get_products_page()`.

This method was then integrated into the `if __name__ == '__main__:` block as follows:

```python

if __name__ == "__main__":
    scraper = Scraper()
    scraper._get_product_info_from_each_page()
    scraper.quit()
```
The biggest takeaways from this milestone were the correct implementation of for-loops, choosing relating XPATHs to extract information from a product page, how to download images locally with the help of Requests and OS, and how to create JSON files that contain a dictionary, using `json.dump()` to store them locally.

## Milestone 5: Documentation & Testing

In this milestone, I firstly refactored the code accordingly:

- Ensuring any unnecessary comments were removed; 
- docstrings were added to all functions; 
- ensuring the use of `self` wasn't excessive; 
- breaking down long methods into small ones that perform individual tasks;
- ensuring there aren't any nested loops.

Then, I created unit tests for the scraper with the help of the `unittest` module; therefore, a test was created for each of the methods within the `Scraper()` class. These tests are written in the `test.py` file. The entire process of unit testing was a very interesting learn and has taught me the importance of code meeting quality standards before deployment. Another learn for me was how Python files can be packaged and used within other scripts, where in this case, the `Scraper()` class was imported from the `DCP.py` file in order to be used within the `test.py` file.

## Milestone 6: Containerising the scraper

After carrying out the final code refactoring and ensuring all tests passed, this milestone required you to run the scraper in headless mode, which would be required for the scraper to run inside the Docker container that would be created later; this was done using `Options()` as follows:

```python

options = Options()
options.add_argument('--headless')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors') 
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions") 
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage') 
options.add_argument('--no-sandbox') 
options.add_argument("--disable-notifications") 
options.add_argument("--disable-infobars")

self.driver = webdriver.Firefox(options = options)
self.url = "https://urushop.co.uk/"
self.get_request = self.driver.get(self.url)
```
The next task was to create a `Dockerfile`, which would build an image of the scraper locally. The file would contain instructions to:

- choose a base image (`python:3.10` in my case); 
- put all the packages required to run the scraper within the container;
- install any dependencies;
- run the Python file containing the scraper.

2 of the dependencies required to build the image were Firefox and Geckodriver, which can be installed as follows:

```python

#update the system and install Firefox
RUN apt-get update
RUN apt -y upgrade
RUN apt-get install -y firefox-esr

# get the latest release of geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-linux32.tar.gz \
    # extract the geckodriver
    && tar -xvzf geckodriver* \
    # add executable permissions to the driver
    && chmod +x geckodriver \
    # move geckodriver to the system path
    && mv geckodriver /usr/local/bin
```
After the image was built, it was run to ensure that it worked properly, and then pushed to Dockerhub:

![harsh2812dcp](https://user-images.githubusercontent.com/67421468/214123909-21b2fffc-64c0-4a05-a8b2-3e47b8c046cb.png)















