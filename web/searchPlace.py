from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="mygeocoder")


def search_coordinates(place_name):
    location = geolocator.geocode(place_name)

    return location.latitude, location.longitude