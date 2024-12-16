# Savage Scraper: Carnivorous Plant Data Collection

A web scraping project using Scrapy to collect inventory data from California Carnivores, focusing on Sarracenia Hybrids.

## Project Overview
- Built for Data Structure & Data Mining with Python course
- Scrapes product names and prices from californiacarnivores.com
- Implements polite scraping practices (respects robots.txt, rate limiting)

## Features
- Custom spider (savagespider.py) for target website
- HTTP caching
- Data cleaning functionality
- Auto-throttling
- JSON output format

## Setup
```bash
# Create virtual environment
python -m venv scraping_env
source scraping_env/bin/activate

# Install dependencies
pip install scrapy

# Run spider
scrapy crawl savagespider -O savageplants.json
```

## Project Structure
```
.
├── savage_scraper/
│   ├── spiders/
│   │   └── savagespider.py
│   ├── settings.py
│   ├── pipelines.py
│   └── middlewares.py
├── scrapy.cfg
└── README.md
```

## Author
Austin Maguire  
UC Davis Continuing and Professional Education
PYT304 - Data Structure & Data Mining with Python