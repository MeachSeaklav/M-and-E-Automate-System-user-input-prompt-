import streamlit as st
import pandas as pd
import os
import openai
from dotenv import load_dotenv
from zip import create_zip_file
from telegram import send_to_telegram
from report_generation import generate_report_with_chatgpt

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key from environment variable
openai.api_key = st.secrets["OPENAI_API_KEY"]

def fetch_data(google_sheet_url):
    try:
        df = pd.read_csv(google_sheet_url)
    except Exception as e:
        st.error(f"Failed to fetch data from Google Sheets: {e}")
        return None
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
            <h5 style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; margin-top: 25px;">Baseline Data for LASED III Project</h5>
        </div>
    """, unsafe_allow_html=True)

    # Google Sheets URL (the one you want to fetch data from directly)
    google_sheet_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vR7xZrIXgZ8FzGeFvj9QbIgI17fKH-zw51rdfHybGQ-bQ4SfKIn3hMJ2L0LmUx8eWNF5ce9auCxQIlI/pub?gid=1504298294&single=true&output=csv'

    # Fetch the data from the predefined Google Sheet
    df = fetch_data(google_sheet_url)

    # Main page layout
    col1, col2 = st.columns([3, 1])

    # Left column for displaying data
    with col1:
        if df is not None:
            # Convert DataFrame to HTML without the index
            html_table = df.to_html(index=False, classes='custom-table', escape=False)

            # Add custom CSS to style the table with your desired background color and no space around it
            st.markdown("""
                <style>
                .table-container {
                    margin: 0px; 
                    border-radius: 10px;
                    height: 380px;
                    width: 1010px;
                    overflow: auto;
                }
                .custom-table {
                    width: 100%;
                    border-collapse: collapse;
                    font-family: Khmer OS Content Regular;
                    font-size: 14px;
                    background-color: rgb(161, 219, 255, 0.3);  /* Light background color for table body */
                    color: white;  
                }
                .custom-table th, .custom-table td {
                    white-space: nowrap;  /* Ensure text stays on one line */
                    text-overflow: ellipsis;  /* Add ellipsis if content overflows */
                    overflow: hidden;  /* Hide overflow content */
                    padding: 8px;
                    text-align: left;
                }
                .custom-table th {
                    margin: 0px; 
                    top: 0px;
                    background-color: black; 
                    color: white; 
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    font-weight: bold; 
                    position: sticky;
                    top: 0; 
                    z-index: 1;
                }
                .custom-table td {
                    background-color: rgb(161, 219, 255, 0.3); /* Lighter stripe for alternating rows */
                    border: 1px solid rgba(255, 255, 255, 0.1); /* Border for cells */
                }
                
                .custom-table td:first-child, .custom-table th:first-child {
                    margin: 0px; 
                    position: sticky;
                    border: 1px none rgba(255, 255, 255, 0.1);
                    left: 0; 
                    background-color: black; 
                    z-index: 1;
                }
                </style>
            """, unsafe_allow_html=True)

            # Wrap the table in a scrollable container
            st.markdown(f"""
                <div class="table-container">
                    {html_table}
                </div>
            """, unsafe_allow_html=True)

    # Right column for prompt input and actions
    with col2:

        # Custom CSS for the text area targeting the correct Streamlit class
        st.markdown("""
            <style>
            div.stTextArea textarea {
                color: white;
                font-size: 16px;
                border-radius: 10px;
                padding: 10px;
                width: 100% !important;
                height: 200px !important;
                border: 1px solid #ccc;
                box-sizing: border-box;
            }
            div.stTextArea textarea:focus {
                border-color: #005000;
                outline: none;
            }
            </style>
        """, unsafe_allow_html=True)

        # Text area input
        user_prompt = st.text_area("How can I assist you?", key="prompt_input_key")

        # Custom CSS for the button
        st.markdown("""
             <style>
             div.stDownloadButton > button, div.stButton > button {
                background-color: #006400;
                color: white;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
                border: none;
                cursor: pointer;
             }
             div.stDownloadButton > button:hover, div.stButton > button:hover {
                background-color: #005000;
                color: #DFFF00;
             }
             </style>
        """, unsafe_allow_html=True)

        if st.button('Generate Report'):
            if not user_prompt.strip():
                st.error("Please enter a prompt to generate the report.")
            else:
                df_cleaned = df.fillna('') if df is not None else None
                if df_cleaned is None:
                    st.error("No data available to generate the report.")
                else:
                    report_title = "Generated Report"
                    report_content, word_filename, pdf_filename = generate_report_with_chatgpt(df_cleaned, report_title, user_prompt)

                    try:
                        if report_content:
                            # Store the report content in session state
                            st.session_state['report_content'] = report_content
                            zip_filename = f'Report.zip'
                            create_zip_file(word_filename, pdf_filename, zip_filename)

                            # st.session_state['report_content'] = report_content
                            st.session_state['zip_filename'] =  zip_filename  # or zip_filename, depending on your choice
                            st.session_state['word_filename'] = word_filename
                            st.session_state['pdf_filename'] = pdf_filename

                            # st.success("Report generated and zip file created successfully.")
                        else:
                            st.error("Failed to generate report.")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")


    # Access the stored report content for reuse
    if 'report_content' in st.session_state:
        st.write(st.session_state['report_content'])

        col_button1, col_button2 = st.columns([1, 8])

        # Custom CSS for both buttons
        st.markdown("""
             <style>
             div.stDownloadButton > button {
                background-color: #006400;
                color: white;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
                border: none;
                cursor: pointer;
                }
             div.stDownloadButton > button:hover {
                background-color: #005000;
                color: #DFFF00;
                }
              </style>
        """, unsafe_allow_html=True)

        # Column 1 - Download Button
        with col_button1:
            if 'word_filename' in st.session_state:
                word_filename = st.session_state['word_filename']
                # Ensure that the file exists before trying to open it
                if os.path.exists(word_filename):
                    with open(word_filename, 'rb') as file:
                        st.download_button(
                            label="Download Report",
                            data=file,
                            file_name=word_filename,
                            mime='application/zip'
                        )
                else:
                    st.error("The zip file could not be found.")

        # Column 2 - Telegram Button
        with col_button2:
            if st.button('Telegram'):
                if 'word_filename' in st.session_state and 'pdf_filename' in st.session_state:
                    word_filename = st.session_state['word_filename']
                    # pdf_filename = st.session_state['pdf_filename']

                    try:
                        # Send report to Telegram
                        send_to_telegram(word_filename, f"Here is your generated report (Word).")
                        # send_to_telegram(pdf_filename, f"Here is your generated report (PDF).")
                        # st.success("Report sent to Telegram successfully!")
                    except Exception as e:
                        st.error(f"Failed to send report to Telegram: {e}")
                else:
                    st.error("Report not found in session state.")
