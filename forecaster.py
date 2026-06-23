from geopy import Nominatim
import httpx

def get_coords(city, ) -> tuple[float, float] | None:
    geolocator = Nominatim(user_agent='rimunomido')
    loc = geolocator.geocode(city)

    if loc is None:
        return None

    lat = loc.latitude
    lon = loc.longitude

    return (lat, lon)

    # Возвращает словарь из нескольких подсловарей.
async def send_request(url, access_key, coords: tuple[float, float]) -> dict | None:
    headers = {'X-Yandex-Weather-Key': access_key}
    query = """
    query GetWeather($lat: Float!, $lon: Float!) {
        weatherByPoint(request: { lat: $lat, lon: $lon }) {
            now {
            cloudiness
            humidity
            precType
            precStrength
            pressure
            temperature
            fahrenheit: temperature(unit: FAHRENHEIT)
            windSpeed
            windDirection
            }
        }
    }
    """
    variables = {
        "lat": coords[0],
        "lon": coords[1]
    }

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.post(url, headers=headers, json={'query': query, 'variables': variables})
            response.raise_for_status()
            return response.json()
    except httpx.exceptions.RequestError as e:
        return None
    except ValueError as e:
        return None