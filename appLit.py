import streamlit as st
import pandas as pd
import plotly.express as px

# Load and preprocess data
df = pd.read_csv('train.csv')
df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 12, 18, 60, 80], labels=['Child', 'Teenager', 'Adult', 'Senior'])
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1

# Streamlit App
st.title("Titanic Interactive Survival Dashboard")
st.markdown("### Analyzing Titanic Data")

# Sidebar controls
st.sidebar.header("Filter Options")
selected_class = st.sidebar.selectbox("Select Passenger Class:", [1, 2, 3], index=0)
gender_filter = st.sidebar.radio("Filter by Gender:", ['All', 'male', 'female'])

# Filter data based on selections
if gender_filter != 'All':
    filtered_df = df[(df['Pclass'] == selected_class) & (df['Sex'] == gender_filter)]
else:
    filtered_df = df[df['Pclass'] == selected_class]

if gender_filter == 'All':
    # Gender distribution pie chart
    # st.markdown(f"### Gender Distribution in Class {selected_class}")
    gender_pie_fig = px.pie(filtered_df, names='Sex', 
                            title=f'Gender Distribution in Class {selected_class}',
                            color_discrete_sequence=px.colors.qualitative.Plotly, 
                            hole=0.3)  
    st.plotly_chart(gender_pie_fig)

# Combined Age group distribution
st.markdown(f"### Age Group Distribution in Class {selected_class}")
age_group_fig = px.histogram(filtered_df, x='AgeGroup', color='AgeGroup',
                             labels={'AgeGroup': 'Age Group'},
                             title=f'Age Group Distribution in Class {selected_class}',
                             color_discrete_sequence=px.colors.qualitative.Pastel)  
st.plotly_chart(age_group_fig)

# Fare distribution using Violin Plot
# st.markdown(f"### Fare Distribution in Class {selected_class}")
fare_violin = px.violin(filtered_df, y='Fare', color='Sex' if gender_filter == 'female' else None, box=True, points='all',
                        title=f'Fare Distribution in Class {selected_class}',
                        labels={'Fare': 'Fare'},
                        color_discrete_map={'female': 'pink'} if gender_filter == 'female' else None)
fare_violin.update_traces(meanline_visible=True)
st.plotly_chart(fare_violin)

# Family size survival rate
# st.markdown(f"### Survival by Family Size in Class {selected_class}")
family_size_fig = px.histogram(filtered_df, x='FamilySize', color='Survived', barmode='group',
                               labels={'FamilySize': 'Family Size', 'Survived': 'Survived'},
                               title=f'Survival by Family Size in Class {selected_class}',
                               category_orders={'Survived': [0, 1]},color_discrete_sequence=px.colors.qualitative.Pastel1)
                            #    color_discrete_map={'0': 'green', '1': 'blue'})  
st.plotly_chart(family_size_fig)
