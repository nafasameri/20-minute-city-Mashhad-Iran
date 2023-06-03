import requests
import pandas as pd


# Define the relation ID
relation_id = 5725071

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

    df = pd.DataFrame([relation])
    df.to_csv('5725071.csv')

    # df = pd.DataFrame(relation['members'])
    # df.to_csv('members.csv')

    # Extract information from the relation
    relation_tags = relation["tags"]
    relation_members = relation["members"]
    # relation_geometry = relation["geometry"]

    # Print the extracted information
    print("Relation Tags:", relation_tags)
    print("Relation Members:", relation_members)
    # print("Relation Geometry:", relation_geometry)
else:
    print("Relation not found.")

#
#
#
# import osmnx as ox
#
# # Define the relation ID
# relation_id = 5725142
#
# # Retrieve the relation as a MultiPolygon
# relation = ox.geocode_to_gdf(query=f"relation/{relation_id}", which_result=10)
#
# # Print the relation information
# print(relation)
# df = pd.DataFrame(relation)
# df.to_csv('relation2.csv')
#
#
#
#
#
#
# import osmnx as ox
#
# # Define the relation ID
# relation_id = 5725142
#
# # Retrieve the relation as a MultiPolygon
# relation = ox.geocode_to_gdf(query=f"relation/{relation_id}", which_result=1)
# print(relation.keys())
#
# # Check if the "leisure" column exists
# if "leisure" in relation.columns:
#     # Filter parks within the relation
#     parks = relation[relation["leisure"] == "park"]
#
#     # Print the parks within the relation
#     if not parks.empty:
#         print(parks)
#     else:
#         print("No parks found within the relation.")
# else:
#     print("The 'leisure' column does not exist in the relation.")
#
#
#
#
#
#
#
#
#
# import osmnx as ox
#
# # Define the coordinates of the point
# latitude = 36.327567524
# longitude = 59.586795798
#
# # Define the distance to search around the point (in meters)
# distance = 5000  # Adjust the distance as needed
#
# # Retrieve parks near the point
# parks = ox.geometries_from_point((latitude, longitude), tags={"leisure": "park"}, dist=distance)
#
# # Print the parks near the point
# print(parks)
# df = pd.DataFrame(parks)
# df.to_csv('parks.csv')
#
#
#
#
#
#
#
# import osmnx as ox
# from shapely.geometry import Polygon
#
# # Define the coordinates of the polygon vertices
# polygon_vertices = [(35.123, 59.987), (35.234, 59.876), (35.345, 59.765), (35.456, 59.654)]
#
# # Create a polygon geometry from the vertices
# polygon = Polygon(polygon_vertices)
#
# # Retrieve parks within the polygon
# parks = ox.geometries_from_polygon(polygon, tags={"leisure": "park"})
#
# # Print the parks within the polygon
# print(parks)


