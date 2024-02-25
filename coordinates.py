import requests
import pandas as pd

relation_ids = [6728830, 6728896, 6728897, 6728863, 6729507, 6729037, 6729036,
                6729035, 6729508, 6729501, 6729111, 6729112, 6729034, 6729033,
                6729032, 6729110, 6729502, 6729503, 6729109, 6729031, 6729505, 6729506]

for relation_id in relation_ids:
    # Define the relation ID
    # relation_id = 6663864

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
        # print(relation)

        # df = pd.DataFrame([relation])
        # df.to_csv('tehran.csv')

        # df = pd.DataFrame(relation['members'])
        # df.to_csv('members.csv')

        # Extract information from the relation
        relation_tags = relation["tags"]
        relation_members = relation["members"]
        relation_bounds = relation["bounds"]

        # Print the extracted information
        # print("Relation Tags:", relation_tags)
        # print("Relation Members:", relation_members)
        print(relation_tags['name'], relation_bounds)

        # for x in relation_members:
        #     print(x)
        #     if x['type'] == "relation":
        #         print(x['ref'])
    else:
        print("Relation not found.")