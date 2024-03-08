import pandas as pd 
import matplotlib.pyplot as plt
import os
import requests
import csv 
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')


def fetch_neows_data(start_date, end_date, api_key):
    base_url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}'
    response = requests.get(base_url)
    return response.json()

def neows_to_csv(neows_data, csv_filename):
    
    neo_data = neows_data['near_earth_objects']
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
api_key = API_KEY
csv_filename = f"new_data_{start_date}_{end_date}"
neows_data = fetch_neows_data(start_date, end_date, api_key)

neows_to_csv(neows_data, csv_filename)

df_name = 'neows_2024-02-14_2024-02-20.csv'
df = pd.read_csv(df_name)
# new_df = df.sort_values(by="Absolute Magnitude", ascending=False)
# print(new_df.head())

def TakeConditions():
    speed = []
    distance = []
    diameter = []
    hazard_warning = []
    abs_magnitude = []

    for name, vel_s, vel_h, dist, diameter_min, diameter_max, warning, abs_mag in zip(df['Name'],
                                                                            df['Relative Velocity (km/s)'],
                                                                            df['Relative Velocity (km/h)'],
                                                                            df['Miss Distance (kilometers)'],
                                                                            df['Estimated Diameter Min (km)'],
                                                                            df['Estimated Diameter Max (km)'],
                                                                            df['Potentially Hazardous'],
                                                                            df['Absolute Magnitude']):
        name = name.replace('(', "").replace(')', "").strip().upper()
        speed.append({'Name': name, 'Relative Velocity (km/s)': round(vel_s, 2), 'Relative Velocity (km/h)': round(vel_h, 2)})
        distance.append({'Name': name, 'Miss Distance (kilometers)': round(dist, 2)})
        diameter.append({'Name': name, 'Estimated Diameter Min (km)': round(diameter_min, 2), 'Estimated Diameter Max (km)': round(diameter_max, 2)})
        hazard_warning.append({'Name': name, 'Potentially Hazardous': warning})
        abs_magnitude.append({'Name': name, 'Absolute Magnitude': round(abs_mag, 2)})
    
    new_velocity = pd.DataFrame(speed)
    new_distance = pd.DataFrame(distance)
    new_diameter = pd.DataFrame(diameter)
    new_hazard = pd.DataFrame(hazard_warning)
    new_abs_mag = pd.DataFrame(abs_magnitude)

    new_velocity.to_csv('speed.csv', index=False)
    new_distance.to_csv('distance.csv', index=False)
    new_diameter.to_csv('diameter.csv', index=False)
    new_hazard.to_csv('hazard.csv', index=False)
    new_abs_mag.to_csv("absolute_magnitude.csv", index=False)


def calculate_danger_score(asteroid):
    points = 0
    dist = asteroid['Miss Distance (kilometers)']
    if dist < 7000000:
        points += 0
    elif dist >=  1000000 and dist <= 7000000:
        points += int((1 + (dist-7000000) * (25-1)/(abs(1000000-7000000))))
    else:
        points += 25
    
    vel = asteroid['Relative Velocity (km/h)']
    if vel < 45000:
        points += 0
    elif vel >= 45000 and vel <= 156900:
        points += int((1 + (vel-45000) * (25-1)/(156900-45000)))
    else:
        points += 25

    diam = asteroid['Estimated Diameter Min (km)']
    if diam < 0.100:
        points += 0
    elif diam >= 0.100 and diam <= 5.4:
        points += int((1 + (diam-0.100) * (25-1)/(5.4-0.100)))
    else:
        points += 25

    abs_mag = asteroid['Absolute Magnitude']
    if abs_mag < 22.00:
        points += 0
    elif abs_mag >= 22.00 and abs_mag <= 30:
        points += int((1 + (abs_mag-22.00) * (25-1)/(30-22.00)))
    else:
        points += 25
    return(points)

modified_df = df
modified_df['Hazard Points'] = df.apply(calculate_danger_score, axis=1)
modified_df.to_csv(f'modified_{df_name}')


def plot_point_to_parameter(column_name, start_date, end_date):
    # column_df = df[str(column_name)]
    new_df = pd.read_csv(f'modified_neows_{start_date}_{end_date}.csv')
    # new_df.plot(kind='scatter', x = 'Hazard Points', y=column_name, figsize=(15,5), title=f'Trend of {column_name} against Hazard Points', xlabel = 'Hazard Points', ylabel = column_name)
    plt.figure(figsize=(15, 5))
    plt.scatter(new_df[column_name], new_df['Hazard Points'])
    plt.title(f'Trend of {column_name} against Hazard Points')
    plt.ylabel('Hazard Points')
    plt.xlabel(column_name)
    plt.show()


    

# Algorithm For Hazard Points
# IF speed > 45mkm/h poses danger. From 45 = 1pt, max=25
# IF 




#Take Speed, Distance, Diameter, Hazard Warning
# def TakeConditions():
#     speed = []
#     distance = []
#     diameter =[]
#     hazard_warning = []

#     for name in df['Name']:
#         name = name.replace('(', "")
#         name = name.replace(')', "")
#         name = name.strip().upper()
#         speed.append({'Name': name})
#         distance.append({'Name': name})
#         diameter.append({'Name': name})
#         hazard_warning.append({'Name': name})
        
#     for vel_s, vel_h in df['Relative Velocity (km/s)'], df['Relative Velocity (km/h)']:
#         vel_s = vel_s.round(vel_s, 2)
#         vel_h = vel_h.round(vel_h, 2)
#         speed.append({'Relative Velocity (km/s)': vel_s,'Relative Velocity (km/h)': vel_h})
    
#     for dist in df['Miss Distance (kilometers)']:
#         dist = dist.round(dist, 2)
#         distance.append({'Miss Distance (kilometers)': dist})
    
#     for diameter_min, diameter_max in df['Estimated Diameter Min (km)'], df['Estimated Diameter Max (km)']:
#         diameter_min = diameter_min.round(diameter_min, 2)
#         diameter_max = diameter_max.round(diameter_max, 2)
#         diameter.append({'Estimated Diameter Min (km)': diameter_min, 'Estimated Diameter Max (km)': diameter_max})

#     for warning in df['Potentially Hazardous']:
#         hazard_warning.append({'Potentially Hazardous': warning})
#     new_velocity = pd.DataFrame('speed.csv')
#     new_distance = pd.DataFrame('distance.csv')
#     new_diameter = pd.DataFrame('diameter.csv')
#     new_hazard = pd.DataFrame('hazard.csv')

#     print(new_distance.head())
#     print(new_velocity.head())
#     print(new_diameter.head())
#     print(new_hazard.head())
# TakeConditions()





# array1=df["Name"].values # as numpy array
# array2=list(df["Estimated Diameter Max (km)"].values) # as python array


# array_new = pd.DataFrame(array1)
# print(array_new)
# array_new2 = pd.DataFrame(array2)
# print(array_new2)