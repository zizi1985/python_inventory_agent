import streamlit as st
from inventory_checker import get_inventory_data, get_low_stock_items
from llm_agent import draft_purchase_order
from email_utils import send_approval_request, send_email

st.set_page_config(page_title="🤖 AI Reorder Assistant", page_icon="🤖", layout="wide")
st.title("🤖 AI Reorder Assistant Agent")

df = get_inventory_data()

if df is not None:
    st.success("✅ uploaded data.")
    st.dataframe(df)

    low_stock = get_low_stock_items(df)

    if not low_stock.empty:
        st.warning(f"⚠️ {len(low_stock)} items need to be reordered.")
        st.dataframe(low_stock)

        for _, item in low_stock.iterrows():
            with st.expander(f"{item['sku']} | inventory: {item['on_hand_qty']}"):
                st.write(f"Producer: {item.get('supplier', 'unKnown')}")
                st.write(f"order count: {item.get('reorder_qty', 0)}")

                if st.button(f"🧾 produce order  ({item['sku']})"):
                    po = draft_purchase_order(item)
                    st.code(po, language="markdown")
                    if st.button(f"📨 snd order to producer ({item['sku']})"):
                        send_email(item["supplier_email"], f"Purchase Order for {item['sku']}", po)
                        st.success("✅ sent order.")
    else:
        st.info("📦 no item under threshold.")
