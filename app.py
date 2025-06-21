import streamlit as st
import pandas as pd
import os
import tempfile
import sys

# Make local modules importable
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from TitleAndTableExtraction import Extraction_title_and_data
from Validation import validation
from Transformation import transformation
from Final_System import sanitize, store_in_db1  # noqa: F401  (if sanitize unused)

# ──────────────────────────────────────────────────────────────────────────────
# 1.  Streamlit page config
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Detention Data Uploader", layout="wide")
st.title("📊 ICE DETENTION SYSTEM")
st.write("Upload an Excel file to extract, validate, transform, and store detention data.")

# ──────────────────────────────────────────────────────────────────────────────
# 2.  Ask the user for their API key (masked)
# ──────────────────────────────────────────────────────────────────────────────
api_key = st.text_input(
    "🔑 Enter your OpenAI (or other) API key",
    type="password",
    help="Your key stays only in this session and is **not** logged."
)

# ──────────────────────────────────────────────────────────────────────────────
# 3.  File uploader
# ──────────────────────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader("📂 Upload Excel file", type=["xlsx"])

# ──────────────────────────────────────────────────────────────────────────────
# 4.  Main pipeline
# ──────────────────────────────────────────────────────────────────────────────
if uploaded_file is not None:
    if not api_key:
        st.warning("Please provide a valid API key before processing the file.")
        st.stop()

    # Save upload to a temp file so downstream functions can read it
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(uploaded_file.getvalue())
        temp_file_path = tmp.name

    st.success("File uploaded successfully!")

    try:
        # 4‑A Extraction  ────────────────────────────────────────────
        st.info("🔍 Extracting tables…")
        dfs = Extraction_title_and_data(
            temp_file_path,
            source_filename=uploaded_file.name,
            api_key=api_key        # ← pass it through
        )

        # Convert keys to “Table 1”, “Table 2”, …
        tables = {f"Table {i}": df for i, df in enumerate(dfs.values(), start=1)}

        # 4‑B Validation  ────────────────────────────────────────────
        st.info("✅ Validating tables…")
        validated_tables, report = validation(tables)

        # 4‑C Transformation  ───────────────────────────────────────
        st.info("🔧 Transforming tables…")
        transformed_tables = transformation(validated_tables)

        # 4‑D Preview  ──────────────────────────────────────────────
        st.success("✅ Tables processed successfully. Preview below:")
        selected_table = st.selectbox("Select a table to preview", list(transformed_tables.keys()))
        st.dataframe(transformed_tables[selected_table])

        # 4‑E Upload to Snowflake  ─────────────────────────────────
        if st.button("📤 Upload to Snowflake"):
            store_in_db1(transformed_tables)
            st.success("Data uploaded to Snowflake successfully!")

    except Exception as e:
        st.error(f"❌ Error occurred: {e}")
