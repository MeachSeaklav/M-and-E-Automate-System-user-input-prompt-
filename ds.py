import streamlit as st
import pandas as pd
import os
import openai
from dotenv import load_dotenv
from zip import create_zip_file
from telegram import send_to_telegram
from report_generation import generate_report_with_chatgpt
import streamlit as st
import pandas as pd
import os
import openai
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key from environment variable
openai.api_key = st.secrets["OPENAI_API_KEY"]

# def fetch_data(google_sheet_url):
#     try:
#         df = pd.read_csv(google_sheet_url)
#         df.insert(0, "No", range(1, len(df) + 1))
#     except Exception as e:
#         st.error(f"Failed to fetch data from Google Sheets: {e}")
#         return None
#     return df

# def dashboard():
#     st.set_page_config(
#         page_title="DCx Co., Ltd",
#         page_icon="https://dcxsea.com/asset/images/logo/LOGO_DCX.png",
#         layout="wide",
#         initial_sidebar_state="collapsed"
#     )
    
#     st.markdown("""
#     <div style="display: flex; justify-content: center; align-items: center; margin-top: -40px; margin-bottom: 20px;">
#         <img src="https://dcxsea.com/asset/images/logo/LOGO_DCX.png" style="width: 200px; margin-right: 15px;">
#         <h4 style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; color: white; margin-bottom: -90px;">DCx Co., Ltd</h4>
#     </div>
#     """, unsafe_allow_html=True)

#     hide_st_style = """
#                 <style>
#                 #MainMenu {visibility: hidden;}
#                 footer {visibility: hidden;}
#                 </style>
#                 """
#     st.markdown(hide_st_style, unsafe_allow_html=True)

#     # Header section
#     st.markdown("""
#         <div style="display: flex; align-items: center;">
#             <img src="https://cdn3d.iconscout.com/3d/free/thumb/free-line-chart-growth-3814121-3187502.png" alt="logo" style="width: 70px; margin-right: 15px;">
#             <h5 style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; margin-top: 25px;">ប្រព័ន្ធគ្រប់គ្រងព័ត៌មានជលផល(Fisheries Information Management System (FIMS))</h5>
#         </div>
#     </div>
# """, unsafe_allow_html=True)

#     # Google Sheets URL (the one you want to fetch data from directly)
#     google_sheet_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTDG2d2dfb6GHeGUy-nULaIkY26I1cbDA0vMnuyEXFS2vpqtU8E_0kfPCMGtxPXv_w8Vp8bXytV5ipN/pub?gid=680814381&output=csv'

#     # Fetch the data from the predefined Google Sheet
#     df = fetch_data(google_sheet_url)

#     # Main page layout
#     col1, col2 = st.columns([3, 1])

#     # Left column for displaying data
#     with col1:
#         if df is not None:
#             # Convert DataFrame to HTML without the index
#             html_table = df.to_html(index=False, classes='custom-table', escape=False)

#             # Add custom CSS to style the table with your desired background color and no space around it
#             st.markdown("""
#                 <style>
#                 .table-container {
#                     margin: 0px; 
#                     border-radius: 10px;
#                     height: 500px;
#                     width: 100%;
#                     overflow: auto;
#                 }
#                 .custom-table {
#                     width: 100%;
#                     border-collapse: collapse;
                    
#                     font-family: Khmer OS Content Regular;
#                     font-size: 14px;
#                     background-color: rgb(161, 219, 255, 0.3);  /* Light background color for table body */
#                     color: white;  
#                 }
#                 .custom-table th, .custom-table td {
#                     white-space: nowrap;  /* Ensure text stays on one line */
#                     text-overflow: ellipsis;  /* Add ellipsis if content overflows */
#                     overflow: hidden;  /* Hide overflow content */
#                     padding: 8px;
#                     text-align: left;
#                 }
#                 .custom-table th {
#                     text-align: center;
#                     margin: 0px; 
#                     top: 0px;
#                     background-color: black; 
#                     color: white; 
#                     border: 1px solid rgba(255, 255, 255, 0.1);
#                     font-weight: bold; 
#                     position: sticky;
#                     top: 0; 
#                     z-index: 1;
#                 }
#                 .custom-table td {
#                     background-color: rgb(161, 219, 255, 0.3); /* Lighter stripe for alternating rows */
#                     border: 1px solid rgba(255, 255, 255, 0.1); /* Border for cells */
#                 }
                
#                 .custom-table td:first-child, .custom-table th:first-child {
#                     margin: 0px; 
#                     position: sticky;
#                     border: 1px none rgba(255, 255, 255, 0.1);
#                     left: 0; 
#                     background-color: black; 
#                     z-index: 1;
#                 }
#                 </style>
#             """, unsafe_allow_html=True)

#             # Wrap the table in a scrollable container
#             st.markdown(f"""
#                 <div class="table-container">
#                     {html_table}
#                 </div>
#             """, unsafe_allow_html=True)

#     # Right column for prompt input and actions
#     with col2:

#         # Custom CSS for the text area targeting the correct Streamlit class
#         st.markdown("""
#             <style>
#             div.stTextArea textarea {
#                 color: white;
#                 font-size: 16px;
#                 border-radius: 10px;
#                 padding: 10px;
#                 width: 100% !important;
#                 height: 200px !important;
#                 border: 1px solid #ccc;
#                 box-sizing: border-box;
#             }
#             div.stTextArea textarea:focus {
#                 border-color: #005000;
#                 outline: none;
#             }
#             </style>
#         """, unsafe_allow_html=True)

#         # Text area input
#         user_prompt = st.text_area("How can I assist you?", key="prompt_input_key")

#         # Custom CSS for the button
#         st.markdown("""
#              <style>
#              div.stDownloadButton > button, div.stButton > button {
#                 background-color: #006400;
#                 color: white;
#                 padding: 10px;
#                 font-size: 16px;
#                 border-radius: 5px;
#                 border: none;
#                 cursor: pointer;
#              }
#              div.stDownloadButton > button:hover, div.stButton > button:hover {
#                 background-color: #005000;
#                 color: #DFFF00;
#              }
#              </style>
#         """, unsafe_allow_html=True)

#         if st.button('Generate Report'):
#             if not user_prompt.strip():
#                 st.error("Please enter a prompt to generate the report.")
#             else:
#                 df_cleaned = df.fillna('') if df is not None else None
#                 if df_cleaned is None:
#                     st.error("No data available to generate the report.")
#                 else:
#                     report_title = "Generated Report"
#                     report_content, word_filename, pdf_filename = generate_report_with_chatgpt(df_cleaned, report_title, user_prompt)

#                     try:
#                         if report_content:
#                             # Store the report content in session state
#                             st.session_state['report_content'] = report_content
#                             zip_filename = f'Report.zip'
#                             create_zip_file(word_filename, pdf_filename, zip_filename)

#                             # st.session_state['report_content'] = report_content
#                             st.session_state['zip_filename'] =  zip_filename  # or zip_filename, depending on your choice
#                             st.session_state['word_filename'] = word_filename
#                             st.session_state['pdf_filename'] = pdf_filename

#                             # st.success("Report generated and zip file created successfully.")
#                         else:
#                             st.error("Failed to generate report.")
#                     except Exception as e:
#                         st.error(f"An error occurred: {e}")


#     # Access the stored report content for reuse
#     if 'report_content' in st.session_state:
#         st.write(st.session_state['report_content'])

#         col_button1, col_button2 = st.columns([1, 8])

#         # Custom CSS for both buttons
#         st.markdown("""
#              <style>
#              div.stDownloadButton > button {
#                 background-color: #006400;
#                 color: white;
#                 padding: 10px;
#                 font-size: 16px;
#                 border-radius: 5px;
#                 border: none;
#                 cursor: pointer;
#                 }
#              div.stDownloadButton > button:hover {
#                 background-color: #005000;
#                 color: #DFFF00;
#                 }
#               </style>
#         """, unsafe_allow_html=True)

#         # Column 1 - Download Button
#         with col_button1:
#             if 'word_filename' in st.session_state:
#                 word_filename = st.session_state['word_filename']
#                 # Ensure that the file exists before trying to open it
#                 if os.path.exists(word_filename):
#                     with open(word_filename, 'rb') as file:
#                         st.download_button(
#                             label="Download Report",
#                             data=file,
#                             file_name=word_filename,
#                             mime='application/zip'
#                         )
#                 else:
#                     st.error("The zip file could not be found.")

#         # Column 2 - Telegram Button
#         with col_button2:
#             if st.button('Telegram'):
#                 if 'word_filename' in st.session_state and 'pdf_filename' in st.session_state:
#                     word_filename = st.session_state['word_filename']
#                     # pdf_filename = st.session_state['pdf_filename']

#                     try:
#                         # Send report to Telegram
#                         send_to_telegram(word_filename, f"Here is your generated report (Word).")
#                         # send_to_telegram(pdf_filename, f"Here is your generated report (PDF).")
#                         # st.success("Report sent to Telegram successfully!")
#                     except Exception as e:
#                         st.error(f"Failed to send report to Telegram: {e}")
#                 else:
#                     st.error("Report not found in session state.")




def fetch_data(google_sheet_url):
    try:
        df = pd.read_csv(google_sheet_url)
        # st.success("Data successfully fetched from Google Sheets!")
        # df.insert(0, "No", range(1, len(df) + 1))  # Add row numbers
        # st.write(df)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

def process_and_clean_data(df): 
    if df is None or df.empty:
        return pd.DataFrame()
    
    # Step 2: Remove empty rows and columns
    df.dropna(how='all', inplace=True)  # Remove rows where all elements are NaN
    df.dropna(axis=1, how='all', inplace=True)  # Remove columns where all elements are NaN
    df.reset_index(drop=True, inplace=True)

    # Step 3: Drop unnecessary columns
    columns_to_drop = ['_id', '_uuid', '_submission_time', '_validation_status', '_status', '_submitted_by', '_index']
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')

    # Step 4: Rename columns
    column_rename_map = {
        "អធិការដ្ឋាន": "Inspectorate",
        "ខេត្ត": "Province",
        "កាលបរិច្ឆេទរាយការណ៍": "Date",
        "nat_sum": "Natural Resource Total",
        "aqu_sum": "Aquaculture Total",
        "total_sum": "Overall Total",
        "sum_pro": "Processed Products Total",
        "sum_crime": "Crime Cases Total",
        "sum_exhibit": "Exhibits Total",
        "sum_enforce": "Enforcement Actions Total",
        "ចំនួនអ្នកនេសាទសរុប (នាក់)": "Total Fishermen (people)",
        "ចំនួនស្រី្តអ្នកនេសាទ\u200b (នាក់)": "Female Fishermen (people)",
        "ចំនួនកសិករវារីវប្បករសរុប (នាក់)": "Total Farmers (people)",
        "ចំនួនស្រី្តវារីវប្បករ (នាក់)": "Female Farmers (people)",
        "ចំនួនស្រះចិញ្ចឹមសរុប (ស្រះ, ថង់ផ្លាស្ទីក, បែរ)": "Total Ponds (count)",
        "ទំហំស្រះចិញ្ចឹមសរុប (ហិកតា)": "Total Pond Area (hectares)",
        "ចំនួនអ្នកកែច្នៃសរុប (នាក់)": "Total Processors (people)",
        "ចំនួនស្រី្តជាអ្នកកែច្នៃ (នាក់)": "Female Processors (people)"
    }
    df.rename(columns=column_rename_map, inplace=True)
    
    return df

def filter_data(df, date_range=None, provinces=None, inspectorates=None):
    if df.empty:
        return df
    today = datetime.today()
    # Filter by Date
    if date_range == 'Today':
        df = df[df['Date'] == today.strftime('%Y-%m-%d')]
    elif date_range == 'Last 7 Days':
        start = today - timedelta(days=7)
        df = df[pd.to_datetime(df['Date'], errors='coerce') >= start]
    elif date_range == 'Last Month':
        start = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        end = today.replace(day=1) - timedelta(days=1)
        df = df[(pd.to_datetime(df['Date'], errors='coerce') >= start) & (pd.to_datetime(df['Date'], errors='coerce') <= end)]
    elif date_range == 'Last 3 Months':
        start = today - timedelta(days=90)
        df = df[pd.to_datetime(df['Date'], errors='coerce') >= start]
    elif date_range == 'Last 12 Months':
        start = today - timedelta(days=365)
        df = df[pd.to_datetime(df['Date'], errors='coerce') >= start]
    

    # Filter by Province
    if provinces:
        df = df[df['Province'].isin(provinces)]

    # Filter by Inspectorate
    if inspectorates:
        df = df[df['Inspectorate'].isin(inspectorates)]

    return df
def pivot_data(df):
    if 'Province' in df.columns and 'Date' in df.columns:
        all_dates = sorted(df['Date'].dropna().unique())
        all_provinces = sorted(df['Province'].dropna().unique())
        pivot_df = df.pivot_table(index='Province', columns='Date', aggfunc='size', fill_value=0)
        pivot_df['Row totals'] = pivot_df.sum(axis=1)
        grand_totals = pivot_df.sum(axis=0)
        grand_totals.name = 'Grand totals'
        pivot_df = pd.concat([pivot_df, grand_totals.to_frame().T])
        pivot_df = pivot_df.reset_index()
        return pivot_df
    else:
        return df
def dashboard():
    st.set_page_config(
        page_title="DCx Co., Ltd",
        page_icon="https://dcxsea.com/asset/images/logo/LOGO_DCX.png",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; margin-top: -40px; margin-bottom: 20px;">
        <img src="https://dcxsea.com/asset/images/logo/LOGO_DCX.png" style="width: 200px; margin-right: 15px;">
        <h4 style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; color: white; margin-bottom: -90px;">DCx Co., Ltd</h4>
    </div>
    """, unsafe_allow_html=True)

    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    # Header section
    st.markdown("""
        <div style="display: flex; align-items: center;">
            <img src="https://cdn3d.iconscout.com/3d/free/thumb/free-line-chart-growth-3814121-3187502.png" alt="logo" style="width: 70px; margin-right: 15px;">
            <h5 style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; margin-top: 25px;">ប្រព័ន្ធគ្រប់គ្រងព័ត៌មានជលផល(Fisheries Information Management System (FIMS))</h5>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Google Sheets URL (the one you want to fetch data from directly)
    google_sheet_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTDG2d2dfb6GHeGUy-nULaIkY26I1cbDA0vMnuyEXFS2vpqtU8E_0kfPCMGtxPXv_w8Vp8bXytV5ipN/pub?gid=680814381&output=csv'
    df = fetch_data(google_sheet_url)
    if not df.empty:
        df = process_and_clean_data(df)  # Apply cleaning and renaming here

        # Check if 'Province' exists after cleaning
        if 'Province' in df.columns:
            # Filters
            date_range = st.selectbox("Select Date Range", ['All', 'Today', 'Last 7 Days', 'Last Month', 'Last 3 Months', 'Last 12 Months'])
            provinces = st.multiselect("Select Province", options=df['Province'].dropna().unique())
            inspectorates = st.multiselect("Select Inspectorate", options=df['Inspectorate'].dropna().unique())

            # Filter data
            filtered_data = filter_data(df, date_range, provinces, inspectorates)
            pivot_df = pivot_data(filtered_data)
            

            # Display table
            st.dataframe(pivot_df)
        else:
            st.error("'Province' column is missing from the cleaned data.")
    else:
        st.warning("No data available to display.")

