import csv
import requests
import os

os.chdir('C:/Users/Editor PC 2/Desktop/francis/Python/NASA_NEWOS')

# Function to fetch data from NASA NeoWs API
def fetch_neows_data(start_date, end_date, api_key):
    base_url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}'
    response = requests.get(base_url)
    print(response.json())
    return response.json()


# Function to convert NEOs data to CSV
def neows_to_csv(neows_data, csv_filename):
    # Extract NEOs data from the response
    neo_data = neows_data['near_earth_objects']
    
    # Open CSV file in write mode
    with open(csv_filename, 'w', newline='') as csvfile:
        # Create CSV writer object
        writer = csv.writer(csvfile)
        
        # Write header row
        writer.writerow(['Date', 'Name', 'Reference ID', 'Absolute Magnitude', 'Close Approach Date', 'Relative Velocity (km/s)', 'Relative Velocity (km/h)', 'Estimated Diameter Min (km)', 'Estimated Diameter Max (km)', 'Miss Distance (kilometers)', 'Potentially Hazardous'])
        # 'estimated_diameter': {'kilometers': {'estimated_diameter_min': 0.1138557521, 'estimated_diameter_max': 0.2545892014}, 'meters': {'estimated_diameter_min': 113.8557521352, 'estimated_diameter_max': 254.5892014037}, 'miles': {'estimated_diameter_min': 0.0707466626, 'estimated_diameter_max': 0.1581943467}, 'feet': {'estimated_diameter_min': 373.5425058353, 'estimated_diameter_max': 835.2664355335}}, 'is_potentially_hazardous_asteroid': False
        # [{'close_approach_date': '2024-02-20', 'close_approach_date_full': '2024-Feb-20 15:39', 'epoch_date_close_approach': 1708443540000, 'relative_velocity': {'kilometers_per_second': '12.0869269092', 'kilometers_per_hour': '43512.9368731621', 'miles_per_hour': '27037.2468032157'}, 'miss_distance': {'astronomical': '0.2452661254', 'lunar': '95.4085227806', 'kilometers': '36691289.942992898', 'miles': '22798910.3710540724'}, 'orbiting_body': 'Earth'}]
        
        # Write NEOs data to CSV
        for date, neos_list in neo_data.items():
            for neo in neos_list:
                name = neo['name']
                reference_id = neo['neo_reference_id']
                abs_magnitude = neo['absolute_magnitude_h']
                close_approach_data = neo['close_approach_data'][0]  # Assuming there's only one close approach
                close_approach_date = close_approach_data['close_approach_date']
                relative_velocity_s = close_approach_data['relative_velocity']['kilometers_per_second']
                relative_velocity_h = close_approach_data['relative_velocity']['kilometers_per_hour']
                diameter_min = neo['estimated_diameter']['kilometers']['estimated_diameter_min']
                diameter_max = neo['estimated_diameter']['kilometers']['estimated_diameter_max']
                miss_distance_km = close_approach_data['miss_distance']['kilometers']
                potential_hazard = neo['is_potentially_hazardous_asteroid']
                
                # Write NEO data to CSV row
                writer.writerow([date, name, reference_id, abs_magnitude, close_approach_date, relative_velocity_s, relative_velocity_h, diameter_min, diameter_max, miss_distance_km, potential_hazard])

start_date = '2024-02-15'
end_date = '2024-02-20'
api_key = 'JX2y9dGrVLsftq4K3sVTM7SBzULM3R1cAQ8h1BGm'
csv_filename = 'neows_data.csv'

# Fetch data from NASA NeoWs API
neows_data = fetch_neows_data(start_date, end_date, api_key)

# Convert NEOs data to CSV
# neows_to_csv(neows_data, csv_filename)

fetch_neows_data('2024-02-15', '2024-02-20', 'JX2y9dGrVLsftq4K3sVTM7SBzULM3R1cAQ8h1BGm')

# {'estimated_diameter_min': 350.3805805155, 'estimated_diameter_max': 783.4747960285}}, 'is_potentially_hazardous_asteroid': False
# relative_velocity': {'kilometers_per_second': '13.1182804852', 'kilometers_per_hour': '47225.809746859'
