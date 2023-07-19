import os

import numpy as np
import pandas as pd

# amenities = pd.read_csv('amenity/all-AmentiesCount.csv')
# roads = pd.read_csv('amenity/all-RoadLength.csv')
# amenities = amenities['amenity']
# highwaies = roads['highway']

# public transport, cycling infrastructure, and the integration of land use planning and transport policies.
# walk or bike ride.
# This involves integrating residential, commercial, educational, and recreational facilities within close proximity.
# Walkability and Cycling Infrastructure
# Pedestrian-friendly streets, well-designed sidewalks, dedicated bike lanes, and bike-sharing programs facilitate active modes of transportation.
# buses, trams, or metro networks, enhance connectivity within the city.
# This includes access to grocery stores, healthcare facilities, schools, parks, and recreational spaces.
# well-connected network of pedestrian-friendly streets, dedicated cycling lanes, and efficient public transportation systems.
# Factors such as social norms, urban morphology, and historical heritage should be taken into account.

# ['busway', 'footway', 'bank', 'living_street', 'road', 'track', 'atm', 'bus_station', 'college', 'clinic', 'dentist', 'doctors', 'hospital', 'marketplace', 'pharmacy', 'school']
from shapely import Polygon, wkt

category = [{'public transport': ['bureau_de_change', 'bus_station', 'car_sharing', 'busway', 'road', 'track',
                                  'motorway', 'path', 'motorcycle_parking', 'parking', 'car_rental', 'corridor',
                                  'taxi', 'fuel', 'parking_entrance']},
            {'cycling infrastructure': ['bicycle_parking', 'bicycle_rental', 'cycleway']},
            {'sidewalks': ['footway', 'pedestrian']},
            {'residential': ['residential']},
            {'public safety': ['fire_station', 'police']},
            {'commercial': ['atm', 'bank', 'register_office', 'post_box', 'post_office', 'marketplace',
                            'vending_machine']},
            {'educational': ['college', 'university', 'driving_school', 'school', 'kindergarten', 'music_school']},
            {'recreational': ['cafe', 'cinema', 'fast_food', 'restaurant', 'ice_cream', 'food_court', 'rest_area',
                              'drinking_water', 'internet_cafe', 'library', 'place_of_worship', 'social_centre',
                              'service', 'social_facility', 'theatre', 'toilets', 'townhall', 'waste_basket',
                              'waste_disposal']},
            {'healthcare': ['dentist', 'doctors', 'clinic', 'pharmacy', 'hospital', 'veterinary']}]

keywords = ['atm', 'bureau_de_change', 'bus_station', 'car_sharing', 'busway', 'road', 'track',
            'motorway', 'path', 'motorcycle_parking', 'parking', 'car_rental', 'corridor', 'vending_machine'
            'taxi', 'fuel', 'parking_entrance', 'bicycle_parking', 'bicycle_rental', 'music_school'
            'cycleway', 'footway', 'pedestrian', 'residential', 'fire_station', 'police', 'bank', 'register_office',
            'post_box', 'post_office', 'college', 'university', 'driving_school', 'school', 'kindergarten',
            'cafe', 'cinema', 'fast_food', 'restaurant', 'ice_cream', 'food_court', 'rest_area',
            'drinking_water', 'internet_cafe', 'library', 'place_of_worship', 'social_centre', 'service',
            'social_facility', 'theatre', 'toilets', 'townhall', 'waste_basket', 'waste_disposal', 'marketplace',
            'dentist', 'doctors', 'clinic', 'pharmacy', 'hospital', 'veterinary']

results = {}
count = []

for path, subdirs, files in os.walk('amenity/'):
    for i in range(len(files)):
        try:
            key = files[i].split('-')[0]
            # print(files[i].split('-')[0])
            name = files[i].split('-')[2]

            a = pd.read_csv('amenity/' + files[i])

            if name == 'AmentiesCount.csv':
                name = 'amenity'
            elif name == 'RoadLength.csv':
                name = 'highway'

            common_amenities = [{keywords[i]: a['count'].iloc[a[name].to_list().index(keywords[i])]}
                                for i in range(len(keywords))
                                if keywords[i] in a[name].to_list()]
            # print(common_amenities)

            count = []

            for i, cat in enumerate(category):
                cat_count = 0
                for amenity in common_amenities:
                    if list(amenity.keys())[0] in list(cat.values())[0]:
                        cat_count += list(amenity.values())[0]
                count.append(cat_count)

            item = results.get(key)
            if item is not None:
                count = [c + i for c, i in zip(count, item)]

            total_count = len(count)
            percentage = (sum(1 for c in count if c >= 1) / total_count) * 100
            count.append(round(percentage, 2))

            results.__setitem__(key, count)

            # common_amenities = [{keywords[i]: a['count'].iloc[a['amenity'].to_list().index(keywords[i])]}
            #                     for i in range(len(keywords))
            #                     if keywords[i] in a['amenity'].to_list()]
            # # print(common_amenities)
            #
            # count = []
            # for key in keywords:
            #     key_count = 0
            #     for amenity in common_amenities:
            #         if key in amenity:
            #             key_count = amenity[key]
            #     count.append(key_count)
            #
            # row = files[i].split('-')[0], count
            # results.__setitem__(files[i].split('-')[0], count)

            # common_amenities = [{amenities['amenity'].iloc[i]: a['count'].iloc[a['amenity'].to_list().index(amenities['amenity'].iloc[i])]}
            #                     for i in range(len(amenities))
            #                     if amenities['amenity'].iloc[i] in a['amenity'].to_list()]
            # print(common_amenities)

        except:
            pass

# categories = ['zone']
categories = [list(dic.keys())[0] for dic in category]
categories.append('percentage')

df = pd.DataFrame(results, index=categories)
df = df.transpose()

total_results = len(results)
percentages = []
for key in categories:
    percentages.append(round((sum(1 for res in df[key] if res >= 1) / total_results) * 100, 2))

percentages.pop()
percentages.append(np.mean(df['percentage']))
results.__setitem__('percentage', percentages)

df = pd.DataFrame(results, columns=results.keys(), index=categories)
# print(df.head())
# df = df.transpose()
# df.to_html('results.html')
# df.to_csv('results.csv')


# from matplotlib import pyplot as plt
# plt.hist(percentages, categories)
# plt.show()



import json
import requests
import pandas as pd

relation_ids = [5710706, 5711010, 5711407, 5711567, 5712345, 5714586, 5714602, 5714616, 5722613, 5724225,
                5724306, 5725071, 5725072, 8863117, 8863118, 9042658, 9042659, 9042653, 9042654, 9042650,
                9042651, 9042652, 8834223, 8834224, 8834225, 8834226, 8834227, 9068587, 8810327, 8810328,
                8810329, 8810330, 8873128, 8873129, 9042655, 9042656, 9042657, 9042648, 9042649, 8873125,
                8873126, 8873127, 9042646, 9042660, 9042661, 8873134, 8873135, 8873136, 8873130, 8873131,
                8873132, 8873133, 8796705, 8796706, 8796707, 8796708, 8796694, 8796698, 8796699, 8796700,
                10235671, 8796695, 8796696, 8796701, 8796702, 10374714, 10374716, 8796697, 8796703, 8796704,
                11009418, 8785942, 8785943, 8785944, 8785946, 8785947, 8785948, 8785945, 8785949, 8785950,
                8785951, 8785952, 8824631, 8824632, 8824633, 8824629, 8824630, 8824634, 8824635, 8824636,
                8824637, 8824638, 8824639, 8824640, 8824641, 8824642, 8824643, 8824644, 8824645, 8824646,
                8824866, 8824867, 8824868, 8824869, 8824870, 9068585, 9068586, 8824871, 8824872, 8824873,
                8824874, 8824875, 8824876, 8792420, 8792421, 8792422, 8792423, 8792424, 8792425, 8792426,
                8788794, 8792427, 8788795, 8788796, 8788797, 8788798, 8788799, 8788800, 8788801, 8788802,
                8788803, 8788804, 8788805, 8788806, 8788807, 8788808, 11009422, 11009423, 11009424, 11009428,
                11009429, 11009430, 11009431, 11009432, 11009433, 11009435, 8810560, 8810561, 8810562, 8810563,
                8810557, 8810558, 8810559, 8810554, 8810555, 8810556, 8833948, 8833949, 8833659, 8833660,
                8833661, 8833662, 8833663, 8833664, 11248722, 8833665, 8833666, 8833667, 8833668, 8833669,
                8833670, 10374717, 10374718, 8815020, 8815673, 8815674, 8815675, 8815676, 8815662, 8815668,
                8815669, 8815670, 8815671, 8815672, 8815663, 8815664, 8815665, 8815666, 8815667, 8815016,
                8815017, 8815018, 8815019, 8815020, 8815021, 8815013, 8815014, 8815015, 10776078, 8833775,
                8833777, 8833778, 8833779, 11248723, 8833768, 8833769, 8833770, 8833771, 11248724, 8833772,
                8833773, 8833774, 8833776, 8833839, 8833840, 8833841, 8833842, 8833843, 8833844, 8833845,
                8833846, 8833847, 8833950, 9042642, 8833947, 9042643, 9042644, 9042645]


features = []
for relation_id in relation_ids:
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    relation({relation_id});
    out geom;
    """

    response = requests.get(overpass_url, params={"data": query})
    data = response.json()

    try:
        relation = data["elements"][0]
        name = relation['tags']['name']
        geometry = relation['members'][0]['geometry']

        percentage = df[name].iloc[-1]

        coordinates = []
        for geo in geometry:
            coordinates.append([geo['lat'], geo['lon']])
        # coordinates.append([geometry[0]['lat'], geometry[0]['lon']])
        # print(coordinates)

        polygon = Polygon(coordinates)
        # Print the polygon as a WKT string
        print(polygon.wkt)
        boundary = wkt.loads(polygon.wkt)
        print(polygon.wkt)

        features.append({
            "type": "Feature",
            "id": str(relation_id),
            "properties": {
                "name": name,
                "density": percentage
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [coordinates]
            }
        })

    except:
        print("Relation not found.")


staticdata = {
    "type": "FeatureCollection",
    "features": features
}
print(staticdata)

json_data = json.dumps(staticdata)
print(json_data)

with open("data.json", "w") as file:
    file.write(json_data)