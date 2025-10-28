import pandas as pd
import streamlit as st
from io import StringIO, BytesIO

def get_inventory_data():
    """
    get inventory data from url or uploaded file.
    """
    data_source = st.radio("📊 data resourcse:", ["upload CSV/Excel", "Google Sheet (published)"])

    if data_source == "upload CSV/Excel":
        uploaded = st.file_uploader("upload inventory file", type=["csv", "xlsx"])
        if uploaded:
            if uploaded.name.endswith(".csv"):
                df = pd.read_csv(StringIO(uploaded.getvalue().decode("utf-8")))
            else:
                df = pd.read_excel(BytesIO(uploaded.getvalue()))
            return df
        else:
            st.info("⏳ please upload a csv file")
            return None

    else:
        sheet_url = st.text_input("🔗 enter csv sheet url from google sheet:")
        if sheet_url:
            try:
                df = pd.read_csv(sheet_url)
                return df
            except Exception as e:
                st.error(f"❌ error when reading Google Sheet: {e}")
                return None
        else:
            st.info("⏳ please enter csv sheet link")
            return None


def get_low_stock_items(df):
    """
   filter items that under threshold.
    """
    if {"on_hand_qty", "reorder_threshold"}.issubset(df.columns):
        low_stock = df[df["on_hand_qty"] < df["reorder_threshold"]]
        return low_stock
    else:
        st.error("not found columns!: on_hand_qty و reorder_threshold")
        return pd.DataFrame()
