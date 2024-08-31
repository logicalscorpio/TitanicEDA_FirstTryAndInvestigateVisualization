import streamlit as st
import pandas as pd
import plotly.express as px

# !pipreqs . --force

df = pd.read_csv('train.csv')
df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 12, 18, 60, 80], labels=['Child', 'Teenager', 'Adult', 'Senior'])
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1

st.title("Titanic Interactive Survival Dashboard")
st.markdown("### Analyzing Titanic Data by Passenger Class and Gender")

st.sidebar.header("Filter Options")
selected_class = st.sidebar.selectbox("Select Passenger Class:", [1, 2, 3], index=0)
gender_filter = st.sidebar.radio("Filter by Gender:", ['All', 'male', 'female'])

if gender_filter != 'All':
    filtered_df = df[(df['Pclass'] == selected_class) & (df['Sex'] == gender_filter)]
else:
    filtered_df = df[df['Pclass'] == selected_class]

# Survival by gender
st.markdown(f"### Survival by Gender in Class {selected_class}")
survival_fig = px.histogram(filtered_df, x='Survived', color='Sex', barmode='group',
                            labels={'Survived': 'Survived', 'Sex': 'Gender'},
                            title=f'Survival by Gender in Class {selected_class}',
                            color_discrete_map={'female': 'pink', 'male': 'blue'})
st.plotly_chart(survival_fig)

# Age group distribution by gender
st.markdown(f"### Age Group Distribution by Gender in Class {selected_class}")
age_gender_fig = px.histogram(filtered_df, x='AgeGroup', color='Sex', barmode='group',
                              labels={'AgeGroup': 'Age Group', 'Sex': 'Gender'},
                              title=f'Age Group Distribution by Gender in Class {selected_class}',
                              color_discrete_map={'female': 'pink', 'male': 'blue'})
st.plotly_chart(age_gender_fig)

# Fare distribution using Violin Plot
st.markdown(f"### Fare Distribution in Class {selected_class}")
fare_violin = px.violin(filtered_df, y='Fare', color='Sex' if gender_filter == 'female' else None, box=True, points='all',
                        title=f'Fare Distribution in Class {selected_class}',
                        labels={'Fare': 'Fare'},
                        color_discrete_map={'female': 'pink'} if gender_filter == 'female' else None)
fare_violin.update_traces(meanline_visible=True)
st.plotly_chart(fare_violin)

# Family size survival rate
st.markdown(f"### Survival by Family Size in Class {selected_class}")
family_size_fig = px.histogram(filtered_df, x='FamilySize', color='Survived', barmode='group',
                               labels={'FamilySize': 'Family Size', 'Survived': 'Survived'},
                               title=f'Survival by Family Size in Class {selected_class}')
st.plotly_chart(family_size_fig)
