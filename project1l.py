import re
import requests
import tkinter as tk
from PIL import ImageTk, Image
from countryinfo import CountryInfo
import json
import os
import sys
from dotenv import load_dotenv


load_dotenv()

GEONAMES_USER = os.getenv("GEONAMES_USER")
API_KEY = os.getenv("OPENWEATHER_API_KEY")


flag_frame = None
flag_label = None

def validate_input(city):
    if not re.match(r"^[A-Za-z\s]+,\s[A-Za-z]{2}$", city.strip()):
        result_label.config(text='Invalid form.\nType: "city, country code(2 letterss)"', font=large_font)
        return False
    return True

def fetch_weather():
    city = entry.get()

    if not validate_input(city):
        return

    site = 'https://api.openweathermap.org/data/2.5/weather'
    inputs = {'q': city, 'units': 'metric', 'appid': API_KEY}
    response = requests.get(url=site, params=inputs)
    data = response.json()

    if data['cod'] == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']

        result_text = f'Now in {city}:\nAppearance: {weather_description}\nTemperature: {temperature}°C\nHumidity: {humidity}%\nPressure: {pressure} hPa'
        result_label.config(text=result_text, font=large_font)
    else:
        result_label.config(text='Error fetching weather data', font=large_font)

def get_city_population(city):
    endpoint = f'http://api.geonames.org/searchJSON?q={city}&maxRows=10&username={GEONAMES_USER}'
    response = requests.get(endpoint)
    jsonResponse = json.loads(response.text)

    if 'geonames' in jsonResponse and jsonResponse['geonames']:
        population = jsonResponse['geonames'][0].get('population', 'N/A')
        formatted_population = "{:,}".format(int(population))
        result_label.config(text=f"Population of {city}: {formatted_population}", font=large_font)
    else:
        result_label.config(text='No data available for this city.')

def get_coordinates():
    city = entry.get()

    if not validate_input(city):
        return

    site = 'https://api.openweathermap.org/data/2.5/weather'
    inputs = {'q': city, 'units': 'metric', 'lang':'pt', 'appid': API_KEY}
    response = requests.get(url=site, params=inputs)
    data = response.json()

    if data['cod'] == 200:
        longitude = data['coord']['lon']
        latitude = data['coord']['lat']
        result_label.config(text=f"As coordenadas de {city} sao \nLongitude: {longitude}, Latitude: {latitude}", font=large_font)
    else:
        result_label.config(text='Error fetching data', font=large_font)

def get_country_info():
    global flag_frame, flag_label

    if flag_frame is not None:
        flag_frame.destroy()
        flag_frame = None
        flag_label = None

    input_value = entry.get()
    country_code = input_value.split(",")[-1].strip()  # Extract the last part of input as country code
    country_info = CountryInfo(country_code)

    # Get the full names of languages
    languages = country_info.languages()

    capital = country_info.capital()
    area = country_info.area()
    formatted_area = "{:,}".format(int(area))
    # Get the full names of currencies
    currencies = country_info.currencies()

    population = country_info.population()
    formatted_population = "{:,}".format(int(population))

    result_text = (
        f"Country: {country_info.name().capitalize()}\n"
        f"Capital: {capital}\n"
        f"Area: {formatted_area} square kilometers\n"
        f"Currencies: {', '.join(currencies)}\n"
        f"Languages: {', '.join(languages)}\n"
        f"Population: {formatted_population}"
    )
    result_label.config(text=result_text, font=large_font)

def fetch_flag():
    global flag_frame, flag_label

    city = entry.get()
    country_code = city.split(",")[-1].strip().upper()
    country_info = CountryInfo(country_code)
    country_name = country_info.name()

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    flag_path = os.path.join(base_path, "flags", f"{country_code}.png")

    try:
        flag_image = Image.open(flag_path)
        flag_image = flag_image.resize((50, 50), Image.LANCZOS)
        flag_photo = ImageTk.PhotoImage(flag_image)

        if flag_frame is None:
            flag_frame = tk.Frame(window)
            flag_frame.place(x=135, y=350, anchor='nw')

        if flag_label is not None:
            flag_label.pack_forget()

        flag_label = tk.Label(flag_frame, image=flag_photo)
        flag_label.image = flag_photo
        flag_label.pack()

        window.update_idletasks()

    except FileNotFoundError:
        result_label.config(text="Flag not found", font=large_font)


window = tk.Tk()
window.title('EarthCompanion, byAnestis')

window.geometry('320x420')

large_font = ('Helvetica', 12)  # You can adjust the font and size as needed

# City label
city_label = tk.Label(window, text='Type the city name: ', font=large_font)
city_label.pack()

# Entry
entry = tk.Entry(window, font=large_font)
entry.pack()

# Button - Tempo
button_weather = tk.Button(window, text='Weather', command=fetch_weather, font=large_font)
button_weather.pack()

# Button - Populacao
button_city_population = tk.Button(window, text='Population', font=large_font, command=lambda: get_city_population(entry.get()))
button_city_population.pack()


# Button - oordenadas
button_coordinates = tk.Button(window, text='Coordinates', command=get_coordinates, font=large_font)
button_coordinates.pack()

# Button - Get Country Info
button_country_info = tk.Button(window, text='Country Info', command=get_country_info, font=large_font)
button_country_info.pack()

# Result label
result_label = tk.Label(window, text="", font=large_font)
result_label.pack()

# Button - Fetch Flag
button_flag = tk.Button(window, text='Flag', command=fetch_flag, font=large_font)
button_flag.pack()

# Result label
result_label = tk.Label(window, text="")
result_label.pack()

window.mainloop()