---

# 🌾 Harvest Compass: AgriProfit & Loan Estimator 🌱

**Empowering farmers to make data-driven, sustainable crop choices!** 🌿💧

---

## 🌍 Overview

**Harvest Compass** is a Streamlit-based web app that helps farmers make **profitable and sustainable cropping decisions**.
By combining **pincode-level weather data, crop economics, and trained ML models**, it provides:

* **Smart crop recommendations**
* **Profitability & loan eligibility estimates**
* **Farmer-friendly UI with colorful insights**

This tool bridges the gap between **agricultural data, financial institutions, and rural farmers**.

---

## 🔑 Features

✔ Enter your **pincode** and **land area** to get:

* 🌦 **Weather summary** for your location
* 🌱 **Top crop recommendations** with suitability scores
* 📊 **Recommended crop ratio** (best land allocation strategy)
* 💰 **Estimated cost of production, profit, and loan amount**
* 🎨 **Simple, colorful UI** with helpful icons & messages

---

## 🛠️ Tech Stack / Files

* **Python 3.8+**
* **Streamlit** – Interactive web app
* **Scikit-learn** – ML modeling (Random Forest)
* **Pandas / NumPy** – Data preprocessing
* **Requests** – Weather API integration

📂 **Project Files**

* `streamlit_app.py` → Main Streamlit UI
* `app_logic.py` → Core logic (crop, weather & profit estimation)
* `df_pincodes_selected.csv` → Pincode & location dataset
* `df_crop_profit.csv` → Crop economics dataset (cost, yield, profit)
* `random_forest_model.pkl` → Pre-trained ML model

---

## 🚀 How to Run Locally

### 1. Install Requirements

Make sure you have **Python 3.8+** and **Streamlit** installed.

```bash
pip install streamlit pandas numpy requests scikit-learn
```

### 2. Run the App

Open **Anaconda Prompt** (or any terminal with the correct environment):

```bash
streamlit run streamlit_app.py
```

Open the link shown in the terminal (e.g., `http://localhost:8501`)

---

## 🌐 Share Your App

To share with others:

* Deploy on **Streamlit Community Cloud** (recommended)
* OR use a tunneling service like **ngrok**

⚠️ Do **not** share your local/private IP for public access.

---

## 📊 Example Output

**Input:**

* Pincode = `613005`
* Land Area = `2 hectares`

**Output:**

* Weather: *Moderate rainfall, suitable for maize & chickpea*
* Top Crop Recommendations: 🌽 Maize (85%) | 🌱 Chickpea (78%) | 🌾 Paddy (60%)
* Suggested Crop Ratio: *60% Maize + 40% Chickpea*
* Cost of Production: ₹65,000
* Expected Profit: ₹95,000
* Loan Eligibility: ₹70,000

---

## 👨‍🌾 Impact

* **Empowers farmers** with crop & credit insights
* **Reduces loan risks** for banks
* **Supports sustainable farming** using weather & profit data
* **Scalable** across districts & states

---

## 📌 Future Scope

* Integration of **groundwater & soil datasets**
* Real-time **market price APIs**
* **SMS/IVR support** for rural low-connectivity regions
* Direct **bank API integration** for automated loan approvals

---


<div align="center">
	<h3>🌿 Together, Let’s Harvest Sustainability</h3>
	<b>Made by Sanjeshwaran L</b>
</div>

---
