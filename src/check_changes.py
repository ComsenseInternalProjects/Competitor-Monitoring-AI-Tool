import pandas as pd
import streamlit as st
import os 

# Function to check for changes in the data
def check_for_changes(previous_data, current_data):
    if previous_data is None:
        return pd.DataFrame(), pd.DataFrame()
    
    added_rows = current_data[~current_data.isin(previous_data)].dropna()
    removed_rows = previous_data[~previous_data.isin(current_data)].dropna()

    return added_rows, removed_rows

# Function to display change details
def display_change_details(data, added_rows, removed_rows):
    tabs = ["Data"]
    tab_contents = [data]
    
    if not added_rows.empty:
        tabs.append("Added Rows")
        tab_contents.append(added_rows)
    if not removed_rows.empty:
        tabs.append("Removed Rows")
        tab_contents.append(removed_rows)
    
    if added_rows.empty and removed_rows.empty:
        st.info("No changes detected.")
        st.dataframe(data, use_container_width=True,hide_index=True)  # Display without index
    else:
        st.subheader("Data and Changes:")
        tabs_container = st.tabs(tabs)
        for i, tab_content in enumerate(tab_contents):
            with tabs_container[i]:
                st.dataframe(tab_content, use_container_width=True,hide_index=True)  # Display without index

# Function to save data and handle permission errors
def save_data(data, filename):
    full_path = os.path.join(os.getcwd(), filename)  # Get the full path
    try:
        data.to_csv(full_path, index=False)
    except PermissionError as e:
        st.error(f"Permission error while saving {filename}: {e}")