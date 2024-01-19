import googlemaps


map_client = googlemaps.Client(api_gmaps_key)
distance = 20
search_string = "Bualuang ATM"
response = map_client.places_nearby(
     location=(lat, lng),
     keyword=search_string,
     radius=distance
)
