import os 
import pandas as pd
import requests
import csv
import json

os.chdir('C:/Users/Editor PC 2/Desktop/francis/Python/NASA_NEWOS')

def Asteroidneows():
    def fetch_newos_data(start_date, end_date, api_key):
        base_url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}'
        response = requests.get(base_url)
        return response.json()
    
    def newos_to_csv(newos_data, csv_filename):
        
        neo_data = newos_data['near_earth_objects']

        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            writer.writerow(['Date', 'Name', 'Reference ID', 'Absolute Magnitude', 'Close Approach Date', 'Relative Velocity (km/s)',  'Relative Velocity (km/h)', 'Estimated Diameter Min (km)', 'Estimated Diameter Max (km)', 'Miss Distance (km)', 'Orbitiing Body', 'Potentially Hazardous'])
            # 'absolute_magnitude_h': 24.74, 'estimated_diameter': {'kilometers': {'estimated_diameter_min': 0.0299609084, 'estimated_diameter_max': 0.0669946278}
            # 'close_approach_data': [{'close_approach_date': '2021-01-01', 'close_approach_date_full': '2021-Jan-01 11:00', 'epoch_date_close_approach': 1609498800000, 'relative_velocity': {'kilometers_per_second': '11.3411969891', 'kilometers_per_hour': '40828.309160747', 'miles_per_hour': '25369.1235449097'}, 'miss_distance': {'astronomical': '0.0802024851', 'lunar': '31.1987667039', 'kilometers': '11998120.939666737', 'miles': '7455286.6456734906'}, 'orbiting_body': 'Earth'}]

            for date, neos_list in neo_data.items():
                for neo in neos_list:
                    name = neo['name']
                    reference_id = neo['neo_reference_id']
                    abs_magnitude = neo['absolute_magnitude_h']
                    close_approach_data = neo['close_approach_data'][0]
                    close_approach_date = close_approach_data['close_approach_date']
                    relative_velocity_s = close_approach_data['relative_velocity']['kilometers_per_second']
                    relative_velocity_h = close_approach_data['relative_velocity']['kilometers_per_hour']
                    est_diameter_min = neo['estimated_diameter']['kilometers']['estimated_diameter_min']
                    est_diameter_max = neo['estimated_diameter']['kilometers']['estimated_diameter_max']
                    miss_distance = close_approach_data['miss_distance']
                    orbiting_body = close_approach_data['orbiting_body']
                    potential_hazard = neo['is_potentially_hazardous_asteroid']

                    writer.writerow([date, name, reference_id, abs_magnitude, close_approach_date, relative_velocity_s, relative_velocity_h, est_diameter_min, est_diameter_max, miss_distance, orbiting_body, potential_hazard])
    
    start_date = input('Start Date:')
    end_date = input('End Date: ')
    api_key = 'JX2y9dGrVLsftq4K3sVTM7SBzULM3R1cAQ8h1BGm'
    csv_filename = f"new_data_{start_date}_{end_date}"

    newos_data = fetch_newos_data(start_date, end_date, api_key)
    
    newos_to_csv(newos_data, csv_filename)
Asteroidneows()

