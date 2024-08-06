# # import plotly
# # import plotly.express as px
# #
# # fig = px.choropleth(locations=["Iran"], locationmode='country names')
# #
# # fig.show()
#
#
# import pandas as pd
# import matplotlib.pyplot as plt
#
# # df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
# #                    dtype={"fips": str})
# df = pd.DataFrame({
#     "fips": ["01001"],
#     "unemp": [100]
# })
#
# # Load the county boundary coordinates
# # from urllib.request import urlopen
# # import json
# # with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
# #     counties = json.load(response)
#
#
# import plotly.express as px
#
# mashhad = {'type': 'FeatureCollection',
#            'features': [
#                 {'type': 'Feature', 'id': '5725142', 'properties':
#                 {'name': 'شهر مشهد', 'amenity': 100}, 'geometry':
#                 {'type': 'Polygon', 'coordinates':
#                     [[[[36.39, 59.68], [36.39, 59.68], [36.39, 59.68], [6.39, 59.68],
#                        [36.39, 59.68], [36.39, 59.68], [36.39, 59.68], [36.39, 59.68],
#                        [36.39, 59.68], [36.39, 59.67], [36.39, 59.67], [36.39, 59.67],
#                        [36.39, 59.67], [36.40, 59.68], [36.40, 59.67], [36.40, 59.68],
#                        [36.40, 59.68], [36.40, 59.68], [36.40, 59.68], [36.40, 59.68],
#                        [36.40, 59.68], [36.40, 59.67], [36.40, 59.67], [36.40, 59.67],
#                        [36.40, 59.67], [36.40, 59.67], [36.40, 59.67]]]]}}]}
#
#
# fig = px.choropleth(df,
#                     geojson=mashhad,
#                     locations='fips',
#                     color='unemp',
#                     color_continuous_scale="Viridis",
#                     range_color=(0, 12),
#                     scope="asia",
#                     labels={'unemp': 'unemployment rate'}
#                     )
# fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
#
# # Improve the legend
# fig.update_layout(coloraxis_colorbar=dict(
#     thicknessmode="pixels", thickness=10,
#     lenmode="pixels", len=150,
#     yanchor="top", y=0.8,
#     ticks="outside", ticksuffix=" %",
#     dtick=5
# ))
#
# fig.show()





# import pandas as pd
# import ast
# import matplotlib.pyplot as plt
# import folium
#
# # دیتاست را بارگیری کنید (من فرض می‌کنم دیتاست در یک فایل CSV به نام 'data.csv' ذخیره شده است)
# data = pd.read_csv('results.csv')
#
# # تبدیل رشته‌های مختصات به لیست
# data['coordinates'] = data['coordinates'].apply(lambda x: ast.literal_eval(x))
#
# # رسم نقشه با استفاده از folium
# m = folium.Map(location=[36.3, 59.5], zoom_start=11)
#
# # تعیین رنگ بر اساس درصد و رسم نقاط بر روی نقشه
# for index, row in data.iterrows():
#     percentage = row['percentage']
#     coordinates = row['coordinates']
#     try:
#         lat, lon = coordinates[0]['lat'], coordinates[0]['lon']
#         color = 'green' if percentage >= 80 else 'red' if percentage >= 60 else 'blue'
#         folium.CircleMarker(location=[lat, lon], radius=5, color=color, fill=True).add_to(m)
#     except:
#         pass
#
# # ذخیره نقشه به فایل HTML
# m.save('map.html')
#
# # نمایش نقشه با matplotlib
# plt.imshow(plt.imread('map.html'))
# plt.axis('off')
# plt.show()








import pandas as pd
import ast
import matplotlib.pyplot as plt
import folium

# دیتاست را بارگیری کنید (من فرض می‌کنم دیتاست در یک فایل CSV به نام 'data.csv' ذخیره شده است)
data = pd.read_csv('results-mashhad.csv')

# تبدیل رشته‌های مختصات به لیست
data['coordinates'] = data['coordinates'].apply(lambda x: ast.literal_eval(x))

# ایجاد نقشه با استفاده از folium
m = folium.Map(location=[36.3, 59.5], zoom_start=11)

# تعیین رنگ بر اساس درصد و ایجاد چند ضلعی‌ها بر روی نقشه
for index, row in data.iterrows():
    # print(index, row)
    try:
        percentage = row['percentage']
        coordinates = [(coord['lat'], coord['lon']) for coord in row['coordinates']]
        print(percentage, coordinates)
        color = 'green' if percentage >= 80 else 'blue' if percentage >= 60 else 'yellow' if percentage >= 40 else 'red'
        print(color, coordinates)

        folium.Polygon(locations=coordinates, color=color, fill=True, fill_opacity=0.5).add_to(m)
    except:
        pass

# ذخیره نقشه به فایل HTML
m.save('map_with_polygons1.html')

# Save the map as a PNG image directly
image_path = 'map_with_polygons.png'
m.save(outfile=image_path)