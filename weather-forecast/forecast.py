import requests
import json
import argparse

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def handle_response(response: requests.Response) -> dict | None:
	"""
	Handles the response from an API request and returns the JSON data if the response is successful.

	Args:
		response (requests.Response): The response object from the API request.

	Returns:
		dict | None: The JSON data from the response if the status code is 200, otherwise None.
	"""
	if response.status_code == 200:
		return response.json()
	else:
		return None

def get_forecast_response(latitude: float, longitude: float) -> dict | None:
	response = requests.get(FORECAST_URL,
				params={
					"latitude": latitude,
					"longitude": longitude,
					"hourly": "temperature_2m",
					"forecast_days": 1,
				})
	response = handle_response(response)
	return response
	

def main() -> None:
	parser = argparse.ArgumentParser(description="Get the weather forecast for a location.")
	parser.add_argument("--latitude", type=float, help="Latitude of the location")
	parser.add_argument("--longitude", type=float, help="Longitude of the location")
	args = parser.parse_args()

	if args.latitude and args.longitude:
		latitude = args.latitude
		longitude = args.longitude
	else:
		latitude = float(input("Enter latitude: "))
		longitude = float(input("Enter longitude: "))

	response = get_forecast_response(latitude, longitude)
	if response:
		print("Forecast data:\n\n")
		print(json.dumps(response, indent=2))
	else:
		print("Failed to get forecast data.")

if __name__ == "__main__":
	main()
