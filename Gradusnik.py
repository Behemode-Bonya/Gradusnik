from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import requests


def main():
    city_name = input("введите название города: ")
    start_date = input("введите начальную дату: ")
    end_date = input("введите конечную дату: ")

    data_set = "geonames-postal-code@public/records"
    payload = {
        "limit": 20,
        "where": f'place_name:"{city_name}" and country_code:"RU"'
        }
    url = f"https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/{data_set}"

    response = requests.get(url,params = payload)
    response.raise_for_status()
    city_response = response.json()

    if city_response["total_count"] == 0:
        print("Мурино не было найдено,программа останавливается")
        exit()
        
    latitude = city_response["results"][0]["latitude"]
    longitude = city_response["results"][0]["longitude"]
    url_meteo = "https://archive-api.open-meteo.com/v1/era5"
    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly":"temperature_2m"
        }
    response = requests.get(url_meteo,params = payload)
    response.raise_for_status()
    meteo_info = response.json()["hourly"]
    temperature_value = meteo_info["temperature_2m"]
    temperature_date = meteo_info["time"]
    df = pd.DataFrame(list(zip(temperature_date,temperature_value)),columns = ["date","temp"])
    df["date"] = pd.to_datetime(df["date"])

    plt.plot(df["date"],df["temp"])
    plt.xlabel("даты")
    plt.ylabel("Температуры (°C)")
    plt.title(f"график температуры в {city_name}")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.show()


if __name__ == "__main__" :
    main()


