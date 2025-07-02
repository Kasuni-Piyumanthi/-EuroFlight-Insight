## EuroFlight-Insight
Analyzing European airport departures for informed council decisions.

## Description
A Python-based air traffic analysis program that processes structured CSV datasets of European airport departures. Designed to assist councils and planners in making informed decisions by providing key metrics on airline activity, delays, runway usage, weather conditions, and destination trends.

## 📊 Features

- ✅ Validates user input for airport codes and year
- 📁 Loads CSV files containing 12-hour departure records
- 📈 Outputs:
  - Total flights
  - Runway usage statistics
  - Long-haul flight counts
  - Airline-specific departure percentages
  - Delays and weather conditions
  - Most common destinations
- 📝 Appends results to a `results.txt` log file
- 📉 Draws hourly flight distribution histograms by airline using `graphics.py`
- 🔁 Allows multiple datasets to be loaded and analyzed in a single session
