import pandas as pd
import numpy as np

keepCols = ['state_postal','state_fips','state_icpsr','county_name','county_fips','jurisdiction','precinct',
            'candidate_normalized','party','votes','winner','total_county_votes','votes_normalized']

dtypes = {"state_postal":str,
          "states_fips":np.int64,
          "state_icpsr":np.int64,
          "county_name":str,
          "county_fips":str,
          "jurisdiction":str,
          "precinct":str,          
          "candidate_normalized":str,
          "party":str,
          "votes":np.int64,
          "winner":str,
          "total_county_votes":np.int64,
          "votes_normalized":np.float64
         }

df = pd.read_csv('data\\2016-precinct-president-prepared.csv',encoding="ISO-8859-1", low_memory=False, usecols=keepCols, dtype=dtypes)
# print(df.info())


top4 = df[['candidate_normalized','votes']].groupby('candidate_normalized').sum().sort_values(by='votes', ascending=False)[:4]
trim_df = df.query('candidate_normalized in @top4.index.values')

df.drop(columns=['state_fips','state_icpsr','party'], inplace=True)

# Free up some memory from the much larger dataframe
del df

# print(trim_df.info())


import plotly.express as px
from urllib.request import urlopen
import json


# Load the geojson file (required) for plotly county plots. If it fails grab the file from internet and save it
try:
    counties = json.load("data\\geojson-counties-fips.json")
except:
    with urlopen("https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json") as response:
        counties = json.load(response)
        with open("data\\geojson-counties-fips.json","w") as json_file:
            json.dump(counties, json_file)
    
    
colors = {"clinton":"blues","trump":"reds","johnson":"greys","stein":"greens"}

for candidate in top4[:2].index.values:
    aggregate= {"state_postal":"first","state_fips":"first","state_icpsr":"first",
                "county_name":"first","candidate_normalized":"first","party":"first","votes":"sum"}
    trimmed_df = trim_df.query("candidate_normalized==@candidate").groupby(by='county_fips').agg(func=aggregate).reset_index()
    print("{} - Precinct Turnout 2016 Election".format(candidate.upper()))
    fig = px.choropleth_mapbox(trimmed_df, geojson=counties, locations="county_fips", color="votes",
                               color_continuous_scale=colors[candidate],
                               hover_name="county_name",
#                                title='@candidate.upper() - Precinct Turnout 2016 Election', # NOT WORKING
#                                mapbox_style="carto-positron",
                               mapbox_style="carto-darkmatter",
#                                mapbox_style="open-street-map",
#                                mapbox_style="stamen-toner",
#                                mapbox_style="stamen-watercolor",
                               center = {"lat": 40.0902, "lon": -95.7129}, zoom=3, 
#                                opacity=0.5,
                               labels={"votes":"Votes"}
                          )
    fig.update_geos(showrivers=True, rivercolor="Blue", resolution=50)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.write_image("images/{}_precinct_level.png".format(candidate))
    fig.write_html("images/{}_precinct_level.html".format(candidate))
    fig.show()
    print('\n')


import plotly.express as px
from urllib.request import urlopen
import json


# Load the geojson file (required) for plotly county plots. If it fails grab the file from internet and save it
try:
    counties = json.load("data\\geojson-counties-fips.json")
except:
    with urlopen("https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json") as response:
        counties = json.load(response)
        with open("data\\geojson-counties-fips.json", "w") as json_file:
            json.dump(counties, json_file)
    
    
colors = {"clinton":"blues","trump":"reds","johnson":"greys","stein":"greens"}

for candidate in top4[:2].index.values:
    aggregate= {"state_postal":"first","state_fips":"first","state_icpsr":"first","county_name":"first",
                "candidate_normalized":"first","party":"first","votes_normalized":"sum"}
    trimmed_df = trim_df.query("candidate_normalized==@candidate").groupby(by=["county_fips","jurisdiction"]).agg(func=aggregate).reset_index()
    print("{} - Precinct Turnout 2016 Election".format(candidate.upper()))
    fig = px.choropleth_mapbox(trimmed_df, geojson=counties, locations="county_fips", color="votes_normalized",
                               color_continuous_scale=colors[candidate],
                               hover_name="county_name",
#                                title='@candidate.upper() - Precinct Turnout 2016 Election', # NOT WORKING
#                                mapbox_style="carto-positron",
                               mapbox_style="carto-darkmatter",
#                                mapbox_style="open-street-map",
#                                mapbox_style="stamen-toner",
#                                mapbox_style="stamen-watercolor",
                               center = {"lat": 40.0902, "lon": -95.7129}, zoom=3, 
#                                opacity=0.5,
                               labels={"votes_normalized":"Normalized Votes"}
                          )
    fig.update_geos(showrivers=True, rivercolor="Blue", resolution=50)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.write_image("images/{}_precinct_level_normalized.png".format(candidate))
    fig.write_html("images/{}_precinct_level_normalized.html".format(candidate))
    fig.show()
    print('\n')


# import plotly.express as px
# from urllib.request import urlopen
# import json


# # Load the geojson file (required) for plotly county plots. If it fails grab the file from internet and save it
# try:
#     counties = json.load("data\\geojson-counties-fips.json")
# except:
#     with urlopen("https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json") as response:
#         counties = json.load(response)
#         with open("data\\geojson-counties-fips.json", "w") as json_file:
#             json.dump(counties, json_file)
    
    
# colors = {"clinton":"blue","trump":"red","johnson":"grey","stein":"green"}


# print("County level 2016 Election".format(candidate.upper()))
# fig = px.choropleth_mapbox(trim_df, geojson=counties, locations="county_fips", color="winner",
#                            color_discrete_map=colors,
# #                            labels={"winner":"Party"},
#                            hover_name="county_name",
# #                            title='@candidate.upper() - Precinct Turnout 2016 Election', # NOT WORKING
# #                            mapbox_style="carto-positron",
#                            mapbox_style="carto-darkmatter",
# #                            mapbox_style="open-street-map",
# #                            mapbox_style="stamen-toner",
# #                            mapbox_style="stamen-watercolor",
#                            center = {"lat": 40.0902, "lon": -95.7129}, zoom=3, 
# #                            opacity=0.5,
#                            labels={"votes_normalized":"Normalized Votes"}
#                           )
# fig.update_geos(showrivers=True, rivercolor="Blue", resolution=50)
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.write_image("images/{}_precinct_level_county_winners.png".format(candidate))
# fig.write_html("images/{}_precinct_level_county_winners.html".format(candidate))
# fig.show()


del trim_df
