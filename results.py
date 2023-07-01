import os
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


category = [{'public transport': ['bureau_de_change', 'bus_station', 'car_sharing', 'busway', 'road', 'track',
                                  'motorway', 'path', 'motorcycle_parking', 'parking', 'car_rental', 'corridor',
                                  'taxi', 'fuel', 'parking_entrance']},
            {'cycling infrastructure': ['bicycle_parking', 'bicycle_rental', 'cycleway']},
            {'sidewalks': ['footway', 'pedestrian']},
            {'residential': ['residential']},
            {'public safety': ['fire_station', 'police']},
            {'commercial': ['atm', 'bank', 'register_office', 'post_box', 'post_office']},
            {'educational': ['college', 'university', 'driving_school', 'school', 'kindergarten', 'music_school']},
            {'recreational': ['cafe', 'cinema', 'fast_food', 'restaurant', 'ice_cream', 'food_court', 'rest_area',
                              'drinking_water', 'internet_cafe', 'library', 'place_of_worship', 'social_centre',
                              'service', 'social_facility', 'theatre', 'toilets', 'townhall', 'waste_basket',
                              'waste_disposal']},
            {'stores': ['marketplace', 'vending_machine']},
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
                common_amenities = [{keywords[i]: a['count'].iloc[a['amenity'].to_list().index(keywords[i])]}
                                    for i in range(len(keywords))
                                    if keywords[i] in a['amenity'].to_list()]
            elif name == 'RoadLength.csv':
                common_amenities = [{keywords[i]: a['count'].iloc[a['highway'].to_list().index(keywords[i])]}
                                    for i in range(len(keywords))
                                    if keywords[i] in a['highway'].to_list()]

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
            count.append(percentage)

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

categories = [list(dic.keys())[0] for dic in category]
categories.append('acc')
df = pd.DataFrame(results, index=categories)
df = df.transpose()
df.to_html('results.html')
df.to_csv('results.csv')
