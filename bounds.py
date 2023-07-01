import osmpy
import requests
import pandas as pd
from shapely import wkt
from shapely.geometry import Polygon

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

for relation_id in relation_ids:
    # relation_id = 5725071

    # Define the Overpass API query to retrieve the relation data
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    relation({relation_id});
    out geom;
    """

    # Send the query to the Overpass API
    response = requests.get(overpass_url, params={"data": query})
    data = response.json()

    # Process the relation data
    if "elements" in data:
        relation = data["elements"][0]  # Assuming the relation is the first element in the response

        # df = pd.DataFrame([relation])
        # df.to_csv(str(relation_id) + '.csv')

        name = relation['tags']['name']
        bounding_box = relation['bounds']
        print(name, "Relation Bounds:", bounding_box)

        # Create a polygon from the bounding box coordinates
        polygon = Polygon([
            (bounding_box['minlon'], bounding_box['minlat']),
            (bounding_box['maxlon'], bounding_box['minlat']),
            (bounding_box['maxlon'], bounding_box['maxlat']),
            (bounding_box['minlon'], bounding_box['maxlat']),
            (bounding_box['minlon'], bounding_box['minlat'])
        ])

        # Print the polygon as a WKT string
        # print(polygon.wkt)

        boundary = wkt.loads(polygon.wkt)
        relation_boundary = osmpy.get('Amenities', boundary)

        try:
            RoadLength = osmpy.get('RoadLength', boundary)
            # print(RoadLength)
            df = pd.DataFrame(RoadLength)
            df.to_csv(
                '/content/drive/My Drive/Colab Notebooks/amenity/' + name + '-' + str(relation_id) + '-RoadLength.csv')
        except:
            pass

        try:
            AmentiesCount = osmpy.get('AmentiesCount', boundary)
            # print(AmentiesCount)
            df = pd.DataFrame(AmentiesCount)
            df.to_csv('/content/drive/My Drive/Colab Notebooks/amenity/' + name + '-' + str(
                relation_id) + '-AmentiesCount.csv')
        except:
            pass

        df = pd.DataFrame(relation_boundary)
        df.to_csv('/content/drive/My Drive/Colab Notebooks/amenity/' + name + '-' + str(relation_id) + '.csv')

    else:
        print("Relation not found.")
