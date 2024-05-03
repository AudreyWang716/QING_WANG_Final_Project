import pandas as pd
import plotly.express as px
import streamlit as st
import statsmodels.api as sm

# Add the page title
st.title('City-level Analysis')

# Add the page intro using markdown
st.markdown('''
            Similar to the State-level Analysis, this page offers an in-depth analysis at the factors that influence the distribution of music events across various cities in the United States. 
            <br> This page features four **interactive visualizations** as well: **1 bar chart** illustrating the number of music events per city and **3 scatter plots with regression lines**. These plots also examine the relationships between **city population**, **median household income**, **the number of airports**, and **the number of music events**. 
            <br> Each chart is equipped with key statistics and comprehensive analyses to enhance the understanding of how various elements affect the urban music event landscape. Explore the data to see how demographics and city infrastructure correlate with entertainment offerings across cities.
            ''', unsafe_allow_html=True)



## load data file
data = pd.read_csv('WANG_QING_final_data.csv')




# Code for creating a bar charts for the number of events of each city
# Insert a Markdown header
st.markdown("""
#### **Bar Chart for Number of Music Events per City**
""", unsafe_allow_html=True)

# Create an expander, which users can click to view its contents
expander1 = st.expander("Click to view")
with expander1:
    # Remove duplicate activities to ensure each event is only counted once in its corresponding city and state
    unique_events_per_city = data.drop_duplicates(subset=['Event Number', 'City', 'State']).groupby(['City', 'State']).size().reset_index(name='Number of Events')

    # Sort the results in descending order
    unique_events_per_city_sorted = unique_events_per_city.sort_values(by='Number of Events', ascending=False)

    # Create a new column for the Y-axis labels of the chart, including city and state names
    unique_events_per_city_sorted['City_State'] = unique_events_per_city_sorted['City'] + ', ' + unique_events_per_city_sorted['State']

    # Create an interactive horizontal bar chart
    fig = px.bar(unique_events_per_city_sorted, x='Number of Events', y='City_State', orientation='h',
                 labels={'Number of Events': 'Number of Events', 'City_State': 'City, State'},
                 title='Number of Music Events per City',
                 color_discrete_sequence=['lightcoral'])

    # Update the layout to improve the visual presentation
    fig.update_layout(
        xaxis_title='Number of Events',
        yaxis_title='City, State',
        height=1200,  
        width=800,
        margin=dict(l=0, r=0, t=50, b=0),
        yaxis={'categoryorder': 'total ascending', 'tickangle': 0},
        showlegend=False
    )
    # Plot the chart
    st.plotly_chart(fig, use_container_width=True)


    # Add the interactive instruction, styling for smaller, italic font in a specific color
    st.markdown('''
                <style>
                .small-font {
                    font-size: 14px;
                    font-style: italic;
                    color: lightcoral
                }
                </style>
                <div class="small-font">
                Hover over the bar to view specific data for each city.
                </div>
                &nbsp;
                ''', unsafe_allow_html=True)
    
    # Add analysis text
    st.markdown('''
                ##### Analysis
                - This chart displays the number of music events per city across the United States. **Las Vegas, Nevada**, leads with the highest number of events, significantly outpacing other cities, followed closely by **Chicago, Illniois** and **Los Angeles, California**. This suggests a strong concentration of music events in major urban centers
                - In contrast, cities like **Eau Claire, Wisconsin** and **Pasco, Washington**, host the fewest music events, indicating a lower demand or capacity for such events in smaller cities or less metropolitan areas
                - Overall, the distribution of music events across U.S. cities shows distinct **urban-rural disparities**, with major metropolitan areas and cities known for their cultural scenes hosting the majority of events''')







# Code for creating charts and analysis of the relationship between city population and number of events
# Insert a Markdown header
st.markdown("""
#### **Relationship between City Population and Number of Music Events**
""", unsafe_allow_html=True)

# Create an expander, which users can click to view its contents
expander2 = st.expander("Click to view")
with expander2:
    # Remove duplicate events to ensure each event is counted only once per city
    unique_events_per_city = data.drop_duplicates(subset=['Event Number', 'City']).groupby('City').size().reset_index(name='Number of Events')
    
    # Get population data for each city (make sure there are no duplicate city data)
    city_population = data.drop_duplicates(subset='City')[['City', 'Population_city']]

    # Merge event data with population data
    merged_data = pd.merge(unique_events_per_city, city_population, on='City')

    # Create a scatter plot with a regression line
    fig = px.scatter(merged_data, x='Population_city', y='Number of Events',
                     trendline="ols",
                     labels={"Population_city": "City Population", "Number of Events": "Number of Music Events"},
                     title="Relationship between City Population and Number of Music Events")

    # Update plot aesthetics
    fig.update_traces(marker=dict(color='lightcoral'), selector=dict(mode='markers'))
    fig.update_traces(line=dict(color='lightcoral'), selector=dict(type='scatter', mode='lines'))

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)

    # Add the interactive instruction, styling for smaller, italic font in a specific color
    st.markdown('''
                <style>
                .small-font {
                    font-size: 14px;
                    font-style: italic;
                    color: lightcoral
                }
                </style>
                <div class="small-font">
                Hover over the points and the regression line to view specific data.
                </div>
                &nbsp;
                ''', unsafe_allow_html=True)

    # Perform regression analysis using statsmodels to obtain detailed statistics
    X = sm.add_constant(merged_data['Population_city'])  # add constant term
    model = sm.OLS(merged_data['Number of Events'], X)
    results = model.fit()

    # Extract key statistical data
    r_squared = results.rsquared
    params = results.params
    p_values = results.pvalues
    slope = params['Population_city']
    intercept = params['const']
    p_value_slope = p_values['Population_city']

    # Display key statistical data
    st.markdown(f'''
                **Key Statistics:**
                - R² value: {r_squared:.3f}
                - Slope (coefficient for City Population): {slope:.10f}
                - Intercept: {intercept:.3f}
                - p-value for Slope: {p_value_slope:.10f}''')
    
    # Add analysis text
    st.markdown('''
                ##### Analysis
                - The scatter plot reveals a positive slope (0.001), showing a **positive correlation** where cities with greater populations tend to have more music events
                - The R² value of 0.318 indicates that about **32%** of the variation in music event numbers is accounted for by the size of the city population, which points to a **moderate correlation**
                - The p-value for the slope, being extremely low (0.0000000000), verifies that this correlation is **statistically significant**
                - Overall, this analysis indicates that the city population is a significant predictor of its music event frequency, though other important factors might also influence this outcome
                ''')








# Code for creating chart and analysis of the relationship between city mdeian househole income and number of events
# Insert a Markdown header
st.markdown("""
#### **Relationship between Median Household Income and Number of Music Events per City**
""", unsafe_allow_html=True)

# Create an expander, which users can click to view its contents
expander3 = st.expander("Click to view")
with expander3:
    # Clean data: remove currency symbols and commas, and convert to numeric type
    data['Median Household Income_city'] = pd.to_numeric(data['Median Household Income_city'].replace('[\$,]', '', regex=True))

    # Obtain median household income data for each state, ensuring no duplicate state data
    city_income = data.drop_duplicates(subset='City')[['City', 'Median Household Income_city']]

    # Merge event data with income data
    merged_data = pd.merge(unique_events_per_city, city_income, on='City')

    # Create a scatter plot with a regression line
    fig = px.scatter(merged_data, x='Median Household Income_city', y='Number of Events',
                     trendline="ols",
                     labels={"Median Household Income_city": "Median Household Income", "Number of Events": "Number of Music Events"},
                     title="Relationship between Median Household Income and Number of Music Events per City")

    # Update plot aesthetics
    fig.update_traces(marker=dict(color='lightcoral'), selector=dict(mode='markers'))
    fig.update_traces(line=dict(color='lightcoral'), selector=dict(type='scatter', mode='lines'))

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)

    # Add the interactive instruction, styling for smaller, italic font in a specific color
    st.markdown('''
                <style>
                .small-font {
                    font-size: 14px;
                    font-style: italic;
                    color: lightcoral
                }
                </style>
                <div class="small-font">
                Hover over the points and the regression line to view specific data.
                </div>
                &nbsp;
                ''', unsafe_allow_html=True)
    
    # Perform regression analysis using statsmodels to obtain detailed statistics
    X = sm.add_constant(merged_data['Median Household Income_city'])  # add constant term
    model = sm.OLS(merged_data['Number of Events'], X)
    results = model.fit()

    # Extract key statistical data
    r_squared = results.rsquared
    params = results.params
    p_values = results.pvalues
    slope = params['Median Household Income_city']
    intercept = params['const']
    p_value_slope = p_values['Median Household Income_city']

    # Display key statistical data
    st.markdown(f'''
                **Key Statistics:**
                - R² value: {r_squared:.3f}
                - Slope (coefficient for City Median Household Income): {slope:.10f}
                - Intercept: {intercept:.3f}
                - p-value for Slope: {p_value_slope:.10f}''')
    
    # Add analysis text
    st.markdown('''
                ##### Analysis
                - The scatter plot reveals a slight positive slope (0.004), indicating a **weak positive correlation** where cities with higher median household incomes tend to have slightly more music events
                - The R² value of 0.029 indicates that only about **2.9%** of the variation in the number of music events can be explained by median household income, pointing to a very **weak correlation**
                - The p-value for the slope is 0.0027506150, suggesting that while the correlation is **statistically significant**
                - Overall, this analysis implies that median household income has little influence on the number of music events in a city, it is not a strong predictor compared to other potential influences
                ''')






# Code for creating chart and analysis of the relationship between number of airports in the city and number of events
# Insert a Markdown header
st.markdown("""
#### **Relationship between Number of Airports and Number of Music Events per City**
""", unsafe_allow_html=True)

# Create an expander, which users can click to view its contents
expander4 = st.expander("Click to view")
with expander4:
    # Remove duplicate airport data to ensure that each airport is only counted once
    unique_airports_per_city = data.drop_duplicates(subset=['IATA', 'City']).groupby('City').size().reset_index(name='Number of Airports')

    # Count the number of airports in each state
    merged_data = pd.merge(unique_events_per_city, unique_airports_per_city, on='City', how='left')
    merged_data['Number of Airports'] = merged_data['Number of Airports'].fillna(0)  # 处理没有机场的城市

    # Create a scatter plot with a regression line
    fig = px.scatter(merged_data, x='Number of Airports', y='Number of Events',
                     trendline="ols",
                     labels={"Number of Airports": "Number of Airports", "Number of Events": "Number of Music Events"},
                     title="Relationship between Number of Airports and Number of Music Events per City")

    # Update plot aesthetics
    fig.update_traces(marker=dict(color='lightcoral'), selector=dict(mode='markers'))
    fig.update_traces(line=dict(color='lightcoral'), selector=dict(type='scatter', mode='lines'))

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)

    # Add the interactive instruction, styling for smaller, italic font in a specific color
    st.markdown('''
                <style>
                .small-font {
                    font-size: 14px;
                    font-style: italic;
                    color: lightcoral
                }
                </style>
                <div class="small-font">
                Hover over the points and the regression line to view specific data.
                </div>
                &nbsp;
                ''', unsafe_allow_html=True)
    
    # Perform regression analysis using statsmodels to obtain detailed statistics
    X = sm.add_constant(merged_data['Number of Airports'])  # add constant term
    model = sm.OLS(merged_data['Number of Events'], X)
    results = model.fit()

    # Extract key statistical data
    r_squared = results.rsquared
    params = results.params
    p_values = results.pvalues
    slope = params['Number of Airports']
    intercept = params['const']
    p_value_slope = p_values['Number of Airports']

    # Display key statistical data
    st.markdown(f'''
            **Key Statistics:**
            - R² value: {r_squared:.3f}
            - Slope (coefficient for Number of Airposts in a City): {slope:.10f}
            - Intercept: {intercept:.3f}
            - p-value for Slope: {p_value_slope:.10f}''')

    # Add analysis text
    st.markdown('''
                ##### Analysis
                - The scatter plot displays a positive slope (205.3603729343), suggesting a **positive correlation** where cities with a greater number of airports tend to host more music events
                - The R² value of 0.187 indicates that approximately **18.7%** of the variability in the number of music events can be explained by the number of airports in a city, pointing to a **weak correlation**
                - The p-value for the slope is extremely low (0.0000000000), confirming that this correlation is **statistically significant**
                - Overall, this analysis suggests that the presence of airports in a city has a certain impact on the number of music events, although it accounts for less than a fifth of the variation in event frequency. This implies that other factors also play significant roles in determining the distribution of music events in cities
                ''')