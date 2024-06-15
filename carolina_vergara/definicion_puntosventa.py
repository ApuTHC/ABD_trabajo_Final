import json
import random
from geopy.geocoders import Nominatim

# Definir las coordenadas aproximadas de Medellín
lat_range = (6.217, 6.317)  # Latitud de Medellín
lon_range = (-75.567, -75.467)  # Longitud de Medellín

# Inicializar el geolocalizador
geolocator = Nominatim(user_agent="medellin_locator")

# Función para obtener la comuna y barrio según las coordenadas
def get_location_info(latitude, longitude):
    location = geolocator.reverse((latitude, longitude), language='es')
    address = location.raw['address']
    comuna = address.get('suburb', 'No encontrado')
    barrio = address.get('neighbourhood', 'No encontrado')
    return comuna, barrio

# Generar puntos de venta únicos
def generate_valid_points(n):
    valid_points = []
    while len(valid_points) < n:
        lat = round(random.uniform(*lat_range), 6)
        lon = round(random.uniform(*lon_range), 6)
        comuna, barrio = get_location_info(lat, lon)
        if comuna != 'No encontrado' and barrio != 'No encontrado':
            valid_points.append({"latitude": lat, "longitude": lon, "commune": comuna, "neighborhood": barrio})
    return valid_points

# Generar y guardar 100 puntos válidos
points_of_sale = generate_valid_points(100)

with open('valid_points.json', 'w') as file:
    json.dump(points_of_sale, file)

