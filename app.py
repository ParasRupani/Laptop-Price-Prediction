import streamlit as st
import pickle
import pandas as pd
import joblib
from scipy.special import inv_boxcox
from scipy.stats import boxcox_normmax

# Load the trained model pipeline and the DataFrame used for training (for categories)
with open('./DataProcessing/best_random_forest_model.pkl', 'rb') as model_file:
    pipe = joblib.load(model_file)
df = pickle.load(open('df.pkl', 'rb'))

# Streamlit UI layout
st.title("Laptop Price Predictor")

# Assuming your DataFrame 'df' includes all the categories used during training
# Adjust these fields based on your actual features
col1, col2, col3, col4 = st.columns(4)

with col1:
    company = st.selectbox('Brand', df['Brand'].unique())
    laptop_type = st.selectbox('Type', df['Laptop_Type'].unique())
    refurbished = st.selectbox('Refurbished', ['No', 'Yes'])
    os_name = st.selectbox('OS', df['OS_Name'].unique())
    color = st.selectbox('Color', df['base_color'].unique())

with col2:
    ram = st.selectbox('RAM (in GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64])
    cpu_brand = st.selectbox('CPU Brand', df['Processor Brand'].unique())
    cpu_type = st.selectbox('CPU Type', df['ProcessorManufacturer'].unique())
    cpu_speed = st.number_input('Processor Speed (GHz)', min_value=0.1, max_value=5.0, step=0.1)
    
with col3:
    gpu_brand = st.selectbox('GPU Brand', df['Graphics_Coprocessor_Brand'].unique())
    gpu_memory = st.selectbox('GPU Memory (in GB)', [2, 4, 6, 8, 12, 16])
    primary_memory = st.selectbox('Primary Memory Type', df['Hard Disk Description'].unique())
    memory_type = st.selectbox('Memory Type', df['Memory Technology'].unique())

with col4:    
    screen_size = st.number_input('Screen Size (in inches)', min_value=10.0, max_value=20.0, step=0.1)
    resolution = st.selectbox('Screen Resolution', ['1920x1080', '1366x768', '1600x900', '3840x2160', '3200x1800', '2880x1800', '2560x1600', '2560x1440', '2304x1440'])
    weight = st.number_input('Weight of the Laptop (kg)', min_value=0.5, max_value=10.0, step=0.1)

# Button to make predictions
if st.button('Predict Price'):
    X_res = int(resolution.split('x')[0])
    Y_res = int(resolution.split('x')[1])
    ppi = ((X_res**2) + (Y_res**2))**0.5/screen_size

    if refurbished == 'Yes':
        refurbished = 1
    else:
        refurbished = 0

    # Prepare input data as a DataFrame to match the training data structure
    input_data = pd.DataFrame({
        'Brand': [company],
        'Laptop_Type': [laptop_type],
        'Refurbished': [refurbished],
        'DisplaySizeInches': [screen_size],
        'HorizontalPixels': [X_res],
        'VerticalPixels': [Y_res],
        'PPI': [ppi],
        'OS_Name': [os_name],
        'WeightKg': [weight],
        'RAM_in_GB': [ram],
        'Processor Brand': [cpu_brand],
        'ProcessorManufacturer': [cpu_type],
        'ProcessorSpeedGHz': [cpu_speed],
        'Graphics_Coprocessor_Brand': [gpu_brand],
        'Graphics Storage (GB)': [gpu_memory],
        'Hard Disk Description': [primary_memory],
        'Memory Technology': [memory_type],
        'base_color': [color]
    })

    # Predict using the pipeline
    predicted_price = pipe.predict(input_data)

    lambda_value = 0.3007754147558123

    # Display the predicted price
    st.success(f"The predicted price of this configuration is ${inv_boxcox(predicted_price[0], lambda_value):.2f}")
