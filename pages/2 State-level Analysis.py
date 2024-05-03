import streamlit as st
import pandas as pd
import plotly.express as px
import statsmodels.api as sm

# Add the page title
st.title('State-level Analysis')

# Add the page intro using markdown
st.markdown('''
            This page contains comprehensive examination of the factors influencing the distribution of music events across different states in the United States. 
            <br> Four detailed **interactive visualizations** are featured in this page: **1 bar chart** illustrating the number of music events per state and **3 scatter plots with regression lines** analyzing the relationships between **state population**, **median household income**, **number of airports**, and **the number of music events**. 
            <br> Each chart is paired with key statistics and thoughtful analyses to enhance the understanding of how various elements affect the music event landscape at the state level. Dive into the data to explore how demographics and infrastructure correlate with entertainment offerings across the states.
            ''', unsafe_allow_html=True)



# load data file
data = pd.read_csv('WANG_QING_final_data.csv')



# Code for creating a bar charts for the number of events of each state
# Insert a Markdown header
st.markdown("""
#### **Bar Chart for Number of Music Events per State**
""", unsafe_allow_html=True)

# Create an expander, which users can click to view its contents
expander1 = st.expander("Click to view")
with expander1:
    # Remove duplicate events to ensure each event is counted only once per state
    unique_events_per_state = data.drop_duplicates(subset=['Event Number', 'State']).groupby('State').size()

    # Sort the results in descending order to display the states with the most events at the top
    unique_events_per_state_sorted = unique_events_per_state.sort_values(ascending=False)

    # Create an interactive horizontal bar chart
    fig = px.bar(unique_events_per_state_sorted, orientation='h',
                 labels={'value': 'Number of Events', 'index': 'State'},
                 title='Number of Music Events per State',
                 color_discrete_sequence=['lightcoral'])

    # Update the layout to improve the visual presentation
    fig.update_layout(
        xaxis_title='Number of Events',
        yaxis_title='State',
        height=800,  
        width=800,   
        margin=dict(l=0, r=0, t=50, b=0),  # Adjust chart margins
        yaxis={'categoryorder': 'total ascending', 'tickangle': 0},
        showlegend = False
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
                Hover over the bar to view specific data for each state.
                </div>
                &nbsp;
                ''', unsafe_allow_html=True)
    
    # Add analysis text
    st.markdown('''
                ##### Analysis:
                - This chart displays the number of music events per state in the United States. Notably, **Nevada** has the highest number of events, significantly surpassing other states, followed by **California** and **Texas**
                - In contrast, **Kentucky**, **Alaska**, and **Vermont** have the fewest events
                - Overall, the distribution of music events across the U.S. shows clear **regional differences**, with major cities and tourist-heavy states hosting more events''')








# Code for creating charts and analysis of the relationship between state population and number of events
# Insert a Markdown header
st.markdown("""
#### **Relationship between State Population and Number of Music Events**
""", unsafe_allow_html=True)

# Create an expander, which users can click to view its contents
expander2 = st.expander("Click to view")
with expander2:
    # Remove duplicate events to ensure each event is counted only once per state
    data_unique_events = data.drop_duplicates(subset=['Event Number', 'State'])

    # Count the number of events per state
    events_per_state = data_unique_events.groupby('State').size().reset_index(name='Number of Events')

    # Ensure the population data is in integer format
    if data['Population_state'].dtype == 'O':  # Object type, typically used for strings
        data['Population_state'] = data['Population_state'].str.replace(',', '').astype(int)
    elif data['Population_state'].dtype != 'int':
        data['Population_state'] = data['Population_state'].astype(int)

    # Obtain population data for each state, ensuring no duplicate state data
    state_population = data.drop_duplicates(subset='State')[['State', 'Population_state']]

    # Merge event data with population data
    merged_data = pd.merge(events_per_state, state_population, on='State')

    # Create a scatter plot with a regression line
    fig = px.scatter(merged_data, x='Population_state', y='Number of Events', 
                     trendline="ols", 
                     labels={"Population_state": "State Population", "Number of Events": "Number of Music Events"},
                     title="Relationship between State Population and Number of Music Events")

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
    X = sm.add_constant(merged_data['Population_state'])  # Add a constant term
    model = sm.OLS(merged_data['Number of Events'], X)
    results = model.fit()

    # Extract key statistical data
    r_squared = results.rsquared
    params = results.params
    p_values = results.pvalues
    slope = params['Population_state']
    intercept = params['const']
    p_value_slope = p_values['Population_state']

    # Display key statistical data
    st.markdown(f'''
                **Key Statistics:**
                - R² value: {r_squared:.3f}
                - Slope (coefficient for State Population): {slope:.10f}
                - Intercept: {intercept:.3f}
                - p-value for Slope: {p_value_slope:.10f}''')
    
    # Add analysis text
    st.markdown('''
                ##### Analysis:
                - The scatter plot, with a slope of 0.0001072983, indicates a **positive correlation** between state population and the number of music events
                - The R² value of 0.436 suggests that approximately **44%** of the variability in the number of music events is explained by population size, highlighting a **moderate correlation**
                - The extremely low p-value (0.0000002487) confirms that this relationship is **statistically significant** 
                - Overall, this analysis indicates that state population size is a significant predictor of the number of music events, but there could be other substantial factors influencing the distribution of music events
                ''')









# Code for creating chart and analysis of the relationship between state mdeian househole income and number of events
# Insert a Markdown header
st.markdown("""
#### **Relationship between Median Household Income and Number of Music Events per State**
""", unsafe_allow_html=True)

# Create an expander, which users can click to view its contents
expander3 = st.expander("Click to view")
with expander3:
    # Ensure median household income data is in integer format and handle possible formatting issues
    if data['Median Household Income_state'].dtype == 'O':  # Object type
        data['Median Household Income_state'] = data['Median Household Income_state'].str.replace(',', '').str.replace('$', '').astype(int)
    elif data['Median Household Income_state'].dtype != 'int':
        data['Median Household Income_state'] = data['Median Household Income_state'].astype(int)

    # Obtain median household income data for each state, ensuring no duplicate state data
    state_income = data.drop_duplicates(subset='State')[['State', 'Median Household Income_state']]

    # Merge event data with income data
    merged_data = pd.merge(events_per_state, state_income, on='State')

    # Create a scatter plot with a regression line
    fig = px.scatter(merged_data, x='Median Household Income_state', y='Number of Events', 
                     trendline="ols", 
                     labels={"Median Household Income_state": "Median Household Income", "Number of Events": "Number of Music Events"},
                     title="Relationship between Median Household Income and Number of Music Events per State")

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
    X = sm.add_constant(merged_data['Median Household Income_state'])  # add constant term
    model = sm.OLS(merged_data['Number of Events'], X)
    results = model.fit()

    # Extract key statistical data
    r_squared = results.rsquared
    params = results.params
    p_values = results.pvalues
    slope = params['Median Household Income_state']
    intercept = params['const']
    p_value_slope = p_values['Median Household Income_state']

    # Display key statistical data
    st.markdown(f'''
                **Key Statistics:**
                - R² value: {r_squared:.3f}
                - Slope (coefficient for State Median Household Income): {slope:.10f}
                - Intercept: {intercept:.3f}
                - p-value for Slope: {p_value_slope:.10f}''')
    
    # Add analysis text
    st.markdown('''
                ##### Analysis:
                - The scatter plot shows a very slight positive slope (0.0177235229), suggesting a **weak positive correlation** where higher median incomes are associated with a slight increase in the number of music events
                - The R² value of 0.029 indicates that only about **2.9%** of the variability in the number of music events can be explained by differences in median household income. This low percentage points to a **very weak correlation**
                - Additionally, the p-value for the slope is 0.2405559097, which is **not statistically significant**
                - Overall, this analysis suggests that state median household income is not a strong predictor of the number of music events
                ''')








# Code for creating chart and analysis of the relationship between number of airports in a state and number of events
# Insert a Markdown header
st.markdown("""
#### **Relationship between Number of Airports and Number of Music Events per State**
""", unsafe_allow_html=True)

# Create an expander, which users can click to view its contents
expander4 = st.expander("Click to view")
with expander4:
    # Remove duplicate airport data to ensure that each airport is only counted once
    data_unique_airports = data.drop_duplicates(subset=['IATA', 'State'])

    # Count the number of airports in each state
    airports_per_state = data_unique_airports.groupby('State').size().reset_index(name='Number of Airports')

    # Merge event data and airport data
    merged_data = pd.merge(events_per_state, airports_per_state, on='State')

    # Create a scatter plot with a regression line
    fig = px.scatter(merged_data, x='Number of Airports', y='Number of Events', 
                     trendline="ols", 
                     labels={"Number of Airports": "Number of Airports", "Number of Events": "Number of Music Events"},
                     title="Relationship between Number of Airports and Number of Music Events per State")

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
                - Slope (coefficient for Number of Airports in a State): {slope:.10f}
                - Intercept: {intercept:.3f}
                - p-value for Slope: {p_value_slope:.10f}''')
    
    # Add analysis text
    st.markdown('''
                ##### Analysis:
                - The scatter plot displays a strong positive slope (85.2325497393), indicating a **positive correlation** where states with more airports host a notably higher number of music events
                - The R² value of 0.430 implies that approximately **43%** of the variability in the number of music events can be explained by the number of airports in a state, highlighting a **moderate correlation**
                - The p-value for the slope is extremely low (0.0000003114), confirming that the correlation is **statistically significant**
                - Overall, this analysis suggests that the number of airports in a state is a clear predictor of the number of music events, but there could be other substantial factors as well
                ''')
