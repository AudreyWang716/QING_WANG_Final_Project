import streamlit as st
import pandas as pd

# Add the page title
st.title('Datasets & Overview')

# Create 2 tabs for Description & Overview
tabs = st.tabs(['Datasets Description','Data Overview','Specific Search'])

 



# Add text into the Datasets Description tab
with tabs[0]:
    st.header('Datasets Description')
    st.markdown("""
    This page include the URLs, API docs, and descriptions of the 3 datasets used for this projects.
    
    &nbsp;
    #### **Data Source 1: Ticketmaster API**
    - **URL:** [Ticketmaster Developer](https://developer.ticketmaster.com/)
    - **API Docs:** [Getting Started with Ticketmaster API](https://developer.ticketmaster.com/products-and-docs/apis/getting-started/)
    - **Brief Description:** 
      *The Ticketmaster API provides detailed information about concerts, sports events, and other entertainment activities, including event dates, venues, attractions, genres, artists/performers, ticket price ranges, and availability. This allows for the analysis of live event trends, artist popularity, and geographic distribution of music events.*

    #### **Data Source 2: Census.gov API**
    - **URLs:** 
      - [Data Census Main Page](https://data.census.gov/)
      - [Census Developers Page](https://www.census.gov/data/developers.html)
    - **API Docs:** [Census API User Guide](https://www.census.gov/data/developers/guidance/api-user-guide.Example_API_Queries.html#list-tab-559651575)
    - **Brief Description:** 
      *The U.S. Census Bureau's API offers comprehensive demographic and economic data for the United States, including information on population, income, and employment rates at the state and city levels. This dataset can be used to analyze demographic trends and economic conditions in various regions.*

    #### **Data Source 3: Wikipedia Airports Lists**
    - **URLs:**         
      - From  [List of Airports by IATA Code: A](https://en.wikipedia.org/wiki/List_of_airports_by_IATA_airport_code:_A)
      - Through  [List of Airports by IATA Code: Z](https://en.wikipedia.org/wiki/List_of_airports_by_IATA_airport_code:_Z)
    - **Brief Description:** 
      *This dataset provides structured and comprehensive data, including IATA codes, ICAO codes, airport names, and locations served, which is instrumental for analyzing global air travel connectivity and trends.*
    """)






# Add contents into the Data Overview tab
with tabs[1]:
    st.header('Data Overview')

    # Load data
    data = pd.read_csv('WANG_QING_final_data.csv')

    # Calculate the number of unique states and cities
    unique_states = data['State'].nunique()
    unique_cities = data.groupby('State')['City'].nunique().sum()
    
    # Calculate the number of unique events and airports
    unique_events = data['Event Number'].nunique() 
    unique_airports = data['IATA'].nunique()  

    # Add text message to display an overview of the data collected and import the above variables into the text
    st.markdown(f'''
    This project exclusively analyzes data from the United States market. It has collected the following data metrics from the three sources:

    &nbsp;
    #### Ticketmaster Data
    _Data on all music events held in the United States from the past six months to the upcoming year:_
    - **Event number**
    - **City** where the event is held
    - **State** where the event is held

    #### Census Data
    _Demographic and income data for every state and city in the U.S.:_
    - **State code**
    - **State name**
    - **State population**
    - **State median household income**
    - **City code**
    - **City name**
    - **City population**
    - **City median household income**

    #### Airport Information
    _Information on all airports in the United States:_
    - **IATA code**
    - **ICAO code**
    - **Airport name**
    - **City** where the airport is located
    - **State** where the airport is located
    
    &nbsp;
    #### Data Integration
    Using Pandas dataframes for data modeling, common attributes such as city and state names served as keys to merge relevant datasets. After data integration and cleansing, data on **{unique_events} music events** and **{unique_airports} airports** across **{unique_states} states** and **{unique_cities} cities** in the United States has been successfully compiled.

    _**Note:** In the process of merging and cleaning the data from multiple sources, inconsistencies in key identifiers such as city or state names—due to variations in spelling, the use of abbreviations, or incomplete records—prevented some entries in the original datasets from being aligned. Consequently, the number of entries in the consolidated dataset may be less than the actual situation._
    ''')
  
    

    



# Add contents into the Data Overview tab
with tabs[2]:
    st.header('Specific Search')
    st.markdown('''Here is an interactive tool designed for quick access to specific state or city data! ''')
    st.markdown('''
                <style>
                .small-font {
                    font-size: 14px;
                    font-style: italic;
                    color: lightcoral
                }
                </style>
                <div class="small-font">
                Select the States/Cities level, then choose the ones you are interested in, you will get the information about that State/City.
                </div>
                &nbsp;
                &nbsp;
                ''', unsafe_allow_html=True)
    
    
    
    
    
    # The following code creates an interactive tool that allows users to quickly access data for a specific state or city

    # Calculate the number of unique events and airports per state
    state_events = data.drop_duplicates(subset=['Event Number', 'State']).groupby('State').size()
    state_airports = data.drop_duplicates(subset=['IATA', 'State']).groupby('State').size()

    # Calculate the number of unique events and airports per city
    city_events = data.drop_duplicates(subset=['Event Number', 'City', 'State']).groupby(['City', 'State']).size()
    city_airports = data.drop_duplicates(subset=['IATA', 'City', 'State']).groupby(['City', 'State']).size()

    # Clean up income data and convert it to integer format
    data['Median Household Income_city'] = data['Median Household Income_city'].replace('[\$,]', '', regex=True).astype(int)
    data['Median Household Income_state'] = data['Median Household Income_state'].replace('[\$,]', '', regex=True).astype(int)

    # Update DataFrame storing economic indicators for states and cities
    state_pop_income = data.drop_duplicates(subset='State').set_index('State')[['Population_state', 'Median Household Income_state']]
    city_pop_income = data.drop_duplicates(subset=['City', 'State']).set_index(['City', 'State'])[['Population_city', 'Median Household Income_city']]


    # add st.radio for users to selects analysis level: State or City
    level = st.radio("Level:", ['State', 'City'])

    if level == 'State':
        # Add a dropdown menu for users to select a state
        state = st.selectbox('Select a State:', sorted(data['State'].unique()))
        # Retrieve the number of unique events for the selected state, defaulting to 0 if the state is not found
        events_count_state = state_events.get(state, 0)
        # Retrieve the number of unique airports for the selected state, defaulting to 0 if the state is not found
        airports_count_state = state_airports.get(state, 0)
        # Access the population and median household income for the selected state from the state_pop_income DataFrame
        population_state, median_income_state = state_pop_income.loc[state]

        # Create a DataFrame to store and display the data
        df = pd.DataFrame({
            "Metric": ["Total Number of Events", "Population", "Median Household Income", "Number of Airports"],
            "Value": [events_count_state, population_state, median_income_state, airports_count_state]
        })
        # Display the table
        st.table(df.set_index('Metric'))

    elif level == 'City':
        # Add a dropdown menu to select a state, sorting the unique states alphabetically
        state = st.selectbox('Select a State for City:', sorted(data['State'].unique()))
        # Once a state is selected, provide a second dropdown to select a city from the selected state
        city = st.selectbox('Select a City:', sorted(data[data['State'] == state]['City'].unique()))
        # Retrieve the count of unique events for the selected city and state, defaulting to 0 if not found
        events_count_city = city_events.get((city, state), 0)
        # Retrieve the count of unique airports for the selected city and state, defaulting to 0 if not found
        airports_count_city = city_airports.get((city, state), 0)
        # Access the population and median household income for the selected city and state from the DataFrame
        population_city, median_income_city = city_pop_income.loc[(city, state)]

        # Create a DataFrame to store and display the data
        df = pd.DataFrame({
            "Metric": ["Total Number of Events", "Population", "Median Household Income", "Number of Airports"],
            "Value": [events_count_city, population_city, median_income_city, airports_count_city]
        })
        # Display the table
        st.table(df.set_index('Metric'))














