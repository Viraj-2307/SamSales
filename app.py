# import streamlit as st
# import pandas as pd
# from pathlib import Path

# # ================= CONFIG ================= #
# DATA_DIR = Path("data")
# EXCEL_FILE = DATA_DIR / "multiple.xlsx"

# REQUIRED_COLUMNS = [
#     "PRODUCT_NAME",
#     "COMPANY_CODE_NAME",
#     "PRODUCT_CODE_NUMBER",
#     "COMPANY",
#     "SIZE",
#     "HEIGHT",
#     "WEIGHT",
#     "DESCRIPTION",
#     "RATE",
# ]

# OPTIONAL_COLUMNS = ["SIZE", "HEIGHT", "WEIGHT"]

# # ================= UTILS ================= #
# @st.cache_data(show_spinner=False)
# def load_excel():
#     if not EXCEL_FILE.exists():
#         return pd.DataFrame(columns=REQUIRED_COLUMNS + OPTIONAL_COLUMNS)

#     df = pd.read_excel(EXCEL_FILE)
#     df.columns = [c.strip().upper() for c in df.columns]

#     # Ensure required columns exist
#     missing_required = set(REQUIRED_COLUMNS) - set(df.columns)
#     if missing_required:
#         st.error(f"Missing REQUIRED columns: {missing_required}")
#         return pd.DataFrame(columns=REQUIRED_COLUMNS + OPTIONAL_COLUMNS)

#     # Add optional columns if missing
#     for col in OPTIONAL_COLUMNS:
#         if col not in df.columns:
#             df[col] = None

#     df["RATE"] = pd.to_numeric(df["RATE"], errors="coerce")

#     return df.dropna(subset=["PRODUCT_NAME", "COMPANY", "RATE"])

# def clean_unique(series):
#     """Return sorted unique values without NaN"""
#     return sorted(series.dropna().unique())


# def format_description(desc):
#     if not isinstance(desc, str):
#         return []

#     desc = desc.replace("•", ".")
#     return [p.strip() for p in desc.split(".") if p.strip()]


# def highlight_best(row, min_rate):
#     return ["background-color: #d4f7dc" if row["RATE"] == min_rate else "" for _ in row]


# # ================= PAGE ================= #
# st.set_page_config(
#     page_title="Advanced Product Comparison",
#     layout="wide",
# )

# st.title("📊 Advanced Product Rate Comparison")
# st.caption("Smart comparison from a single Excel source")

# df = load_excel()

# if df.empty:
#     st.warning("Excel file is missing or empty.")
#     st.stop()

# # ================= FILTERS ================= #
# col1, col2, col3, col4 = st.columns(4)

# with col1:
#     product = st.selectbox(
#         "🔍 Product",
#         clean_unique(df["PRODUCT_NAME"]),
#         index=None,
#         placeholder="Select product",
#     )

# if product:
#     df_p = df[df["PRODUCT_NAME"] == product]

#     with col2:
#         size = st.selectbox(
#             "📐 Size (Optional)",
#             ["All"] + clean_unique(df_p["SIZE"]),
#             index=0,
#         )

#     with col3:
#         height = st.selectbox(
#             "📏 Height (Optional)",
#             ["All"] + clean_unique(df_p["HEIGHT"]),
#             index=0,
#         )

#     with col4:
#         weight = st.selectbox(
#             "⚖️ Weight (Optional)",
#             ["All"] + clean_unique(df_p["WEIGHT"]),
#             index=0,
#         )

#     # ================= APPLY FILTERS ================= #
#     final_df = df_p.copy()

#     if size != "All":
#         final_df = final_df[final_df["SIZE"] == size]

#     if height != "All":
#         final_df = final_df[final_df["HEIGHT"] == height]

#     if weight != "All":
#         final_df = final_df[final_df["WEIGHT"] == weight]

#     if final_df.empty:
#         st.warning("No matching products found.")
#         st.stop()

#     # Replace NaN display values
#     final_df[["SIZE", "HEIGHT", "WEIGHT"]] = final_df[
#         ["SIZE", "HEIGHT", "WEIGHT"]
#     ].fillna("N/A")

#     # ================= KPIs ================= #
#     st.divider()

#     min_rate = final_df["RATE"].min()
#     max_rate = final_df["RATE"].max()
#     avg_rate = final_df["RATE"].mean()

#     k1, k2, k3 = st.columns(3)
#     k1.metric("🏆 Best Rate", f"₹ {min_rate:,.2f}")
#     k2.metric("📈 Highest Rate", f"₹ {max_rate:,.2f}")
#     k3.metric("📊 Average Rate", f"₹ {avg_rate:,.2f}")

#     # ================= TABLE ================= #
#     st.subheader("💰 Available Options")

#     table_df = final_df[
#         [
#             "COMPANY",
#             "COMPANY_CODE_NAME",
#             "PRODUCT_CODE_NUMBER",
#             "SIZE",
#             "HEIGHT",
#             "WEIGHT",
#             "RATE",
#         ]
#     ].reset_index(drop=True)

#     styled = table_df.style.apply(
#         lambda r: highlight_best(r, min_rate), axis=1
#     )

#     st.dataframe(styled, width='stretch')

#     # ================= BEST VALUE ================= #
#     best_row = final_df.loc[final_df["RATE"].idxmin()]

#     st.success(
#         f"🏆 **Best Value:** {best_row['COMPANY']} – "
#         f"{best_row['COMPANY_CODE_NAME']} at ₹ {best_row['RATE']:,.2f}"
#     )

#     # ================= DESCRIPTION ================= #
#     st.subheader("📄 Product Descriptions")

#     for _, row in final_df.iterrows():
#         with st.expander(
#             f"{row['COMPANY']} • {row['COMPANY_CODE_NAME']} • ₹ {row['RATE']:,.2f}"
#         ):
#             bullets = format_description(row["DESCRIPTION"])
#             if bullets:
#                 for b in bullets:
#                     st.markdown(f"- {b}")
#             else:
#                 st.write("No description available.")

#     # ================= CHART ================= #
#     st.subheader("📈 Rate Comparison")
#     chart_df = final_df[["COMPANY", "RATE"]].set_index("COMPANY")
#     st.bar_chart(chart_df)

#     # ================= EXPORT ================= #
#     st.subheader("⬇️ Download Comparison")

#     csv = table_df.to_csv(index=False).encode("utf-8")
#     st.download_button(
#         "Download as CSV",
#         csv,
#         "product_comparison.csv",
#         "text/csv",
#     )

# # ================= FOOTER ================= #
# st.divider()
# st.caption("Powered by Streamlit • Single Excel Architecture")

# import streamlit as st
# import urllib.parse
# import pandas as pd
# from pathlib import Path
# import os

# # ================= CONFIG ================= #
# DATA_DIR = Path("data")
# EXCEL_FILE = DATA_DIR / "multiple.xlsx"

# REQUIRED_COLUMNS = [
#     "PRODUCT_NAME",
#     "COMPANY_CODE_NAME",
#     "PRODUCT_CODE_NUMBER",
#     "COMPANY",
#     "DESCRIPTION",
#     "RATE",
# ]

# OPTIONAL_COLUMNS = ["SIZE", "HEIGHT", "WEIGHT"]

# # ================= UTILS ================= #
# @st.cache_data(show_spinner=False)
# def load_excel():
#     if not EXCEL_FILE.exists():
#         return pd.DataFrame(columns=REQUIRED_COLUMNS + OPTIONAL_COLUMNS)

#     df = pd.read_excel(EXCEL_FILE)
#     df.columns = [c.strip().upper() for c in df.columns]

#     missing_required = set(REQUIRED_COLUMNS) - set(df.columns)
#     if missing_required:
#         st.error(f"Missing REQUIRED columns: {missing_required}")
#         return pd.DataFrame(columns=REQUIRED_COLUMNS + OPTIONAL_COLUMNS)

#     for col in OPTIONAL_COLUMNS:
#         if col not in df.columns:
#             df[col] = None

#     df["RATE"] = pd.to_numeric(df["RATE"], errors="coerce")

#     return df.dropna(subset=["PRODUCT_NAME", "COMPANY", "RATE"])


# def clean_unique(series):
#     return sorted(series.dropna().unique())


# def format_description(desc):
#     if not isinstance(desc, str):
#         return []
#     desc = desc.replace("•", ".")
#     return [p.strip() for p in desc.split(".") if p.strip()]


# def highlight_best(row, min_rate):
#     return ["background-color: #d4f7dc" if row["RATE"] == min_rate else "" for _ in row]

# # ================= PAGE ================= #
# st.set_page_config(page_title="Advanced Product Comparison", layout="wide")

# st.title("📊 Advanced Product Rate Comparison")
# st.caption("Multi-select smart comparison from a single Excel source")

# df = load_excel()

# if df.empty:
#     st.warning("Excel file is missing or empty.")
#     st.stop()

# # ================= FILTERS (MULTI SELECT) ================= #
# col1, col2, col3, col4, col5 = st.columns(5)

# with col1:
#     products = st.multiselect(
#         "🔍 Product",
#         clean_unique(df["PRODUCT_NAME"]),
#     )

# with col2:
#     companies = st.multiselect(
#         "🏭 Company",
#         clean_unique(df["COMPANY"]),
#     )

# with col3:
#     sizes = st.multiselect(
#         "📐 Size",
#         clean_unique(df["SIZE"]),
#     )

# with col4:
#     heights = st.multiselect(
#         "📏 Height",
#         clean_unique(df["HEIGHT"]),
#     )

# with col5:
#     weights = st.multiselect(
#         "⚖️ Weight",
#         clean_unique(df["WEIGHT"]),
#     )

# # ================= APPLY FILTERS ================= #
# final_df = df.copy()

# if products:
#     final_df = final_df[final_df["PRODUCT_NAME"].isin(products)]

# if companies:
#     final_df = final_df[final_df["COMPANY"].isin(companies)]

# if sizes:
#     final_df = final_df[final_df["SIZE"].isin(sizes)]

# if heights:
#     final_df = final_df[final_df["HEIGHT"].isin(heights)]

# if weights:
#     final_df = final_df[final_df["WEIGHT"].isin(weights)]

# if final_df.empty:
#     st.warning("No matching products found.")
#     st.stop()

# final_df[["SIZE", "HEIGHT", "WEIGHT"]] = final_df[
#     ["SIZE", "HEIGHT", "WEIGHT"]
# ].fillna("N/A")

# # ================= KPIs ================= #
# st.divider()

# min_rate = final_df["RATE"].min()
# max_rate = final_df["RATE"].max()
# avg_rate = final_df["RATE"].mean()

# k1, k2, k3 = st.columns(3)
# k1.metric("🏆 Best Rate", f"₹ {min_rate:,.2f}")
# k2.metric("📈 Highest Rate", f"₹ {max_rate:,.2f}")
# k3.metric("📊 Average Rate", f"₹ {avg_rate:,.2f}")

# # ================= TABLE ================= #
# st.subheader("💰 Available Options")

# table_df = final_df[
#     [
#         "COMPANY",
#         "COMPANY_CODE_NAME",
#         "PRODUCT_CODE_NUMBER",
#         "SIZE",
#         "HEIGHT",
#         "WEIGHT",
#         "RATE",
#     ]
# ].reset_index(drop=True)

# styled = table_df.style.apply(
#     lambda r: highlight_best(r, min_rate), axis=1
# )

# st.dataframe(styled, width='stretch')

# # ================= BEST VALUE ================= #
# best_row = final_df.loc[final_df["RATE"].idxmin()]

# st.success(
#     f"🏆 **Best Value:** {best_row['COMPANY']} – "
#     f"{best_row['COMPANY_CODE_NAME']} at ₹ {best_row['RATE']:,.2f}"
# )

# # ================= DESCRIPTION ================= #
# st.subheader("📄 Product Descriptions")

# for _, row in final_df.iterrows():
#     with st.expander(
#         f"{row['COMPANY']} • {row['COMPANY_CODE_NAME']} • ₹ {row['RATE']:,.2f}"
#     ):
#         bullets = format_description(row["DESCRIPTION"])
#         if bullets:
#             for b in bullets:
#                 st.markdown(f"- {b}")
#         else:
#             st.write("No description available.")

# # ================= CHART ================= #
# st.subheader("📈 Rate Comparison")
# chart_df = final_df.groupby("COMPANY")["RATE"].min()
# st.bar_chart(chart_df)

# # ================= PURCHASE ================= #
# st.subheader("🛒 Purchase")

# if "show_order" not in st.session_state:
#     st.session_state.show_order = False

# if st.button("🛒 Buy Now", type="primary"):
#     st.session_state.show_order = True

# # ================= ORDER BOX (MODAL REPLACEMENT) ================= #
# if st.session_state.show_order:
#     st.divider()
#     st.subheader("✅ Confirm Purchase")

#     st.markdown(
#         f"""
#         **Product:** {best_row['COMPANY_CODE_NAME']}  
#         **Company:** {best_row['COMPANY']}  
#         **Rate:** ₹ {best_row['RATE']:,.2f}
#         """
#     )

#     quantity = st.number_input("Enter Quantity", min_value=1, step=1)

#     col1, col2 = st.columns(2)

#     with col1:
#         if st.button("✅ Confirm Order"):
#             message = (
#                 f"🛒 New Order\n\n"
#                 f"Product: {best_row['COMPANY_CODE_NAME']}\n"
#                 f"Company: {best_row['COMPANY']}\n"
#                 f"Quantity: {quantity}\n"
#                 f"Rate: ₹ {best_row['RATE']:,.2f}\n"
#                 f"Total: ₹ {best_row['RATE'] * quantity:,.2f}"
#             )

#             encoded_msg = urllib.parse.quote(message)

#             phone_numbers = [
#                 "919106861749",
#                 "918780701769",
#             ]

#             st.success("📲 Send order via WhatsApp")

#             for num in phone_numbers:
#                 st.markdown(
#                     f"""
#                     <a href="https://wa.me/{num}?text={encoded_msg}" target="_blank">
#                         <button style="padding:10px 16px; background:#25D366; color:white;
#                         border:none; border-radius:6px; font-size:16px; cursor:pointer;">
#                             Send to {num}
#                         </button>
#                     </a>
#                     """,
#                     unsafe_allow_html=True,
#                 )

#             st.session_state.show_order = False

#     with col2:
#         if st.button("❌ Cancel"):
#             st.session_state.show_order = False

# # ================= FOOTER ================= #
# st.divider()
# st.caption("Powered by Streamlit • Excel Product Comparison")


# import streamlit as st
# import pandas as pd
# import urllib.parse
# from pathlib import Path
# from datetime import datetime
# import uuid

# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# # ================== GOOGLE SHEETS ================== #
# @st.cache_resource
# def connect_orders_sheet():
#     scope = [
#         "https://spreadsheets.google.com/feeds",
#         "https://www.googleapis.com/auth/drive",
#     ]
#     creds = ServiceAccountCredentials.from_json_keyfile_name(
#         "credentials.json", scope
#     )
#     client = gspread.authorize(creds)
#     return client.open("Orders").worksheet("orders")


# def save_order(product, company, rate, quantity):
#     sheet = connect_orders_sheet()
#     sheet.append_row(
#         [
#             str(uuid.uuid4())[:8],
#             product,
#             company,
#             rate,
#             quantity,
#             rate * quantity,
#             "NEW",
#             datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         ]
#     )


# def load_orders():
#     sheet = connect_orders_sheet()
#     return pd.DataFrame(sheet.get_all_records())


# def update_order_status(order_id, status):
#     sheet = connect_orders_sheet()
#     orders = pd.DataFrame(sheet.get_all_records())
#     idx = orders.index[orders["ORDER_ID"] == order_id][0] + 2
#     sheet.update_cell(idx, 7, status)


# # ================== PRODUCT DATA ================== #
# DATA_DIR = Path("data")
# EXCEL_FILE = DATA_DIR / "multiple.xlsx"

# REQUIRED_COLUMNS = [
#     "PRODUCT_NAME",
#     "COMPANY_CODE_NAME",
#     "PRODUCT_CODE_NUMBER",
#     "COMPANY",
#     "DESCRIPTION",
#     "RATE",
# ]

# OPTIONAL_COLUMNS = ["SIZE", "HEIGHT", "WEIGHT"]


# @st.cache_data
# def load_products():
#     df = pd.read_excel(EXCEL_FILE)
#     df.columns = [c.strip().upper() for c in df.columns]

#     for col in OPTIONAL_COLUMNS:
#         if col not in df.columns:
#             df[col] = None

#     df["RATE"] = pd.to_numeric(df["RATE"], errors="coerce")
#     return df.dropna(subset=["PRODUCT_NAME", "COMPANY", "RATE"])


# # ================== APP ================== #
# st.set_page_config("Product Ordering System", layout="wide")
# st.title("📦 Product Comparison & Ordering")

# df = load_products()

# # ================== FILTERS ================== #
# col1, col2, col3, col4, col5 = st.columns(5)

# products = col1.multiselect("Product", sorted(df["PRODUCT_NAME"].unique()))
# companies = col2.multiselect("Company", sorted(df["COMPANY"].unique()))
# sizes = col3.multiselect("Size", sorted(df["SIZE"].dropna().unique()))
# heights = col4.multiselect("Height", sorted(df["HEIGHT"].dropna().unique()))
# weights = col5.multiselect("Weight", sorted(df["WEIGHT"].dropna().unique()))

# filtered = df.copy()
# if products:
#     filtered = filtered[filtered["PRODUCT_NAME"].isin(products)]
# if companies:
#     filtered = filtered[filtered["COMPANY"].isin(companies)]
# if sizes:
#     filtered = filtered[filtered["SIZE"].isin(sizes)]
# if heights:
#     filtered = filtered[filtered["HEIGHT"].isin(heights)]
# if weights:
#     filtered = filtered[filtered["WEIGHT"].isin(weights)]

# if filtered.empty:
#     st.warning("No products found")
#     st.stop()

# # ================== BEST PRODUCT ================== #
# best = filtered.loc[filtered["RATE"].idxmin()]

# st.success(
#     f"🏆 Best Option: **{best['COMPANY']} – {best['COMPANY_CODE_NAME']}** @ ₹{best['RATE']}"
# )

# st.dataframe(
#     filtered[
#         [
#             "COMPANY",
#             "COMPANY_CODE_NAME",
#             "PRODUCT_CODE_NUMBER",
#             "SIZE",
#             "HEIGHT",
#             "WEIGHT",
#             "RATE",
#         ]
#     ],
#     width='stretch',
# )

# # ================== BUY ================== #
# st.divider()
# st.subheader("🛒 Place Order")

# quantity = st.number_input("Quantity", min_value=1, step=1)

# if st.button("🛒 Buy Now", type="primary"):
#     save_order(
#         best["COMPANY_CODE_NAME"],
#         best["COMPANY"],
#         best["RATE"],
#         quantity,
#     )

#     message = f"""
# New Order 📦

# Product: {best['COMPANY_CODE_NAME']}
# Company: {best['COMPANY']}
# Quantity: {quantity}
# Rate: ₹{best['RATE']}
# Total: ₹{best['RATE'] * quantity}
# """
#     encoded = urllib.parse.quote(message)

#     for num in ["919106861749", "918780701769"]:
#         st.markdown(
#             f"""
#             <a href="https://wa.me/{num}?text={encoded}" target="_blank">
#             <button style="padding:10px;background:#25D366;color:white;border:none;border-radius:6px">
#             Send to {num}
#             </button></a>
#             """,
#             unsafe_allow_html=True,
#         )

# st.caption("Powered by Streamlit • Google Sheets • WhatsApp Click-to-Chat")

# import streamlit as st
# import pandas as pd
# import urllib.parse
# from pathlib import Path
# from datetime import datetime
# import uuid

# import gspread,json
# from google.oauth2.service_account import Credentials
# from oauth2client.service_account import ServiceAccountCredentials

# # ================== GOOGLE SHEETS ================== #
# SHEET_ID = "1TsxO6Cy1bZpN-RjA_E8ZuxY9YSNJeU5lnf6jPkGbLEY"
# SHEET_NAME = "orders"

# @st.cache_resource
# def connect_orders_sheet():
#     scope = [
#         "https://www.googleapis.com/auth/spreadsheets",
#         "https://www.googleapis.com/auth/drive",
#     ]

#     with open("credentials.json") as f:
#         info = json.load(f)

#     creds = Credentials.from_service_account_info(info, scopes=scope)
#     client = gspread.authorize(creds)

#     return client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

# def save_order(product, company, rate, quantity, area):
#     sheet = connect_orders_sheet()
#     sheet.append_row(
#         [
#             str(uuid.uuid4())[:8],
#             product,
#             company,
#             rate,
#             quantity,
#             rate * quantity,
#             area,
#             "NEW",
#             datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         ]
#     )

# # ================== PRODUCT DATA ================== #
# DATA_DIR = Path("data")
# EXCEL_FILE = DATA_DIR / "multiple.xlsx"
# OPTIONAL_COLUMNS = ["SIZE", "HEIGHT", "WEIGHT"]

# @st.cache_data
# def load_products():
#     df = pd.read_excel(EXCEL_FILE)
#     df.columns = [c.strip().upper() for c in df.columns]

#     # Ensure optional columns exist
#     for col in OPTIONAL_COLUMNS:
#         if col not in df.columns:
#             df[col] = pd.NA

#     # Properly clean optional columns (BLANKS stay NaN)
#     for col in OPTIONAL_COLUMNS:
#         df[col] = (
#             df[col]
#             .apply(lambda x: pd.NA if pd.isna(x) or str(x).strip() == "" else x)
#         )

#     df["RATE"] = pd.to_numeric(df["RATE"], errors="coerce")

#     return df.dropna(subset=["PRODUCT_NAME", "COMPANY", "RATE"])

# # ================== APP ================== #
# st.set_page_config("Product Ordering System", layout="wide")
# st.title("📦 Product Comparison & Ordering")

# df = load_products()

# # ================== AREA → WHATSAPP ================== #
# AREA_TO_WHATSAPP = {
#     "Mumbai": ["919106861749", "918780701769"],
#     "Delhi": ["919999999999"],
#     "Bangalore": ["918888888888"],
# }

# selected_area = st.selectbox("📍 Select Area", AREA_TO_WHATSAPP.keys())
# active_numbers = AREA_TO_WHATSAPP[selected_area]

# # ================== FILTERS ================== #
# cols = st.columns(5)

# products = cols[0].multiselect("Product", sorted(df["PRODUCT_NAME"].unique()))
# companies = cols[1].multiselect("Company", sorted(df["COMPANY"].unique()))
# # sizes = cols[2].multiselect("Size", sorted(df["SIZE"].dropna().unique()))
# # heights = cols[3].multiselect("Height", sorted(df["HEIGHT"].dropna().unique()))
# # weights = cols[4].multiselect("Weight", sorted(df["WEIGHT"].dropna().unique()))
# sizes = (
#     cols[2].multiselect("Size", sorted(df["SIZE"].dropna().unique()))
#     if df["SIZE"].notna().any()
#     else []
# )

# heights = (
#     cols[3].multiselect("Height", sorted(df["HEIGHT"].dropna().unique()))
#     if df["HEIGHT"].notna().any()
#     else []
# )

# weights = (
#     cols[4].multiselect("Weight", sorted(df["WEIGHT"].dropna().unique()))
#     if df["WEIGHT"].notna().any()
#     else []
# )


# filtered = df.copy()
# if products: filtered = filtered[filtered["PRODUCT_NAME"].isin(products)]
# if companies: filtered = filtered[filtered["COMPANY"].isin(companies)]
# if sizes: filtered = filtered[filtered["SIZE"].isin(sizes)]
# if heights: filtered = filtered[filtered["HEIGHT"].isin(heights)]
# if weights: filtered = filtered[filtered["WEIGHT"].isin(weights)]

# if filtered.empty:
#     st.warning("No products found")
#     st.stop()

# # ================== SESSION STATE ================== #
# if "buy_row" not in st.session_state:
#     st.session_state.buy_row = None

# if "order_saved" not in st.session_state:
#     st.session_state.order_saved = False

# if "last_order_data" not in st.session_state:
#     st.session_state.last_order_data = None

# # ================== PRODUCT TABLE ================== #
# st.subheader("Products")

# for idx, row in filtered.iterrows():
#     col1, col2, col3, col4, col5, col6 = st.columns([2,2,2,1,1,1])

#     col1.write(row["COMPANY"])
#     col2.write(row["COMPANY_CODE_NAME"])
#     col3.write(row["PRODUCT_CODE_NUMBER"])
#     if pd.notna(row["SIZE"]):
#         col4.write(row["SIZE"])
#     else:
#         col4.write("")
#     col5.write(f"₹{row['RATE']}")

#     if col6.button("🛒 Buy", key=f"buy_{idx}"):
#         st.session_state.buy_row = row
#         st.session_state.order_saved = False

# # ================== BUY POPUP ================== #
# if st.session_state.buy_row is not None:
#     st.divider()
#     st.subheader("🛒 Confirm Order")

#     row = st.session_state.buy_row

#     quantity = st.number_input(
#         "How much quantity do you want?",
#         min_value=1,
#         step=1,
#     )

#     if st.button("✅ Confirm Order"):
#         save_order(
#             row["COMPANY_CODE_NAME"],
#             row["COMPANY"],
#             row["RATE"],
#             quantity,
#             selected_area,
#         )

#         message = f"""
#     New Order 📦
#     Area: {selected_area}
#     Product: {row['COMPANY_CODE_NAME']}
#     Company: {row['COMPANY']}
#     Quantity: {quantity}
#     Rate: ₹{row['RATE']}
#     Total: ₹{row['RATE'] * quantity}

#     I want to buy this quantity.
#     """

#         st.session_state.last_order_data = {
#             "message": urllib.parse.quote(message),
#             "dealers": active_numbers,
#         }

#         st.session_state.order_saved = True
#         st.session_state.buy_row = None

#         st.success("✅ Order saved successfully")
        
# # ================== DEALER SELECTION POPUP ================== #
# if st.session_state.order_saved and st.session_state.last_order_data:
#     st.divider()
#     st.subheader("📨 Send Order to Dealer")

#     dealers = st.session_state.last_order_data["dealers"]
#     encoded_msg = st.session_state.last_order_data["message"]

#     st.info(f"We have **{len(dealers)} dealers** in {selected_area}. Select one:")

#     cols = st.columns(len(dealers))

#     for i, num in enumerate(dealers):
#         with cols[i]:
#             st.markdown(
#                 f"""
#                 <a href="https://wa.me/{num}?text={encoded_msg}" target="_blank">
#                 <button style="
#                     width:100%;
#                     padding:12px;
#                     background:#25D366;
#                     color:white;
#                     border:none;
#                     border-radius:8px;
#                     font-size:16px;
#                 ">
#                 Send to {num}
#                 </button>
#                 </a>
#                 """,
#                 unsafe_allow_html=True,
#             )

#     if st.button("❌ Cancel"):
#         st.session_state.order_saved = False
#         st.session_state.last_order_data = None

# st.caption("Powered by Streamlit • Google Sheets • WhatsApp")

import streamlit as st
import pandas as pd
import urllib.parse
from pathlib import Path
from datetime import datetime
import uuid
import json
import gspread
from google.oauth2.service_account import Credentials

# ================== PAGE CONFIG ================== #
st.set_page_config("Product Ordering System", layout="wide")
st.title("📦 Product Comparison & Ordering")

# ================== GOOGLE SHEETS ================== #
SHEET_ID = "1TsxO6Cy1bZpN-RjA_E8ZuxY9YSNJeU5lnf6jPkGbLEY"
SHEET_NAME = "orders"

@st.cache_resource
def connect_orders_sheet():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    with open("credentials.json") as f:
        info = json.load(f)

    creds = Credentials.from_service_account_info(info, scopes=scope)
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

def save_order(product, company, rate, qty, area):
    sheet = connect_orders_sheet()
    sheet.append_row([
        str(uuid.uuid4())[:8],
        product,
        company,
        rate,
        qty,
        rate * qty,
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

df = load_products()

# ================== DEALERS (AREA BASED) ================== #
AREA_TO_DEALERS = {
    "Mumbai": [
        {
            "name": "Shree Traders",
            "gst": "27ABCDE1234F1Z5",
            "phone": "919106861749",
        },
        {
            "name": "Om Enterprises",
            "gst": "27XYZDE9876Q1Z2",
            "phone": "918780701769",
        },
    ],
    "Delhi": [
        {
            "name": "Delhi Hardware",
            "gst": "07AAAAA1111A1Z1",
            "phone": "919999999999",
        }
    ],
}

selected_area = st.selectbox("📍 Select Area", AREA_TO_DEALERS.keys())
active_dealers = AREA_TO_DEALERS[selected_area]

# ================== FILTERS ================== #
c1, c2, c3, c4, c5 = st.columns(5)

products = c1.multiselect("Product", sorted(df["PRODUCT_NAME"].unique()))
companies = c2.multiselect("Company", sorted(df["COMPANY"].unique()))
sizes = c3.multiselect("Size", sorted(df["SIZE"].dropna().unique()))
heights = c4.multiselect("Height", sorted(df["HEIGHT"].dropna().unique()))
weights = c5.multiselect("Weight", sorted(df["WEIGHT"].dropna().unique()))

filtered = df.copy()
if products: filtered = filtered[filtered["PRODUCT_NAME"].isin(products)]
if companies: filtered = filtered[filtered["COMPANY"].isin(companies)]
if sizes: filtered = filtered[filtered["SIZE"].isin(sizes)]
if heights: filtered = filtered[filtered["HEIGHT"].isin(heights)]
if weights: filtered = filtered[filtered["WEIGHT"].isin(weights)]

if filtered.empty:
    st.warning("No products found")
    st.stop()

# ================== SESSION STATE ================== #
st.session_state.setdefault("buy_row", None)
st.session_state.setdefault("order_saved", False)
st.session_state.setdefault("last_order", None)

# ================== PRODUCT LIST ================== #
st.subheader("🧾 Products")

for idx, row in filtered.iterrows():
    col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 1, 1, 1])

    col1.write(row["COMPANY"])
    col2.write(row["COMPANY_CODE_NAME"])
    col3.write(row["PRODUCT_CODE_NUMBER"])
    col4.write(row["SIZE"] if pd.notna(row["SIZE"]) else "")
    col5.write(f"₹{int(row['RATE'])}")

    if col6.button("🛒 Buy", key=f"buy_{idx}"):
        st.session_state.buy_row = row
        st.session_state.order_saved = False

# ================== ORDER CONFIRM ================== #
if st.session_state.buy_row is not None:
    st.divider()
    st.subheader("🛒 Confirm Order")

    row = st.session_state.buy_row
    qty = st.number_input("Quantity", min_value=1, step=1)

    if st.button("✅ Confirm Order"):
        save_order(
            row["COMPANY_CODE_NAME"],
            row["COMPANY"],
            row["RATE"],
            qty,
            selected_area,
        )

        message = f"""
New Order 📦
Area: {selected_area}
Product: {row['COMPANY_CODE_NAME']}
Company: {row['COMPANY']}
Quantity: {qty}
Rate: ₹{row['RATE']}
Total: ₹{row['RATE'] * qty}
"""

        st.session_state.last_order = {
            "msg": urllib.parse.quote(message),
            "dealers": active_dealers,
        }

        st.session_state.order_saved = True
        st.session_state.buy_row = None
        st.success("✅ Order saved successfully")

# ================== DEALER SELECTION ================== #
if st.session_state.order_saved and st.session_state.last_order:
    st.divider()
    st.subheader("📨 Send Order to Dealer")

    encoded_msg = st.session_state.last_order["msg"]

    for dealer in st.session_state.last_order["dealers"]:
        st.markdown(f"""
**🏪 Dealer:** {dealer['name']}  
**🧾 GST:** `{dealer['gst']}`  
**📞 Phone:** {dealer['phone']}
""")

        st.markdown(
            f"""
            <a href="https://wa.me/{dealer['phone']}?text={encoded_msg}" target="_blank">
            <button style="
                padding:10px 18px;
                background:#25D366;
                color:white;
                border:none;
                border-radius:8px;
                font-size:15px;
            ">
            Send WhatsApp
            </button>
            </a>
            """,
            unsafe_allow_html=True,
        )
        st.divider()

    if st.button("❌ Cancel"):
        st.session_state.order_saved = False
        st.session_state.last_order = None

st.caption("Powered by Streamlit • Google Sheets • WhatsApp")

