import pandas as pd
import numpy as np
import os
import pickle
import datetime
from TitleAndTableExtraction import Extraction_title_and_data
from Validation import validation
from Transformation import transformation
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv
# PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
# WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
# USER = os.getenv("SNOWFLAKE_USER")
# ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")

USER = "Michael"
PASSWORD = "RelevantResearch@1234"
WAREHOUSE = "COMPUTE_WH"
ACCOUNT = "vqkklwj-nn52820"
SCHEMA = "PUBLIC"
SNOWFLAKE_DATABASE = "DETENTIONDATA"
conn = snowflake.connector.connect(
    user = USER,
    password = PASSWORD,
    account =  ACCOUNT,
    warehouse = WAREHOUSE,
    database = "DETENTIONDATA",
    schema = "DETENTIONDATA",
    role = "ACCOUNTADMIN"
)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)  # No line wrapping
# pd.set_option('display.max_colwidth', None)  # Show full column contents
source_file = "C:\\Users\\acer\\Desktop\\Relevant Research\\System Design\\FY25_detentionStats06202025.xlsx" 

def Clean_file():
    print('Clean file')
    #Cleaning Function
def Extract_table():
    #extract data
    all_dfs = Extraction_title_and_data(source_file)
    print("Extract all table titles and data")
    return all_dfs
def save_processed_tables_to_excel(table_dataframes, source_filename):
    if not table_dataframes:
        print("No data to save.")
        return None

    # Define fixed output directory
    output_dir = r"C:\Users\acer\Desktop\Relevant Research\System Design"

    # Clean and prepare filename
    base_name = os.path.splitext(os.path.basename(source_filename))[0]
    safe_name = "".join(c for c in base_name if c not in r'<>:"/\|?*')
    output_filename = f"{safe_name}_processed.xlsx"
    output_path = os.path.join(output_dir, output_filename)

    # Write to Excel
    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        for i, (title, df) in enumerate(table_dataframes.items(), start=1):
            sheet_name = f"Table {i}"
            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)

    print(f"✅ Saved Excel file to: {output_path}")
def Validation_function(tables:dict):
    tables_after_validation, report = validation(tables)
    return tables_after_validation
def Transformation_function(tables_after_validation:dict):
    tables_after_transformation = transformation(tables_after_validation)
    return tables_after_transformation
def sanitize(name: str) -> str:
    """
    Convert 'Table 1' → 'TABLE_1', and ensure valid table name.
    """
    return name.strip().replace(" ", "_").upper() if name else ""
def store_in_db1(dfs: dict,user,password,schema):
    USER = user
    PASSWORD = password
    WAREHOUSE = "COMPUTE_WH"
    ACCOUNT = "vqkklwj-nn52820"
    SCHEMA = schema
    SNOWFLAKE_DATABASE = "DETENTIONDATA"
    conn = snowflake.connector.connect(
        user = USER,
        password = PASSWORD,
        account =  ACCOUNT,
        warehouse = WAREHOUSE,
        database = "DETENTIONDATA",
        schema = schema,
        role = "ACCOUNTADMIN"
    )
    print(f"🔍 {len(dfs)} tables found: {list(dfs.keys())}")

    conn.autocommit = True
    with conn.cursor() as cursor:

        # ── 1️⃣  EARLY RELEASE‑DATE CHECK ──────────────────────────
        if "Table 2" not in dfs or "Release_date" not in dfs["Table 2"].columns:
            print("⚠️  Cannot find 'Table 2' or its 'Release_date' column. Proceeding without date gate.")
        else:
            incoming_set = set(
                pd.to_datetime(dfs["Table 2"]["Release_date"], errors="coerce")
                  .dt.strftime("%Y-%m-%d")
                  .dropna()
                  .unique()
            )
            print(f"📅 Incoming Release_date(s): {sorted(incoming_set)}")

            # Try quoted column name first, fall back to unquoted if needed
            try:
                cursor.execute(
                    'SELECT DISTINCT "Release_date" FROM DETENTIONDATA.PUBLIC.TABLE_2'
                )
            except Exception:
                cursor.execute(
                    'SELECT DISTINCT RELEASE_DATE FROM DETENTIONDATA.PUBLIC.TABLE_2'
                )

            existing_set = {
                (row[0].strftime("%Y-%m-%d")
                 if isinstance(row[0], (datetime.date, datetime.datetime))
                 else str(row[0]))
                for row in cursor.fetchall()
            }
            print(f"📅 Existing Release_date(s): {sorted(existing_set)}")

            if incoming_set and incoming_set.issubset(existing_set):
                print("✅ Data already loaded for these date(s). Skipping upload.")
                return  # early exit

        # ── 2️⃣  ORIGINAL UPLOAD LOGIC ────────────────────────────
        cursor.execute("SHOW TABLES")
        existing_tables = {row[1].upper() for row in cursor.fetchall()}

        expected_tables = [f"Table {i}" for i in range(1, 18)]
        missing_tables  = [t for t in expected_tables if t not in dfs]
        if missing_tables:
            print(f"⚠️ Missing tables: {missing_tables}")

        for name in expected_tables:
            if name not in dfs:
                print(f"⛔ Skipping {name}: not found in current file.")
                continue
            if not name.strip():
                print("⛔ Skipping unnamed table.")
                continue

            table_name = sanitize(name)
            if not table_name:
                print(f"⛔ Skipping invalid table name: '{name}'")
                continue

            df        = dfs[name]
            overwrite = table_name not in existing_tables

            try:
                success, _, nrows, _ = write_pandas(
                    conn,
                    df,
                    table_name        = table_name,
                    overwrite         = overwrite,
                    auto_create_table = True
                )
                if success:
                    print(f"✅ {table_name}: Uploaded {nrows} rows.")
                else:
                    print(f"❌ {table_name}: Upload failed.")
            except Exception as e:
                print(f"❌ {table_name}: Exception occurred → {e}")


output_file = "C:\\Users\\acer\\Desktop\\Relevant Research\\System Design\\dfs.txt"
def main():
    # file_path = "C:\\Users\\acer\\Desktop\\Relevant Research\\System Design\\dfs1.txt"
    # with open(file_path,"rb") as f:
    #     dfs = pickle.load(f)
    output_file_path = "C:\\Users\\acer\\Desktop\\Relevant Research\\System Design\\"
    dfs = Extract_table()
    tables = {}
    for i, (title, df) in enumerate(dfs.items(), start=1):
        key = f"Table {i}"
        tables[key] = df
    
    tables_after_validation = Validation_function(tables)
    tables_after_transformation = Transformation_function(tables_after_validation)
    save_processed_tables_to_excel(tables_after_transformation,source_file)
    store_in_db1(tables_after_transformation)
    print(tables_after_transformation["Table 8"])
if __name__ == "__main__":
    main()