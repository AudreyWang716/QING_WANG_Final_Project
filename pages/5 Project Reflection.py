import streamlit as st

# Add page title
st.title('Project Reflection')

# Add main content markdown
st.markdown('''
            ##### 1. What did you set out to study?
            The purpose of this project was to analyze the distribution of music events across various states and cities in the United States and to understand how different factors like population size, median household income, and the number of airports(one of the indexes of infrastructure) influence this distribution. Originally, the project aimed to not only identify the direct effects of demographics on entertainment events but also opens avenues to explore how larger populations in accessible regions may lead to higher event frequencies and diverse entertainment offerings, and this focus was maintained throughout the project's duration.
            
            ##### 2. What did you discover/what were your conclusions?
            The findings confirmed some of the initial assumptions but also provided new insights:
            - **Population Size:** As anticipated, there was a positive correlation between population size and the number of music events, both at the city and state level.
            - **Infrastructure:** The number of airports in a state influenced the number of music events, underscoring the importance of accessibility for event frequency.
            - **Economic Factors:** Contrary to the expectations, median household income had a lesser impact on the number of music events than hypothesized, indicating that wealthier demographics do not necessarily correlate with more music events.
            
            ##### 3. What difficulties did you have in completing the project?
            - At the start, the biggest challenge was picking the right datasets and settling on a clear theme for the project. It took a while to figure out which data sources to use and how to pull them all together. Also, finding websites we could actually scrape data from, while sticking to all the rules and policies, really took up a lot of time and slowed things down at the beginning (I got banned by the first scrape-able website I chose).
            - Another challenge was figuring out how to present everything in the web app and what kind of analysis to do. Deciding on the layout, picking the right visuals, and figuring out the best ways to analyze the data took a lot of trial and error, adding an extra layer of complexity to the project.

            ##### 4. What skills did you wish you had while you were doing the project?
            - Firstly, I wished for better skills in web scraping and API integration, which would have improved the efficiency of data collection and allowed access to a wider array of data sources. 
            - Secondly, I realized the importance of advanced data manipulation and cleaning techniques, particularly for standardizing datasets to ensure precise analyses. 
            - Additionally, enhanced proficiency in using libraries such as Pandas and Matplotlib would have been beneficial for tackling more complex data analysis tasks and creating dynamic visualizations. 
            - Lastly, more sophisticated skills in statistical analysis and predictive modeling were desired to enable deeper and more insightful conclusions from the data.

            ##### 5. What would you do “next” to expand or augment the project?
            - **Integrating More Data Sources:** By including more detailed data on music event types, participant demographics, and economic impact assessments, the project can deepen its understanding of the cultural and economic contributions of music events. This could provide a clearer picture of how different types of events cater to various audience segments and their respective impacts on local economies.
            - **Economic and Engagement Impact Studies:** Conducting a detailed economic analysis alongside integrating user engagement data from social media and ticket sales would provide a comprehensive view of the economic benefits and audience engagement of music events. 
            - **Comparative Analysis:** Expanding the analysis to compare the U.S. music event landscape with those of other countries could reveal cultural differences and similarities in entertainment consumption. 
            ''')