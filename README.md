# First-Project
First project of the UT Data Analysis & Visualization Boot Camp

# Project Objectives and Overview
The objective of this first project is to utilize the skills learned thus far in the boot camp, including but not limited to python, pandas, matplotlib and API calls to analzye data and attempt to draw inferences. For this project, we utilized 2 data sources (both via an API) to retrieve weather data from DarkSky and Austin crime data from data.austingovernment.org. For each crime, we obtained the corresponding weather to the nearest hour, gathering data for the last 2 years. We then performed our analysis in an attempt to determine various relationships between crime events and weather conditions in Austin, TX.

## Analysis 1 - Temperature Impact on Crime Rates by Crime Type (Top 5)
Based on the plot, it appears that overall, more crimes happen when temperatures are higher. There is a noticeable blip in the 70-79 degree range where crime rates for all types decrease or plateau before significantly increasing. At the high-end of the temperature ranges, we noticed that there are many plateaus, but also a significant decrease for burglary of vehicles. Potential drawbacks of this analysis is that no other variables were controlled for. As an example, tt is possible that seasonal events, which are unrelated to temperature, affect these results. 

## Analysis 2 - Moon Phase Impact on Crime Rates by Crime Type (Top 5)
Based on the plot, there seems to be a slight outlier for First Quarter Moon for burglary of vehicles, where the rate of that particular crime is higher than in other phases. Otherwhise, there does not appear to be any noticeable trends between moon phase and crime rates among the top 5 crime types. A potential drawbacks of this analysis is that moon phase could be correlated to a monthly event. 

## Analysis 3 - Precipitation Intensity on Crime Rate by Crime Location Type (Top 5)
Based on the plot, it appears that crimes occuring on streets, highways, roads, and alleys increase at the high-end of the precipitation intensity scale. It's also of note that the most common crime location is residence / homes. A potential drawback of this analysis is the granularity of the data. 

# Conclusions 
While the analysis was interesting, it's hard to properly identify correlations as we didn't run any regressions, so we don't know what is statistically significant.  We also didn't control for a multitude of variables that could be impacting our analysis. 