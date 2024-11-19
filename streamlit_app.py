import streamlit as st
import pandas as pd
import requests

# Title of the app
st.title("Network Security Model Prediction")

# File uploader for CSV file
uploaded_file = st.file_uploader("Upload a CSV file for prediction", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)

    # Display the dataframe
    st.write("Data Preview:")
    st.dataframe(df)

    # Button to trigger prediction
    if st.button("Predict"):
        # Convert the DataFrame to JSON format for the API request
        json_data = df.to_json(orient="records")

        # Make a POST request to the prediction endpoint
        response = requests.post(
            "http://localhost:8000/predict", files={"file": uploaded_file}
        )

        if response.status_code == 200:
            # Get the predictions from the response
            predictions = response.json()
            st.write("Predictions:")
            st.dataframe(predictions)
        else:
            st.error("Error in prediction: " + response.text)

# Instructions for the user
st.write("Please upload a CSV file containing the features for prediction.")
