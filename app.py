import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import plotly.figure_factory as ff
from streamlit_option_menu import option_menu


st.set_page_config("wide")
st.title("Customer satisfaction Analysis")

selected=option_menu("Main menu",["📊Data Visualization📈","Insights🔍","👀 Actions"],orientation="horizontal")


df=pd.read_csv("test.csv")

if selected=="📊Data Visualization📈":
    col1, col2 = st.columns(2,gap="large")
    with col1:
        satisfaction_counts = df['satisfaction'].value_counts()
        satisfaction_df = pd.DataFrame({'Satisfaction': satisfaction_counts.index, 'Count': satisfaction_counts.values})
        fig = px.pie(satisfaction_df, values='Count', names='Satisfaction', 
             title='Percentage of Satisfaction', 
             labels={'Satisfaction': 'Satisfaction'},
             template='plotly_white',
             hole=0.7, # Adjust hole size if needed
             )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        fig = px.histogram(df, x='Gender', color='satisfaction',marginal="box", barmode='group',title="relation b/w gender and satisfaction")
        st.plotly_chart(fig,use_container_width=True)


    with col1:
        fig = px.histogram(df, x='Customer Type', color='satisfaction',marginal="box", barmode='group',title="relation b/w Customer type and satisfaction")
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        fig = px.histogram(df, x='Type of Travel', color='satisfaction',marginal="box", barmode='group',title="relation b/w travel type and satisfaction")
        st.plotly_chart(fig,use_container_width=True)

    with col1:
        fig = px.histogram(df, x='Class', color='satisfaction',marginal="box", barmode='group',title="relation b/w Class and satisfaction")
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        scatter_fig = go.Figure()
        scatter_fig.add_trace(go.Scatter(x=df['Departure Delay in Minutes'], 
                                 y=df['Arrival Delay in Minutes'],
                                 mode='markers',
                                 marker=dict(color='blue'),  # Adjust marker color if needed
                                 name='Scatter Plot'))

# Line plot
        line_fig = go.Figure()

        line_fig.add_trace(go.Scatter(x=df['Departure Delay in Minutes'], 
                              y=df['Arrival Delay in Minutes'],
                              mode='lines',
                              line=dict(color='green'),  # Adjust line color if needed
                              name='Line Plot'))
        scatter_fig.update_layout(title='Scatter Plot of Arrival Delay vs. Departure Delay',
                          xaxis_title='Departure Delay in Minutes',yaxis_title='Arrival Delay in Minutes')
        line_fig.update_layout(title='Line Plot of Arrival Delay vs. Departure Delay',
                       xaxis_title='Departure Delay in Minutes',
                       yaxis_title='Arrival Delay in Minutes')

        st.plotly_chart(scatter_fig,use_container_width=True)

    with col1:
        def kde_sklearn(x, x_grid, bandwidth=0.2, **kwargs):
    
            from sklearn.neighbors import KernelDensity
            kde_skl = KernelDensity(bandwidth=bandwidth, **kwargs)
            kde_skl.fit(x[:, np.newaxis])
            log_pdf = kde_skl.score_samples(x_grid[:, np.newaxis])
            return np.exp(log_pdf)

# Generating data for KDE
        flight_distance = df['Flight Distance']
        x_grid = np.linspace(flight_distance.min(), flight_distance.max(), 1000)
        kde_values = kde_sklearn(flight_distance.values, x_grid)

# Plot histogram with KDE curve
        fig = go.Figure()

# Histogram
        fig.add_trace(go.Histogram(x=flight_distance,
                            histnorm='probability density',  # Normalize to get density histogram
                            opacity=0.75,  # Adjust opacity if needed
                            name='Histogram'))

# KDE curve
        fig.add_trace(go.Scatter(x=x_grid, y=kde_values, mode='lines', name='KDE'))

# Update layout
        fig.update_layout(title='Histogram with KDE for Flight Distance',
                  xaxis_title='Flight Distance',
                  yaxis_title='Density')
        
        st.plotly_chart(fig,use_container_width=True)

    # with col2:
    #     plt.title("distribution of flight distances")
    #     sns.histplot(x='Flight Distance',data = df ,hue='Inflight service',kde=True)
    #     st.pyplot(plt)

        
    with col2:

        fig = px.bar(df, x='Seat comfort', y='Flight Distance', color='satisfaction', 
                barmode='group',  # Grouped bars
                title='Bar Plot of Flight Distance by Seat Comfort and Satisfaction',
                labels={'Seat comfort': 'Seat Comfort', 'Flight Distance': 'Flight Distance'},
                )

# Update layout
        fig.update_layout(xaxis_title='Seat Comfort',
                    yaxis_title='Flight Distance')
        st.plotly_chart(fig,use_container_width=True)

    with col1:
        fig = px.histogram(df, x='Age', color='satisfaction',marginal="box", barmode='group',title="relation b/w Age and satisfaction")
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        fig = px.histogram(df, x='Age', color='Class',marginal="box", barmode='group',title="relation b/w Age and Class")
        st.plotly_chart(fig,use_container_width=True)

    with col1:
        fig = px.histogram(df, x='Age', color='Type of Travel',marginal="box", barmode='group',title="relation b/w Age and type of travel")
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        fig = px.histogram(df, x='Flight Distance', color='satisfaction',marginal="box", barmode='group',title="relation b/w Flight Distance and satisfaction")
        st.plotly_chart(fig,use_container_width=True)

    with col1:
        on_board_services = ['Food and drink', 'Seat comfort', 'Inflight entertainment', 
                        'On-board service', 'Cleanliness', 'Leg room service', 'Inflight service']
        average_ratings = df[on_board_services].mean()

    # Create a DataFrame from average ratings
        average_ratings_df = pd.DataFrame({'Service': average_ratings.index, 
                                    'Average Satisfaction Rating': average_ratings.values})

        # Create bar plot using Plotly Express
        fig = px.bar(average_ratings_df, x='Service', y='Average Satisfaction Rating', 
                title='Average Satisfaction Ratings for On-board Services',
                labels={'Service': 'Service', 'Average Satisfaction Rating': 'Average Rating'})

    # Rotate x-axis labels for better readability
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        off_board_services = ['Departure/Arrival time convenient', 'Ease of Online booking', 
                        'Gate location', 'Baggage handling', 'Checkin service', 
                        'Departure Delay in Minutes', 'Arrival Delay in Minutes']

    # Calculate average ratings for off-board services
        average_ratings2 = df[off_board_services].mean()

    # Create a DataFrame from average ratings
        average_ratings_df2 = pd.DataFrame({'Service': average_ratings2.index, 
                                        'Average Satisfaction Rating': average_ratings2.values})

    # Create bar plot using Plotly Express
        fig = px.bar(average_ratings_df2, x='Service', y='Average Satisfaction Rating', 
                title='Average Satisfaction Ratings for Off-board Services',
                labels={'Service': 'Service', 'Average Satisfaction Rating': 'Average Rating'})

    # Rotate x-axis labels for better readability
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig,use_container_width=True)

    with col1:
        fig = px.histogram(df, x='Customer Type', color='Online boarding',
                    title='Count of Customer Types by Online Boarding',
                    labels={'Customer Type': 'Customer Type', 'Online boarding': 'Online Boarding'},
                    barmode='group')

    # Update layout
        fig.update_layout(xaxis_title='Customer Type', yaxis_title='Count')
        st.plotly_chart(fig,use_container_width=True)
    with col2:
        fig = px.violin(df, y='Departure Delay in Minutes', title='Departure Delay in Minutes')
        st.plotly_chart(fig,use_container_width=True)

    with col1:
        fig = px.violin(df, y='Arrival Delay in Minutes', title='Arrival Delay in Minutes')
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        correlation_matrix = df.corr(numeric_only=True)

    # Create heatmap using Plotly
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.index,
            colorscale='Viridis',  # Choose the colorscale you prefer
            colorbar=dict(title='Correlation'),
        ))

    # Update layout
        fig.update_layout(title='Heatmap of Correlation Matrix',
                        xaxis_title='Features',
                        yaxis_title='Features')
        st.plotly_chart(fig,use_container_width=True)

    with col1:
        fig = px.density_contour(df, x='Baggage handling', facet_col='Gender', color='Gender',
                            marginal_x='histogram', 
                            title='KDE Plot of Baggage Handling by Gender',
                            labels={'Baggage handling': 'Baggage Handling', 'Gender': 'Gender'},
                            color_discrete_sequence=px.colors.qualitative.Set2)

    # Update layout
        #fig.update_layout(xaxis_title='Baggage Handling')
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        fig = px.histogram(df, x='Cleanliness', color='satisfaction', barmode='overlay',
                    marginal='rug', opacity=0.7, 
                    title='Plot of Cleanliness by Satisfaction',
                    labels={'Cleanliness': 'Cleanliness', 'satisfaction': 'Satisfaction'},
                    color_discrete_sequence=px.colors.qualitative.Set1)

    # Update layout
        fig.update_layout(xaxis_title='Cleanliness', yaxis_title='Density')
        st.plotly_chart(fig,use_container_width=True)

    with col1:
        fig = px.box(df, x='Class', y='Age', color='Gender', 
                title='Age by Class and Gender',
                labels={'Class': 'Class', 'Age': 'Age', 'Gender': 'Gender'})

    # Update layout
        fig.update_layout(xaxis_title='Class', yaxis_title='Age')
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        fig = px.histogram(df, x='Inflight wifi service', color='satisfaction', 
                    barmode='group', 
                    title='Distribution of Inflight Wifi Service by Satisfaction Level',
                    labels={'Inflight wifi service': 'Inflight Wifi Service', 'satisfaction': 'Satisfaction Level'},
                    color_discrete_sequence=px.colors.qualitative.Set1)

    # Update layout
        fig.update_layout(xaxis_title='Inflight Wifi Service', yaxis_title='Frequency')
        st.plotly_chart(fig,use_container_width=True)

if selected=="Insights🔍":
    st.write("1. Analysis shows that the most common ages are the ranges of 20s and 40s so knowing thier purpose for travel can tell us more about thier opinions")
    st.write("2. Buisness purpose exceeds personal purpose and they are more commom with the buisness class so they are most likely to care more about smaller details")
    st.write("3. Personal traveller are the ones more likeley to show their unsatisfaction")
    st.write("4. Customers are more satisfied with long flights than shorter ones")
    st.write("5.  Men are more satistfied with baggage handling than women")
    st.write("6. Flights are on time most of times except in multiple occasions where one of them exceeded 1600 mins of wait")
    st.write("7. Loyal customers seems to be satidfied with the online services which may be one of reasons they prefer this airline")
    st.write("8. taking a quik look at the correlation between given features showed that the highest correlation was betwween delay in arrival and depature which is pretty convenient as they affect each other")
    st.write("9. clienliness also highly affect food and drink,seat comfort and inflight entertainmnet")
    st.write("10 .Wifi service and ease of online booking are correlated which shows how clients use internet in most of their tasks")
    st.header("Analysis Findings Summary:")
    st.write("  -> This airline seems to have alot of unsatisfied customers")
    st.write("  -> The average ages that we found (20s,40s) can help set the target audience in order to provide the needed advertisment to attract them and different ones for older and younger ages")
    st.write("  -> Since buisness travels are more common, qualities as cleanliness and food and drink are taken more in considers as customers lead to want luxerious treatment")
    st.write("  -> Economy class is more common with the personal travellers")
    st.write(" -> People satisfied with cleanliness tend to be satisfied with the airline")
    st.write("  -> Longer flights also seem to have better reputation at this airline")
    st.write("  -> Clients are more satisfied of on-board services that is more related to the airplane itself than the off-board ones")
    st.write("  -> Services as Ease of Online booking , Gate location , Baggage handling and Checkin service need to be improved as they doesn't seem to have good ratings ")
    st.write("  -> Delays aren't common but the couple situations that had occured seem to be long and can reach 26 hours")
    st.write("  -> Loyal customers seem to be used to online boarding")
    st.write("  -> Females are more dissatisfied than males")
    st.write("  -> The customers who travelled on Eco class are more Dissatified")
    st.write("  -> Most of the customers who are not satisfied are belongs to the age groups (1-40) and (60-80)")

if selected=="👀 Actions":

    # Targeted Advertising
    st.header("Targeted Advertising")
    st.write("Utilize the knowledge of the most common age ranges (20s and 40s) to tailor advertising campaigns that resonate with these demographics. Understand their purposes for travel and craft messages that address their needs and preferences.")

    # Enhance Business Class Experience
    st.header("Enhance Business Class Experience")
    st.write("Since business travelers are more common and tend to focus on smaller details, invest in improving the quality of services in business class such as cleanliness, food and drink offerings, and overall comfort.")

    # Address Personal Traveler Concerns
    st.header("Address Personal Traveler Concerns")
    st.write("Recognize that personal travelers are more likely to express dissatisfaction. Identify pain points specific to this group and implement measures to address them, potentially focusing on economy class services and amenities.")

    # Improve On-board Services
    st.header("Improve On-board Services")
    st.write("Given that customers are more satisfied with on-board services compared to off-board ones, allocate resources to enhance the in-flight experience, such as improving Wi-Fi service, inflight entertainment, and seat comfort.")

    # Address Delay Concerns
    st.header("Address Delay Concerns")
    st.write("While delays are infrequent, addressing the instances of prolonged delays promptly is crucial. Implement measures to minimize delays and improve communication with customers during delay situations.")

    # Enhance Online Booking Experience
    st.header("Enhance Online Booking Experience")
    st.write("Since loyal customers seem to value online services, focus on improving features like ease of online booking to cater to their preferences and streamline the booking process for all customers.")

    # Gender-Specific Improvements
    st.header("Gender-Specific Improvements")
    st.write("Recognize that there is a gender disparity in satisfaction levels, particularly regarding baggage handling. Investigate the reasons behind this and implement measures to address any discrepancies in service quality.")

    # Target Dissatisfied Age Groups
    st.header("Target Dissatisfied Age Groups")
    st.write("Focus attention on age groups (1-40) and (60-80) who are more likely to express dissatisfaction. Conduct targeted surveys or feedback sessions to understand their specific concerns and preferences, then implement changes accordingly.")

    # Monitor and Improve Cleanliness
    st.header("Monitor and Improve Cleanliness")
    st.write("Since satisfaction with cleanliness correlates with overall satisfaction, prioritize cleanliness across all touchpoints of the customer journey, including aircraft, terminals, and lounges.")

    # Offer Incentives for Loyalty
    st.header("Offer Incentives for Loyalty")
    st.write("Implement loyalty programs or incentives to reward repeat customers and encourage continued patronage. This could include perks such as priority boarding, lounge access, or discounts on future bookings.")





