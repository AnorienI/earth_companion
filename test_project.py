from project import validate_input, get_city_population, fetch_weather, get_coordinates, get_country_info


def test_validate_input():
    assert validate_input('New York') == False
    assert validate_input('Paris, FR') == True
    assert validate_input('Berlin, DE') == True
    assert validate_input('Tokyo, JP') == True

def test_get_city_population():
    assert get_city_population("New York") == None
    assert get_city_population("Paris") == None
    assert get_city_population("Berlin") == None
    assert get_city_population("Tokyo") == None

def test_fetch_weather():
    assert fetch_weather("New York") == None
    assert fetch_weather("Paris") == None
    assert fetch_weather("Berlin") == None
    assert fetch_weather("Tokyo") == None

def test_get_coordinates():
    assert get_coordinates("New York") == None
    assert get_coordinates("Paris") == None
    assert get_coordinates("Berlin") == None
    assert get_coordinates("Tokyo") == None

def test_get_country_info():
    assert get_country_info("New York") == None
    assert get_country_info("Paris") == None
    assert get_country_info("Berlin") == None
    assert get_country_info("Tokyo") == None