# Linkedin_scrapy

Scraps LinkedIn public profiles and saves them in a structured database

First spider saves urls into a database an checks if there are already in the historic database 
scrapy crawl linkedin -o urls_linkedin.json

Second spider crawls the public profiles.

