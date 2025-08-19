# Harvest Compass AgriProfit & Loan Estimator 🌱

Empowering farmers to make data-driven, sustainable crop choices! 🌾💧

## Features
- Enter your pincode and land area to get:
  - Weather summary for your location
  - Top crop recommendations with suitability scores
  - Recommended crop ratio
  - Estimated cost of production, profit, and loan amount
- Simple, colorful UI with helpful icons and messages

## How to Run Locally
1. **Install requirements**
   - Make sure you have Python 3.8+ and `streamlit` installed.
   - Install dependencies:
     ```
     pip install streamlit pandas numpy requests scikit-learn
     ```
2. **Run the app**
   - Open Anaconda Prompt (or your terminal with the correct environment activated)

   - Start the app:
     ```
     streamlit run streamlit_app.py
     ```
   - Open the link shown in the terminal (e.g., http://localhost:8501)

## Share Your App
- To share with anyone on the internet, deploy on [Streamlit Community Cloud](https://streamlit.io/cloud) or use a tunneling service like [ngrok](https://ngrok.com/).
- **Do not share your local/private IP for public access.**

## Files
- `streamlit_app.py` — Main Streamlit UI
- `app_logic.py` — Core logic for crop, weather, and profit estimation
- `df_pincodes_selected.csv` — Pincode and location data
- `df_crop_profit.csv` — Crop profit/cost data
- `random_forest_model.pkl` — Trained ML model

---

<div align="center">
  <b>🌿 Together Let's Harvest Sustainability</b><br>
  <sub>made by Sanjeshwaran L</sub>
</div>
