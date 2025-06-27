import pandas as pd

def validation(tables:dict):
    if tables is None:
        print("No values in table dictionary")
    table1_df = tables["Table 1"]
    clean_df1,report_1 = validate_table_1(table1_df)
    tables["Table 1"] = clean_df1
    table2_df = tables["Table 2"]
    clean_df2,report_2 = validate_table_2(table2_df)
    tables["Table 2"] = clean_df2
    table3_df = tables["Table 3"]
    clean_df3,report_3 = validate_table_3(table3_df)
    tables["Table 3"] = clean_df3
    table4_df = tables["Table 4"]
    clean_df4,report_4 = validate_table_4(table4_df)
    tables["Table 4"] = clean_df4
    report = {**report_1,**report_2,**report_3,**report_4}
    table5_df = tables["Table 5"]
    clean_df5,report_5 = validate_table_5(table5_df)
    tables["Table 5"] = clean_df5
    table6_df = tables["Table 6"]
    clean_df6,report_6 = validate_table_6(table6_df)
    tables["Table 6"] = clean_df6
    table7_df = tables["Table 7"]
    clean_df7,report_7 = validate_table_7(table7_df)
    tables["Table 7"] = clean_df7
    # table8_df = tables["Table 8"]
    # clean_df8 = validate_table_8(table8_df)
    # tables["Table 8"] = clean_df8
    table9_df = tables["Table 9"]
    clean_df9 = validate_table_9(table9_df)
    tables["Table 9"] = clean_df9
    table15_df = tables["Table 15"]
    clean_df15,report_15 = validate_table_15(table15_df)
    tables["Table 15"] = clean_df15
    table16_df = tables["Table 16"]
    clean_df16,report_16 = validate_table_16(table16_df)
    tables["Table 16"] = clean_df16
    report = {**report_1,**report_2,**report_3,**report_4,**report_5,**report_6,**report_7,**report_15,**report_16}
    return tables,report
def validate_table_1(df):
    clean_df1 = df.copy()
    report = {
        "row_corrections":[],
        "summary_correction":{},
    }
    total_row = clean_df1[clean_df1['Processing Disposition']=='Total']
    data_rows = clean_df1[clean_df1['Processing Disposition'] != 'Total']
    ##For Row level validation##
    for idx,row in data_rows.iterrows():
        adult = row['Adult']
        if 'FSC' in data_rows.columns:
            fsc = row['FSC']
            expected_total = fsc + adult
        else:
            expected_total = adult
        actual_total = row['Total']
        if expected_total != actual_total:
            clean_df1.at[idx,'Total'] = expected_total
            report["row_corrections"].append({
                "index": idx,
                "reported_total": actual_total,
                "corrected_total": expected_total
            })
            print(f"✅ Row {idx}: Total corrected from {actual_total} to {expected_total}")
    if not total_row.empty:
        total_idx = total_row.index[0]
        data_rows_idx = data_rows.index
        all_cols = ['FSC', 'Adult', 'Total']
        if 'FSC' in clean_df1.columns:
            cols_to_check = all_cols
        else:
            # Exclude 'FSC' if missing
            cols_to_check = [col for col in all_cols if col != 'FSC']
        for col in cols_to_check:
            # expected_sum = data_rows[col].sum()
            expected_sum = clean_df1.loc[data_rows_idx,col].sum()
            reported_sum = clean_df1.at[total_idx,col]
            if expected_sum != reported_sum:
                clean_df1.at[total_idx,col] = expected_sum
                report["summary_correction"][col] = {
                    "reported": reported_sum,
                    "corrected": expected_sum
                }
                print(f"🔁 Summary '{col}': corrected from {reported_sum} to {expected_sum}")
    return clean_df1, report
def validate_table_2(df):
    df = df.head(1).copy()
    df.columns = df.columns.str.strip().str.replace(r'\s+',' ',regex=True)
    df['FSC'] = df['FSC'].fillna(0)
    df['Adult'] = df['Adult'].fillna(0)
    all_cols = ['FSC', 'Adult', 'Total']
    if 'FSC' in df.columns:
        cols_to_check = all_cols
    else:
        # Exclude 'FSC' if missing
        cols_to_check = [col for col in all_cols if col != 'FSC']
    for col in cols_to_check:
        df[col] = pd.to_numeric(df[col],errors='coerce').fillna(0)
    clean_df2 = df
    report_of_table_2 = {
        "Table Name":'Table 2',
        "row_correction":[]
    }
    # Get 'Adult' value, fallback to 0 if missing or NaN
    adult = df['Adult'].iat[0] if 'Adult' in df.columns and pd.notna(df['Adult'].iat[0]) else 0
    # Get 'FSC' value safely, fallback to 0 if missing or NaN
    fsc = df['FSC'].iat[0] if 'FSC' in df.columns and pd.notna(df['FSC'].iat[0]) else 0
    expected_total = fsc + adult
    actual_total = df['Total'].iat[0]
    if expected_total != actual_total:
        df.at[df.index[0], 'Total'] = expected_total
        report_of_table_2["row_correction"].append({
            "reported_total": actual_total,
            "corrected_total": expected_total
        })
        print(f"✅ Row : Total corrected from {actual_total} to {expected_total}")
        
    return df,report_of_table_2
def validate_table_3(df):
    df.columns = df.columns.str.strip().str.replace(r'\s+',' ',regex=True)
    df['Total Detained'] = df['Total Detained'].fillna(0)
    total_idx = df[df['Detention Facility Type'] == 'Total'].index[0]
    data_idx = df[df['Detention Facility Type'] != 'Total'].index
    report_of_table_3 = {
        "Table Name":'Table 3',
        "row_correction":[]
    }
    cols_to_check = ['Total Detained']
    for col in cols_to_check:
        expected = df.loc[data_idx,col].sum()
        reported = df.at[total_idx,col]
        if expected != reported:
            df.at[total_idx,col] = expected
            report_of_table_3["row_correction"].append({
            "reported_total": reported,
            "corrected_total": expected
        })
        print(f"✅ Row : Total corrected from {reported} to {expected}")      
    print("Validating table 3")
    return df,report_of_table_3
def validate_table_4(df):
    total_idx = df[df['Criminality']=='Total'].index[0]
    data_row_idx = df[df['Criminality'] != 'Total'].index
    report_of_table_4 = {
        "Table Name":'Table 4',
        "row_correction":[],
        "summary_correction":{},
    }
    for idx in data_row_idx:
        ice = df.at[idx,'ICE']
        cbp = df.at[idx,'CBP']
        expected_total = ice + cbp
        actual_total = df.at[idx,'Total']
        expected_ice_percent =ice/expected_total
        expected_cbp_percent = cbp/expected_total
        actual_ice_percent =  df.at[idx,'Percent ICE']
        actual_cbp_percent = df.at[idx,'Percent CBP']
        if expected_total != actual_total:
            df.at[idx,'Total'] = expected_total
            report_of_table_4["row_correction"].append({
                'reported_total': actual_total,
                'expected_total': expected_total
            })
            print(f"✅ Row : Total corrected from {actual_total} to {expected_total}") 
        if not pd.isna(actual_ice_percent) and round(expected_ice_percent, 9) != round(actual_ice_percent, 9):
            df.at[idx, 'Percent ICE'] = expected_ice_percent
            report_of_table_4["row_correction"].append({
                'index': idx,
                'reported_ice_percent': actual_ice_percent,
                'expected_ice_percent': expected_ice_percent
            })
            print(f"✅ Row : Ice percent  corrected from {actual_ice_percent} to {expected_ice_percent}") 

        if not pd.isna(actual_cbp_percent) and round(expected_cbp_percent, 9) != round(actual_cbp_percent, 9):
            df.at[idx, 'Percent CBP'] = expected_cbp_percent
            report_of_table_4["row_correction"].append({
                'index': idx,
                'reported_cbp_percent': actual_cbp_percent,
                'expected_cbp_percent': expected_cbp_percent
            }) 
            
            print(f"✅ Row : CBP percent corrected from {actual_cbp_percent} to {expected_ice_percent}")    
    cols_to_check = ['ICE','CBP','Total']
    for col in cols_to_check:
        expected = df.loc[data_row_idx,col].sum()
        reported = df.at[total_idx,col]
        if expected != reported:
            df.at[total_idx,col] = expected
            report_of_table_4["summary_correction"][col] = {
                    "reported": reported,
                    "corrected": expected
                }
            print(f"✅ Column: Total corrected from {reported} to {expected}") 
    print("validate table 4")
    return df,report_of_table_4
def validate_table_5(df):
    total_idx =  df[df['Agency']=='Total'].index[0]
    data_rows_idx = df[df['Agency'] != 'Total'].index
    report_of_table_5 = {
        "Table Name":'Table 5',
        "row_correction":[],
        "summary_correction":{},
    }
    for idx in data_rows_idx:
            monthly_values = [df.at[idx, col] if not pd.isna(df.at[idx, col]) else 0 
                              for col in ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 
                                          'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']]
            expected_total = sum(monthly_values)
            actual_total = df.at[idx, 'Total']
            if pd.isna(actual_total) or abs(expected_total - actual_total) > 1e-6:
                df.at[idx, 'Total'] = expected_total
                report_of_table_5['row_correction'].append({
                    'index': idx,
                    'reported_total': actual_total,
                    'expected_total': expected_total
                })
                print(f"✅ Row : Total corrected from {actual_total} to {expected_total}") 
    cols_to_check = ['Oct' ,'Nov' ,'Dec','Jan' ,'Feb' ,'Mar','Apr', 'May', 'Jun' ,'Jul', 'Aug' ,'Sep','Total']
    for col in cols_to_check:
            expected = df.loc[data_rows_idx, col].sum(skipna=True)
            reported = df.at[total_idx, col]
            if pd.isna(reported) or abs(expected - reported) > 1e-6:
                df.at[total_idx, col] = expected
                report_of_table_5['summary_correction'][col] = {
                    'Column':col,
                    'expected': expected,
                    'reported': reported,
                }
                print(f"✅ Column : Column:{col} corrected from {reported} to {expected}") 
    print("Table 5 validated")
    return df,report_of_table_5
def validate_table_6(df):
    df.columns = df.columns.str.strip().str.replace(r'\s+',' ',regex=True)
    df['Convicted Criminal'] = df['Convicted Criminal'].fillna(0)
    df['Pending Criminal Charges'] = df['Pending Criminal Charges'].fillna(0)
    df['Other Immigration Violator'] = df['Other Immigration Violator'].fillna(0)
    df['Total'] = df['Total'].fillna(0)
    total_idx = df[df['Facility Type']=='Total'].index[0]
    data_rows_idx = df[df['Facility Type'] != 'Total'].index
    report_of_table_6 = {
        "Table Name":'Table 6',
        "row_correction":[],
        "summary_correction":{},
    }
    for idx in data_rows_idx:
        Convicted_Criminal = df.at[idx, 'Convicted Criminal']
        Pending_Criminal_Charges = df.at[idx, 'Pending Criminal Charges']
        Other_Immigration_Violator = df.at[idx, 'Other Immigration Violator']
        expected_total = Convicted_Criminal + Pending_Criminal_Charges + Other_Immigration_Violator
        actual_total = df.at[idx, 'Total']
        if expected_total != actual_total:
            df.at[idx,'Total'] = expected_total
            report_of_table_6['row_correction'].append({
                'index': idx,
                'reported_total': actual_total,
                'expected_total': expected_total
            })
            print(f"✅ Row : Total corrected from {actual_total} to {expected_total}")
    cols_to_check = ['Convicted Criminal', 'Pending Criminal Charges', 'Other Immigration Violator', 'Total']
    for col in cols_to_check:
        expected = df.loc[data_rows_idx, col].sum()
        reported = df.at[total_idx, col]
        if expected != reported:
            df.at[total_idx, col] = expected
            report_of_table_6['summary_correction'][col]={
                'Column':col,
                'expected': expected,
                'reported': reported,
                }
            print(f"✅ Columns: {col} : Total corrected from {reported} to {expected}")
    print("Validated Table 6")
    return df,report_of_table_6
def validate_table_7(df):
    total_idx = df[df['Facility Type']=='Total'].index[0]
    data_rows_idx = df[df['Facility Type'] != 'Total'].index
    report_of_table_7 = {
        "Table Name":'Table 7',
        "row_correction":[],
        "summary_correction":{}
    }
    expected_total = df.loc[data_rows_idx,'Total'].sum()
    reported_total = df.at[total_idx,'Total']
    if expected_total != reported_total:
        df.at[total_idx,'Total'] = expected_total
        report_of_table_7['summary_correction']={
            'expected_total': expected_total,
            'reported_total': reported_total
        }
        print(f"Column Total: Total changes from {reported_total} to {expected_total}")
    print('validated table 7')
    return df,report_of_table_7
# def validate_table_8(df):
#     if df.columns[0] == 'Unnamed: 0':
#         df  = df.rename(columns = {"Unnamed: 0":"Removals","Removals":"Total"})
#     return df

def validate_table_9(df):
    df.iloc[:,0] = df.iloc[:,0].ffill()
    df['Criminality'] = df['Criminality'].fillna('Criminality Total')
    # total_idx = df[df['Releease Reason'] == 'Total'].index[0]
    # data_rows_idx = df[df['Release Reason'] != 'Total'].index
    # updated_df = df.copy()
    # cols_to_check =['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar','Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']
    # for col in cols_to_check:
    #     bonded_total = df['Release Reason']
    print("Validated Table 9")
    return df
def validate_table_15(df):
    data_idx = df.index
    report_of_table_15 = {
        "Table Name":'Table 15',
        "row_correction":[]
    }
    for idx in data_idx:
       monthly_values = [df.at[idx, col] if not pd.isna(df.at[idx, col]) else 0 
                              for col in ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 
                                          'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']]
       expected_total = sum(monthly_values)
       actual_total = df.at[idx,'FY Overall']
       if pd.isna(actual_total) or abs(expected_total - actual_total) > 1e-6:
            df.at[idx, 'Total'] = expected_total
            report_of_table_15['row_correction'].append({
                'index': idx,
                'reported_total': actual_total,
                'expected_total': expected_total
            })
            print(f"✅ Row : FY Overall corrected from {actual_total} to {expected_total}") 
    return df,report_of_table_15
def validate_table_16(df):
    df.iloc[:,0] = df.iloc[:,0].ffill()
    data_idx = df.index
    report_of_table_16 = {
        "Table Name":'Table 16',
        "row_correction":[]
    }
    for idx in data_idx:
        monthly_values = [df.at[idx, col] if not pd.isna(df.at[idx, col]) else 0 for col in ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar','Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']]
        expected_total = sum(monthly_values)
        actual_total = df.at[idx,'FY Overall']
        if expected_total != actual_total:
            df.at[idx, 'Total'] = expected_total
            report_of_table_16['row_correction'].append({
                'index': idx,
                'reported_total': actual_total,
                'expected_total': expected_total
            })
            print(f"✅ Row : FY Overall corrected from {actual_total} to {expected_total}") 
    return df,report_of_table_16