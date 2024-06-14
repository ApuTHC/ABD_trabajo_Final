import json
import time
import uuid
import random
from datetime import datetime, timedelta
import pytz
from geopy.geocoders import Nominatim
from meteostat import Point, Hourly

# Definir las coordenadas aproximadas de Medellín
lat_range = (6.217, 6.317)  # Latitud de Medellín
lon_range = (-75.567, -75.467)  # Longitud de Medellín

# Generar 100 puntos de venta únicos
points_of_sale = [(round(random.uniform(*lat_range), 6), round(random.uniform(*lon_range), 6)) for _ in range(100)]

# Generar 200 empleados, 2 por cada punto de venta
employees = {i: (f"Employee_{i*2+1}", f"Employee_{i*2+2}") for i in range(100)}

# Inicializar el geolocalizador
geolocator = Nominatim(user_agent="medellin_locator")

# Función para obtener la comuna y barrio según las coordenadas
def get_location_info(latitude, longitude):
    location = geolocator.reverse((latitude, longitude), language='es')
    address = location.raw['address']
    comuna = address.get('suburb', 'No encontrado')
    barrio = address.get('neighbourhood', 'No encontrado')
    return comuna, barrio

# Función para obtener la temperatura actual
def get_current_temperature(latitude, longitude):
    location = Point(latitude, longitude)
    start = datetime.now() - timedelta(hours=1)
    end = datetime.now()
    data = Hourly(location, start, end)
    data = data.fetch()
    temperature = data['temp'].mean() if not data.empty else 'No data'
    return round(temperature, 1)

# Generar datos simulados
def generate_event():
    pos_index = random.randint(0, 99)
    pos = points_of_sale[pos_index]
    worker = employees[pos_index]
    date_now = datetime.now(pytz.timezone('America/Bogota'))
    comuna, barrio = get_location_info(pos[0], pos[1])
    temperature = get_current_temperature(pos[0], pos[1])
    
    event = {
        "latitude": pos[0],
        "longitude": pos[1],
        "date": date_now.strftime("%d/%m/%Y %H:%M:%S"),
        "customer_id": random.randint(1000, 2000),
        "employee_id": worker[0] if date_now.weekday() < 5 else worker[1],  # Lunes a Viernes / Fines de Semana
        "quantity_products": random.randint(1, 50),
        "order_id": str(uuid.uuid4()),
        "commune": comuna,
        "neighborhood": barrio,
        "partition_date": date_now.strftime("%d%m%Y"),
        "event_date": date_now.strftime("%d/%m/%Y %H:%M:%S"),
        "event_day": date_now.day,
        "event_hour": date_now.hour,
        "event_minute": date_now.minute,
        "event_month": date_now.month,
        "event_second": date_now.second,
        "event_year": date_now.year,
        "current_temperature": temperature
    }
    return event

def main():
    for _ in range(100):
        event = generate_event()
        # Aquí se puede guardar el evento en un archivo JSON, base de datos, etc.
        # Ejemplo de guardado en un archivo JSON
        with open('simulated_data2.json', 'a') as file:
            file.write(json.dumps(event) + "\n")
        # Esperar 1 segundo antes de generar el siguiente evento
        time.sleep(1)

if __name__ == "__main__":
    main()
