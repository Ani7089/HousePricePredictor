import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Plotting Demo")

st.title('Analytics')

new_df = pd.read_csv('E:\HousePricePredictor\Dataset\99Acres_gurgaon_hyderabad_Secunderabad_SelectedFeatures_with_fewChange.csv')
feature_text = pickle.load(open('E:\HousePricePredictor\df.pkl','rb'))


group_df = new_df.groupby('LOCALITY').mean()[['PRICE','PRICE_SQFT','AREA','LATITUDE','LONGITUDE']]

st.header('Sector Price per Sqft Geomap')
fig = px.scatter_mapbox(group_df, lat="LATITUDE", lon="LONGITUDE", color="PRICE_SQFT", size='AREA',
                  color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                  mapbox_style="open-street-map",width=1200,height=700,hover_name=group_df.index)

st.plotly_chart(fig,use_container_width=True)

st.header('Features Wordcloud')

wordcloud = WordCloud(width = 800, height = 800,
                      background_color ='black',
                      stopwords = set(['s']),  # Any stopwords you'd like to exclude
                      min_font_size = 10).generate(feature_text)

plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad = 0)
st.pyplot()

st.header('Area Vs Price')

property_type = st.selectbox('Select Property Type', new_df['PROPERTY_TYPE'].unique().tolist())


if property_type == 'Residential Apartment':
    fig1 = px.scatter(new_df[new_df['PROPERTY_TYPE'] == 'Residential Apartment'], x="AREA", y="PRICE", color="BEDROOM_NUM", title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)
elif property_type == 'Independent/Builder Floor':
    fig1 = px.scatter(new_df[new_df['PROPERTY_TYPE'] == 'Independent/Builder Floor'], x="AREA", y="PRICE", color="BEDROOM_NUM", title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)
else:
    fig1 = px.scatter(new_df[new_df['PROPERTY_TYPE'] == 'Independent House/Villa'], x="AREA", y="PRICE", color="BEDROOM_NUM", title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)

st.header('BHK Pie Chart')

sector_options = new_df['LOCALITY'].unique().tolist()
sector_options.insert(0,'overall')

selected_sector = st.selectbox('Select Sector', sector_options)

if selected_sector == 'overall':

    fig2 = px.pie(new_df, names='bedRoom')

    st.plotly_chart(fig2, use_container_width=True)
else:

    fig2 = px.pie(new_df[new_df['LOCALITY'] == selected_sector], names='bedRoom')

    st.plotly_chart(fig2, use_container_width=True)

st.header('Side by Side BHK price comparison')

fig3 = px.box(new_df[new_df['BEDROOM_NUM'] <= 4], x='bedRoom', y='price', title='BHK Price Range')

st.plotly_chart(fig3, use_container_width=True)


st.header('Side by Side Distplot for property type')

fig3 = plt.figure(figsize=(10, 4))
sns.distplot(new_df[new_df['PROPERTY_TYPE'] == 'Residential Apartment']['PRICE'],label='Residential Apartment')
sns.distplot(new_df[new_df['PROPERTY_TYPE'] == 'Independent/Builder Floor']['PRICE'], label='Independent builder')
sns.distplot(new_df[new_df['PROPERTY_TYPE'] == 'Independent House/Villa']['PRICE'], label='Independent villa')
plt.legend()
st.pyplot(fig3)