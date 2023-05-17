# import folium
# from folium.plugins import MarkerCluster
# from streamlit_folium import folium_static
# import time
# import pandas as pd
# import streamlit as st
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from google.oauth2 import service_account
# import io
# from pytz import timezone

# # Define the default page configuration settings
# default_config = {
#     'page_title': 'My Streamlit App',
#     'page_icon': None,
#     'layout': 'wide',
#     'initial_sidebar_state': 'auto'
# }

# # Set the page configuration
# st.set_page_config(**default_config)

# # Define constants for Google Drive API
# SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
# SERVICE_ACCOUNT_FILE = 'fetch-url-384806-32bff5946d0d.json'

# st.title("DATA DASHBOARD & LIVE LOCATIONS")
# # Create a Streamlit container to display the results
# filename_container = st.empty()
# tabs_container = st.empty()

# interval_seconds = 30
# total_records = 0
# processed_file_ids = []


# # Define function to authenticate and create Google Drive API service

# def create_drive_service():
#     creds = None
#     try:
#         creds = service_account.Credentials.from_service_account_file(
#             SERVICE_ACCOUNT_FILE, scopes=SCOPES)
#     except Exception as e:
#         st.write(f"Error: {e}")
#     service = build('drive', 'v3', credentials=creds)
#     return service


# # Define function to read CSV files from a Google Drive folder
# def read_csv_from_drive(folder_id):
#     service = create_drive_service()
#     file_list = []
#     try:
#         query = f"'{folder_id}' in parents and mimeType='text/csv'"
#         results = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
#         items = results.get('files', [])
#         for item in items:
#             file_id = item['id']
#             file_name = item['name']
#             file = service.files().get_media(fileId=file_id).execute()
#             csv_data = pd.read_csv(io.StringIO(file.decode('utf-8')))
#             file_list.append((file_name, csv_data))
#     except HttpError as error:
#         st.write(f"An error occurred: {error}")
#     return file_list


# # Define function to load CSV data into a pandas DataFrame
# def load_data(file_list):
#     df_list = []
#     for file in file_list:
#         file_name, csv_data = file
#         csv_data.columns = [col.strip().lower() for col in csv_data.columns]
#         df_list.append(csv_data)
#     df = pd.concat(df_list, axis=0)
#     return df


# # Define function to display summary statistics of a DataFrame
# def display_summary_statistics(df):
#     global total_records

#     # Compute the analysis metrics
#     total_records += df['Count'].sum()

#     # create a timezone object for IST
#     ist = timezone('Asia/Kolkata')

#     # define a function to convert a timestamp to IST and return a human-readable string
#     def convert_timestamp(timestamp):
#         if timestamp != 0:
#             # convert the timestamp to a pandas datetime object with UTC timezone
#             dt = pd.to_datetime(timestamp, unit='s').tz_localize('UTC')
#             # convert the timezone to IST
#             dt = dt.astimezone(ist)
#             # format the datetime object as a human-readable string
#             return dt.strftime('%d/%b/%Y %H:%M:%S')
#         else:
#             return pd.NaT

#     df['Last Time IST'] = df.groupby('Mac ID', group_keys=False)['Last Time'].apply(
#         lambda x: x.apply(convert_timestamp))

#     start_time = pd.to_datetime(df['Last Time IST']).min().strftime('%d/%b/%Y %H:%M:%S')
#     end_time = pd.to_datetime(df['Last Time IST']).max().strftime('%d/%b/%Y %H:%M:%S')

#     mac_stats = df[['No', 'Mac ID', 'Location', 'Average Interval', 'Maximum Interval',
#                     'Minimum Interval', 'Last Time', 'Active']].reset_index(
#         drop=True)
#     mac_stats.index += 1

#     # Display the updated results

#     st.subheader(f"1.Total Records: {int(total_records)}")
#     # Display the updated results

#     st.subheader(f"2.Start Time: {start_time} IST")
#     # Display the updated results

#     st.subheader(f"3.End Time: {end_time} IST")
#     # Display the updated results

#     st.subheader("4.Summary Table:")
#     # Display the updated results

#     # Set the "No" column as the index
#     mac_stats = mac_stats.set_index("No")
#     st.write(mac_stats)


# total_records1 = 0


# # Define function to display a map of a DataFrame's latitude and longitude data
# def display_map(df):
#     global total_records1
#     # Compute the analysis metrics
#     total_records1 += df['Count'].sum()

#     # create a timezone object for IST
#     ist = timezone('Asia/Kolkata')

#     # define a function to convert a timestamp to IST and return a human-readable string
#     def convert_timestamp(timestamp):
#         if timestamp != 0:
#             # convert the timestamp to a pandas datetime object with UTC timezone
#             dt = pd.to_datetime(timestamp, unit='s').tz_localize('UTC')
#             # convert the timezone to IST
#             dt = dt.astimezone(ist)
#             # format the datetime object as a human-readable string
#             return dt.strftime('%d/%b/%Y %H:%M:%S')
#         else:
#             return pd.NaT

#     df['Last Time IST'] = df.groupby('Mac ID', group_keys=False)['Last Time'].apply(
#         lambda x: x.apply(convert_timestamp))

#     start_time = pd.to_datetime(df['Last Time IST']).min().strftime('%d/%b/%Y %H:%M:%S')
#     end_time = pd.to_datetime(df['Last Time IST']).max().strftime('%d/%b/%Y %H:%M:%S')

#     # Create a map object centered at the first location in the data
#     m = folium.Map(location=[df['Latitude'][0], df['Longitude'][0]], zoom_start=3)

#     # Create a marker cluster for the locations
#     marker_cluster = MarkerCluster().add_to(m)

#     # Add markers for each location in the data, with color based on the value of 'Status' column
#     active_locations = set()
#     active_locations_names = []
#     for i, row in df.iterrows():
#         if row['Active'] == 1:
#             active_locations.add((row['Location']))
#             icon_color = 'green'
#         else:
#             icon_color = 'orange'
#         popup_text = f"<b>{row['Mac ID']}"
#         folium.Marker(location=[row['Latitude'], row['Longitude']], tooltip=popup_text,
#                       icon=folium.Icon(color=icon_color)).add_to(marker_cluster)

#         active_locations_names = ','.join(active_locations).replace('{', '').replace('}', ''). \
#             replace("'", '')

#     active_records = len(df[df['Active'] == 1])

#     # Display the updated results

#     st.subheader("Live map of locations")
#     folium_static(m, width=800, height=600)

#     st.subheader(f"1.Total Records: {int(total_records1)}")

#     st.subheader(f"2.Start Time: {start_time} IST")

#     st.subheader(f"3.End Time: {end_time} IST")

#     st.subheader(f"4.Active Devices: {active_records} ")

#     st.subheader(f"5.Location of Active Device: {active_locations_names} ")


# def display_unknown_macid(df):
#     if any(value == 1 for value in df['Unknown Mac ID']):
#         st.warning('Yes')
#     else:
#         st.warning('No')


# def display_no_data(df):
#     if any(value == 1 for value in df['No Data']):
#         st.warning(1)
#     else:
#         st.warning(0)


# def display_data_unchanged(df):
#     if any(value == 1 for value in df['Data Unchanged']):
#         st.warning(1)
#     else:
#         st.warning(0)


# def display_data_dead(df):
#     if any(value == 1 for value in df['Data Dead']):
#         st.warning(1)
#     else:
#         st.warning(0)

# # Define main fction to run Streamlit app
# def main():
#     folder_id = '1CU1NdgBVRMosEulzkB-HXUFJJM2Wl6ij'
#     file_list = []
#     if folder_id:
#         new_files = read_csv_from_drive(folder_id)
#         if new_files:
#             file_list.extend(new_files)
#             # st.write(f"Found {len(new_files)} new CSV file(s) in folder.")

#         if file_list:
#             file_list = sorted(file_list, key=lambda x: x[0])
            
#             for file_name, df in file_list:
#                 # Display file name
#                 with filename_container:
#                     st.write(f"File: {file_name}")

#                     # Display summary statistics and map in tabs
#                 with tabs_container:
#                     tabs = st.tabs(
#                         ["Summary Statistics", "Map", "Unknown Mac ID", "No Data", "Data Unchanged", "Data Dead"])
#                     with tabs[0]:
#                         display_summary_statistics(df)
#                     with tabs[1]:
#                         display_map(df)
#                     with tabs[2]:
#                         display_unknown_macid(df)
#                     with tabs[3]:
#                         display_no_data(df)
#                     with tabs[4]:
#                         display_data_unchanged(df)
#                     with tabs[5]:
#                         display_data_dead(df)

#                 # Pause for 30 seconds before displaying next file
#                 time.sleep(30)
#         else:
#             st.write("No CSV files found in folder.")

#         # Pause for 3000 seconds before checking for new files
#         time.sleep(3000)


# if __name__ == "__main__":
#     main()


import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import time
import pandas as pd
import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import io
from pytz import timezone

# Define the default page configuration settings
default_config = {
    'page_title': 'DATA DASHBOARD ',
    'page_icon': None,
    'layout': 'wide',
    'initial_sidebar_state': 'auto'
}

# Set the page configuration
st.set_page_config(**default_config)

# Define constants for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'fetch-url-384806-32bff5946d0d.json'

st.title("DATA DASHBOARD & LIVE LOCATIONS")
# Create a Streamlit container to display the results
filename_container = st.empty()
tabs_container = st.empty()

interval_seconds = 30
interval_seconds_new = 5000
total_records = 0
processed_file_ids = []


# Define function to authenticate and create Google Drive API service

def create_drive_service():
    creds = None
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    except Exception as e:
        st.write(f"Error: {e}")
    service = build('drive', 'v3', credentials=creds)
    return service


# Define function to read CSV files from a Google Drive folder
def read_csv_from_drive(folder_id):
    service = create_drive_service()
    file_list = []
    try:
        query = f"'{folder_id}' in parents and mimeType='text/csv'"
        results = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        for item in items:
            file_id = item['id']
            file_name = item['name']
            file = service.files().get_media(fileId=file_id).execute()
            csv_data = pd.read_csv(io.StringIO(file.decode('utf-8')))
            file_list.append((file_name, csv_data))
    except HttpError as error:
        st.write(f"An error occurred: {error}")
    return file_list


# Define function to load CSV data into a pandas DataFrame
def load_data(file_list):
    df_list = []
    for file in file_list:
        file_name, csv_data = file
        csv_data.columns = [col.strip().lower() for col in csv_data.columns]
        df_list.append(csv_data)
    df = pd.concat(df_list, axis=0)
    return df


# Define function to display summary statistics of a DataFrame
def display_summary_statistics(df):
    global total_records

    # Compute the analysis metrics
    total_records += df['Count'].sum()

    # Find the minimum and maximum 'Last Time IST' values, excluding rows where the value is 0
    ist_times = pd.to_datetime(df['Last Time IST'], format='%d/%b/%Y %H:%M:%S', errors='coerce')
    ist_times = ist_times[ist_times.notna()]
    start_time = ist_times.min().strftime('%d/%b/%Y %H:%M:%S')
    end_time = ist_times.max().strftime('%d/%b/%Y %H:%M:%S')

    mac_stats = df[['No', 'Mac ID', 'Location', 'Average Interval', 'Maximum Interval',
                    'Minimum Interval', 'Last Time IST', 'Active', 'Battery', 'F/w Version']].reset_index(
        drop=True)
    # Replace null values in 'Battery' and 'F/w Version' columns with a placeholder
    mac_stats['Battery'].fillna('', inplace=True)
    mac_stats['F/w Version'].fillna('', inplace=True)
    mac_stats.index += 1

    # Display the updated results

    st.subheader(f"1.Total Records: {int(total_records)}")
    # Display the updated results

    st.subheader(f"2.Start Time: {start_time} IST")
    # Display the updated results

    st.subheader(f"3.End Time: {end_time} IST")
    # Display the updated results

    st.subheader("4.Summary Table:")
    # Display the updated results

    # Set the "No" column as the index
    mac_stats = mac_stats.set_index("No")
    # st.write(mac_stats)
    st.dataframe(mac_stats, width=1400)


total_records1 = 0


# Define function to display a map of a DataFrame's latitude and longitude data
def display_map(df):
    global total_records1
    # Compute the analysis metrics
    total_records1 += df['Count'].sum()

    # Find the minimum and maximum 'Last Time IST' values, excluding rows where the value is 0
    ist_times = pd.to_datetime(df['Last Time IST'], format='%d/%b/%Y %H:%M:%S', errors='coerce')
    ist_times = ist_times[ist_times.notna()]
    start_time = ist_times.min().strftime('%d/%b/%Y %H:%M:%S')
    end_time = ist_times.max().strftime('%d/%b/%Y %H:%M:%S')

    # Create a map object centered at the first location in the data
    # m = folium.Map(location=[df['Latitude'][0], df['Longitude'][0]], zoom_start=4)

    # Create a map object centered at the coordinates of India
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=6)
    # folium.Popup('India', parse_html=True).add_to(m)

    # Create a marker cluster for the locations
    marker_cluster = MarkerCluster().add_to(m)

    # Add markers for each location in the data, with color based on the value of 'Status' column
    active_locations = set()
    active_locations_names = []
    for i, row in df.iterrows():
        if row['Active'] == 1:
            active_locations.add((row['Location']))
            icon_color = 'green'
        else:
            icon_color = 'orange'
        popup_text = f"<b>{row['Mac ID']}"
        folium.Marker(location=[row['Latitude'], row['Longitude']], tooltip=popup_text,
                      icon=folium.Icon(color=icon_color)).add_to(marker_cluster)

        active_locations_names = ','.join(active_locations).replace('{', '').replace('}', ''). \
            replace("'", '')

    active_records = len(df[df['Active'] == 1])

    # Display the updated results

    st.subheader("Live map of locations")
    folium_static(m, width=900, height=1100)

    st.subheader(f"1.Total Records: {int(total_records1)}")

    st.subheader(f"2.Start Time: {start_time} IST")

    st.subheader(f"3.End Time: {end_time} IST")

    st.subheader(f"4.Active Devices: {active_records} ")

    st.subheader(f"5.Location of Active Device: {active_locations_names} ")


def display_unknown_macid(df):
    mac_ids = df.loc[df['Unknown Mac ID'] == 1, 'Mac ID'].tolist()
    if len(mac_ids) == 0:
        st.warning("None")
    else:
        st.write(mac_ids)


def display_no_data(df):
    mac_ids = df.loc[df['No Data'] == 1, 'Mac ID'].tolist()
    if len(mac_ids) == 0:
        st.warning("None")
    else:
        st.write(mac_ids)


def display_data_unchanged(df):
    mac_ids = df.loc[df['Data Unchanged'] == 1, 'Mac ID'].tolist()
    if len(mac_ids) == 0:
        st.warning("None")
    else:
        st.write(mac_ids)


def display_data_dead(df):
    mac_ids = df.loc[df['Data Dead'] == 1, 'Mac ID'].tolist()
    if len(mac_ids) == 0:
        st.warning("None")
    else:
        st.write(mac_ids)



# Define main function to run Streamlit app
def main():
    folder_id = '1CU1NdgBVRMosEulzkB-HXUFJJM2Wl6ij'      # 1CU1NdgBVRMosEulzkB-HXUFJJM2Wl6ij FETCHED folder
    # folder_id = '1G4FnXmCN2Els0KqI0eG3vE66hpohEspl'   # Kiran's processed folder
    file_list = []
    if folder_id:
        new_files = read_csv_from_drive(folder_id)
        if new_files:
            file_list.extend(new_files)
            # st.write(f"Found {len(new_files)} new CSV file(s) in folder.")

        if file_list:
            # Sort the file list by filename
            file_list = sorted(file_list, key=lambda x: x[0])

            for file_name, df in file_list:
                # Display file name
                with filename_container:
                    st.write(f"File: {file_name}")

                    # Display summary statistics and map in tabs
                with tabs_container:
                    tabs = st.tabs(
                        ["Summary Statistics", "Map", "Unknown Mac ID", "No Data", "Data Unchanged", "Data Dead"])
                    with tabs[0]:
                        display_summary_statistics(df)
                    with tabs[1]:
                        display_map(df)
                    with tabs[2]:
                        display_unknown_macid(df)
                    with tabs[3]:
                        display_no_data(df)
                    with tabs[4]:
                        display_data_unchanged(df)
                    with tabs[5]:
                        display_data_dead(df)

                # Pause for 30 seconds before displaying next file
                time.sleep(interval_seconds)
        else:
            st.write("No CSV files found in folder.")

        # Pause for 3000 seconds before checking for new files
        time.sleep(interval_seconds_new)


if __name__ == "__main__":
    main()

