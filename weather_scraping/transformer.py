# script to import and transform the data
from dateutil import parser
import pandas as pd


def string_fixer(string_guy):
    fixed_string = string_guy[string_guy.find(":") + 2:]
    if ":" in fixed_string:
        fixed_string = fixed_string[fixed_string.find(":") + 2:].strip()
    if "then" in fixed_string:
        fixed_string = fixed_string[:fixed_string.find("then") - 1].strip()
    if "and Areas Fog" in fixed_string:
        fixed_string = fixed_string[:-13].strip()
    if "Areas " in fixed_string:
        fixed_string = fixed_string[6:].strip()
    if "Slight Chance" in fixed_string:
        fixed_string = fixed_string.replace("Slight Chance ", "").strip()
    if "Chance" in fixed_string:
        fixed_string = fixed_string.replace("Chance ", "").strip()
    if "Likely" in fixed_string:
        fixed_string = fixed_string.replace(" Likely", "").strip()
    return fixed_string


df = pd.read_csv("weather_data.csv")

wind_direction, wind_speed, wind_gusts, time = [], [], [], []
df = df.drop_duplicates(subset=["Update Time"]).reset_index(drop=True)
df = df.dropna().reset_index(drop=True)
for i in range(len(df)):
    # print(df["Temperature C"][i])
    df["Temperature C"][i] = int(df["Temperature C"][i][:-2])
    if df["Wind Chill"][i] == "0":
        df["Wind Chill"][i] = 0
    else:
        df["Wind Chill"][i] = int(df["Wind Chill"][i][df["Wind Chill"][i].find("(") + 1:-3])
    df["Humidity"][i] = int(df["Humidity"][i][:-1])
    if df["Wind"][i] == "Calm":
        wind_speed.append(0)
        wind_direction.append(0)
        wind_gusts.append(0)
    elif len(df["Wind"][i]) >= 13:
        # there are gusts
        wind_speed.append(int(df["Wind"][i][-6:-4].strip()))
        wind_direction.append(df["Wind"][i][:2].strip())
        wind_gusts.append(int(df["Wind"][i][7:9].strip()))
    elif df["Wind"][i][:4] == "Vrbl":
        wind_speed.append(int(df["Wind"][i][-6:-4].strip()))
        wind_direction.append(0)
        wind_gusts.append(0)
    else:
        wind_speed.append(int(df["Wind"][i][-6:-4].strip()))
        wind_direction.append(df["Wind"][i][:2].strip())
        wind_gusts.append(0)

    df["Barometric pressure"][i] = float(df["Barometric pressure"][i][df["Barometric pressure"][i].find("(") + 1:-4])
    df["Visibility"][i] = float(df["Visibility"][i][:-3])
    df["Short term forecast"][i] = string_fixer(df["Short term forecast"][i])
    df["2-day forecast"][i] = string_fixer(df["2-day forecast"][i])
    df["4-day forecast"][i] = string_fixer(df["4-day forecast"][i])
    time.append(int(parser.parse(df["Update Time"][i][:-3]).hour) + 1)
df = df.drop(columns=["Temperature F", "Wind", "temp", "Update Time"])
df = df.join(pd.DataFrame(
    {"Wind Speed": wind_speed, "Wind Direction": wind_direction, "Wind Gusts": wind_gusts, "Time": time}, index=df.index
))

wind_dir_dict = {0: 0, "N": 1, "NE": 2, "E": 3, "SE": 4, "S": 5, "SW": 6, "W": 7, "NW": 8}
df = df.replace({"Wind Direction": wind_dir_dict})

# I created a special dictionary to help make the connection to weathereather_translation = {"Sunny": 5, "Clouds": 4, "Windy": 3, "Rain": 2, "Fog": 1, "Snow": 0}

fixed_dict = {"Light Snow": 0, "Heavy Snow and Blustery": 0, "Heavy Snow": 0, "Snow": 0, "Wintry Mix and Patchy Fog": 0,
              "Winter Weather Advisory": 0, "Winter Storm Warning": 0, "Wintry Mix": 0, "Snow Showers": 0,
              "Snow and Breezy": 0,

              "Light Snow Fog/Mist and Breezy": 1, "Light Snow Fog/Mist": 1, "Fog/Mist": 1, "Snow Fog/Mist": 1,
              "Freezing Fog": 1, "Snow and Patchy Fog": 1, "Fog": 1, "Patchy Fog": 1,

              "Rain/Snow": 2, "Rain": 2, "Showers and Breezy": 2, "Drizzle/Snow": 2, "Rain and Breezy": 2,
              "Patchy Freezing Drizzle and Patchy Fog": 2, "Patchy Freezing Drizzle": 2, "Showers": 2, "Drizzle": 2,

              "Blustery. Rain/Snow": 3, "Snow and Blustery": 3, "Partly Cloudy and Blustery": 3, "Red Flag Warning": 3,
              "Wind Chill Advisory": 3, "Mostly Sunny and Windy": 3, "A Few Clouds and Windy": 3, "Sunny and Windy": 3,

              "Overcast": 4, "Partly Cloudy": 4, "Mostly Cloudy": 4, "Overcast and Breezy": 4,
              "Mostly Cloudy and Breezy": 4, "Increasing Clouds": 4, "Cloudy": 4, "Partly Cloudy and Breezy": 4,

              "Gradual Clearing and Breezy": 5, "A Few Clouds": 5, "Fair": 5, "Decreasing Clouds": 5,
              "Decreasing Clouds and Breezy": 5, "Mostly Clear and Breezy": 5, "Partly Sunny": 5, "Sunny": 5,
              "Mostly Sunny": 5, "Sunny and Breezy": 5, "Mostly Clear": 5, "Clear": 5, "Mostly Sunny and Breezy": 5,
              "A Few Clouds and Breezy": 5, "Becoming Sunny": 5, "Partly Sunny and Breezy": 5, "Breezy. Sunny": 5}

df["Current Conditions"].replace(fixed_dict, inplace=True)
df["Short term forecast"].replace(fixed_dict, inplace=True)
df["2-day forecast"].replace(fixed_dict, inplace=True)
df["4-day forecast"].replace(fixed_dict, inplace=True)
for c in df.columns:
    df[c] = pd.to_numeric(df[c])
df.to_csv("cleaned_data.csv", index=False, header=["Current Conditions", "Temperature C", "Wind Chill C",
                                                   "Short term forecast", "2-day forecast", "4-day forecast",
                                                   "Humidity %", "Barometric pressure (mb)", "Visibility (mi)",
                                                   "Wind Speed (mph)", "Wind Direction", "Wind Gusts (mph)", "Time"])
