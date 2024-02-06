# Cyclical Market Rates

## Overview

The project you've been asked to do involves analyzing financial data to understand how certain economic indicators might influence the Federal Reserve's (FED) decision on interest rates, specifically in the context of 2024. Here's a breakdown of the requirements and the context provided:

### Contextual Background

As of the start of 2024, the market consensus leans heavily towards the expectation of rate cuts by the Federal Reserve, alongside a bearish outlook on the US Dollar (USD) and a belief that inflation concerns are well-addressed ("inflation is in the bag").

The message hints at a skepticism towards this consensus, suggesting that the market's rigid expectations might not align with the unfolding economic reality. Specifically, it raises the question of what would happen if the Federal Reserve decides to hike rates instead in 2024.
Project Requirements:

### Economic Indicators Analysis

You are to analyze 6-month prints (data points) for three key economic indicators:

* CPI (Consumer Price Index): Measures changes in the price level of a basket of consumer goods and services, serving as a key indicator of inflation.
* GDP (Gross Domestic Product): Represents the total dollar value of all goods and services produced over a specific time period, indicating the health of the economy.
* Employment: Refers to labor market data, such as unemployment rates or job growth, which reflect the employment health within the economy.
* Historical Analysis: Investigate if any 6-month period data for these indicators have ever led to a rate cut by the Federal Reserve. The theory posited here is that historically, such data points have more often led to a rate increase rather than a decrease.

### Financial Market Analysis

Add in the 6-month returns for major stock indices, which include:

* SP (S&P 500 Index): A stock market index that measures the stock performance of 500 large companies listed on stock exchanges in the United States.
* NDX (NASDAQ-100): An index of the 100 largest, most actively traded U.S companies listed on the NASDAQ stock exchange.
* RTY (Russell 2000 Index): A small-cap stock market index representing the bottom two-thirds of the Russell 3000 index.
* DOW (Dow Jones Industrial Average): A stock market index that measures the stock performance of 30 large companies listed on stock exchanges in the United States.

### Objective

The overarching goal seems to be to challenge or validate the market's expectation of rate cuts in 2024 by examining historical data trends in key economic indicators and stock market performance. The hypothesis is that strong performances in these indicators typically lead to rate hikes, not cuts.

To carry out this project, you would need access to historical economic data and stock market performance data. Analysis could involve statistical methods to identify patterns or correlations between these economic indicators and FED's rate decisions, as well as the impact of these indicators on stock market indices.

## How to Run

```
poetry run python -m rateradar.scripts.02_data_cleaning
```

## Data Series References

https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/real-time-data-set-full-time-series-history

| Series  | File |  Source  | Comment |
|---|---|---|---|
| Consumer Price Index (%)     | inflation/pcpi_first_second_third.xlsx  | https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/pcpi  | |
| Core Consumer Price Index (%) | inflation/pcpix_first_second_third.xlsx | https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/pcpix | |
| Consumer Price Index (Raw)  | inflation/pcpiMvMd.xlsx | https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/real-time-data/data-files/xlsx/pcpimvmd.xlsx?la=en&hash=652DCE5337C1BFD5BB297577157F5E0D | |
| GDP Output | gdp/routput_first_second_third.xlsx | https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/real-time-data/data-files/xlsx/routput_first_second_third.xlsx?la=en&hash=7B8E18E3DC34170B2D4F684F7EBBE631 | |
| Unemployment Rate | employment/rucQvMd.xlsx | https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/real-time-data/data-files/xlsx/routputmvqd.xlsx?la=en&hash=403C8B9FD72B33F83C1EE5C59D015C86 | |
| Fed Runds Rate | rates/fedfunds_1m.csv | TradingView | |
| SPX | indices/spx_1m.csv | TradingView | |
| NDX | indices/ndx_1m.csv | TradingView | |
| DJI | indices/dji_1m.csv | TradingView | |
| RTY | indices/rty_1m.csv | TradingView | |


### Notes on Inflation Data Series

The Philly Fed provides inflation data in two different ways. The first is the Month Over Month percentage values per the first_second_third metrics. The other way is the raw CPI values used to calculate the percentage values.

The percentage values provided unfortunately only go back to 1998, so I need to use the raw values. The raw values are provided in the inflation/pcpiMvMd(x).xlsx files. The percent change is then calculated for each month.