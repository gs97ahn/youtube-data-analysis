# Youtube Data Analysis

**Big data analysis on youtubers based on increase and decrease of subscribers and comments during the increase and
decrease period.**

![Python](https://img.shields.io/badge/Python-3.8-6db33f?logo=Python&style=flat)
![SpringBoot](https://img.shields.io/badge/Youtube_API-v3-6db33f?logo=Youtube&style=flat)

## Websites Used
- <a href="https://www.youtube.com/" target="_blank">Youtube</a>
- <a href="https://www.noxinfluencer.com/" target="_blank">Noxinfluencer</a>

## Motivation

Many dream of becoming a famous Youtuber these days. Youtube contents itself, for sure, influences a channel's fame.
However, Youtube users writing comments also influence a channel's popularity. Therefore, this project analyze top 30 
popularity increase and decrease channels and compare the comments during the increase and decrease period.

## How it Works
### 0️⃣ Dependency Installation

```
pip install -r requirements.txt
```

### 1️⃣ Web Scrape
Web scrape statistics of top 30 increase and decrease categories.

```
python3 ./web_scrape.py
```

### 2️⃣ API
Query maximum of 10 most recent videos and get all the comments.

```
python 3 ./api_query.py
```