import streamlit as st
import numpy as np
import pandas as pd
import pickle
import sklearn

import category_encoders as ce


st.set_page_config(page_title="Viz Demo")


with open('data.pkl','rb') as file:
    df = pickle.load(file)

with open('model.pkl','rb') as file:
    pipeline = pickle.load(file)


st.header('Enter your inputs')


# property_type
property_type = st.selectbox('Property Type',sorted(df['PROPERTY_TYPE'].unique().tolist()))
owner_type = st.selectbox('owner Type', sorted(df['OWNTYPE'].unique().tolist()))

# sector
locality = st.selectbox('location',sorted(df['LOCALITY'].unique().tolist()))

bedrooms = float(st.selectbox('Number of Bedroom',sorted(df['BEDROOM_NUM'].unique().tolist())))

facing = float(st.selectbox('Facing',sorted(df['FACING'].unique().tolist())))

balcony = st.selectbox('Balconies',sorted(df['BALCONY_NUM'].unique().tolist()))

property_age = st.selectbox('Property Age',sorted(df['AGE'].unique().tolist()))

built_up_area = float(st.number_input('Built Up Area'))

floor_num = float(st.number_input('How many floors'))

furnish = st.selectbox('Furnishing', sorted(df['FURNISH'].unique().tolist()))

luxury = st.selectbox('Luxuries', sorted(df['LUXURY'].unique().tolist()))

swimming = st.selectbox('Swimming pool', sorted(df['SWIMMING_POOL'].unique().tolist()))

floor = float(st.number_input('Which floor'))


if st.button('Predict'):

    # form a dataframe
    data = [[property_type,Owner_type, bedrooms, furnish, facing,property_age,floor_num,built_up_area,balcony,floor,bedrooms,locality,luxury,swimming,1,1,1,1,1,1]]
    columns = ['PROPERTY_TYPE',
                'OWNTYPE',
                'BEDROOM_NUM',
                'FURNISH',
                'FACING',
                'AGE',
                'TOTAL_FLOOR',
                'AREA',
                'BALCONY_NUM',
                'FLOOR_NUM',
                'BHK',
                'LOCALITY',
                'LUXURY',
                'SWIMMING_POOL',
                'POWER_BACKUP',
                'CLUB_HOUSE',
                'ATM',
                'GYM',
                'WASTE_DISPOSAL',
                'GAS_PIPELINE']

    # Convert to DataFrame
    one_df = pd.DataFrame(data, columns=columns)

    #st.dataframe(one_df)

    # predict
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price - 0.20
    high = base_price + 0.20

    # display
    st.text("The price of the flat is between {} Cr and {} Cr".format(round(low,2),round(high,2)))