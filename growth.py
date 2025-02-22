import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="🧹 Data Sweeper", layout='wide')

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Description with Icons
st.title("🧹 Data Sweeper - Sterling Integrator by Nimoo Khan")
st.write("🔄 Transform your files between CSV and Excel formats with built-in data cleaning and visualization. 🚀")

# File Uploader with Icon
uploaded_files = st.file_uploader("📂 Upload your files (Accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # ✅ Fix for reading CSV/Excel
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)

            elif file_ext == ".xlsx":
                df = pd.read_excel(file, engine="openpyxl")

            else:
                st.error(f"❌ Unsupported file type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"⚠️ Error reading {file.name}: {e}")
            continue

        # File Details
        st.write(f"📊 Preview of {file.name}:")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🛠 Data Cleaning Options")
        if st.checkbox(f"🧼 Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑 Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed!")

            with col2:
                if st.button(f"🛠 Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    if not numeric_cols.empty:
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.write("✅ Missing values filled!")
                    else:
                        st.warning("⚠️ No numeric columns found for filling missing values!")

        # Column Selection
        st.subheader("📌 Select Columns to Keep")
        columns = st.multiselect(f"📋 Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader("📊 Data Visualization")
        numeric_data = df.select_dtypes(include='number')
        if not numeric_data.empty:
            if st.checkbox(f"📉 Show visualization for {file.name}"):
                st.bar_chart(numeric_data.iloc[:, :min(2, len(numeric_data.columns))])
        else:
            st.warning("⚠️ No numeric data available for visualization!")

        # Conversion Options
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"📎 Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"💾 Convert {file.name}"):
            buffer = BytesIO()
            file_name = file.name.replace(file_ext, f".{conversion_type.lower()}")

            try:
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    mime_type = "text/csv"

                elif conversion_type == "Excel":
                    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                        df.to_excel(writer, index=False)
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                buffer.seek(0)
                st.download_button(
                    label=f"⬇️ Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )
                st.success(f"✅ Successfully converted {file.name} to {conversion_type}!")

            except Exception as e:
                st.error(f"⚠️ Error converting {file.name}: {e}")

st.success("🎉 All files processed successfully! 🚀")

