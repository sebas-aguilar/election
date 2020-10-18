import pandas as pd
import numpy as np

# keepCols = ['year','state','state_po','candidate','party','writein','candidatevotes','totalvotes']
df = pd.read_csv('data\\1976-2016-president.csv')#,usecols = keepCols)


years = df["year"].drop_duplicates().to_numpy()
print(years)


df_2016 = df.query('year == 2016')


candidates = df_2016['candidate'].drop_duplicates().to_numpy()
print(candidates)


votes = df_2016[['candidate','candidatevotes']].groupby(by='candidate').sum()
sorted_votes = votes.sort_values(by='candidatevotes', ascending=False)
total_votes = sorted_votes.sum()[0]
vote_percentage = sorted_votes['candidatevotes'].to_numpy() / total_votes * 100

sorted_votes = sorted_votes.assign(percentage=pd.Series(vote_percentage,index=sorted_votes.index).values)
print(sorted_votes)


sorted_votes[:5].plot(y='percentage', kind='bar', title='2016 - Top 5 candidates', figsize=(15,10), 
                      rot=75, xlabel='Candidate names', ylabel='Percentage of the vote')


parties = df_2016[['party','candidatevotes']].groupby(by='party').sum()
parties_sorted = parties.sort_values(by='candidatevotes', ascending=False)
print(parties_sorted)


lib = df_2016.query("party == 'libertarian'")
green =  df_2016.query("party == 'green'")

import plotly.express as px

lib_fig = px.choropleth(lib,
                    title='Libertarian Party Vote Distribution',
                    locations ="state_po", 
                    color ="candidatevotes", 
                    scope ="usa",
                    locationmode="USA-states",
                    color_continuous_scale="Greys",
                    labels={"candidatevotes":"Party Votes"}
                    )
lib_fig.update_geos(showlakes=True, showrivers=True, rivercolor='lightblue', resolution=110)
lib_fig.update_layout(title_x=0.45)
lib_fig.show()

green_fig = px.choropleth(green,
                    title='Green Party Vote Distribution',
                    locations ="state_po", 
                    color ="candidatevotes", 
                    scope ="usa",
                    locationmode="USA-states",
                    color_continuous_scale="Greens",
                    labels={"candidatevotes":"Party Votes"}
                    )
green_fig.update_layout(title_x=0.45)
green_fig.update_geos(showlakes=True, showrivers=True, rivercolor='lightblue', resolution=110)
green_fig.show()


rep = df_2016.query("party == 'republican'")
dem =  df_2016.query("party == 'democrat'")

import plotly.express as px

rep_fig = px.choropleth(rep,
                    title='Republican Party Vote Distribution',
                    locations ="state_po", 
                    color ="candidatevotes", 
                    scope ="usa",
                    locationmode="USA-states",
                    color_continuous_scale="Reds",
                    labels={"candidatevotes":"Party Votes"}
                    )
rep_fig.update_geos(showlakes=True, resolution=110)#,showrivers=True, rivercolor='blue', resolution=110)
rep_fig.update_layout(title_x=0.45)
rep_fig.show()

dem_fig = px.choropleth(dem,
                    title='Democrat Party Vote Distribution',
                    locations ="state_po", 
                    color ="candidatevotes", 
                    scope ="usa",
                    locationmode="USA-states",
                    color_continuous_scale="Blues",
                    labels={"candidatevotes":"Party Votes"}
                    )
dem_fig.update_layout(title_x=0.45)
dem_fig.update_geos(showlakes=True, resolution=110)#,showrivers=True, rivercolor='blue', resolution=110)
dem_fig.show()


rep = df_2016.query("party == 'republican'")
dem =  df_2016.query("party == 'democrat'")

# # Redundant, already exists column 'totalvotes'
# total_votes_by_state = df_2016[['candidatevotes','state']].groupby(by='state').sum()
# total_votes_by_state.rename(columns = {'candidatevotes':'total_votes_in_state'}, inplace = True)
# rep_adj = pd.merge(rep, total_votes_by_state, how='outer', on=['state'])

rep_adj = rep.assign(votesnormalized = 100*rep['candidatevotes']/rep['totalvotes'])
dem_adj = dem.assign(votesnormalized = 100*dem['candidatevotes']/dem['totalvotes'])

import plotly.express as px

rep_adj_fig = px.choropleth(rep_adj,
                    title='2016 - Republican Party Control',
                    locations ="state_po", 
                    color ="votesnormalized", 
                    scope ="usa",
                    locationmode="USA-states",
                    color_continuous_scale="Reds",
                    range_color=(0, 100),
                    labels={"votesnormalized":"Party Control"},
                    height=800, width=800
                    )
rep_adj_fig.update_geos(showlakes=True, resolution=110)#,showrivers=True, rivercolor='blue', resolution=110)
rep_adj_fig.update_layout(title_x=0.45)
rep_adj_fig.show()

dem_adj_fig = px.choropleth(dem_adj,
                    title='2016 - Democrat Party Control',
                    locations ="state_po", 
                    color ="votesnormalized", 
                    scope ="usa",
                    locationmode="USA-states",
                    color_continuous_scale="Blues",
                    range_color=(0, 100),
                    labels={"votesnormalized":"Party Control"},
                    height=800, width=800
                    )
dem_adj_fig.update_layout(title_x=0.45)
dem_adj_fig.update_geos(showlakes=True, resolution=110)#,showrivers=True, rivercolor='blue', resolution=110)
dem_adj_fig.show()


rep = df.query("party == 'republican'")
dem = df.query("party == 'democrat' or party == 'democratic-farmer-labor'")

# # Redundant, already exists column 'totalvotes'
# total_votes_by_state = df_2016[['candidatevotes','state']].groupby(by='state').sum()
# total_votes_by_state.rename(columns = {'candidatevotes':'total_votes_in_state'}, inplace = True)
# rep_adj = pd.merge(rep, total_votes_by_state, how='outer', on=['state'])

rep_adj = rep.assign(votesnormalized = 100*rep['candidatevotes']/rep['totalvotes'])
dem_adj = dem.assign(votesnormalized = 100*dem['candidatevotes']/dem['totalvotes'])

from plotly.subplots import make_subplots
import plotly.express as px

rep_adj_fig = px.choropleth(rep_adj,
                    title='Republican Party Control (1976-2016)',
                    locations ="state_po", 
                    color ="votesnormalized", 
                    scope ="usa",
                    animation_frame='year',
                    locationmode="USA-states",
                    color_continuous_scale="Reds",
                    range_color=(0, 100),
                    labels={"votesnormalized":"Party Control"},
                    height=800, width=800
                    )
rep_adj_fig.update_geos(showlakes=True, resolution=110)#,showrivers=True, rivercolor='blue', resolution=110)
rep_adj_fig.update_layout(title_x=0.45)
rep_adj_fig.write_html("images/rep_adj_fig.html")
rep_adj_fig.show()

dem_adj_fig = px.choropleth(dem_adj,
                    title='Democrat Party Control (1976-2016)',
                    locations ="state_po", 
                    color ="votesnormalized", 
                    scope ="usa",
                    animation_frame='year',
                    locationmode="USA-states",
                    color_continuous_scale="Blues",
                    range_color=(0, 100),
                    labels={"votesnormalized":"Party Control"},
                    height=800, width=800
                    )
dem_adj_fig.update_geos(showlakes=True, resolution=110)#,showrivers=True, rivercolor='blue', resolution=110)
dem_adj_fig.update_layout(title_x=0.45)
dem_adj_fig.write_html("images/dem_adj_fig_fig.html")
dem_adj_fig.show()


# # Feature not yet implemented to facet px.chloropleth plots
# fig = make_subplots(rows=1, cols=2, specs=[[{'type':'choropleth'},{'type':'choropleth'}]])
# fig.add_trace(rep_adj_fig.data[0], row=1, col=1)
# fig.add_trace(dem_adj_fig.data[0], row=1, col=2)
# fig.update_geos(scope ="usa", showlakes=True, showrivers=True, rivercolor='blue', resolution=110)
# fig.update_layout(title_x=0.45)
# fig.update_traces(showscale=False)
# fig.show()


r_vs_d_vs_i = df.query("party == 'democrat' or party == 'democratic-farmer-labor' or party == 'republican' or party == 'independent'")

# Replace value1 with value2
mask = r_vs_d_vs_i['party'] == 'democratic-farmer-labor'
r_vs_d_vs_i.loc[mask,'party'] = 'democrat'

# Assign new winner column, will update to correct value
r_vs_d_vs_i = r_vs_d_vs_i.assign(winner=r_vs_d_vs_i['party'])



grouped = r_vs_d_vs_i[['year','state','candidatevotes','party','winner']].groupby(by=['year','state'])

for group in grouped:
    sub_df = group[1]
    majority = sub_df['candidatevotes'].max()
    index = sub_df.query('candidatevotes == @majority').index.tolist()

    mask = sub_df['party'].index.tolist()
    r_vs_d_vs_i.loc[mask,['winner']] = sub_df['party'][index].values[0]



# Generate plot
winners_fig = px.choropleth(r_vs_d_vs_i,
                    title='Electoral Landscape (1976-2016)',
                    locations ="state_po", 
                    color ="winner", 
                    scope ="usa",
                    animation_frame='year',
                    animation_group='party',
                    locationmode="USA-states",
                    color_discrete_map={"democrat":"blue","republican":"red","independent":"black"},
                    labels={"winner":"Party"},
                    height=900, width=1200
                    )
winners_fig.update_geos(showlakes=True, resolution=110)#,showrivers=True, rivercolor='blue', resolution=110)
winners_fig.update_layout(title_x=0.45)
winners_fig.write_image("images/winners_fig.png")
winners_fig.write_html("images/winners_fig.html")
winners_fig.show()
