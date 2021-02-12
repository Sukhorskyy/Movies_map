'''
GitHub address:

Module create a map of movies made in the user area
Also it requires from user to input the year of film making
The program works only for locations in the following countries: 
Ukraine, Germany, Austria, Poland, Czech Republic, Slovenia.

Required data files: europe_loc.csv, world.json
'''

import folium
import pandas
import geopy.distance


def create_map(years_range, coordinates):
    '''
    (str, tuple) -> None
    Create map using user's coordinates and year
    '''
    data = pandas.read_csv("europe_loc.csv", error_bad_lines=False)
    data = data[data['year'] == str(years_range)]
    data = data.drop_duplicates(subset =["place"])
    lat_list = data['latitude'].tolist()
    lon_list = data['longitude'].tolist()
    dist = []
    for i in range(len(lat_list)):
        dist.append(calculate_distance((lat_list[i], lon_list[i]), coordinates))
    data['distanse'] = dist
    data = data[data['distanse'] <= 300]
    data = data.sort_values(by=['distanse'])
    if len(data) >= 10:
        data = data.iloc[:10]

    lat = data['latitude']
    lon = data['longitude']
    name = data['name']
    map = folium.Map(location=list(coordinates), zoom_start=6, control_scale=True)
    fg = folium.FeatureGroup(name='map', )
    for lt, ln, nm in zip(lat, lon, name):
        fg.add_child(folium.Marker(location=[lt, ln], \
            popup=nm, icon=folium.Icon(color="red", icon="camera")))
    folium.Circle(radius=300000, location=list(coordinates), popup="Radius", color="#3186cc").add_to(map)
    map.add_child(fg)
    map.add_child(folium.Marker(location=list(coordinates), \
        popup="Your location", icon=folium.Icon(color="green", icon="user")))

    fg_pp = folium.FeatureGroup(name="Population")
    fg_pp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(), \
        style_function=lambda x: {'fillColor': '#FBEEE6' \
        if x['properties']['POP2005'] < 10000000 \
            else '#EDBB99' if 10000000 <= x['properties']['POP2005'] < 15000000 \
            else '#DC7633' if 15000000 <= x['properties']['POP2005'] < 20000000 \
            else '#BA4A00' if 20000000 <= x['properties']['POP2005'] < 25000000 \
            else '#A04000' if 30000000 <= x['properties']['POP2005'] < 35000000 \
            else '#6E2C00'}))
    map.add_child(fg_pp)
    map.add_child(folium.LayerControl())

    file_name = str(years_range)+ '_movies_map.html'
    map.save(file_name)


def get_data_from_user():
    '''
    () -> (str, tuple)
    Ask user to input year and coordinates
    '''
    years_range = input('Please enter a year you would like to have a map for: ')
    coordinates = input('Please enter your location (format: lat, long): ')
    coordinates = coordinates.split(',')
    for i in range(2):
        coordinates[i] = coordinates[i].strip()
    return years_range, tuple(coordinates)


def calculate_distance(coord_1, coord_2):
    '''
    (tuple, tuple) -> float
    Return distance between two coordinates
    >>> print(calculate_distance((50.2547, 28.6587), (49.8397, 24.0297)))
    334.69622493405905
    >>> print(calculate_distance((50.2547, 28.6587), (51.8397, 18.0297)))
    765.1874990038626
    '''
    dist = geopy.distance.distance(coord_1, coord_2).km
    return dist


def main():
    user_data = get_data_from_user()
    print('Map is generating...')
    print('Please wait...')
    create_map(user_data[0], user_data[1])
    print('Finished. Please have look at the map ' + str(user_data[0]) + '_movies_map.html')


if __name__ == "__main__":
    main()
