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

## Category
Since the comments may vary drastically depending on which category the youtubers are in, the Youtube channels are split
into six different categories which are:
- Autos & Vehicles
- Entertainment
- Gaming
- How to & Style
- Science & Technology
- Travel & Events

## Conclusion
In the experiment, ratios and z-scores are calculated with 60 channels for each postivie/negative status in six 
different categories. The test is done using 30 channels for each positive/negative status in six different categories 
as well.



### Test results
<table>
    <thead>
        <tr>
            <th colspan="2">Present ~</th>
            <th>Autos & Vehicles</th>
            <th>Entertainment</th>
            <th>Gaming</th>
            <th>How to & Style</th>
            <th>Science & Technology</th>
            <th>Travel & Events</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="2">Duplicate</td>
            <td>Ratio</td>
            <td>53.85%</td>
            <td>72.73%</td>
            <td>56.86%</td>
            <td>50.91%</td>
            <td>52.00%</td>
            <td>52.83%</td>
        </tr>
        <tr>
            <td>Z-Score</td>
            <td>57.69%</td>
            <td>72.73%</td>
            <td>56.86%</td>
            <td>50.91%</td>
            <td>52.00%</td>
            <td>52.83%</td>
        </tr>
        <tr>
            <td rowspan="2">No Duplicate</td>
            <td>Ratio</td>
            <td>53.85%</td>
            <td>59.09%</td>
            <td>56.86%</td>
            <td>50.91%</td>
            <td>52.00%</td>
            <td>52.83%</td>
        </tr>
        <tr>
            <td>Z-Score</td>
            <td>55.77%</td>
            <td>59.09%</td>
            <td>56.86%</td>
            <td>50.91%</td>
            <td>54.00%</td>
            <td>52.83%</td>
        </tr>
    </tbody>
</table>

<table>
    <thead>
        <tr>
            <th colspan="2">Present ~ 1 Week Ago</th>
            <th>Autos & Vehicles</th>
            <th>Entertainment</th>
            <th>Gaming</th>
            <th>How to & Style</th>
            <th>Science & Technology</th>
            <th>Travel & Events</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="2">Duplicate</td>
            <td>Ratio</td>
            <td>45.45%</td>
            <td>59.09%</td>
            <td>52.94%</td>
            <td>45.45%</td>
            <td>48.00%</td>
            <td>50.94%</td>
        </tr>
        <tr>
            <td>Z-Score</td>
            <td>48.08%</td>
            <td>59.09%</td>
            <td>52.94%</td>
            <td>47.27%</td>
            <td>50.00%</td>
            <td>50.94%</td>
        </tr>
        <tr>
            <td rowspan="2">No Duplicate</td>
            <td>Ratio</td>
            <td>48.08%</td>
            <td>59.09%</td>
            <td>52.94%</td>
            <td>45.45%</td>
            <td>48.00%</td>
            <td>50.94%</td>
        </tr>
        <tr>
            <td>Z-Score</td>
            <td>48.08%</td>
            <td>59.09%</td>
            <td>52.94%</td>
            <td>47.27%</td>
            <td>50.00%</td>
            <td>50.94%</td>
        </tr>
    </tbody>
</table>

<table>
    <thead>
        <tr>
            <th colspan="2">1 Week Ago ~ 2 Week Ago</th>
            <th>Autos & Vehicles</th>
            <th>Entertainment</th>
            <th>Gaming</th>
            <th>How to & Style</th>
            <th>Science & Technology</th>
            <th>Travel & Events</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="2">Duplicate</td>
            <td>Ratio</td>
            <td>21.15%</td>
            <td>13.64%</td>
            <td>15.69%</td>
            <td>21.82%</td>
            <td>32.00%</td>
            <td>39.62%</td>
        </tr>
        <tr>
            <td>Z-Score</td>
            <td>19.23%</td>
            <td>22.73%</td>
            <td>11.76%</td>
            <td>20.00%</td>
            <td>34.00%</td>
            <td>39.62%</td>
        </tr>
        <tr>
            <td rowspan="2">No Duplicate</td>
            <td>Ratio</td>
            <td>21.15%</td>
            <td>15.91%</td>
            <td>15.69%</td>
            <td>21.82%</td>
            <td>32.00%</td>
            <td>39.62%</td>
        </tr>
        <tr>
            <td>Z-Score</td>
            <td>19.23%</td>
            <td>22.73%</td>
            <td>11.76%</td>
            <td>20.00%</td>
            <td>34.00%</td>
            <td>39.62%</td>
        </tr>
    </tbody>
</table>

## How it Works
#### 🛑 Watch out
In order to run this code, you must get a Youtube API key from 
[Google Developer console](https://console.cloud.google.com/apis/dashboard) and have the key as `API_KEY` as an 
environment variable.

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

#### 🛑 Watch Out
Youtube only allows people to use 10,000 units/day. If you do not have additional permission, you must fix the code so
it gets data for a single category at a time.

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

### 6️⃣ Test
Test the accuracy of calculated ratio and z-score.

#### 🛑 Watch Out
You must re-do step 1️⃣ and step 2️⃣ to collect data for testing first

```
python test.py
```