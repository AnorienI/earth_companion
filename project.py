import re
import requests
import json
import iso4217
from countryinfo import CountryInfo
from iso639 import Lang


def validate_input(city):
    if not re.match(r"^[A-Za-z\s]+,\s?[A-Za-z]{2}$", city.strip()):
        print('Invalid format.\nEnter: "city, country code(2 letters)"')
        return False
    return True


# Create a mapping of currency codes to full names using the iso4217 module
currency_mapping = {code: iso4217.Currency(code).name for code in iso4217.Currency}


def get_data_from_geonames(endpoint):
    response = requests.get(endpoint)
    jsonResponse = json.loads(response.text)

    if "geonames" in jsonResponse and jsonResponse["geonames"]:
        return jsonResponse["geonames"][0]
    else:
        return None


def get_city_population(city):
    endpoint = (
        f"http://api.geonames.org/searchJSON?q={city}&maxRows=10&username=anorien"
    )
    response = requests.get(endpoint)
    jsonResponse = json.loads(response.text)

    if "geonames" in jsonResponse and jsonResponse["geonames"]:
        population = jsonResponse["geonames"][0].get("population", "N/A")
        formatted_population = "{:,}".format(int(population))
        print(f"Population of {city.capitalize()}: {formatted_population}")
    else:
        print("Population data not available for the specified city.")


def fetch_weather(city):
    if not validate_input(city):
        return

    site = "http://api.openweathermap.org/data/2.5/weather"
    inputs = {"q": city, "units": "metric", "appid": "d26548b0b8421b1c42613df1ec20ed49"}
    response = requests.get(url=site, params=inputs)
    data = response.json()

    if data["cod"] == 200:
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]

        result_text = f"Now in {city.capitalize()}:\nDescription: {weather_description}\nTemperature: {temperature}°C\nHumidity: {humidity}%\nPressure: {pressure} hPa"
        print(result_text)
    else:
        print("Error fetching weather data")


def get_coordinates(city):
    if not validate_input(city):
        return

    site = "http://api.openweathermap.org/data/2.5/weather"
    inputs = {
        "q": city,
        "units": "metric",
        "lang": "pt",
        "appid": "d26548b0b8421b1c42613df1ec20ed49",
    }
    response = requests.get(url=site, params=inputs)
    data = response.json()

    if data["cod"] == 200:
        longitude = data["coord"]["lon"]
        latitude = data["coord"]["lat"]
        print(
            f"The coordinates of {city.capitalize()} are \nLongitude: {longitude}, Latitude: {latitude}"
        )
    else:
        print("Error fetching coordinates data")


def get_country_info(city):
    if not validate_input(city):  # Check if input is in valid format
        return
    input_value = city.lower()
    country_code = input_value.split(",")[-1].strip()
    country_info = CountryInfo(country_code)

    currencies = country_info.currencies()
    language = country_info.languages()
    population = country_info.population()
    capital = country_info.capital()
    area = country_info.area()
    formatted_area = "{:,}".format(int(area))
    full_currency_names = [currency_mapping.get(code, code) for code in currencies]
    full_language_names = [Lang(code).name for code in language]
    formatted_population = "{:,}".format(int(population))

    result_text = (
        f"Country: {country_info.name().capitalize()}\n"
        f"Capital: {capital}\n"
        f"Area: {formatted_area} square kilometers\n"
        f"Currency: {', '.join(full_currency_names)}\n"
        f"Language: {', '.join(full_language_names)}\n"
        f"Population: {formatted_population}"
    )
    print(result_text)


def main():
    city = input("Enter the city name: ")
    if not validate_input(city):  # Check if input is in valid format
        return
    print()
    fetch_weather(city)
    print()
    get_coordinates(city)
    get_city_population(city)
    print()
    get_country_info(city)


if __name__ == "__main__":
    main()