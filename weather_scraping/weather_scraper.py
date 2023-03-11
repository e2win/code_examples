from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time


def scrape_weather_data():
    # Use Selenium to load the page
    driver = webdriver.Firefox()
    driver.get("https://forecast.weather.gov/MapClick.php?x=150&y=135&site=bou&zmx=&zmy=&map_x=150&map_y=135")

    # Parse the page source using Beautiful Soup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find the div containing the current conditions
    conditions_div = soup.find(id="current-conditions")

    # Find the div element with the "current_conditions-summary" id
    summary_div = conditions_div.find(id="current_conditions-summary")

    # Create an empty dictionary
    data = {"Conditions": summary_div.find(class_="myforecast-current").text.strip(),
            "Temperature (°F)": summary_div.find(class_="myforecast-current-lrg").text,
            "Temperature (°C)": summary_div.find(class_="myforecast-current-sm").text,
            }

    # Find the div element with the "current_conditions_detail" id
    detail_div = conditions_div.find(id="current_conditions_detail")

    # find wind chill, if there
    if detail_div.find(text="Wind Chill"):
        data["Wind Chill"] = detail_div.find(text="Wind Chill").find_next().text
    else:
        data["Wind Chill"] = 0

    # forecast
    data["Short Term Forecast"] = soup.find("p", class_="period-name").get_text(separator=' ') + \
                                  ": " + soup.find("p", class_="short-desc").get_text(separator=' ').strip()

    forecast_container = soup.find("div", id="seven-day-forecast-container")
    forecast_items = forecast_container.find_all("li", class_="forecast-tombstone")
    for i, forecast_item in enumerate(forecast_items):
        if i == 4:
            data["Medium Term Forecast"] = forecast_item.find("p", class_="period-name").get_text(separator=' ') + \
                                           ": " + forecast_item.find("p", class_="short-desc").get_text(separator=' ')
        if i == 8:
            data["Long Term Forecast"] = forecast_item.find("p", class_="period-name").get_text(separator=' ') + \
                                         ": " + forecast_item.find("p", class_="short-desc").get_text(separator=' ')

    # Find all rows in the table
    rows = detail_div.find_all('tr')

    # Loop through the rows and extract the data from the table cells
    for row in rows:
        label_cell = row.find('td', class_="text-right")
        value_cell = row.find('td')
        if label_cell and value_cell:
            label = label_cell.find('b').text
            value = label_cell.b.find_next().text
            data[label] = value

    # Close the browser
    driver.close()

    data["Last update"] = data["Last update"].strip()
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Values'])
    df.T.to_csv('weather_data.csv', index=False, mode='a', header=False)

    # harsh way of eliminating log file
    with open("geckodriver.log", 'w') as f:
        f.write('')


scrape_weather_data()
