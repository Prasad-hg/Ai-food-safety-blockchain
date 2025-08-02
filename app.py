import streamlit as st
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import uuid
import datetime
from matplotlib.ticker import MaxNLocator
from PIL import Image

# --- Page Config ---
st.set_page_config(
    page_title="Revolutionizing Food Safety with AI Intelligence and Blockchain Integrity!",
    page_icon="🍏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load Model ---
model = joblib.load('freshness_predictor_model.pkl')
label_mapping = {0: "Fresh", 1: "Semi-Spoiled", 2: "Spoiled"}

# --- Session State Init ---
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = []

if 'prediction_counts' not in st.session_state:
    st.session_state.prediction_counts = {"Fresh": 0, "Semi-Spoiled": 0, "Spoiled": 0}

# --- Sidebar Navigation ---
st.sidebar.title("🍏 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Welcome", "🚀 Take a Short Tour", "🔎 Predict Freshness", "📋 Blockchain Records", "📊 Data Visualizations"]
)

# --- Sidebar Toggle for Timeline ---
show_timeline = st.sidebar.checkbox('🕰️ Show Journey Timeline')

# --- Welcome Page ---
if page == "🏠 Welcome":
    st.title("🍏Revolutionizing Food Safety with AI Intelligence and Blockchain Integrity!")

    img = Image.open("images/welcome_image.png")
    img = img.resize((500, int(img.height * (500 / img.width))))  # Better width
    st.image(img)

    st.markdown("""
    ## Welcome to the Future of Food Safety!
    In this application, you will explore:
    - 🛒 A **customer journey** through a smart supermarket.
    - 🤖 **Real-time prediction** of food freshness.
    - 🔗 **Blockchain tracking** for transparency.
    - 📈 **Visual insights** into your food's journey.
    
    👉 Start by taking a **Quick Tour** from the sidebar!
    """)

# --- Tour Page ---
elif page == "🚀 Take a Short Tour":
    st.title("🚀 Quick Tour: How the System Works")

    steps = [
        {"title": "🏬 Step 1: Enter Supermarket - Apple Section", "image": "images/image1.jpeg", "points": ["Customer enters fruit section.", "Smart sensors track environment."]},
        {"title": "📱 Step 2: Customer Scanning Apple", "image": "images/image2.jpeg", "points": ["Scan QR code on apple.", "Real-time freshness check triggered."]},
        {"title": "📲 Step 3: Mobile Displays Product Status", "image": "images/image3.jpeg", "points": ["Instant feedback on freshness.", "Color-coded status for ease."]},
        {"title": "👨‍💼 Step 4: Manager Monitors Store Alerts", "image": "images/image4.png", "points": ["Store managers monitor products.", "Alerts if spoilage detected."]}
    ]

    for step in steps:
        st.subheader(step["title"])
        img = Image.open(step["image"])
        img = img.resize((400, int(img.height * (400 / img.width))))  # Make compact and consistent
        st.image(img)
        for point in step["points"]:
            st.markdown(f"✅ {point}")
        st.markdown("---")

    st.success("🎉 Tour Completed! Now head to the Prediction Page to experience it yourself!")

# --- Prediction Page ---
elif page == "🔎 Predict Freshness":
    st.title("🔎 Predict Food Freshness + Blockchain Save")

    col1, col2 = st.columns(2)
    with col1:
        temperature = st.text_input("Temperature (°C)", placeholder="Enter (-10 to 50)")
        co2_level = st.text_input("CO2 Level (ppm)", placeholder="Enter (200 to 2000)")
    with col2:
        humidity = st.text_input("Humidity (%)", placeholder="Enter (0 to 100)")
        gas_level = st.text_input("Gas Level", placeholder="Enter (0.0 to 2.0)")

    st.markdown("---")

    food_name = st.text_input('🍎 Food Name', value="Apple")
    batch_id = st.text_input('📦 Batch ID', value=f"BATCH-{uuid.uuid4().hex[:6].upper()}")

    if st.button('🚀 Predict and Save'):
        if not (temperature and humidity and co2_level and gas_level):
            st.error("⚠️ Please fill all sensor fields!")
        else:
            try:
                temperature = float(temperature)
                humidity = float(humidity)
                co2_level = float(co2_level)
                gas_level = float(gas_level)

                input_features = np.array([[temperature, humidity, co2_level, gas_level]])
                prediction = model.predict(input_features)
                predicted_label = label_mapping[prediction[0]]

                st.success(f"🍽️ Predicted Freshness: **{predicted_label}**")

                current_time = datetime.datetime.now()
                timestamps = {
                    'Farm': current_time - datetime.timedelta(days=2),
                    'Transport': current_time - datetime.timedelta(days=1),
                    'Storage': current_time - datetime.timedelta(hours=12),
                    'Supermarket': current_time
                }

                for stage in timestamps.keys():
                    temp_variation = temperature + np.random.uniform(-2, 2)
                    humidity_variation = humidity + np.random.uniform(-5, 5)
                    co2_variation = co2_level + np.random.uniform(-100, 100)
                    gas_variation = gas_level + np.random.uniform(-0.2, 0.2)

                    block = {
                        'Batch_ID': batch_id,
                        'Food_Name': food_name,
                        'Stage': stage,
                        'Temperature': round(temp_variation, 2),
                        'Humidity': round(humidity_variation, 2),
                        'CO2_Level': round(co2_variation, 2),
                        'Gas_Reading': round(gas_variation, 2),
                        'Freshness_Status': predicted_label if stage == 'Supermarket' else "In-Transit",
                        'Timestamp': timestamps[stage].strftime("%Y-%m-%d %H:%M:%S"),
                        'Fake_Hash': str(uuid.uuid4())
                    }
                    st.session_state.blockchain.append(block)

                st.session_state.prediction_counts[predicted_label] += 1
                st.balloons()

            except ValueError:
                st.error("⚠️ Enter valid numeric values!")

# --- Blockchain Records Page ---
elif page == "📋 Blockchain Records":
    st.title("📋 Blockchain Record History")

    if st.session_state.blockchain:
        df = pd.DataFrame(st.session_state.blockchain)
        st.dataframe(df)

        csv = df.to_csv(index=False)
        st.download_button("⬇️ Download Blockchain CSV", csv, "blockchain_data.csv", "text/csv")
    else:
        st.warning("⚠️ No blockchain records available yet.")

# --- Data Visualizations Page ---
elif page == "📊 Data Visualizations":
    st.title("📊 Data Visualization Dashboard")

    if sum(st.session_state.prediction_counts.values()) > 0:
        st.subheader("🥑 Freshness Prediction Distribution")
        labels = list(st.session_state.prediction_counts.keys())
        sizes = list(st.session_state.prediction_counts.values())

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.info("⚠️ No predictions yet.")

# --- Timeline Drawing (only if checkbox selected) ---
if show_timeline:
    st.subheader("🚚📦🍏 Journey Timeline")

    if st.session_state.blockchain:
        df = pd.DataFrame(st.session_state.blockchain)

        batch_options = df['Batch_ID'].unique().tolist()
        selected_batch = st.selectbox("Select Batch ID", batch_options)

        batch_df = df[df['Batch_ID'] == selected_batch].sort_values('Timestamp')

        if not batch_df.empty:
            stages = batch_df['Stage']

            fig, ax1 = plt.subplots(figsize=(14, 8))
            plt.style.use('seaborn-v0_8-dark-palette')

            # Temperature
            color_temp = 'crimson'
            ax1.set_xlabel('Journey Stage', fontsize=14)
            ax1.set_ylabel('Temperature (°C)', color=color_temp, fontsize=14)
            ax1.plot(stages, batch_df['Temperature'], marker='o', color=color_temp, linewidth=2)
            ax1.tick_params(axis='y', labelcolor=color_temp)

            # Humidity
            ax2 = ax1.twinx()
            color_humidity = 'royalblue'
            ax2.set_ylabel('Humidity (%)', color=color_humidity, fontsize=14)
            ax2.plot(stages, batch_df['Humidity'], marker='s', linestyle='--', color=color_humidity, linewidth=2)
            ax2.tick_params(axis='y', labelcolor=color_humidity)

            # CO2 Level
            ax3 = ax1.twinx()
            ax3.spines["right"].set_position(("axes", 1.15))
            color_co2 = 'limegreen'
            ax3.set_ylabel('CO₂ (ppm)', color=color_co2, fontsize=14)
            ax3.plot(stages, batch_df['CO2_Level'], marker='^', linestyle='-.', color=color_co2, linewidth=2)
            ax3.tick_params(axis='y', labelcolor=color_co2)

            # Gas Reading
            ax4 = ax1.twinx()
            ax4.spines["right"].set_position(("axes", 1.3))
            color_gas = 'orchid'
            ax4.set_ylabel('Gas', color=color_gas, fontsize=14)
            ax4.plot(stages, batch_df['Gas_Reading'], marker='D', linestyle=':', color=color_gas, linewidth=2)
            ax4.tick_params(axis='y', labelcolor=color_gas)

             # --- Custom legend ---
            lines_1, labels_1 = ax1.get_legend_handles_labels()
            lines_2, labels_2 = ax2.get_legend_handles_labels()
            lines_3, labels_3 = ax3.get_legend_handles_labels()
            lines_4, labels_4 = ax4.get_legend_handles_labels()

            lines = lines_1 + lines_2 + lines_3 + lines_4
            labels = labels_1 + labels_2 + labels_3 + labels_4

            ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=2, fancybox=True, shadow=True, fontsize=12)



            fig.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("⚠️ No timeline data available.")
    else:
        st.warning("⚠️ No blockchain data yet.")
