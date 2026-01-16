import streamlit as st
import pandas as pd
import urllib.parse
from pathlib import Path
from datetime import datetime
import uuid
import json
import os
import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

# ================== LOAD ENV ================== #
load_dotenv()

# ================== GOOGLE SHEETS ================== #
SHEET_ID = "1TsxO6Cy1bZpN-RjA_E8ZuxY9YSNJeU5lnf6jPkGbLEY"
SHEET_NAME = "orders"

@st.cache_resource
def connect_orders_sheet():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    # 🔐 Build credentials dict from ENV
    service_account_info = {
        "type": os.getenv("GOOGLE_TYPE"),
        "project_id": os.getenv("GOOGLE_PROJECT_ID"),
        "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
        "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace("\\n", "\n"),
        "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
        "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_CERT_URL"),
        "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_CERT_URL"),
    }

    creds = Credentials.from_service_account_info(
        service_account_info,
        scopes=scope
    )

    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)


def save_order(product, company, rate, quantity, area):
    sheet = connect_orders_sheet()
    sheet.append_row([
        str(uuid.uuid4())[:8],
        product,
        company,
        rate,
        quantity,
        rate * quantity,
        area,
        "NEW",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ])

# ================== PRODUCT DATA ================== #
DATA_DIR = Path("data")
EXCEL_FILE = DATA_DIR / "multiple.xlsx"
OPTIONAL_COLUMNS = ["SIZE", "HEIGHT", "WEIGHT"]

@st.cache_data
def load_products():
    df = pd.read_excel(EXCEL_FILE)
    df.columns = [c.strip().upper() for c in df.columns]

    for col in OPTIONAL_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA
        df[col] = df[col].apply(
            lambda x: pd.NA if pd.isna(x) or str(x).strip() == "" else x
        )

    df["RATE"] = pd.to_numeric(df["RATE"], errors="coerce")
    return df.dropna(subset=["PRODUCT_NAME", "COMPANY", "RATE"])

# ================== APP ================== #
st.set_page_config("Product Ordering System", layout="wide")
st.title("📦 Product Comparison & Ordering")

df = load_products()

# ================== AREA → WHATSAPP ================== #
AREA_TO_WHATSAPP = {
    "Mumbai": ["919106861749", "918780701769"],
    "Delhi": ["918866296663"],
    "Bangalore": ["918888888888"],
}

selected_area = st.selectbox("📍 Select Area", AREA_TO_WHATSAPP.keys())
active_numbers = AREA_TO_WHATSAPP[selected_area]

# ================== FILTERS ================== #
cols = st.columns(5)

products = cols[0].multiselect(
    "Product", sorted(df["PRODUCT_NAME"].unique())
)

companies = cols[1].multiselect(
    "Company", sorted(df["COMPANY"].unique())
)

product_selected = len(products) > 0

filtered = df.copy()

if product_selected:
    filtered = filtered[filtered["PRODUCT_NAME"].isin(products)]

if companies:
    filtered = filtered[filtered["COMPANY"].isin(companies)]

sizes, heights, weights = [], [], []

if product_selected:
    if filtered["SIZE"].notna().any():
        sizes = cols[2].multiselect(
            "Size", sorted(filtered["SIZE"].dropna().unique())
        )

    if filtered["HEIGHT"].notna().any():
        heights = cols[3].multiselect(
            "Height", sorted(filtered["HEIGHT"].dropna().unique())
        )

    if filtered["WEIGHT"].notna().any():
        weights = cols[4].multiselect(
            "Weight", sorted(filtered["WEIGHT"].dropna().unique())
        )

if sizes:
    filtered = filtered[filtered["SIZE"].isin(sizes)]

if heights:
    filtered = filtered[filtered["HEIGHT"].isin(heights)]

if weights:
    filtered = filtered[filtered["WEIGHT"].isin(weights)]

if filtered.empty:
    st.warning("No products found")
    st.stop()

# ================== SESSION STATE ================== #
st.session_state.setdefault("buy_row", None)
st.session_state.setdefault("order_saved", False)
st.session_state.setdefault("last_order_data", None)

# ================== PRODUCT TABLE ================== #
st.subheader("Products")

for idx, row in filtered.iterrows():
    col1, col2, col3, col4, col5, col6 = st.columns([2,2,2,1,1,1])

    col1.write(row["COMPANY"])
    col2.write(row["COMPANY_CODE_NAME"])
    col3.write(row["PRODUCT_CODE_NUMBER"])
    col4.write(row["SIZE"] if pd.notna(row["SIZE"]) else "")
    col5.write(f"₹{row['RATE']}")

    if col6.button("🛒 Buy", key=f"buy_{idx}"):
        st.session_state.buy_row = row
        st.session_state.order_saved = False

# ================== BUY POPUP ================== #
if st.session_state.buy_row is not None:
    st.divider()
    st.subheader("🛒 Confirm Order")

    row = st.session_state.buy_row
    quantity = st.number_input("Quantity", min_value=1, step=1)

    if st.button("✅ Confirm Order"):
        save_order(
            row["COMPANY_CODE_NAME"],
            row["COMPANY"],
            row["RATE"],
            quantity,
            selected_area,
        )

        message = f"""
New Order 📦
Area: {selected_area}
Product: {row['COMPANY_CODE_NAME']}
Company: {row['COMPANY']}
Quantity: {quantity}
Rate: ₹{row['RATE']}
Total: ₹{row['RATE'] * quantity}
"""

        st.session_state.last_order_data = {
            "message": urllib.parse.quote(message),
            "dealers": active_numbers,
        }

        st.session_state.order_saved = True
        st.session_state.buy_row = None
        st.success("✅ Order saved successfully")

# ================== DEALER SELECTION ================== #
if st.session_state.order_saved and st.session_state.last_order_data:
    st.divider()
    st.subheader("📨 Send Order to Dealer")

    dealers = st.session_state.last_order_data["dealers"]
    encoded_msg = st.session_state.last_order_data["message"]

    cols = st.columns(len(dealers))
    for i, num in enumerate(dealers):
        with cols[i]:
            st.markdown(
                f"""
                <a href="https://wa.me/{num}?text={encoded_msg}" target="_blank">
                <button style="width:100%;padding:12px;background:#25D366;color:white;
                border:none;border-radius:8px;font-size:16px;">
                Send to {num}
                </button>
                </a>
                """,
                unsafe_allow_html=True,
            )

    if st.button("❌ Cancel"):
        st.session_state.order_saved = False
        st.session_state.last_order_data = None

st.caption("Powered by Streamlit • Google Sheets • WhatsApp")
