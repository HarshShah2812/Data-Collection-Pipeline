# Data-Collection-Pipeline
A repository showcasing the work I did to build a data collection pipeline

Despite having previous Python experience prior to completing this project, this was my first experience building a webscraper, therefore all tools mentioned throughout were learnt whilst doing the project.

## Project Goals

 - Develop a webscraper that collects data from a chosen website primarily with the help of Selenium and Requests;

 - perform unit testing on the webscraper to ensure it works as expected;

 - using Docker to containerise the application and if running successfully, deploying the image to Dockerhub;

 - setting up a CI/CD pipeline using GitHub Actions to automate the deployment of a new Docker image to Dockerhub.

## Milestones 1-2: Setting up the environment and choosing the website

This project was completed with the help of VS Code as the code editor, as well as Git and Github. I created an environment for this project with conda, naming it 'DCPenv'.

The choice of website was based on personal interest. As an enthusiast of Yerba Mate, a caffeinous hot beverage with numerous health benefits consumed primarily in Argentina and Uruguay, as well as southern parts of Brazil, I wanted to explore it further by looking into the types of brands out there that sell this product, as well as the different flavours that exist. Therefore, the natural choice in terms of websites to scrape was [Urushop](https://urushop.co.uk/). Given that the products that they sell aren't solely limited to Yerba Mate, I decided to limit the scope of the project to only include Yerba Mate products.

![yerbamatepage](https://user-images.githubusercontent.com/67421468/213881590-7241cdc6-f664-419e-ba74-1b78d46945ed.png)




