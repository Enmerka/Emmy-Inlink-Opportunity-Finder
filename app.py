import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# App title
st.title("Emmy's Internal Linking Opportunities Finder")

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
    
    # Clean column names (remove leading/trailing spaces and convert to lowercase)
    list_keywords.columns = list_keywords.columns.str.strip().str.lower()

    # Required columns (in lowercase)
    required_columns = ["keyword", "position", "search volume", "keyword difficulty", "url"]

    # Validate necessary columns
    if all(col in list_keywords.columns for col in required_columns):
        st.success("File loaded successfully!")
        
        # Convert DataFrame to list of lists
        list_keywords = list_keywords.values.tolist()

        # Extract unique URLs
        list_urls = list(dict.fromkeys([x[4] for x in list_keywords]))

        # Keyword-URL-position pairs
        list_keyword_url = [[x[4], x[0], x[1]] for x in list_keywords]

        # Absolute route input
        absolute_rute = st.text_input("Insert your absolute route (e.g., https://example.com)")

        # Button to process the data
        if st.button("Find Internal Linking Opportunities"):
            if absolute_rute:
                internal_linking_opportunities = []

                # Iterate over URLs
                for iteration in list_urls:
                    try:
                        page = requests.get(iteration)
                        soup = BeautifulSoup(page.text, 'html.parser')

                        # Extract paragraphs and links
                        paragraphs = [p.text for p in soup.find_all('p')]
                        links = [link.get('href') for link in soup.find_all('a')]

                        # Check for linking opportunities
                        for x in list_keyword_url:
                            for y in paragraphs:
                                if f" {x[1].lower()} " in f" {y.lower()} ":
                                    if iteration != x[0]:
                                        links_presence = any(
                                            x[0].replace(absolute_rute, "") == z.replace(absolute_rute, "")
                                            for z in links if z
                                        )
                                        internal_linking_opportunities.append(
                                            [x[1], y, iteration, x[0], str(links_presence), x[2]]
                                        )
                    except Exception as e:
                        st.error(f"Error processing {iteration}: {e}")

                # Export results to Excel
                if internal_linking_opportunities:
                    output_df = pd.DataFrame(internal_linking_opportunities, columns=[
                        "Keyword", "Text", "Source URL", "Target URL", "Link Presence", "Keyword Position"
                    ])
                    output_file = "internal_linking_opportunities.xlsx"
                    output_df.to_excel(output_file, index=False)

                    st.success("Internal linking opportunities identified!")
                    with open(output_file, "rb") as f:
                        st.download_button(
                            label="Download Output File",
                            data=f,
                            file_name=output_file,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                else:
                    st.warning("No internal linking opportunities found.")
            else:
                st.warning("Please enter an absolute route!")
    else:
        st.error("Uploaded file does not have the required columns!")
        st.write("Uploaded file columns:", list_keywords.columns.tolist())
        st.write("Required columns:", required_columns)

# Sidebar for app instructions
st.sidebar.title("How to Use This App")
st.sidebar.markdown("""
This tool assists SEO specialists, content teams, and general website users in finding internal linking opportunities without having to pay a costly subscription. Internal linking is important in SEO because of the following reasons:

- The anchor texts are used as keyword relevancy signals for the target URL. This means that the keywords used to link to a page can influence the type of queries that page will be relevant for.**
- Internal linking helps to improve a site's internal architecture. This helps search engines to determine the topical authority of the site while easing the flow of PageRank (or link equity).**
- Internal linking improves overall aggregation of implicit user feedback signals across the pages of a site.**
- It can also be used to mold or sculpt the website representation vectors in ways that match what's obtainable for leading sites in the same niche or vertical.**

### If all these seem unclear or complex, join this community[Here](https://chat.whatsapp.com/KiHGrvcJX0i8kXP18aL2g2)
""")
