import streamlit as st
import requests
import pandas as pd

# Fungsi untuk mendapatkan data dari server Flask
def fetch_temperature_data():
    response = requests.get('http://192.168.43.73:5000/temperature')
    if response.status_code == 200:
        data = response.json()
        return data['temperature'], data['humidity'], data['total_siswa']
    else:
        return None, None, None

def streamlit_app():
    # Set page config
    st.set_page_config(
        page_title="Temperature Dashboard",
        page_icon="🌡️",
        layout="wide",
    )

    # Title and description
    st.title("Temperature Dashboard")
    st.markdown("### Real-time Temperature Data from ESP32 and DHT22 Sensor")
    st.markdown("""
        This dashboard displays real-time temperature data sent from an ESP32 device equipped with a DHT22 sensor. 
        The data is updated continuously and visualized in the charts below.
    """)

    # Initialize empty lists to store data
    temperature_data = []
    humidity_data = []
    total_siswa_data = []

    if st.button('Fetch Temperature Data'):
        temperature, humidity, total_siswa = fetch_temperature_data()
        if temperature is not None:
            temperature_data.append(temperature)
            humidity_data.append(humidity)
            total_siswa_data.append(total_siswa)
            
            current_temp = temperature
            avg_temp = sum(temperature_data) / len(temperature_data)

            col1, col2, col3 = st.columns(3)
            col1.metric("Current Temperature", f"{current_temp:.2f} °C")
            col2.metric("Current Humidity", f"{humidity:.2f} %")
            col3.metric("Total Students", f"{total_siswa}")

            # Temperature chart
            st.line_chart(pd.DataFrame({
                'Temperature (°C)': temperature_data
            }, index=range(1, len(temperature_data) + 1)))

            # Humidity chart
            st.line_chart(pd.DataFrame({
                'Humidity (%)': humidity_data
            }, index=range(1, len(humidity_data) + 1)))

            # Display temperature data in DataFrame
            st.header("Data Details")
            df = pd.DataFrame({
                'Time': range(1, len(temperature_data) + 1),
                'Temperature (°C)': temperature_data,
                'Humidity (%)': humidity_data,
                'Total Siswa': total_siswa_data
            })
            st.dataframe(df)
        else:
            st.write("Failed to fetch temperature data.")

    # Additional UI elements for better look and feel
    with st.expander("About this dashboard"):
        st.markdown("""
            This dashboard is powered by Streamlit and Flask. Data is collected in real-time from an ESP32 device 
            equipped with a DHT22 sensor and displayed here for monitoring purposes.
        """)

if __name__ == '__main__':
    streamlit_app()
