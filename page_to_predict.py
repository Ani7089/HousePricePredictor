import streamlit as st
import numpy as np
import pandas as pd
import pickle
import sklearn

import category_encoders as ce


st.set_page_config(page_title="Price Predictor")


with open('E:\HousePricePredictor\df.pkl','rb') as file:
    df = pickle.load(file)

with open('E:\HousePricePredictor\model.pkl','rb') as file:
    pipeline = pickle.load(file)


st.header('Enter your inputs')


# property_type
property_type = st.selectbox('Property Type',sorted(df['PROPERTY_TYPE'].unique().tolist()))
own = st.selectbox('owner Type', ['FreeHold','LeaseHold','Co-operative Society','Power of Attorney'])

if own == 'FreeHold':
    owner_type = 1
elif own == 'LeaseHold':
    owner_type = 2
elif own == 'Co-operative Society':
    owner_type = 3
else:
    owner_type = 4

# sector
locality = st.selectbox('location',sorted(df['LOCALITY'].unique().tolist()))

bedrooms = float(st.selectbox('Number of Bedroom',sorted(df['BEDROOM_NUM'].unique().tolist())))

fac = st.selectbox('Facing',['No Preference',"North",'South','East','West','North-East','North-West','South-East','South-West'])

if fac == 'North':
    facing = 1
elif fac == 'South':
    facing = 2
elif fac == 'East':
    facing = 3
elif fac == 'West':
    facing = 4
elif fac == 'North-East':
    facing = 5
elif fac == 'North-West':
    facing = 6
elif fac == 'South-East':
    facing = 7
elif fac == 'South-West':
    facing = 8
else :
    facing = 0

bal = st.selectbox('Balconies',['1','2','3','3+'])

if bal == '1':
    balcony = 1
elif bal == '2':
    balcony = 2
elif bal == '3':
    balcony = 3
else:
    balcony = 4

property_age = float(st.number_input('Property Age'))

built_up_area = float(st.number_input('Built Up Area'))

floor_num = float(st.number_input('How many floors'))

fur = st.selectbox('Furnishing', ['Furnished','SemiFurnished','Unfurnished'])

if fur == 'Furnished':
    furnish = 1
elif fur == 'Unfurnished':
    furnish = 2
else:
    furnish = 4


luxury = st.selectbox('Luxuries', sorted(df['LUXURY'].unique().tolist()))

sw = st.selectbox('Swimming pool', ['Yes', 'No'])
if sw == 'Yes':
    swimming = 1
else :
    swimming = 0

if property_type == 'Residential Apartment':
    floor = float(st.number_input('FLOOR_NUM'))
else :
    floor = floor_num


if st.button('Predict'):

    # form a dataframe
    data = [[property_type,owner_type, bedrooms, furnish, facing,property_age,floor_num,built_up_area,balcony,floor,bedrooms,locality,luxury,swimming,1,1,1,1,1,1]]
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