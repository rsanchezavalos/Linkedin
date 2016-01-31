# Linkedin_scrapy

scrap LinkedIn public profiles and save them in a structured database

First spider saves urls into a database an checks if there are already in the historic database 
scrapy crawl linkedin -o urls_linkedin.json

Second spider crawls the public profiles.

