import pandas as pd
def transformation(tables_after_validation:dict):
    if tables_after_validation is None:
        print("Tables after validation is empty")
    table1_df = tables_after_validation["Table 1"]
    transformed_table1 = transform_table_1(table1_df)
    tables_after_validation["Table 1"] = transformed_table1
    table2_df = tables_after_validation["Table 2"]
    transformed_table2 = transform_table_2(table2_df)
    tables_after_validation["Table 2"] = transformed_table2
    table4_df = tables_after_validation["Table 4"]
    transformed_table4 = transform_table_4(table4_df)
    tables_after_validation["Table 4"] = transformed_table4
    table5_df = tables_after_validation["Table 5"]
    transformed_table5 = transform_table_5(table5_df)
    tables_after_validation["Table 5"] = transformed_table5
    table6_df = tables_after_validation["Table 6"]
    transformed_table6 = transform_table_6(table6_df)
    tables_after_validation["Table 6"] = transformed_table6
    table8_df = tables_after_validation["Table 8"]
    transformed_table8 = transform_table_8(table8_df)
    tables_after_validation["Table 8"] = transformed_table8
    table9_df = tables_after_validation["Table 9"]
    transformed_table9 = transform_table_9(table9_df)
    tables_after_validation["Table 9"] = transformed_table9
    table10_df = tables_after_validation["Table 10"]
    transformed_table10 = transform_table_10(table10_df)
    tables_after_validation["Table 10"] = transformed_table10
    table11_df = tables_after_validation["Table 11"]
    transformed_table11 = transform_table_11(table11_df)
    tables_after_validation["Table 11"] = transformed_table11
    table12_df = tables_after_validation["Table 12"]
    transformed_table12 = transform_table_12(table12_df)
    tables_after_validation["Table 12"] = transformed_table12
    table13_df = tables_after_validation["Table 13"]
    transformed_table13 = transform_table_13(table13_df)
    tables_after_validation["Table 13"] = transformed_table13
    table14_df = tables_after_validation["Table 14"]
    transformed_table14 = transform_table_14(table14_df)
    tables_after_validation["Table 14"] = transformed_table14
    table15_df = tables_after_validation["Table 15"]
    transformed_table15 = transform_table_15(table15_df)
    tables_after_validation["Table 15"] = transformed_table15
    df =tables_after_validation
    return df
def transform_table_1(df):
    df.columns = df.columns.str.strip().str.replace(r'\s+',' ',regex=True)
    all_cols = ['FSC', 'Adult', 'Total']
    if 'FSC' in df.columns:
        cols_to_check = all_cols
    else:
        # Exclude 'FSC' if missing
        cols_to_check = [col for col in all_cols if col != 'FSC']
    df_melted = df.melt(
        id_vars=['Processing Disposition','EID','Source_filename','Release_date','Table_name','Table_code'],
        value_vars = cols_to_check,
        var_name = 'Facility Type',
        value_name = 'Value'
    )
    columns = df_melted.columns.tolist()
    melted_cols = ['Facility Type','Value']
    for col in melted_cols:
        columns.remove(col)
    agency_idx = columns.index("Processing Disposition")
    new_order = columns[:agency_idx+1] + melted_cols + columns[agency_idx+1:]
    df_melted = df_melted[new_order]
    df_melted = df_melted.sort_values(by=['Release_date','Facility Type'],kind='mergesort')
    df_melted.loc[
        (df_melted["Processing Disposition"]=='Total') &
        (df_melted["Facility Type"]=='Total'),
        'Processing Disposition'
    ] = 'Grand Total'
    return df_melted
def transform_table_2(df):
    df.columns = df.columns.str.strip().str.replace(r'\s+',' ',regex=True)
    all_cols = ['FSC', 'Adult', 'Total']
    if 'FSC' in df.columns:
        cols_to_check = all_cols
    else:
        # Exclude 'FSC' if missing
        cols_to_check = [col for col in all_cols if col != 'FSC']
    df_melted = df.melt(
    id_vars=['ICE Release Fiscal Year','EID','Source_filename','Release_date','Table_name','Table_code'],
    value_vars=cols_to_check,
    var_name= 'Facility Type',
    value_name = 'Value'
    )
    columns = df_melted.columns.tolist()
    melted_cols = ['Facility Type','Value']
    for col in melted_cols:
        columns.remove(col)
    agency_idx = columns.index("ICE Release Fiscal Year")
    new_order = columns[:agency_idx+1] + melted_cols + columns[agency_idx+1:]
    df_melted = df_melted[new_order]
    df_melted = df_melted.sort_values(by=['Release_date','Facility Type'],kind='mergesort')
    return df_melted
def transform_table_4(df):
    df.columns = df.columns.str.strip().str.replace(r'\s+',' ',regex=True)
    df_melted = df.melt(
            id_vars=['Criminality','EID','Source_filename','Release_date','Table_name','Table_code'],
            value_vars=['ICE', 'CBP','Percent ICE','Percent CBP','Total'],
            var_name='Arresting Agency',
            value_name='Count'
    )
    columns = df_melted.columns.tolist()
    melted_cols = ['Arresting Agency','Count']
    for col in melted_cols:
        columns.remove(col)
    agency_idx = columns.index("Criminality")
    new_order = columns[:agency_idx+1] + melted_cols + columns[agency_idx+1:]
    df_melted = df_melted[new_order]
    df_melted = df_melted.sort_values(by=['Release_date'],kind='mergesort')
    df_melted.loc[
        (df_melted['Criminality']=='Total') &
        (df_melted['Arresting Agency']=='Total'),
        'Criminality'
    ]='Grand Total'
    return df_melted
def transform_table_5(df):
    df.columns = df.columns.str.strip().str.replace(r'\s+',' ', regex = True)
    month_cols = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar','Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Total']
    df_melted = df.melt(
    id_vars=['Agency', 'EID', 'Release_date', 'Source_filename', 'Table_name', 'Table_code'],
    value_vars=month_cols,
    var_name='Month',
    value_name='Value'
    )
    df_melted['Release_Year'] = df_melted['Release_date'].astype(str).str.extract(r'(\d{4})').astype(int)
    month_map = {
        'Oct': '10', 'Nov': '11', 'Dec': '12',
        'Jan': '01', 'Feb': '02', 'Mar': '03',
        'Apr': '04', 'May': '05', 'Jun': '06',
        'Jul': '07', 'Aug': '08', 'Sep': '09',
        'FY Overall': '00' 
    }
    df_melted['Month_Num'] = df_melted['Month'].map(month_map)
    df_melted['Calendar_Year'] = df_melted.apply(compute_calendar_year, axis=1)
    df_melted['Year_Month'] = df_melted['Calendar_Year'].astype(str) + '-' + df_melted['Month_Num']
    mask_total = df_melted['Month'] == 'Total'
    df_melted.loc[mask_total, 'Year_Month'] = (
    pd.to_datetime(df_melted.loc[mask_total, 'Release_date']).dt.year.astype(str) + '-00'
    )
    df_melted['Fiscal_Year'] = df_melted.apply(get_fiscal_year, axis=1)
    df_melted = df_melted.drop(columns=['Month_Num', 'Calendar_Year','Month','Release_Year'])
    columns = df_melted.columns.tolist()
    melted_cols = ['Year_Month', 'Fiscal_Year','Value']
    for col in melted_cols:
        columns.remove(col)

    agency_idx = columns.index('Agency')
    new_order = columns[:agency_idx + 1] + melted_cols + columns[agency_idx + 1:]
    df_melted = df_melted[new_order]
    df_melted = df_melted[df_melted['Value'] != 0] 
    df_melted = df_melted.sort_values(by=['Release_date', 'Year_Month','Agency'])
    mask_total_year = df_melted['Year_Month'].str.endswith('-00')
    df_melted.loc[mask_total_year & (df_melted['Agency'] == 'Total'), 'Agency'] = 'Total_FYTD'
    df_melted.loc[mask_total_year & (df_melted['Agency'] == 'CBP'), 'Agency'] = 'CBP_Total'
    df_melted.loc[mask_total_year & (df_melted['Agency'] == 'ICE  '), 'Agency'] = 'ICE_Total'
    return df_melted
def compute_calendar_year(row):
    if row['Month'] in ['Oct', 'Nov', 'Dec']:
        return row['Release_Year'] - 1
    return row['Release_Year']
def get_fiscal_year(row):
    y, m = int(row['Year_Month'][:4]), int(row['Year_Month'][-2:])
    if 10 <= m <= 12:
        return y + 1
    else:
        return y
def transform_table_6(df):
    df.columns = df.columns.str.strip().str.replace(r'\s+',' ',regex=True)
    df_melted = df.melt(
        id_vars=['Facility Type','EID','Source_filename','Release_date','Table_name','Table_code'],
        value_vars=['Convicted Criminal', 'Pending Criminal Charges','Other Immigration Violator', 'Total'],
        var_name='Criminality',
        value_name='Value'
    )
    columns = df_melted.columns.tolist()
    melted_cols = ['Criminality','Value']
    for col in melted_cols:
        columns.remove(col)
    agency_idx = columns.index("Facility Type")
    new_order = columns[:agency_idx+1] + melted_cols + columns[agency_idx+1:]
    df_melted = df_melted[new_order]
    df_melted = df_melted.sort_values(by=['Release_date','Facility Type'],kind='mergesort')
    df_melted.loc[
        (df_melted['Facility Type'] =='Total') &
        (df_melted['Criminality']=='Total'),
        'Facility Type'
    ]='Grand Total'
    return df_melted
def transform_table_9(df):
    df.columns=df.columns.str.strip().str.replace(r'\s+',' ',regex=True)
    df['Release_date'] = pd.to_datetime(df['Release_date']).dt.date
    month_cols = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar',
                'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Total']
    df_melted = df.melt(
        id_vars=['Release Reason','Criminality','EID','Release_date','Source_filename','Table_name','Table_code'],
        value_vars = month_cols,
        var_name = 'Month',
        value_name = 'Value'
    )
    df_melted['Release_Year'] = df_melted['Release_date'].astype(str).str.extract(r'(\d{4})').astype(int)
    month_map = {
        'Oct': '10', 'Nov': '11', 'Dec': '12',
        'Jan': '01', 'Feb': '02', 'Mar': '03',
        'Apr': '04', 'May': '05', 'Jun': '06',
        'Jul': '07', 'Aug': '08', 'Sep': '09',
        'Total': '00' 
    }
    df_melted['Month_Num'] = df_melted['Month'].map(month_map)
    df_melted['Calendar_Year'] = df_melted.apply(compute_calendar_year,axis=1)
    df_melted['Year_Month'] = df_melted['Calendar_Year'].astype(str) + '-' + df_melted['Month_Num']
    mask_total = df_melted['Month']=='Total'
    df_melted.loc[mask_total, 'Year_Month'] = (
        pd.to_datetime(df_melted.loc[mask_total, 'Release_date']).dt.year.astype(str) + '-00'
    )
    df_melted['Fiscal_Year'] = df_melted.apply(get_fiscal_year, axis=1)
    df_melted = df_melted.drop(columns=['Month_Num', 'Calendar_Year','Month','Release_Year'])
    columns = df_melted.columns.tolist()
    melted_cols = ['Year_Month', 'Fiscal_Year','Value']
    for col in melted_cols:
        columns.remove(col)

    agency_idx = columns.index('Criminality')
    new_order = columns[:agency_idx + 1] + melted_cols + columns[agency_idx + 1:]
    df_melted = df_melted[new_order]
    df_melted = df_melted[df_melted['Value'] != 0] 
    df_melted = df_melted.sort_values(by=['Release_date', 'Year_Month'])
    mask_total_year = df_melted['Year_Month'].str.endswith('-00')

    # Replace "Total" → "Total_FYTD"
    df_melted.loc[mask_total_year & (df_melted['Release Reason'] == 'Total'), 'Release Reason'] = 'Total_FYTD'

    # For all other values in 'Release Reason' under that mask, add '_Total' suffix
    df_melted.loc[mask_total_year & (df_melted['Release Reason'] != 'Total_FYTD'), 'Release Reason'] = \
        df_melted.loc[mask_total_year & (df_melted['Release Reason'] != 'Total_FYTD'), 'Release Reason'] + '_Total'
    return df_melted
def transform_table_10(df):
    group = df.groupby('Release_date')
    agency_group_values = []
    for _, groupdf in group:
        n = len(groupdf)
        agency_group_values.extend(['CBP'] * 4 + ['ICE'] * 4 + ['Average'] * 4)
    df.insert(0,'Agency Group',agency_group_values)
    df.columns = df.columns.str.strip().str.replace(r'\s+',' ',regex=True)
    df['Release_date'] = pd.to_datetime(df['Release_date']).dt.date

    month_cols = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar',
                'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'FY Overall']
    df_melted = df.melt(
        id_vars=['Agency Group','Agency','EID','Release_date','Source_filename','Table_name','Table_code'],
        value_vars = month_cols,
        var_name = 'Month',
        value_name = 'Value'
    )
    df_melted['Release_Year'] = df_melted['Release_date'].astype(str).str.extract(r'(\d{4})').astype(int)
    month_map = {
        'Oct': '10', 'Nov': '11', 'Dec': '12',
        'Jan': '01', 'Feb': '02', 'Mar': '03',
        'Apr': '04', 'May': '05', 'Jun': '06',
        'Jul': '07', 'Aug': '08', 'Sep': '09',
        'FY Overall': '00' 
    }
    df_melted['Month_Num'] = df_melted['Month'].map(month_map)
    df_melted['Calendar_Year'] = df_melted.apply(compute_calendar_year,axis=1)
    df_melted['Year_Month'] = df_melted['Calendar_Year'].astype(str) + '-' + df_melted['Month_Num']
    mask_total = df_melted['Month']=='FY Overall'
    df_melted.loc[mask_total, 'Year_Month'] = (
        pd.to_datetime(df_melted.loc[mask_total, 'Release_date']).dt.year.astype(str) + '-00'
    )
    df_melted['Fiscal_Year'] = df_melted.apply(get_fiscal_year, axis=1)
    df_melted = df_melted.drop(columns=['Month_Num', 'Calendar_Year','Month','Release_Year'])
    columns = df_melted.columns.tolist()
    melted_cols = ['Year_Month', 'Fiscal_Year','Value']
    for col in melted_cols:
        columns.remove(col)

    agency_idx = columns.index('Agency')
    new_order = columns[:agency_idx + 1] + melted_cols + columns[agency_idx + 1:]
    df_melted = df_melted[new_order]
    df_melted = df_melted[df_melted['Value'] != 0] 
    df_melted = df_melted.sort_values(by=['Release_date', 'Year_Month'])
    mask_total_year = df_melted['Year_Month'].str.endswith('-00')

    # Replace "Total" → "Total_FYTD"
    df_melted.loc[mask_total_year & (df_melted['Agency Group'] == 'FY Overall'), 'Agency Group'] = 'FY Overall_FYTD'

    # For all other values in 'Agency Group' under that mask, add '_Total' suffix
    df_melted.loc[mask_total_year & (df_melted['Agency Group'] != 'FY Overall_FYTD'), 'Agency Group'] = \
        df_melted.loc[mask_total_year & (df_melted['Agency Group'] != 'FY Overall_FYTD'), 'Agency Group'] + '_Total'
    return df_melted
def transform_table_11(df):
    df.columns = df.columns.str.strip().str.replace(r'\s+',' ',regex=True)
    group = df.groupby('Release_date')
    agency_group_values = []
    for _, groupdf in group:
        n = len(groupdf)
        agency_group_values.extend(['CBP'] * 4 + ['ICE'] * 4 + ['Average'] * 4)
    df.insert(0,'Agency Group',agency_group_values)
    df['Release_date'] = pd.to_datetime(df['Release_date']).dt.date

    month_cols = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar',
                'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'FY Overall']
    df_melted = df.melt(
        id_vars=['Agency Group','Agency','EID','Release_date','Source_filename','Table_name','Table_code'],
        value_vars = month_cols,
        var_name = 'Month',
        value_name = 'Value'
    )
    df_melted['Release_Year'] = df_melted['Release_date'].astype(str).str.extract(r'(\d{4})').astype(int)
    month_map = {
        'Oct': '10', 'Nov': '11', 'Dec': '12',
        'Jan': '01', 'Feb': '02', 'Mar': '03',
        'Apr': '04', 'May': '05', 'Jun': '06',
        'Jul': '07', 'Aug': '08', 'Sep': '09',
        'FY Overall': '00' 
    }
    df_melted['Month_Num'] = df_melted['Month'].map(month_map)
    df_melted['Calendar_Year'] = df_melted.apply(compute_calendar_year,axis=1)
    df_melted['Year_Month'] = df_melted['Calendar_Year'].astype(str) + '-' + df_melted['Month_Num']
    mask_total = df_melted['Month']=='FY Overall'
    df_melted.loc[mask_total, 'Year_Month'] = (
        pd.to_datetime(df_melted.loc[mask_total, 'Release_date']).dt.year.astype(str) + '-00'
    )
    df_melted['Fiscal_Year'] = df_melted.apply(get_fiscal_year, axis=1)
    df_melted = df_melted.drop(columns=['Month_Num', 'Calendar_Year','Month','Release_Year'])
    columns = df_melted.columns.tolist()
    melted_cols = ['Year_Month', 'Fiscal_Year','Value']
    for col in melted_cols:
        columns.remove(col)

    agency_idx = columns.index('Agency')
    new_order = columns[:agency_idx + 1] + melted_cols + columns[agency_idx + 1:]
    df_melted = df_melted[new_order]
    df_melted = df_melted[df_melted['Value'] != 0] 
    df_melted = df_melted.sort_values(by=['Release_date', 'Year_Month'])
    mask_total_year = df_melted['Year_Month'].str.endswith('-00')

    # Replace "Total" → "Total_FYTD"
    df_melted.loc[mask_total_year & (df_melted['Agency Group'] == 'FY Overall'), 'Agency Group'] = 'FY Overall_FYTD'

    # For all other values in 'Agency Group' under that mask, add '_Total' suffix
    df_melted.loc[mask_total_year & (df_melted['Agency Group'] != 'FY Overall_FYTD'), 'Agency Group'] = \
        df_melted.loc[mask_total_year & (df_melted['Agency Group'] != 'FY Overall_FYTD'), 'Agency Group'] + '_Total'
    return df_melted
def transform_table_12(df):
    df.columns = df.columns.str.strip().str.replace(r'\s+',' ',regex=True)
    df['Release_date'] = pd.to_datetime(df['Release_date']).dt.date

    month_cols = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar',
                'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'FY Overall']
    df_melted = df.melt(
        id_vars=['Facility Type','EID','Release_date','Source_filename','Table_name','Table_code'],
        value_vars = month_cols,
        var_name = 'Month',
        value_name = 'Value'
    )
    df_melted['Release_Year'] = df_melted['Release_date'].astype(str).str.extract(r'(\d{4})').astype(int)
    month_map = {
        'Oct': '10', 'Nov': '11', 'Dec': '12',
        'Jan': '01', 'Feb': '02', 'Mar': '03',
        'Apr': '04', 'May': '05', 'Jun': '06',
        'Jul': '07', 'Aug': '08', 'Sep': '09',
        'FY Overall': '00' 
    }
    df_melted['Month_Num'] = df_melted['Month'].map(month_map)
    df_melted['Calendar_Year'] = df_melted.apply(compute_calendar_year,axis=1)
    df_melted['Year_Month'] = df_melted['Calendar_Year'].astype(str) + '-' + df_melted['Month_Num']
    mask_total = df_melted['Month']=='FY Overall'
    df_melted.loc[mask_total, 'Year_Month'] = (
        pd.to_datetime(df_melted.loc[mask_total, 'Release_date']).dt.year.astype(str) + '-00'
    )
    df_melted['Fiscal_Year'] = df_melted.apply(get_fiscal_year, axis=1)
    df_melted = df_melted.drop(columns=['Month_Num', 'Calendar_Year','Month','Release_Year'])
    columns = df_melted.columns.tolist()
    melted_cols = ['Year_Month', 'Fiscal_Year','Value']
    for col in melted_cols:
        columns.remove(col)

    agency_idx = columns.index('Facility Type')
    new_order = columns[:agency_idx + 1] + melted_cols + columns[agency_idx + 1:]
    df_melted = df_melted[new_order]
    df_melted = df_melted[df_melted['Value'] != 0] 
    df_melted = df_melted.sort_values(by=['Release_date', 'Year_Month'])
    mask_total_year = df_melted['Year_Month'].str.endswith('-00')

    # Replace "Total" → "Total_FYTD"
    # First assign 'FY Overall_FYTD' to rows where Facility Type is 'FY Overall'
    # First, handle both 'FY Overall' and 'Total'
    df_melted.loc[mask_total_year & df_melted['Facility Type'].isin(['FY Overall', 'Total']), 'Facility Type'] = 'FY Overall_FYTD'

    # Then suffix _Total to all other values under the mask
    df_melted.loc[mask_total_year & (df_melted['Facility Type'] != 'FY Overall_FYTD'), 'Facility Type'] = \
        df_melted.loc[mask_total_year & (df_melted['Facility Type'] != 'FY Overall_FYTD'), 'Facility Type'] + '_Total'
    return df_melted
def transform_table_13(df):
    df.columns = df.columns.str.strip().str.replace(r'\s+',' ',regex=True)
    df['Release_date'] = pd.to_datetime(df['Release_date']).dt.date
    month_cols = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar',
                'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'FY Overall']
    df_melted = df.melt(
        id_vars=['Facility Type','EID','Release_date','Source_filename','Table_name','Table_code'],
        value_vars = month_cols,
        var_name = 'Month',
        value_name = 'Value'
    )
    df_melted['Release_Year'] = df_melted['Release_date'].astype(str).str.extract(r'(\d{4})').astype(int)
    month_map = {
        'Oct': '10', 'Nov': '11', 'Dec': '12',
        'Jan': '01', 'Feb': '02', 'Mar': '03',
        'Apr': '04', 'May': '05', 'Jun': '06',
        'Jul': '07', 'Aug': '08', 'Sep': '09',
        'FY Overall': '00' 
    }
    df_melted['Month_Num'] = df_melted['Month'].map(month_map)
    df_melted['Calendar_Year'] = df_melted.apply(compute_calendar_year,axis=1)
    df_melted['Year_Month'] = df_melted['Calendar_Year'].astype(str) + '-' + df_melted['Month_Num']
    mask_total = df_melted['Month']=='FY Overall'
    df_melted.loc[mask_total, 'Year_Month'] = (
        pd.to_datetime(df_melted.loc[mask_total, 'Release_date']).dt.year.astype(str) + '-00'
    )
    df_melted['Fiscal_Year'] = df_melted.apply(get_fiscal_year, axis=1)
    df_melted = df_melted.drop(columns=['Month_Num', 'Calendar_Year','Month','Release_Year'])
    columns = df_melted.columns.tolist()
    melted_cols = ['Year_Month', 'Fiscal_Year','Value']
    for col in melted_cols:
        columns.remove(col)

    agency_idx = columns.index('Facility Type')
    new_order = columns[:agency_idx + 1] + melted_cols + columns[agency_idx + 1:]
    df_melted = df_melted[new_order]
    df_melted = df_melted[df_melted['Value'] != 0] 
    df_melted = df_melted.sort_values(by=['Release_date', 'Year_Month'])
    mask_total_year = df_melted['Year_Month'].str.endswith('-00')

    df_melted.loc[mask_total_year & df_melted['Facility Type'].isin(['FY Overall', 'Total']), 'Facility Type'] = 'FY Overall_FYTD'

    # Then suffix _Total to all other values under the mask
    df_melted.loc[mask_total_year & (df_melted['Facility Type'] != 'FY Overall_FYTD'), 'Facility Type'] = \
        df_melted.loc[mask_total_year & (df_melted['Facility Type'] != 'FY Overall_FYTD'), 'Facility Type'] + '_Total'
    return df_melted
def transform_table_14(df):
    df.columns = df.columns.str.strip().str.replace(r'\s+',' ',regex=True)
    df['Release_date'] = pd.to_datetime(df['Release_date']).dt.date
    month_cols = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar',
                'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'FY Overall']
    df_melted = df.melt(
        id_vars=['Arresting Agency','EID','Release_date','Source_filename','Table_name','Table_code'],
        value_vars = month_cols,
        var_name = 'Month',
        value_name = 'Value'
    )   
    df_melted['Release_Year'] = df_melted['Release_date'].astype(str).str.extract(r'(\d{4})').astype(int)
    month_map = {
        'Oct': '10', 'Nov': '11', 'Dec': '12',
        'Jan': '01', 'Feb': '02', 'Mar': '03',
        'Apr': '04', 'May': '05', 'Jun': '06',
        'Jul': '07', 'Aug': '08', 'Sep': '09',
        'FY Overall': '00' 
    }
    df_melted['Month_Num'] = df_melted['Month'].map(month_map)
    df_melted['Calendar_Year'] = df_melted.apply(compute_calendar_year,axis=1)
    df_melted['Year_Month'] = df_melted['Calendar_Year'].astype(str) + '-' + df_melted['Month_Num']
    mask_total = df_melted['Month']=='FY Overall'
    df_melted.loc[mask_total, 'Year_Month'] = (
        pd.to_datetime(df_melted.loc[mask_total, 'Release_date']).dt.year.astype(str) + '-00'
    )
    df_melted['Fiscal_Year'] = df_melted.apply(get_fiscal_year, axis=1)
    df_melted = df_melted.drop(columns=['Month_Num', 'Calendar_Year','Month','Release_Year'])
    columns = df_melted.columns.tolist()
    melted_cols = ['Year_Month', 'Fiscal_Year','Value']
    for col in melted_cols:
        columns.remove(col)

    agency_idx = columns.index('Arresting Agency')
    new_order = columns[:agency_idx + 1] + melted_cols + columns[agency_idx + 1:]
    df_melted = df_melted[new_order]
    df_melted = df_melted[df_melted['Value'] != 0] 
    df_melted = df_melted.sort_values(by=['Release_date', 'Year_Month'])
    mask_total_year = df_melted['Year_Month'].str.endswith('-00')

    df_melted.loc[mask_total_year & df_melted['Arresting Agency'].isin(['FY Overall', 'Total']), 'Arresting Agency'] = 'FY Overall_FYTD'
    df_melted.loc[mask_total_year & (df_melted['Arresting Agency'] != 'FY Overall_FYTD'), 'Arresting Agency'] = \
        df_melted.loc[mask_total_year & (df_melted['Arresting Agency'] != 'FY Overall_FYTD'), 'Arresting Agency'] + '_Total'
    return df_melted
def transform_table_15(df):
    df.columns = df.columns.str.strip().str.replace(r'\s+',' ',regex=True)
    return df

def transform_table_8(df):
    df1=df
    if df1.columns[0] == '':
        df1  = df.rename(columns = {"":"Removals","Removals":"Total"})
    return df1