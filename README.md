# mapping people's happyness over the continental US based on tweets
## 1. processing tweets
* about a million tweets over one year from 2017/05 to 2018/04 over the globe were downloaded
* tweets were filtered by keeping those writen in English and geo-taged
* tweets either geo-taged as a point or a polygon are kept
* for those tweets taged as a polygon, the center latitude and longitude are calcuated to estimate its location
* these tweets were further filtered to keep those posted in the continental US
* the local time of each tweet was retrieved from the UTC time based the time zone revealed by the latitude and longitude
* a pre-trained Hedonometer sentiment analysis to was used to calculate the sentiment score for each tweet, and the sentiment was used as a measure of people's happyness, with higher values representing happier mood
* outliers (those exceeding 5% and 95% percentiles) were removed to eliminate impacts from holidays and other social events like the Florida school shooting tragedy
* these sentiment score of individule tweets were then aggregated into county level and over the whole year and visulazations of its geographic distribution were generated

## 2. process other information
* demographic informations include residents age distribution, education level, population composition, etc. and social-economic information include medium household income, proverty rate, etc. were also collected at the county level
* these data were joined with the sentiment score extracted from tweets
* data cleaning include missing value treatment, data type transformation, unit transformation, etc. were performed

## 3. analysis
* a heatmap was ploted to show the correlations between any combination of two variables, and it shows that the correlation between sentiment and all other variables were not very strong, indicating that there is no trivial linear relationships between any single factor and people's happiness on a county level
* For example, when exploring the relationship between people's happiness and the population size, we found that people are the happiness in counties with moderate population size, compared with small or large population size
*  more EAD are need to find interesting patterns
* decision tree regressor and random forest regressor are run to explore the importance of these demographic and socia-economic information in terms of incluencing people's happiess
* explained variance is used as the metric
* we did not get a high explained variance, indicating that external factors that are not included in this analysis might play a more important role. We leave this as a further direction
* the top 10 important features are those related with population composition, population size, employment rate, the way people are employed, the way people communte to work
