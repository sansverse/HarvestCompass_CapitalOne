import pandas as pd
import numpy as np
import requests
import math
import pickle # To save/load the trained model

# Assuming df_pincodes_selected, model, and df_crop_profit are loaded and available
# You might need to save these objects and load them in your Streamlit app
# Example:
# df_pincodes_selected = pd.read_csv('df_pincodes_selected.csv')
# with open('random_forest_model.pkl', 'rb') as f:
#     model = pickle.load(f)
# df_crop_profit = pd.read_csv('crop_cost_profit_dataset.csv')


def get_lat_lon_from_pincode(pincode, df):
    """
    Retrieves latitude and longitude for a given pincode from a DataFrame.

    Args:
        pincode: The pincode to look up.
        df: The DataFrame containing pincode, latitude, and longitude information.

    Returns:
        A tuple containing (latitude, longitude) if the pincode is found,
        otherwise (None, None).
    """
    result = df[df['pincode'] == pincode]
    if not result.empty:
        latitude = result['latitude'].iloc[0]
        longitude = result['longitude'].iloc[0]
        return (latitude, longitude)
    else:
        return (None, None)

def get_weather_data(latitude, longitude):
    """
    Retrieves historical weather data from the Open-Meteo API.

    Args:
        latitude: The latitude of the location.
        longitude: The longitude of the location.

    Returns:
        A dictionary containing the JSON response from the API, or None if an error occurs.
    """
    base_url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": "2023-01-01", # Using 2023 for annual data
        "end_date": "2023-12-31",
        "daily": ["temperature_2m_mean", "relative_humidity_2m_mean", "precipitation_sum"]
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def process_weather_response(response):
    """
    Processes the Open-Meteo API response to calculate annual weather metrics.

    Args:
        response: A dictionary containing the API response.

    Returns:
        A tuple containing (annual_avg_temperature, annual_avg_humidity, total_annual_rainfall),
        or (None, None, None) if the response is invalid or data is missing.
    """
    if not response or 'daily' not in response:
        return (None, None, None)

    daily_data = response['daily']

    temperature_data = daily_data.get('temperature_2m_mean')
    humidity_data = daily_data.get('relative_humidity_2m_mean')
    precipitation_data = daily_data.get('precipitation_sum')

    if not temperature_data or not humidity_data or not precipitation_data:
        return (None, None, None)

    annual_avg_temperature = np.mean(temperature_data)
    annual_avg_humidity = np.mean(humidity_data)
    total_annual_rainfall = np.sum(precipitation_data)

    return (annual_avg_temperature, annual_avg_humidity, total_annual_rainfall)

def get_estimated_profit_and_loan(pincode, land_area, df_pincodes_selected, model, df_crop_profit):
    """
    Retrieves weather data, predicts top crops, estimates profit and loan for a pincode and land area.

    Args:
        pincode: The pincode for which to retrieve data.
        land_area: The land area in hectares.
        df_pincodes_selected: DataFrame with pincode, lat, lon.
        model: Trained machine learning model.
        df_crop_profit: DataFrame with crop profit data.

    Returns:
        A dictionary containing the results (weather data, top crops, ratio, profit, loan),
        or None if there's an error.
    """
    results = {}

    # 1. Get latitude and longitude from pincode
    latitude, longitude = get_lat_lon_from_pincode(pincode, df_pincodes_selected)
    if latitude is None or longitude is None:
        return {"error": f"Pincode {pincode} not found in the dataset."}

    # 2. Call the get_weather_data function
    weather_data = get_weather_data(latitude, longitude)
    if weather_data is None:
        return {"error": f"Could not retrieve weather data for pincode {pincode}."}

    # 3. Process the weather response
    annual_avg_temperature, annual_avg_humidity, total_annual_rainfall = process_weather_response(weather_data)
    if annual_avg_temperature is None or annual_avg_humidity is None or total_annual_rainfall is None:
        return {"error": f"Could not process weather data for pincode {pincode}."}

    results["weather"] = {
        "temperature": annual_avg_temperature,
        "humidity": annual_avg_humidity,
        "rainfall": total_annual_rainfall
    }

    # 4. Create a DataFrame for model prediction
    weather_input_df = pd.DataFrame({
        'temperature': [annual_avg_temperature],
        'humidity': [annual_avg_humidity],
        'rainfall': [total_annual_rainfall]
    })

    # 5. Get prediction probabilities
    predictions_proba = model.predict_proba(weather_input_df)[0]

    # 6. Get the top two predicted commodities
    top_two_indices = predictions_proba.argsort()[-2:][::-1]
    top_two_commodities = [(model.classes_[i], predictions_proba[i]) for i in top_two_indices]
    results["top_crops"] = top_two_commodities

    # 7. Calculate and display the simplified ratio
    simplified_ratio_num = 1
    simplified_ratio_den = 0
    ratio_display = ""
    if len(top_two_commodities) >= 2:
        commodity1, prob1 = top_two_commodities[0]
        commodity2, prob2 = top_two_commodities[1]

        if prob2 > 0:
            prob1_int = int(prob1 * 1000)
            prob2_int = int(prob2 * 1000)
            gcd_val = math.gcd(prob1_int, prob2_int)
            simplified_ratio_num = prob1_int // gcd_val
            simplified_ratio_den = prob2_int // gcd_val
            ratio_display = f"{simplified_ratio_num}:{simplified_ratio_den}"
        else:
            ratio_display = f"{top_two_commodities[0][0]} (single recommendation)"
            simplified_ratio_num = 1
            simplified_ratio_den = 0 # Only one commodity predicted
    elif len(top_two_commodities) == 1:
         ratio_display = f"{top_two_commodities[0][0]} (single recommendation)"
         simplified_ratio_num = 1
         simplified_ratio_den = 0 # Only one commodity predicted
    else:
        ratio_display = "No clear recommendation"


    results["crop_ratio"] = ratio_display

    # 8. Calculate estimated profit and loan
    estimated_total_profit = 0
    estimated_total_cost_of_production = 0
    total_ratio_parts = simplified_ratio_num + simplified_ratio_den

    if land_area > 0:
        for i, (commodity, _) in enumerate(top_two_commodities):
            profit_cost_row = df_crop_profit[df_crop_profit['Crop'].str.lower() == commodity.lower()]
            if not profit_cost_row.empty:
                profit_per_hectare = profit_cost_row['Profit_per_Hectare (₹)'].iloc[0]
                cost_per_hectare = profit_cost_row['Cost_of_Production_per_Hectare (₹)'].iloc[0]

                if len(top_two_commodities) >= 2 and total_ratio_parts > 0:
                    if i == 0: # First commodity
                        allocated_land = (simplified_ratio_num / total_ratio_parts) * land_area
                    else: # Second commodity
                         allocated_land = (simplified_ratio_den / total_ratio_parts) * land_area
                else: # Only one commodity or ratio is invalid
                     allocated_land = land_area

                estimated_profit_commodity = allocated_land * profit_per_hectare
                estimated_cost_commodity = allocated_land * cost_per_hectare

                estimated_total_profit += estimated_profit_commodity
                estimated_total_cost_of_production += estimated_cost_commodity

            else:
                print(f"Warning: Profit/Cost data not found for {commodity}.") # For debugging in Colab

        results["estimated_profit"] = estimated_total_profit
        results["estimated_cost_of_production"] = estimated_total_cost_of_production

        # 9. Estimate potential loan amount (e.g., 80% of estimated cost of production)
        loan_percentage = 0.80
        estimated_loan_amount = estimated_total_cost_of_production * loan_percentage
        results["estimated_loan_amount"] = estimated_loan_amount

    else:
        results["estimation_message"] = "Please enter a valid land area to estimate profit and loan amount."

    return results

# Example usage (for testing the function in Colab)
# Assuming df_pincodes_selected, model, and df_crop_profit are loaded
# sample_pincode = 495661
# sample_land_area = 10 # Hectares
# analysis_results = get_estimated_profit_and_loan(sample_pincode, sample_land_area, df_pincodes_selected, model, df_crop_profit)
# print("\n--- Analysis Results ---")
# if "error" in analysis_results:
#     print(analysis_results["error"])
# else:
#     print(f"Weather Data: {analysis_results.get('weather')}")
#     print(f"Top Crops: {analysis_results.get('top_crops')}")
#     print(f"Crop Ratio: {analysis_results.get('crop_ratio')}")
#     print(f"Estimated Cost of Production: ₹{analysis_results.get('estimated_cost_of_production', 0):,.2f}")
#     print(f"Estimated Total Profit: ₹{analysis_results.get('estimated_profit', 0):,.2f}")
#     print(f"Estimated Loan Amount: ₹{analysis_results.get('estimated_loan_amount', 0):,.2f}")
#     if "estimation_message" in analysis_results:
#         print(analysis_results["estimation_message"])