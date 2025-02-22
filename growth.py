import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS
st.markdown(
    """
    <style>
    .stApp{
        background-color: black;
        color:white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("📀 Datasweeper Sterling Integrator By Pashmeen Zia")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization. Creating the project for quarter 3!")

# File uploader
uploaded_files = st.file_uploader("Upload your files (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file, encoding='utf-8')
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)  
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # File details
        st.write(f"🔍 Preview of {file.name}")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🛠 Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed!")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    if numeric_cols.any():
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.write("✅ Missing values filled!")
                    else:
                        st.write("⚠ No numeric columns found for filling missing values.")

        # Column selection
        st.subheader("🎯 Select Columns to Keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns] if columns else df  # Prevent empty DataFrame error

        # Data visualization
        st.subheader("📊 Data Visualization")
        numeric_cols = df.select_dtypes(include='number').columns
        if len(numeric_cols) > 0:
            if st.checkbox(f"Show visualization for {file.name}"):
                st.bar_chart(df[numeric_cols])
        else:
            st.write("⚠ No numeric columns available for visualization!")

        # Conversion Options
        st.subheader("🔁 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            file_name = file.name.replace(file_ext, f".{conversion_type.lower()}")

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)  # ✅ Fixed `.to_csv()`
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine="openpyxl")  # ✅ Excel Engine Specified
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)
            st.download_button(
                label=f"📥 Download {file_name}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            ) 

st.success("🎉 All files processed successfully!")
