import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import process

# App title
st.title("Internal Linking Opportunities Finder")

# Instructions for the user
st.markdown("""
### Instructions:
1. Ensure your Excel file follows the exact column order and names:
   - **Keyword**
   - **Position**
   - **Search Volume**
   - **Keyword Difficulty**
   - **URL**
2. Save the file as an `.xlsx` format before uploading.
""")

# File uploader for the keyword sheet
uploaded_file = st.file_uploader("Upload your Excel file with keywords and URLs", type=["xlsx"])

if uploaded_file:
    # Load the Excel file into a DataFrame
    list_keywords = pd.read_excel(uploaded_file)
    
    # Clean column names
    list_keywords.columns = list_keywords.columns.str.strip()  # Remove leading/trailing spaces
    list_keywords.columns = list_keywords.columns.str.lower()  # Convert to lowercase

    # Required columns (also in lowercase)
    required_columns = ["keyword", "position", "search volume", "keyword difficulty", "url"]

    # Validate necessary columns
    if all(col in list_keywords.columns for col in required_columns):
        st.success("File loaded successfully!")
        
        # Rest of the code...
    else:
        st.error("Uploaded file does not have the required columns!")
        print("Uploaded file columns:", list_keywords.columns.tolist())
        print("Required columns:", required_columns)
