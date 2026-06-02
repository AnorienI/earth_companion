import re
import requests
import json
import os
import sys
from dotenv import load_dotenv
import tk
from PIL import ImageTk, Image
from countryinfo import CountryInfo
import pycountry

# Carrega as variáveis de ambiente
load_dotenv()
GEONAMES_USER = os.getenv("GEONAMES_USER")
API_KEY = os.getenv("OPENWEATHER_API_KEY")

flag_frame = None
flag_label = None

def validate_input(city):
    if not re.match(r"^[A-Za-z\s]+,\s?[A-Za-z]{2}$", city.strip()):
        result_label.config(text='Invalid format.\nType: "city, country code(2 letters)"', font=large_font)
        return False
    return True

def get_currency_name(code):
    currency = pycountry.currencies.get(alpha_3=code)
    return currency.name if currency else code

def fetch_weather():
    city = entry.get()
    if not validate_input(city):
        return

    site = "https://api.openweathermap.org/data/2.5/weather"
    inputs = {"q": city, "units": "metric", "appid": API_KEY} # Vindo do .env
    response = requests.get(url=site, params=inputs)
    data = response.json()

    if data.get("cod") == 200:
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]

        result_text = f"Now in {city.capitalize()}:\nDescription: {weather_description}\nTemperature: {temperature}°C\nHumidity: {humidity}%\nPressure: {pressure} hPa"
        result_label.config(text=result_text, font=large_font)
    else:
        result_label.config(text="Error fetching weather data", font=large_font)

def get_coordinates():
    city = entry.get()
    if not validate_input(city):
        return

    site = "https://api.openweathermap.org/data/2.5/weather"
    inputs = {"q": city, "units": "metric", "lang": "pt", "appid": API_KEY} # Vindo do .env
    response = requests.get(url=site, params=inputs)
    data = response.json()

    if data.get("cod") == 200:
        longitude = data["coord"]["lon"]
        latitude = data["coord"]["lat"]
        result_label.config(text=f"The coordinates of {city.capitalize()} are \nLongitude: {longitude}, Latitude: {latitude}", font=large_font)
    else:
        result_label.config(text="Error fetching coordinates data", font=large_font)

def get_city_population():
    city = entry.get()
    if not validate_input(city):
        return

    endpoint = f"http://api.geonames.org/searchJSON?q={city}&maxRows=10&username={GEONAMES_USER}"
    response = requests.get(endpoint)
    jsonResponse = json.loads(response.text)

    if "geonames" in jsonResponse and jsonResponse["geonames"]:
        population = jsonResponse["geonames"][0].get("population", "N/A")
        formatted_population = "{:,}".format(int(population))
        result_label.config(text=f"Population of {city.capitalize()}: {formatted_population}", font=large_font)
    else:
        result_label.config(text="Population data not available.", font=large_font)

def get_country_info():
    global flag_frame, flag_label
    
    # Limpa frames de bandeira anteriores se existirem
    if flag_frame is not None:
        flag_frame.destroy()
        flag_frame = None
        flag_label = None

    city = entry.get()
    if not validate_input(city):
        return

    country_code = city.split(",")[-1].strip().upper()
    country_info = CountryInfo(country_code)

    currencies = country_info.currencies()
    language = country_info.languages()
    population = country_info.population()
    capital = country_info.capital()
    area = country_info.area()
    
    formatted_area = "{:,}".format(int(area))
    formatted_population = "{:,}".format(int(population))
    
    full_currency_names = [get_currency_name(code) for code in currencies]
    full_language_names = []

    for code in language:
        lang = pycountry.languages.get(alpha_2=code)
        full_language_names.append(lang.name if lang else code)

    result_text = (
        f"Country: {country_info.name().capitalize()}\n"
        f"Capital: {capital}\n"
        f"Area: {formatted_area} sq km\n"
        f"Currency: {', '.join(full_currency_names)}\n"
        f"Language: {', '.join(full_language_names)}\n"
        f"Population: {formatted_population}"
    )
    result_label.config(text=result_text, font=large_font)

def fetch_flag():
    global flag_frame, flag_label

    city = entry.get()
    if not validate_input(city):
        return

    country_code = city.split(",")[-1].strip().upper()
    
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    flag_path = os.path.join(base_path, "flags", f"{country_code}.png")

    try:
        flag_image = Image.open(flag_path)
        flag_image = flag_image.resize((50, 50), Image.Resampling.LANCZOS)
        flag_photo = ImageTk.PhotoImage(flag_image)

        if flag_frame is not None:
            flag_frame.destroy()
            
        flag_frame = tk.Frame(window)
        flag_frame.pack(pady=10) # Alinhamento dinâmico automático embaixo

        flag_label = tk.Label(flag_frame, image=flag_photo)
        flag_label.image = flag_photo  # Salva a referência na memória
        flag_label.pack()

        window.update_idletasks()

    except FileNotFoundError:
        if flag_frame is not None:
            flag_frame.destroy()
            flag_frame = None
        result_label.config(text=f"Flag not found ({country_code}.png)", font=large_font)


# --- Configuração da Interface Gráfica ---
window = tk.Tk()
window.title('EarthCompanion')
window.geometry('340x480') # Aumentado levemente para acomodar os textos sem cortar

large_font = ('Helvetica', 12)

city_label = tk.Label(window, text='Type the city name (e.g. London, UK): ', font=large_font)
city_label.pack(pady=5)

entry = tk.Entry(window, font=large_font)
entry.pack(pady=5)

button_weather = tk.Button(window, text='Weather', command=fetch_weather, font=large_font)
button_weather.pack(fill='x', padx=50, pady=2)

button_city_population = tk.Button(window, text='Population', font=large_font, command=get_city_population)
button_city_population.pack(fill='x', padx=50, pady=2)

button_coordinates = tk.Button(window, text='Coordinates', command=get_coordinates, font=large_font)
button_coordinates.pack(fill='x', padx=50, pady=2)

button_country_info = tk.Button(window, text='Country Info', command=get_country_info, font=large_font)
button_country_info.pack(fill='x', padx=50, pady=2)

button_flag = tk.Button(window, text='Flag', command=fetch_flag, font=large_font)
button_flag.pack(fill='x', padx=50, pady=2)

# Apenas UM result_label centralizado no fim
result_label = tk.Label(window, text="", font=large_font, justify="left")
result_label.pack(pady=15)

window.mainloop()