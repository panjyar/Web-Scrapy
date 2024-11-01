# College Web Crawler

This project is a web-based application designed to crawl and display news and upcoming events from all AICTE-approved college websites. Using **Scrapy** for web scraping, **Flask** as a web framework, and **MongoDB** for data storage, this application aggregates information into a central database for easy access.

## Features
- **Web Scraping**: Automatically scrapes news and event data from college websites.
- **Database Integration**: Stores scraped data in MongoDB.
- **API & Web Interface**: Flask provides a simple API and web interface to view and manage the collected data.

## Getting Started

Follow these steps to set up the project on your local machine:

### Prerequisites
Ensure that you have MongoDB installed and running on `localhost:27017`.

### Clone the Repository
```bash
git clone https://github.com/panjyar/Web-Scrapy.git
cd Web-Scrapy
```
Install Dependencies
Install the required packages for Flask and Scrapy:
```
pip install -r requirements_flask.txt
pip install -r requirements_Scrapy.txt
```
Configure MongoDB Connection
Update the MongoDB connection settings as follows:

1. In citnews/settings.py, set:
MongoDB connection details
```
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'All_college'
```
2. In the Backend folder, set:
```
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['All_college']
```
Running the Application
Step 1: Run the Web Crawler
Navigate to the citnews directory and start the Scrapy spider to begin scraping data:
```
cd citnews
scrapy crawl cit
```
Step 2: Run the Flask Application
After scraping, start the Flask application to view the scraped data:
```
cd ../Backend
python app.py
```
Visit http://localhost:5000 in your browser to access the application interface.

## Project Structure
citnews: Contains the Scrapy spider and configurations for scraping college websites.

Backend: Houses the Flask application, which serves as an API and front-end interface.

requirements_flask.txt and requirements_Scrapy.txt: Separate dependencies files to keep Flask and Scrapy environments organized.

## Dependencies

Flask: For API and web interface.
Scrapy: For web scraping.
MongoDB: As the database to store collected data.

