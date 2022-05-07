import openpyxl
import gspread
import oauth2client
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import plotly.express as px
import streamlit as st
import openpyxl

from gsheetsdb import connect

scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open("[iCare] Shopify API (Marek Test)")

# data = sheet.worksheet("Overview")
# print(sheet)

sheet_id = "1ABO9kYFPxsthZBu7ll2jaJ8s"
sheet_name = "109287710"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}-gDh16CxMNatGIks2RI/edit#gid={sheet_name}"

st.set_page_config(page_title="Sales Dashboard",
                    page_icon=":bar_chart:",
                    layout="wide")

conn = connect(creds=creds)

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=5)
    rows = rows.fetchall()
    return rows

# sheet_url = st.secrets("https://docs.google.com/spreadsheets/d/1ABO9kYFPxsthZBu7ll2jaJ8s-gDh16CxMNatGIks2RI/edit#gid=1278083210")
rows = run_query(f'SELECT * FROM "{url}"')

# Print results.
for row in rows:
    st.write(f"{row.name} has a :{row.pet}:")