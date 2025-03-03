# Import commands

import streamlit as st
import pandas as pd
import os 
from io import BytesIO


# setting up of Application 

st.set_page_config(page_title="File Convertor and Exractor by RamZ", layout="wide")
st.title("Transformer")
st.write("Transform your files between Excel and CSV with built in Data Cleaning and Visualization")

uploaded_files = st.file_uploader("Upload your files in XLSX and CSV " , type = ["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported File Version: {file_ext}")
            continue  # Only skip if file format is unsupported

     
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024:.2f} KB")


# show 5 rows of our df

        st.write ("Previoew the Head of the Dataframe")
        st.dataframe(df.head())

# Options for Data Cleaning

        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
                col1 , col2 = st.columns(2)
                with col1:
                    if st.button(f"Remove Duplicates from {file.name}"):
                        df.drop_duplicates(inplace=True)
                        st.write("Duplicate Entries Removed")
                with col2:
                    if st.button (f"Fill Missing Values: {file.name}"):
                        numeric_cols=df.select_dtypes(include=['number']).columns
                        df[numeric_cols]= df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.write("Missing Valued have been filled")

        # choose specific columns to keep and convert

        st.subheader("Select Columns to concert")
        columns = st.multiselect (f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Create some Visualizations 
        st.subheader("Data Visualization")
        if st.checkbox (f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

        # convert the file CSV to Excel or Vice Versa    
        st.subheader("Conversion Options")
        conversion_type = st.radio (f"covert {file.name} to: ", ["CSV", "EXCEL"], key= file.name)
        if st.button (f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
                
            elif conversion_type== "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)

            # Download Button
                st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data= buffer,
                filename=file_name,
                mime= mime_type
            )
                
st.success ("All Files Processed")                
