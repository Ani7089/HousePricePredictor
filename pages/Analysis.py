import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import squarify


st.set_page_config(page_title="Analysis side")

st.title('Analytics')

new_df = pd.read_csv('E:\HousePricePredictor\Dataset\99Acres_gurgaon_hyderabad_Secunderabad_SelectedFeatures_with_fewChange.csv')
with open('E:\HousePricePredictor\df.pkl','rb') as file:
    feature_text = pickle.load(file)


group_df = new_df.groupby('LOCALITY').mean(numeric_only=True)[['PRICE','PRICE_SQFT','AREA','LATITUDE','LONGITUDE']]

st.header('Sector Price per Sqft Geomap')

dense_area = group_df[group_df['PRICE_SQFT'] > group_df['PRICE_SQFT'].quantile(0.75)]  # Adjust the condition as needed
center_lat = dense_area['LATITUDE'].mean()
center_lon = dense_area['LONGITUDE'].mean()

fig = px.scatter_mapbox(group_df, lat="LATITUDE", lon="LONGITUDE", color="PRICE_SQFT", size='AREA',
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10,
                  mapbox_style="open-street-map", width=1200, height=700, hover_name=group_df.index,
                  center=dict(lat=center_lat, lon=center_lon))

st.plotly_chart(fig, use_container_width=True)

st.header('Features Wordcloud')

wordcloud = WordCloud(width = 800, height = 800,
                      background_color ='black',
                      stopwords = set(['s']),  # Any stopwords you'd like to exclude
                      min_font_size = 10).generate(str(feature_text))

fig = plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad = 0)
st.pyplot(fig)

st.header('Area Vs Price')

property_type = st.selectbox('Select Property Type', new_df['PROPERTY_TYPE'].unique().tolist())

fig1 = px.scatter(new_df[new_df['PROPERTY_TYPE'] == property_type], x="AREA", y="PRICE", color="BEDROOM_NUM", title="Area Vs Price")
st.plotly_chart(fig1, use_container_width=True)

st.header('BHK Pie Chart')

sector_options = new_df['LOCALITY'].unique().tolist()
sector_options.insert(0,'overall')

selected_sector = st.selectbox('Select Sector', sector_options)

if selected_sector == 'overall':

    fig2 = px.pie(new_df, names='BEDROOM_NUM')

    st.plotly_chart(fig2, use_container_width=True)
else:

    fig2 = px.pie(new_df[new_df['LOCALITY'] == selected_sector], names='BEDROOM_NUM')

    st.plotly_chart(fig2, use_container_width=True)

st.header('Side by Side BHK price comparison')

fig3 = px.box(new_df[new_df['BEDROOM_NUM'] <= 4], x='BEDROOM_NUM', y='PRICE', title='BHK Price Range')

st.plotly_chart(fig3, use_container_width=True)


st.header('Side by Side Distplot for property type')

fig3 = plt.figure(figsize=(10, 4))
sns.distplot(new_df[new_df['PROPERTY_TYPE'] == 'Residential Apartment']['PRICE'],label='Residential Apartment')
sns.distplot(new_df[new_df['PROPERTY_TYPE'] == 'Independent/Builder Floor']['PRICE'], label='Independent builder')
sns.distplot(new_df[new_df['PROPERTY_TYPE'] == 'Independent House/Villa']['PRICE'], label='Independent villa')
plt.legend()
st.pyplot(fig3)

st.header('')
st.header('Most present Featues in an house')

features = ['SWIMMING_POOL', 'POWER_BACKUP', 'CLUB_HOUSE', 'GYM', 'WASTE_DISPOSAL', 'GAS_PIPELINE']
counts = [new_df[feature].count() for feature in features]
df = pd.DataFrame({'Feature': features, 'Count': counts})
sizes = df['Count'] / df['Count'].sum()
fig, ax = plt.subplots(figsize=(10, 6))
squarify.plot(sizes=sizes, label=df['Feature'], alpha=0.6, ax=ax)
ax.axis('off')
plt.show()

st.pyplot(fig)