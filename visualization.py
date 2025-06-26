import pandas as pd
import snowflake.connector
import snowflake.connector.pandas_tools as pd_tools
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import numpy as np
from datetime import timedelta
def connection_to_snowflake():
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
    return conn
def Visualization():
    #---------  FIG 1  --------------------
    conn = connection_to_snowflake()
    cur1 = conn.cursor()
    cur1.execute("Select * from DETENTIONDATA.DETENTIONDATA.TABLE_1")
    rows = cur1.fetchall()
    columns = [col[0] for col in cur1.description]
    df_main = pd.DataFrame(rows,columns=columns)
    fig1=Barplot_with_number_of_detainees_by_Processing_Disposition(df_main)
    #---------  FIG 2  --------------------
    cur2 = conn.cursor()
    cur2.execute("select * from DETENTIONDATA.DETENTIONDATA.TABLE_4")
    rows2 = cur2.fetchall()
    columns2 = [col[0] for col in cur2.description]
    df_main_4 = pd.DataFrame(rows2, columns=columns2)
    fig2 = Detainees_count_over_time(df_main_4)
    
    #--------- FIG 3  --------------------
    fig3=Detained_population_by_criminal_history_ice_only(df_main_4)
    
    #--------- FIG 4  --------------------
    fig4=ice_vs_cbp(df_main_4)
    #--------- FIG 5 ---------------------
    fig5 = generate_detained_population_table(df_main_4)
    
    return fig1,fig2,fig3,fig4,fig5
def Barplot_with_number_of_detainees_by_Processing_Disposition(df):
    # Ensure datetime conversion
    df['Release_date'] = pd.to_datetime(df['Release_date'])
    df['EID'] = pd.to_datetime(df['EID'])

    # Get max dates
    eid_date = df['EID'].max().date()
    max_date = df["Release_date"].max()

    # Filter relevant data
    df = df[
    (df["Release_date"] == max_date) &
    (df["Facility Type"] == "Total") &
    (df["Processing Disposition"] != "Grand Total")
    ].copy()  


    # Map labels to A, B, C...
    labels = df["Processing Disposition"].unique()
    label_map = {label: chr(65 + i) for i, label in enumerate(labels)}
    df["Label"] = df["Processing Disposition"].map(label_map)

    # Plot setup
    fig, ax = plt.subplots(figsize=(9, 4), dpi = 300)
    sns.barplot(data=df, x="Label", y="Value", hue="Label", palette="viridis", ax=ax, legend=False)


    ax.set_xticks([])  # Remove x-axis ticks
    ax.set_xlabel("Processing Disposition")
    ax.set_ylabel("Number of Detainees")
    ax.set_title(
        f"Barplot with number of detainees by Processing Disposition of {eid_date} "
        f"(Latest Release Date: {max_date.date()})",fontweight='bold'
    )

    # Set Y-limits with some headroom and space below
    max_height = df["Value"].max()
    ax.set_ylim(-max_height * 0.1, max_height * 1.15)

    # Add annotations
    for bar, label in zip(ax.patches, df["Label"]):
        height = bar.get_height()
        x = bar.get_x() + bar.get_width() / 2

        # Value above bar
        ax.text(x, height + max_height * 0.03, f"{int(height):,}",
                ha='center', va='bottom', fontsize=9)

        # Letter below bar (inside plot)
        ax.text(x, -max_height * 0.02, label,
                ha='center', va='top', fontsize=12, fontweight='bold', color='black')

    # Create a legend mapping
    bar_colors = [bar.get_facecolor() for bar in ax.patches]
    legend_texts = [f"{letter}: {full_label}" for (full_label, letter), color in zip(label_map.items(), bar_colors)]
    legend_text = "\n".join(legend_texts)

    # Draw legend inside plot
    props = dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='gray', alpha=0.8)
    ax.text(0.98, 0.95, legend_text, transform=ax.transAxes,
            fontsize=10, va='top', ha='right', bbox=props)

    plt.tight_layout()
    return fig

def Detainees_count_over_time(df):
    filter_grand_total = df[(df['Criminality'] == 'Grand Total') & (df['Arresting Agency'] == 'Total')].copy()
    filter_grand_total['EID'] = pd.to_datetime(filter_grand_total['EID'])
    filter_grand_total = filter_grand_total.sort_values('EID')
    max_date = filter_grand_total['EID'].max().date()
    total_count = filter_grand_total['Count'].sum()
    latest_row = filter_grand_total.iloc[-1]
    latest_date = latest_row['EID']
    latest_value = latest_row['Count']

    # Capture the figure object
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    sns.lineplot(data=filter_grand_total, x='EID', y='Count',
                 color='red', linewidth=2.5, marker='', ax=ax)

    ax.fill_between(filter_grand_total['EID'],
                    filter_grand_total['Count'],
                    color='gray', alpha=0.2)

    ax.text(latest_date, latest_value + 0.1, f"Total: {int(latest_value):,}",
            ha='right', va='bottom', fontsize=10, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='none', pad=2))

    ax.text(filter_grand_total['EID'].iloc[0],
            filter_grand_total['Count'].max() + 0.1,
            f"Total from Jan to till now: {int(total_count):,}",
            ha='left', va='bottom', fontsize=12, fontweight='bold',
            bbox=dict(facecolor='lightyellow', edgecolor='gray', boxstyle='round'))

    ax.set_title(f"Detainee Counts Over Time from 2023-01-09 to {max_date}", fontsize=16, fontweight='bold')
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Number of Detainees", fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, linestyle='--', alpha=0.5)
    fig.tight_layout()

    return fig

def Detained_population_by_criminal_history_ice_only(df):
    ice_data = df.copy()
    ice_data["EID"] = pd.to_datetime(ice_data["EID"], format="%m/%d/%Y")
    ice_data = ice_data[ice_data["EID"] > pd.Timestamp("2025-01-01")]
    ice_data_only = ice_data[(ice_data["Arresting Agency"]=="ICE") & (ice_data["Criminality"]!="Total")]
    ice_after_pivot = ice_data_only.pivot_table(
        index="EID",
        columns="Criminality",
        values="Count",
        aggfunc=lambda x: x.iloc[-1]
    ).reset_index()
    df = ice_after_pivot.copy()
    # Ensure EID is datetime, then format as date
    df["EID"] = pd.to_datetime(df["EID"]).dt.strftime("%Y-%m-%d")
    max_date = df["EID"].max()
    # Clean column names
    df.columns = df.columns.str.strip()

    # Sort by date
    df = df.sort_values("EID")

    # Create numeric y positions
    y_pos = range(len(df))

    # Categories and colors
    categories = ["Convicted Criminal", "Pending Criminal Charges", "Other Immigration Violator"]
    colors = ["#004c6d", "#007baf", "#00b4d8"]

    # Create subplots
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 8), dpi=300)

    for i, category in enumerate(categories):
        bars = axes[i].barh(y_pos, df[category], color=colors[i])
        
        # Bold category titles
        axes[i].set_title(category, fontweight='bold')
        
        axes[i].invert_yaxis()
        axes[i].set_xlabel("Detainee Count")
        axes[i].set_yticks(y_pos)

        if i == 0:
            # Bold date labels on y-axis
            axes[i].set_yticklabels(df["EID"], fontweight='bold')
        else:
            axes[i].set_yticklabels([])
            axes[i].tick_params(axis='y', left=False)
            
        # Increase x-axis limit to add space for labels
        max_width = df[category].max()
        axes[i].set_xlim(0, max_width * 1.2)  # add 20% padding on right

        # Add value labels
        for bar in bars:
            width = bar.get_width()
            y = bar.get_y() + bar.get_height() / 2
            
            offset = max_width * 0.02  # 2% of max width as offset
            
            # Check if label fits outside the bar
            if width + offset > axes[i].get_xlim()[1]:
                # Place label inside the bar, aligned right, white text
                x_pos = width - offset
                ha = 'right'
                color = 'white'
            else:
                # Place label outside the bar, aligned left, black text
                x_pos = width + offset
                ha = 'left'
                color = 'black'

            axes[i].text(x_pos, y, f'{int(width):,}', va='center', ha=ha, fontsize=12, fontweight='bold', color=color)

    # Overall title
    fig.suptitle(f"Total Detained Population by Criminal History (ICE Arrests Only, {max_date})", fontsize=20, fontweight='bold')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    return fig

def ice_vs_cbp(df):
    df["EID"] = pd.to_datetime(df["EID"], format="%m/%d/%Y")
    max_date = df["EID"].max().date()
    df = df[(df['Criminality'] == 'Total') & (df['Arresting Agency'].isin(['ICE', 'CBP'])) & (df['EID'] > pd.Timestamp("2025-01-01"))]
    df_after_pivot = df.pivot_table(
        index="EID",
        columns="Arresting Agency",
        values="Count",
        aggfunc=lambda x: x.iloc[-1]
    )
    df_after_pivot = df_after_pivot.sort_index()

    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)

    max_y_for_plot = 0
    last_x = df_after_pivot.index[-1]
    label_shift_days = 3
    max_x_label = last_x + timedelta(days=label_shift_days)

    color_map = {
        "ICE": "#2b9dce",
        "CBP": "#119d5e"
    }

    for col in df_after_pivot.columns:
        ax.plot(df_after_pivot.index, df_after_pivot[col],
                label=col,
                marker='',
                linewidth=2.5,
                color=color_map.get(col, 'black'))

        last_y = df_after_pivot[col].iloc[-1]
        max_y_for_plot = max(max_y_for_plot, last_y)

        ax.text(
            x=last_x + timedelta(days=label_shift_days),
            y=last_y,
            s=f"{col}: {int(last_y):,}",
            ha='left',
            va='center',
            fontsize=10,
            fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='none', pad=1),
            color=color_map.get(col, 'black')
        )

    ax.set_xlim(right=max_x_label + timedelta(days=1))
    ax.set_ylim(top=max_y_for_plot * 1.05)
    fig.subplots_adjust(right=0.8)

    ax.set_title(f"Detained Population by Arresting Agency ({max_date})", fontsize=14, fontweight='bold')
    ax.set_xlabel("", fontsize=12)
    ax.set_ylabel("Number of Detainees", fontsize=12)
    ax.tick_params(axis='x', rotation=45)

    ax.legend(title="Arresting Agency", loc='center left', bbox_to_anchor=(1, 0.5))

    ax.grid(True, linestyle='--', alpha=0.5)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(True)

    fig.tight_layout()
    return fig # Return the figure object for further use if needed


def generate_detained_population_table(df_main_4):
    ice_data = df_main_4.copy()
    ice_data["EID"] = pd.to_datetime(ice_data["EID"], format="%m/%d/%Y")
    max = ice_data["EID"].max().date()
    ice_data = ice_data[ice_data["EID"] > pd.Timestamp("2025-01-01")]
    ice_data_only = ice_data[(ice_data["Arresting Agency"] == "ICE") & (ice_data["Criminality"] != "Total")]
    
    ice_after_pivot = ice_data_only.pivot_table(
        index="EID",
        columns="Criminality",
        values="Count",
        aggfunc=lambda x: x.iloc[-1]
    ).reset_index()
    
    df_summary = ice_after_pivot.copy()
    df_summary["Total"] = df_summary.loc[:, df_summary.columns != "EID"].sum(axis=1)
    
    criminality_cols = [col for col in df_summary.columns if col not in ["EID", "Total"]]
    for col in criminality_cols:
        df_summary[f"{col}(%)"] = (df_summary[col] / df_summary["Total"]) * 100

    clean_df = df_summary.copy()
    for col in clean_df.columns:
        if col != 'EID':
            clean_df[col] = pd.to_numeric(clean_df[col], errors='coerce').round().astype('Int64')  # Allows NaNs

    df = clean_df[['EID', 'Convicted Criminal','Pending Criminal Charges', 'Other Immigration Violator',
                   'Total', 'Convicted Criminal(%)', 'Pending Criminal Charges(%)',
                   'Other Immigration Violator(%)']]
    
    df["EID"] = pd.to_datetime(df["EID"]).dt.strftime("%Y-%m-%d")

    # Add % symbol to selected percentage columns
    percent_columns = [
        'Convicted Criminal(%)',
        'Pending Criminal Charges(%)',
        'Other Immigration Violator(%)'
    ]

    for col in percent_columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"{x}%" if pd.notna(x) and x != "" else "")

    # Insert blank rows between existing rows to create vertical spacing
    def insert_blank_rows(df):
        empty_row = pd.Series([""] * len(df.columns), index=df.columns)
        new_rows = []
        for i in range(len(df)):
            new_rows.append(df.iloc[i])
            if i != len(df) - 1:
                new_rows.append(empty_row)  # add empty row between rows
        return pd.DataFrame(new_rows).reset_index(drop=True)

    df_with_gaps = insert_blank_rows(df)

    # Add one blank row after the header (for visual spacing)
    blank_row = pd.DataFrame([[""] * len(df.columns)], columns=df.columns)
    df_with_gaps = pd.concat([blank_row, df_with_gaps], ignore_index=True)

    # Header wrapping (optional)
    def wrap_header(col, max_len=12):
        if len(col) > max_len:
            parts = col.split()
            if len(parts) > 1:
                mid = len(parts) // 2
                wrapped = '\n'.join([' '.join(parts[:mid]), ' '.join(parts[mid:])])
            else:
                mid = len(col) // 2
                wrapped = col[:mid] + '\n' + col[mid:]
        else:
            wrapped = col
        return wrapped + '\n\n'  # Add spacing below headers

    wrapped_columns = [wrap_header(col) for col in df_with_gaps.columns]

    # --- Plotting ---
    fig, ax = plt.subplots(figsize=(5, len(df_with_gaps) * 0.3), dpi=300)
    ax.axis('off')

    table = ax.table(
        cellText=df_with_gaps.values,
        colLabels=wrapped_columns,
        loc='center',
        cellLoc='center'
    )

    # Remove all borders first
    for key, cell in table.get_celld().items():
        cell.visible_edges = ''

    # Style header row with bold text and bottom border
    n_rows, n_cols = df_with_gaps.shape
    for col_idx in range(n_cols):
        header_cell = table[0, col_idx]
        header_cell.set_text_props(fontweight='bold')
        header_cell.visible_edges = 'B'  # Bottom edge only

    # Font and column sizing
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(n_cols)))

    # Add title close to the table
    ax.text(0.5, 1.02, f"Detained Population by Criminal History (ICE Arrests Only,{max})",
            fontsize=14, fontweight="bold", ha='center', transform=ax.transAxes)

    fig.subplots_adjust(top=0.8)
    return fig

if __name__ == "__main__":
    Visualization()
    
