# mapping people's happyness over the continental US based on tweets
## 1. processing tweets
<br> about a million tweets over one year from 2017/05 to 2018/04 over the globe were downloaded
<br> tweets were filtered by keeping those writen in English and geo-taged
<br> tweets either geo-taged as a point or a polygon are kept
<br> for those tweets taged as a polygon, the center latitude and longitude are calcuated to estimate its location
<br> these tweets were further filtered to keep those posted in the continental US
<br> the local time of each tweet was retrieved from the UTC time based the time zone revealed by the latitude and longitude
<br> a pre-trained Hedonometer sentiment analysis to was used to calculate the sentiment score for each tweet, and the sentiment was used as a measure of people's happyness, with higher values representing happier mood
<br> outliers (those exceeding 5% and 95% percentiles) were removed to eliminate impacts from holidays and other social events like the Florida school shooting tragedy
<br> these sentiment score of individule tweets were then aggregated into county level and over the whole year and visulazations of its geographic distribution were generated

## 2. process other information
<br> demographic informations include residents age distribution, education level, population composition, etc. and social-economic information include medium household income, proverty rate, etc. were also collected at the county level
<br> these data were joined with the sentiment score extracted from tweets
<br> data cleaning include missing value treatment, data type transformation, unit transformation, etc. were performed

## 3. analysis
<br> a heatmap was ploted to show the correlations between any combination of two variables, and it shows that the correlation between sentiment and all other variables were not very strong, indicating that there is no trivial linear relationships between any single factor and people's happiness on a county level
<br> For example, when exploring the relationship between people's happiness and the population size, we found that people are the happiness in counties with moderate population size, compared with small or large population size
<br> more EAD are need to find interesting patterns
