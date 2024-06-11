import streamlit as st
import pandas as pd

from data_fetch import fetch_data_from_api, fetch_google_data_from_api
from check_changes import check_for_changes, display_change_details, save_data

from email_generate import generate_email

def main():
    st.title("🕵️‍♂️ Monitor Competitors")
    st.subheader("Click recheck for the latest competitor updates")
    if st.button("Recheck"):
        st.session_state['recheck'] = True
    
    if 'recheck' not in st.session_state:
        st.session_state['recheck'] = False

    if st.session_state['recheck']:
        news_response = fetch_data_from_api("************", "*************************")
        project_response = fetch_data_from_api("*********************", "*******************")
        google_news_response = fetch_google_data_from_api("*********************", "*********")
        
        news_data = pd.DataFrame(news_response['result']['capturedLists']['AECOM Website News'])
        project_data = pd.DataFrame(project_response['result']['capturedLists']['AECOM Project Details'])
        google_articles_data = pd.DataFrame(google_news_response['result']['capturedLists']['Articles'])

        # Load previous data with permission handling
        try:
            previous_news_data = pd.read_csv("previous_news_data.csv")
        except FileNotFoundError:
            previous_news_data = None
        except PermissionError as e:
            st.error(f"Permission error while accessing previous_news_data.csv: {e}")
            previous_news_data = None

        try:
            previous_project_data = pd.read_csv("previous_project_data.csv")
        except FileNotFoundError:
            previous_project_data = None
        except PermissionError as e:
            st.error(f"Permission error while accessing previous_project_data.csv: {e}")
            previous_project_data = None

        try:
            previous_google_data = pd.read_csv("previous_google_data.csv")
        except FileNotFoundError:
            previous_google_data = None
        except PermissionError as e:
            st.error(f"Permission error while accessing previous_google_data.csv: {e}")
            previous_google_data = None

        added_news, removed_news = check_for_changes(previous_news_data, news_data)
        added_projects, removed_projects = check_for_changes(previous_project_data, project_data)
        added_google, removed_google = check_for_changes(previous_google_data, google_articles_data)

        if not (added_news.empty and removed_news.empty):
            change_data = pd.concat([added_news, removed_news])
            email_content, send_status = generate_email(change_data, "Competitor's News Data")
            st.markdown("### Email Content:")
            st.write(email_content)

        if not (added_projects.empty and removed_projects.empty):
            change_data = pd.concat([added_projects, removed_projects])
            email_content, send_status = generate_email(change_data, "Competitor's Project Data")
            st.markdown("### Email Content:")
            st.write(email_content)

        if not (added_google.empty and removed_google.empty):
            change_data = pd.concat([added_google, removed_google])
            email_content, send_status = generate_email(change_data, "Google News about Competitors")
            st.markdown("### Email Content:")
            st.write(email_content)


        tabs = st.tabs(["Competitor's News Data", "Competitor's Project Data", "Google News about Competitors"])

        with tabs[0]:
            st.header("AECOM Website News")
            display_change_details(news_data, added_news, removed_news)

        with tabs[1]:
            st.header("AECOM Project Details")
            display_change_details(project_data, added_projects, removed_projects)

        with tabs[2]:
            st.header("Google News")
            display_change_details(google_articles_data, added_google, removed_google)


        # Save current data for future comparison
        save_data(project_data, "./subs/previous_project_data.csv")
        save_data(google_articles_data, "./subs/previous_google_data.csv")

        st.session_state['recheck'] = False

if __name__ == "__main__":
    main()