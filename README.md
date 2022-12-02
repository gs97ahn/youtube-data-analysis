# Youtube Data Analysis

**Big data analysis on youtubers based on increase and decrease of subscribers and comments during the increase and
decrease period.**

![Python](https://img.shields.io/badge/Python-3.8-6db33f?logo=Python&style=flat)
![YoutubeAPI](https://img.shields.io/badge/Youtube_API-v3-6db33f?logo=Youtube&style=flat)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](LICENSE)

## Websites Used
- <a href="https://www.noxinfluencer.com/" target="_blank">Noxinfluencer</a>
- <a href="https://developers.google.com/youtube/v3" target="_blank">Youtube API</a>


## Motivation
Many dream of becoming a famous Youtuber these days. Youtube contents itself, for sure, influences a channel's fame.
However, Youtube users writing comments also influence a channel's popularity. Therefore, this project analyze top 30 
popularity increase and decrease channels and compare the comments during the increase and decrease period.

### Category
Since the comments may vary drastically depending on which category the youtubers are in, the Youtube channels are split
into six different categories which are:
- Autos & Vehicles
- Entertainment
- Gaming
- How to & Style
- Science & Technology
- Travel & Events

## How it Works
### 0️⃣ Dependency Installation

```
pip install -r requirements.txt
```

### 1️⃣ Web Scrape
Web scrape statistics of top 30 increase and decrease categories.

```
python web_scrape.py
```

### 2️⃣ Youtube API
Query maximum of 5 most recent videos and get 100 the comments and statistics.

```
python api_query.py
```

### 3️⃣ Preprocess
Preprocess data by doing the followings:

- Tokenize comments
- Remove punctuation
- Keep English only
- Remove stopwords
- Extract word stem
- Count words
- Ratio
- Z-Score

```
python preprocess_data.py
```

### 5️⃣ Visualization
Visualize data by the followings:

- Wordcloud
- Horizontal Bar Graph
- Vertical Bar Graph

```
python visualize.py
```