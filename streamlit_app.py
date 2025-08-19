
import streamlit as st
import pandas as pd
import pickle
from app_logic import get_estimated_profit_and_loan

# Load data and model
@st.cache_data
def load_data():
	df_pincodes_selected = pd.read_csv('df_pincodes_selected.csv')
	df_crop_profit = pd.read_csv('df_crop_profit.csv')
	with open('random_forest_model.pkl', 'rb') as f:
		model = pickle.load(f)
	return df_pincodes_selected, df_crop_profit, model

df_pincodes_selected, df_crop_profit, model = load_data()


# --- UI ---
st.set_page_config(page_title="AgriProfit Predictor", page_icon="🌾", layout="wide")

st.markdown("""
<style>
.main {
	background: linear-gradient(135deg, #e0ffe0 0%, #e0f7fa 100%);
}
.footer-message {
	position: fixed;
	left: 10px;
	bottom: 10px;
	color: #388e3c;
	font-size: 1.1em;
	font-weight: bold;
	background: #fffde7cc;
	border-radius: 8px;
	padding: 6px 16px;
	z-index: 100;
}
.footer-author {
	position: fixed;
	right: 10px;
	bottom: 10px;
	color: #1976d2;
	font-size: 1em;
	font-weight: bold;
	background: #e3f2fdcc;
	border-radius: 8px;
	padding: 6px 16px;
	z-index: 100;
}
</style>
""", unsafe_allow_html=True)

st.title("🌱 AgriProfit & Loan Estimator")
st.markdown(
	"""
	<span style='font-size:1.2em;'>Empowering farmers to make data-driven, sustainable crop choices! 🌾💧</span>
	""",
	unsafe_allow_html=True
)

# --- Layout: Left (inputs) | Right (results) ---
col1, col2 = st.columns([1,2])

with col1:
	st.header("📍 Enter Your Details")
	# Dropdown for pincode selection
	unique_pincodes = df_pincodes_selected['pincode'].drop_duplicates().astype(str).sort_values().tolist()
	pincode = st.selectbox("Pincode", unique_pincodes, help="Select a 6-digit pincode")
	land_area = st.number_input("Land Area (in hectares)", min_value=0.0, step=0.1, help="Total land area you want to cultivate")
	submitted = st.button("Estimate Profit & Loan 🚜")

with col2:
	if submitted:
		if not pincode.isdigit() or len(pincode) != 6:
			st.error("❌ Please select a valid 6-digit pincode.")
		elif land_area <= 0:
			st.error("❌ Please enter a valid land area greater than 0.")
		else:
			with st.spinner("Crunching numbers and fetching weather data... 🌦️"):
				result = get_estimated_profit_and_loan(int(pincode), land_area, df_pincodes_selected, model, df_crop_profit)
			if "error" in result:
				st.error(f"❌ {result['error']}")
			else:
				st.success("✅ Analysis Complete!")
				st.subheader("🌤️ Weather Summary")
				weather = result.get("weather", {})
				st.write(f"**Avg. Temperature:** {weather.get('temperature', 'N/A'):.2f} °C  |  **Avg. Humidity:** {weather.get('humidity', 'N/A'):.2f}%  |  **Total Rainfall:** {weather.get('rainfall', 'N/A'):.2f} mm")

				st.subheader("🥇 Top Crop Recommendations")
				crops = result.get("top_crops", [])
				if crops:
					for i, (crop, prob) in enumerate(crops, 1):
						st.write(f"{i}. <b>{crop}</b> &mdash; <span style='color:#43a047;font-weight:bold'>{prob*100:.1f}% suitability</span>", unsafe_allow_html=True)
				st.write(f"<b>Recommended Ratio:</b> <span style='color:#fbc02d'>{result.get('crop_ratio','')}</span>", unsafe_allow_html=True)

				st.subheader("💰 Financial Estimates")
				st.write(f"**Estimated Cost of Production:** ₹{result.get('estimated_cost_of_production', 0):,.2f}")
				st.write(f"**Estimated Total Profit:** <span style='color:#388e3c;font-weight:bold'>₹{result.get('estimated_profit', 0):,.2f}</span>", unsafe_allow_html=True)
				st.write(f"**Estimated Loan Amount (80% of cost):** <span style='color:#1976d2;font-weight:bold'>₹{result.get('estimated_loan_amount', 0):,.2f}</span>", unsafe_allow_html=True)
				if "estimation_message" in result:
					st.info(result["estimation_message"])

# --- Footer ---
st.markdown('<div class="footer-message">🌿 Together Let\'s Harvest Sustainability</div>', unsafe_allow_html=True)
st.markdown('<div class="footer-author">made by Sanjeshwaran L</div>', unsafe_allow_html=True)