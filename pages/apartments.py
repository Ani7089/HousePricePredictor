import numpy as np
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

df = pd.read_csv('E:/HousePricePredictor/Dataset/appartments.csv').drop(22)

def extract_list(s):
    return re.findall(r"'(.*?)'", s)

df['TopFacilities'] = df['TopFacilities'].apply(extract_list)

df['FacilitiesStr'] = df['TopFacilities'].apply(' '.join)

tfidf_vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))

tfidf_matrix = tfidf_vectorizer.fit_transform(df['FacilitiesStr'])

cosine_sim1 = cosine_similarity(tfidf_matrix, tfidf_matrix)

def recommend_properties(property_name, cosine_sim=cosine_sim1):
    # Get the index of the property that matches the name
    idx = df.index[df['PropertyName'] == property_name].tolist()[0]

    # Get the pairwise similarity scores with that property
    sim_scores = list(enumerate(cosine_sim1[idx]))

    # Sort the properties based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar properties
    sim_scores = sim_scores[1:6]

    # Get the property indices
    property_indices = [i[0] for i in sim_scores]

    recommendations_df = pd.DataFrame({
        'PropertyName': df['PropertyName'].iloc[property_indices],
        'SimilarityScore': sim_scores
    })

    # Return the top 10 most similar properties
    return recommendations_df

recommend_properties("DLF The Arbour")

import pandas as pd
import json

# Load the dataset
df_appartments = pd.read_csv('E:/HousePricePredictor/Dataset/appartments.csv').drop(22)

# Function to parse and extract the required features from the PriceDetails column
def refined_parse_modified_v2(detail_str):
    try:
        details = json.loads(detail_str.replace("'", "\""))
    except:
        return {}

    extracted = {}
    for bhk, detail in details.items():
        # Extract building type
        extracted[f'building type_{bhk}'] = detail.get('building_type')

        # Parsing area details
        area = detail.get('area', '')
        area_parts = area.split('-')
        if len(area_parts) == 1:
            try:
                value = float(area_parts[0].replace(',', '').replace(' sq.ft.', '').strip())
                extracted[f'area low {bhk}'] = value
                extracted[f'area high {bhk}'] = value
            except:
                extracted[f'area low {bhk}'] = None
                extracted[f'area high {bhk}'] = None
        elif len(area_parts) == 2:
            try:
                extracted[f'area low {bhk}'] = float(area_parts[0].replace(',', '').replace(' sq.ft.', '').strip())
                extracted[f'area high {bhk}'] = float(area_parts[1].replace(',', '').replace(' sq.ft.', '').strip())
            except:
                extracted[f'area low {bhk}'] = None
                extracted[f'area high {bhk}'] = None

        # Parsing price details
        price_range = detail.get('price-range', '')
        price_parts = price_range.split('-')
        if len(price_parts) == 2:
            try:
                extracted[f'price low {bhk}'] = float(price_parts[0].replace('₹', '').replace(' Cr', '').replace(' L', '').strip())
                extracted[f'price high {bhk}'] = float(price_parts[1].replace('₹', '').replace(' Cr', '').replace(' L', '').strip())
                if 'L' in price_parts[0]:
                    extracted[f'price low {bhk}'] /= 100
                if 'L' in price_parts[1]:
                    extracted[f'price high {bhk}'] /= 100
            except:
                extracted[f'price low {bhk}'] = None
                extracted[f'price high {bhk}'] = None

    return extracted
# Apply the refined parsing and generate the new DataFrame structure
data_refined = []

for _, row in df_appartments.iterrows():
    features = refined_parse_modified_v2(row['PriceDetails'])

    # Construct a new row for the transformed dataframe
    new_row = {'PropertyName': row['PropertyName']}

    # Populate the new row with extracted features
    for config in ['1 BHK', '2 BHK', '3 BHK', '4 BHK', '5 BHK', '6 BHK', '1 RK', 'Land']:
        new_row[f'building type_{config}'] = features.get(f'building type_{config}')
        new_row[f'area low {config}'] = features.get(f'area low {config}')
        new_row[f'area high {config}'] = features.get(f'area high {config}')
        new_row[f'price low {config}'] = features.get(f'price low {config}')
        new_row[f'price high {config}'] = features.get(f'price high {config}')

    data_refined.append(new_row)

df_final_refined_v2 = pd.DataFrame(data_refined).set_index('PropertyName')

df_final_refined_v2['building type_Land'] = df_final_refined_v2['building type_Land'].replace({'':'Land'})

categorical_columns = df_final_refined_v2.select_dtypes(include=['object']).columns.tolist()

ohe_df = pd.get_dummies(df_final_refined_v2, columns=categorical_columns, drop_first=True)

ohe_df.fillna(0,inplace=True)

from sklearn.preprocessing import StandardScaler

# Initialize the scaler
scaler = StandardScaler()

# Apply the scaler to the entire dataframe
ohe_df_normalized = pd.DataFrame(scaler.fit_transform(ohe_df), columns=ohe_df.columns, index=ohe_df.index)

ohe_df_normalized.head()

from sklearn.metrics.pairwise import cosine_similarity

# Compute the cosine similarity matrix
cosine_sim2 = cosine_similarity(ohe_df_normalized)

def recommend_properties_with_scores(property_name, top_n=247):

    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim2[ohe_df_normalized.index.get_loc(property_name)]))

    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n+1]]

    # Retrieve the names of the top properties using the indices
    top_properties = ohe_df_normalized.index[top_indices].tolist()

    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })

    return recommendations_df

# Test the recommender function using a property name
recommend_properties_with_scores('M3M Golf Hills')

def distance_to_meters(distance_str):
    try:
        if 'Km' in distance_str or 'KM' in distance_str:
            return float(distance_str.split()[0]) * 1000
        elif 'Meter' in distance_str or 'meter' in distance_str:
            return float(distance_str.split()[0])
        else:
            return None
    except:
        return None

# Extract distances for each location
import ast
location_matrix = {}
for index, row in df.iterrows():
    distances = {}
    for location, distance in ast.literal_eval(row['LocationAdvantages']).items():
        distances[location] = distance_to_meters(distance)
    location_matrix[index] = distances

# Convert the dictionary to a dataframe
location_df = pd.DataFrame.from_dict(location_matrix, orient='index')

# Display the first few rows
location_df.index = df.PropertyName

location_df.fillna(54000,inplace=True)

from sklearn.preprocessing import StandardScaler
# Initialize the scaler
scaler = StandardScaler()

# Apply the scaler to the entire dataframe
location_df_normalized = pd.DataFrame(scaler.fit_transform(location_df), columns=location_df.columns, index=location_df.index)

cosine_sim3 = cosine_similarity(location_df_normalized)

def recommend_properties_with_scores(property_name, top_n=247):

    cosine_sim_matrix = 30*cosine_sim1 + 20*cosine_sim2 + 8*cosine_sim3
    # cosine_sim_matrix = cosine_sim3

    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df_normalized.index.get_loc(property_name)]))

    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n+1]]

    # Retrieve the names of the top properties using the indices
    top_properties = location_df_normalized.index[top_indices].tolist()

    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })

    return recommendations_df

# Test the recommender function using a property name
recommend_properties_with_scores('Ireo Victory Valley')

st.title('Select Location and Radius')

selected_location = st.selectbox('Location',sorted(location_df.columns.to_list()))

radius = st.number_input('Radius in Kms')

if st.button('Search'):
    result_ser = location_df[location_df[selected_location] < radius*1000][selected_location].sort_values()

    for key, value in result_ser.items():
        st.text(str(key) + " " + str(round(value/1000)) + ' kms')

st.title('Recommend Appartments')
selected_appartment = st.selectbox('Select an appartment',sorted(location_df.index.to_list()))

if st.button('Recommend'):
    recommendation_df = recommend_properties_with_scores(selected_appartment)

    st.dataframe(recommendation_df)

