import streamlit as st
import pandas as pd
import tempfile

# Import your SensorData class
from sensor_data_class import SensorData

# -----------------------------------------------------------------------------
# Session State Initialization
# -----------------------------------------------------------------------------
if "sensor_storage" not in st.session_state:
    st.session_state["sensor_storage"] = {}

# -----------------------------------------------------------------------------
# Page Title
# -----------------------------------------------------------------------------
st.title("Multi-File Sensor Data Tracker")
st.write(
    "Upload sensor CSV files and analyze them using the SensorData class."
)

# -----------------------------------------------------------------------------
# File Upload
# -----------------------------------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    file_name = uploaded_file.name

    if file_name not in st.session_state["sensor_storage"]:
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".csv"
            ) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                temp_path = tmp_file.name

            # Create SensorData object
            sensor_data = SensorData.load_csv(temp_path)

            # Store object using filename as key
            st.session_state["sensor_storage"][file_name] = sensor_data

            st.success(
                f"Successfully loaded and stored '{file_name}'!"
            )

        except Exception as e:
            st.error(f"Error processing file: {e}")

# -----------------------------------------------------------------------------
# Sidebar Object Selection
# -----------------------------------------------------------------------------
st.sidebar.header("Stored Sensor Objects")

if st.session_state["sensor_storage"]:

    selected_file = st.sidebar.selectbox(
        "Select sensor dataset:",
        options=list(st.session_state["sensor_storage"].keys())
    )

    sensor_data = st.session_state["sensor_storage"][selected_file]

    # -------------------------------------------------------------------------
    # Summary Metrics
    # -------------------------------------------------------------------------
    st.markdown("---")
    st.subheader(f"Active Dataset: `{selected_file}`")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Avg Temperature",
            f"{sensor_data.average_temperature():.2f} °C"
        )

    with col2:
        st.metric(
            "Max Humidity",
            f"{sensor_data.max_humidity():.2f} %"
        )

    with col3:
        st.metric(
            "Total CO₂",
            f"{sensor_data.total_co2():.0f}"
        )

    # -------------------------------------------------------------------------
    # Statistics Table
    # -------------------------------------------------------------------------
    stats_df = pd.DataFrame({
        "Metric": [
            "Average Temperature",
            "Maximum Humidity",
            "Minimum Humidity",
            "Total CO2",
            "Median Temperature"
        ],
        "Value": [
            round(sensor_data.average_temperature(), 2),
            round(sensor_data.max_humidity(), 2),
            round(sensor_data.min_humidity(), 2),
            round(sensor_data.total_co2(), 2),
            round(sensor_data.median_temperature(), 2)
        ]
    })

    st.subheader("Sensor Statistics")
    st.dataframe(
        stats_df,
        use_container_width=True,
        hide_index=True
    )

    # -------------------------------------------------------------------------
    # Average Temperature Per Sensor
    # -------------------------------------------------------------------------
    avg_sensor_df = pd.DataFrame(
        sensor_data.average_temperature_per_sensor().items(),
        columns=[
            "Sensor",
            "Average Temperature (°C)"
        ]
    )

    avg_sensor_df["Average Temperature (°C)"] = (
        avg_sensor_df["Average Temperature (°C)"].round(2)
    )

    st.subheader("Average Temperature Per Sensor")
    st.dataframe(
        avg_sensor_df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.sidebar.info(
        "No sensor datasets uploaded yet. Upload a CSV file to begin."
    )