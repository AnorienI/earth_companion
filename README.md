# WeatherApp - A Simple Weather Prediction Program

Actually, it is two (2) applications: project.py and project1.py. Unfortunately I couldn't find a way to pytest the tkinter app(project1.py), that's why I'm providing the terminal window application(project.py) and the corresponding test file (test_project.py).  Another problem I had with the tkinter application was that I could not wrap it in a main function. I wrapped the tkinter window class in my main function, but then the other functions did not have access to the 'entry', 'result_label', and 'window' elements.

In the terminal window application the user is prompted to input a city followed by a two letter country code, separated by a comma. The program prints out the current weather, the city's population and coordinates, and some information about the country in which the city is found (country name, currency, language, country population).

### Video Demo: [Watch the Demo Video]https://youtu.be/ZGFM5_Vwtvk?si=DwzsVH8MMkcXT46k

#### Description:
The WeatherApp is a simple Python program that allows users to retrieve weather information for a given location. Inspired by my father's self-taught weather prediction skills using a barometer. I remember him approaching this old antiquated barometer and tap onto its glass top as if to get the pointer ustuck (the pointer was never stuck) and then predict faultlessly the weather. Another thing my father had done was to provide me with books, at a time when there was not even television, let alone computers and internet. I 'traveled' the world through the pages of those books, and that's why I included the geographical information.  This app serves as a humble tribute to his memory.

In the terminal window application the user is prompted to input a city followed by a two letter country code, separated by a comma. The program prints out the current weather, the city's population and coordinates, and some information about the country in which the city is found (country name, currency, language, country population).

This program provides the following features:
- Current weather data of a city or town
- Population information of a given city or town
- The coordinates (latitude, londitude) of the city or town
- Information of the country in which  the city or town is found
 #- Display of the corresponding country's flag: Only in the tkinter application(project1.py)

By inputting the name of a city or town users can be informed of the weather and relevant geographical information. It is nostalgia that drove me to code this program.

**Instructions:**
1. Run the Python program "WeatherApp.py".

2. Input the name of a city or town. You can enter 'city name, country code(2 letters)' as in 'cambridge, us', with a space between the comma and the two letter  country code, or as in 'cambridge,us' without a space after the comma. Any other format will raise an exception and the user will see a message, informing them of the correct form.

3. In the gui(tkinter) app: Click on the desired button to receive the corresponding information.
In the terminal app: Enter a city name and country code as prompted and upon pressing the enter button the program returns three (3) blocks of information, all at one time 1) the weather report, 2) the city's population and coordinates, and 3) the information of the country of the said city. In the terminal application, unlike the GUI app, there are no flags displayed.

**Dependencies:**
- Python (3.x recommended)
- Required Python packages (can be installed using pip):
  - requests
   #- tkinter: Only necessary in the project1.py application
   #- PIL: Only necessaery in the project1.py application
  - countryinfo # for information of the country of the city in question
  - geopy
  - iso421 # for the language formatted (full) name
  - iso639 # for the currency formatted name
  - json
  - re # for validating the input

Feel free to explore and tinker with the program. Your curiosity could turn you into a modern-day weather predictor, reminiscent of my father's barometer rituals.

Just follow these indications:  "The lower the needle goes (and therefore the lower the air pressure), the worse the weather will be: rain, cold, gloom, clouds, etc. And the higher the needle goes (the higher the air pressure), the milder the temperature, the sunnier and warmer the weather will be.'

Since our 'barometer' is digital and there's no needle, here's how to read the output: "A barometric reading over 30.20 inHg is generally considered high, and high pressure is associated with clear skies and calm weather. A barometric reading below 29.80 inHg is generally considered low, and low pressure is associated with warm air and rainstorms."

---

*Created with nostalgia and code by [Anestis Mystakidis]*

[Watch the Demo Video]https://youtu.be/ZGFM5_Vwtvk?si=TvgyibE6bEjIplZV