import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder

# Set page config
st.set_page_config(
    page_title="Car Market Value Predictor",
    page_icon="🚗",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin-top: 2rem;
        text-align: center;
    }
    .price-display {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ff4b4b;
    }
    .electric-badge {
        background-color: #4CAF50;
        color: white;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 12px;
        margin-left: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Load resources
@st.cache_resource
def load_model():
    with open('src/car_price_model.pkl', 'rb') as f:
        return pickle.load(f)

@st.cache_resource
def load_encoders():
    with open('label_encoders.pkl', 'rb') as f:
        return pickle.load(f)

@st.cache_resource
def load_distinct_values():
    with open('distinct_values.pkl', 'rb') as f:
        return pickle.load(f)

@st.cache_resource
def load_electric_info():
    with open('electric_car_info.pkl', 'rb') as f:
        return pickle.load(f)

try:
    model = load_model()
    label_encoders = load_encoders()
    distinct_values = load_distinct_values()
    electric_info = load_electric_info()
except Exception as e:
    st.error(f"Error loading model files: {e}")
    st.stop()

# Header
st.markdown('<h1 class="main-header">🚗 Car Market Value Predictor</h1>', unsafe_allow_html=True)
st.markdown("### Get an accurate estimate of your car's market value based on its specifications")

# Create form
with st.form("car_details_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Car Specifications")
        
        car_make = st.selectbox(
            "Car Make & Model",
            options=distinct_values['car'],
            help="Select your car's make and model"
        )
        
        year = st.slider(
            "Manufacturing Year",
            min_value=distinct_values['min_year'],
            max_value=distinct_values['max_year'],
            value=2020,
            help="Select the year your car was manufactured"
        )
        
        fuel_type = st.selectbox(
            "Fuel Type",
            options=distinct_values['enginetype'],
            help="Select your car's fuel type",
            key="fuel_type_select"
        )
        
        # Show electric car note
        if any(electric in fuel_type for electric in electric_info['electric_types']):
            st.info("🔌 Electric car selected - engine size will be set to 0")
        
    with col2:
        st.subheader("Additional Details")
        
        # Conditionally show engine size (not for electric cars)
        if any(electric in fuel_type for electric in electric_info['electric_types']):
            engine_size = electric_info['default_engine_value']
            st.write(f"Engine Size: {engine_size}L (Electric Vehicle)")
        else:
            engine_size = st.slider(
                "Engine Size (L)",
                min_value=float(distinct_values['min_engine']),
                max_value=float(distinct_values['max_engine']),
                value=2.0,
                step=0.1,
                help="Select your car's engine size in liters"
            )
        
        mileage = st.slider(
            "Mileage (km)",
            min_value=float(distinct_values['min_km']),
            max_value=float(distinct_values['max_km']),
            value=50000.0,
            step=1000.0,
            help="Enter your car's current mileage in kilometers"
        )
        
        city = st.selectbox(
            "City",
            options=distinct_values['city'],
            help="Select your city"
        )
    
    # Submit button
    submitted = st.form_submit_button("🚀 Estimate Market Value", use_container_width=True)

# Prediction logic
if submitted:
    try:
        # Prepare input data
        input_data = {
            'enginetype': fuel_type,
            'city': city,
            'year': year,
            'car': car_make,
            'engine': engine_size,
            'converted_km': mileage
        }
        
        # Convert to DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Encode categorical variables with unseen label handling
        for col in ['enginetype', 'city', 'car']:
            if col in input_df.columns:
                # Handle unseen labels by using the most common class
                if input_data[col] in label_encoders[col].classes_:
                    input_df[col] = label_encoders[col].transform([input_data[col]])[0]
                else:
                    # Use the first class (usually most common) for unseen labels
                    input_df[col] = 0
        
        # Ensure correct data types
        input_df = input_df.astype(float)
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        
        # Display result
        st.markdown("---")
        st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
        st.markdown("### Estimated Market Value")
        
        # Add electric badge if it's an electric car
        badge_html = ""
        if any(electric in fuel_type for electric in electric_info['electric_types']):
            badge_html = '<span class="electric-badge">ELECTRIC</span>'
        
        st.markdown(f'<div class="price-display">${prediction:,.2f} {badge_html}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Show input summary
        st.subheader("📋 Input Summary")
        summary_col1, summary_col2 = st.columns(2)
        
        with summary_col1:
            st.write(f"**Car:** {car_make}")
            st.write(f"**Year:** {year}")
            st.write(f"**Fuel Type:** {fuel_type}")
        
        with summary_col2:
            st.write(f"**Engine Size:** {engine_size}L")
            st.write(f"**Mileage:** {mileage:,.0f} km")
            st.write(f"**City:** {city}")
        
        # Additional info
        st.info("""
        💡 **Note:** This estimate is based on historical market data and machine learning algorithms. 
        Actual market price may vary based on:
        - Vehicle condition and maintenance history
        - Market demand and seasonality
        - Additional features and options
        - Local market conditions
        """)
        
    except Exception as e:
        st.error(f"Error making prediction: {str(e)}")
        st.write("Please try different input values or contact support if the issue persists.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with ❤️ using Streamlit and Scikit-learn</p>
    <p>Note: Predictions are estimates based on historical data. Always consult multiple sources for accurate pricing.</p>
</div>
""", unsafe_allow_html=True)
