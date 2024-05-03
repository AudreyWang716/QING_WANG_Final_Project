import streamlit as st

# Add page title
st.title('Conclusion & Insights')

# Add page intro markdown
st.markdown('''
            This section synthesizes the findings from previous comprehensive analysis of music events across different states and cities in the United States, offering key insights and conclusions drawn from the interactive visualizations and detailed analyses.
            ''')

# Add header and Key Conclusion markdown
st.header('Key Conclusion')
st.markdown('''
            **1. Population as a Primary Driver:** Both at the state and city levels, population size has proven to be a significant predictor of the number of music events. Areas with larger populations tend to host more events, highlighting the demand for entertainment in denser, more urbanized settings.
            <br>
            <br> **2. Impact of Infrastructure:** The availability of airports plays a certain role in the number of music events a state can support. States with more airports tend to have more music events, suggesting that ease of access is key for both performers and attendees.
            <br>
            <br> **3. Economic Influence:** While median household income showed some correlation with the number of music events, its impact is relatively minor compared to factors like population and infrastructure. The analysis indicates that wealthier areas do not necessarily host more events, contrary to what might be expected.
            <br>
            <br> **4. Regional Variations:** There are clear regional differences in the distribution of music events. Tourist-heavy states and major urban centers such as Nevada and California, and cities like Las Vegas, Chicago, and Los Angeles, host a disproportionately high number of events. This reflects not only their larger populations and better infrastructure but also possibly cultural preferences and local government support for the arts.
            ''', unsafe_allow_html=True)

# Add header and Insights markdown
st.header('Insights for Strategic Initiatives')
st.markdown('''
            **1. Enhancing Transportation and Accessibility:** There's a clear linkage between the number of airports and the frequency of music events in states, underscoring the importance of accessibility. Enhancing transportation links, including airports and public transit within cities, could substantially increase the number of events, benefiting local economies and cultural life.
            <br>
            <br>**2. Focused Event Promotion:** The data reveals opportunities in cities and states that currently host fewer music events. Event organizers can leverage this information to tailor their promotional efforts and expand into these less saturated markets, potentially increasing cultural offerings and diversity.
            <br>
            <br>**3. Supportive Cultural Policies:** Insights from this analysis should encourage policymakers to craft supportive cultural policies. By fostering an environment that encourages music events, especially in areas with lower event frequencies, governments can promote cultural inclusivity and economic growth.
            ''', unsafe_allow_html=True)
