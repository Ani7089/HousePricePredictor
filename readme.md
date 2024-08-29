# House Price Prediction Project

## Overview

This project focuses on predicting house prices using data scraped from 99acres.com. The goal is to build a predictive model that can accurately estimate house prices based on various features. The project involves data scraping, data cleaning, exploratory data analysis (EDA), feature selection, and model building using the Random Forest algorithm.

## Features

- **Data Collection**: Web scraping of house listing data from 99acres.com, including features like location, size, number of rooms, amenities, and price.
- **Data Cleaning**: Handling missing values, correcting data types, and filtering outliers to prepare the dataset for analysis.
- **Exploratory Data Analysis (EDA)**: Analyzing the dataset to understand the distribution of variables, relationships between features, and key insights.
- **Feature Selection**: Identifying and selecting the most relevant features for predicting house prices.
- **Model Building**: Developing a house price prediction model using the Random Forest algorithm.

## Dataset

### Data Collection

- **Source**: The dataset was created by scraping data from [99acres.com](https://www.99acres.com), a real estate platform that lists properties for sale and rent.
- **Content**: The dataset includes various features such as:
  - `location`: The location of the property.
  - `size`: The size of the property (in square feet).
  - `bedrooms`: Number of bedrooms.
  - `bathrooms`: Number of bathrooms.
  - `price`: The price of the property.
  - `amenities`: Additional features such as parking, security, etc.
  
### Data Cleaning

- **Process**: 
  - Handling missing values by imputing or removing incomplete entries.
  - Correcting data types (e.g., converting price and size to numerical formats).
  - Filtering out outliers that could skew the analysis and model performance.

## Exploratory Data Analysis (EDA)

- **Techniques Used**:
  - **Descriptive Statistics**: Summarizing the central tendency, dispersion, and shape of the dataset’s distribution.
  - **Visualizations**: Creating histograms, box plots, scatter plots, and correlation matrices to understand relationships between features.
  - **Insights**: Identifying trends, patterns, and anomalies in the dataset that could influence model performance.

## Feature Selection

- **Process**:
  - **Correlation Analysis**: Selecting features with high correlation with the target variable (price) and low correlation with each other.
  - **Feature Importance**: Using techniques like Random Forest feature importance to rank and select the most impactful features.
  
## Model Building

- **Algorithm**: The house price prediction model is built using the Random Forest algorithm, chosen for its robustness and ability to handle large datasets with many features.
- **Training**: The model is trained on the cleaned and processed dataset, using selected features to predict house prices.
- **Evaluation**: The model's performance is evaluated using metrics such as Mean Absolute Error (MAE), Mean Squared Error (MSE), and R-squared.

## Installation

### Prerequisites

- Python 3.x
- Required Python libraries (listed in `requirements.txt`):
  - NumPy
  - Pandas
  - Scikit-learn
  - Matplotlib
  - Seaborn
  - BeautifulSoup (for web scraping)
  - Requests (for web scraping)

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/house-price-prediction.git
2. Navigate to the project directory:
    ```bash
    cd HousePricePrediction

3. Install the required libraries:
    ```bash
    pip install -r requirements.txt
4. Run the web scraping script to generate the dataset (optional if you already have the dataset):
    ```bash
    python web_scraping.py


### Results
The model's performance metrics (MAE, MSE, R-squared) are saved in the results directory.
Visualizations and insights from the EDA process are also saved for reference.

### Future Work
Experimenting with other machine learning algorithms such as XGBoost or Gradient Boosting for potential improvements.
Implementing hyperparameter tuning to optimize the Random Forest model.
Deploying the model as a web application or API for real-time house price predictions.
  
### Contributions
Contributions are welcome! Please feel free to submit a pull request or report issues.
