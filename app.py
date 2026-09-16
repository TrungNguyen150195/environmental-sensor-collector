import streamlit as st
import pandas as pd
import numpy as np

# 1. Initialize session state to store multiple NumPy objects if not already done
if "numpy_storage" not in st.session_state:
    st.session_state["numpy_storage"] = {}

st.title("Multi-File NumPy Object Tracker")
st.write("Upload CSV files to store them as unique NumPy data objects.")

# 2. File uploader widget
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    file_name = uploaded_file.name

    # Process and store the file if it hasn't been saved yet
    if file_name not in st.session_state["numpy_storage"]:
        try:
            df = pd.read_csv(uploaded_file)
            # Convert to NumPy array
            numpy_arr = df.to_numpy()

            # Save into our session state dictionary using the filename as the key
            st.session_state["numpy_storage"][file_name] = numpy_arr
            st.success(f"Successfully stored '{file_name}' as a NumPy object!")
        except Exception as e:
            st.error(f"Error processing file: {e}")

# 3. Drop-down Menu to access stored objects
st.sidebar.header("Stored NumPy Objects")

if st.session_state["numpy_storage"]:
    # Drop-down list populated by the keys of our storage dictionary
    selected_object_name = st.sidebar.selectbox(
        "Select an object to inspect:",
        options=list(st.session_state["numpy_storage"].keys())
    )

    # Retrieve the active array from storage
    active_array = st.session_state["numpy_storage"][selected_object_name]

    # Display the selected object's metadata and contents
    st.markdown("---")
    st.subheader(f"Active Object: `{selected_object_name}`")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Array Shape", value=str(active_array.shape))
    with col2:
        st.metric(label="Data Type (dtype)", value=str(active_array.dtype))

    st.write("**Array Representation:**")
    st.code(repr(active_array), language="python")

else:
    st.sidebar.info("No objects stored yet. Upload a CSV file to begin.")
