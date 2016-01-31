# Linkedin_scrapy

@ Scraps LinkedIn public profiles and saves them in a structured database

-) Choose the search terms to look for in linkedin database and change them in the principal spider "lindekin.py" 
lista = ["team leader","java","ecommerce","e-commerce","javascript","javascript+backbone"]

Run in terminal: 
scrapy crawl linkedin -o mobile.json
The spider saves the founded urls into a json file an checks if there are already in the historic database 

-) Run crawl_linkedin script to scrape the founded urls 
This script crawls the web pages using selenium and stores the founded data into a tsv to be later converted to a xlsx for the client.
