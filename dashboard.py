import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

df = pd.read_csv("ShelterDogs.csv")
df['date_found'] = pd.to_datetime(df['date_found'])
df['year_found'] = df['date_found'].dt.year

st.title('Dogs for Adoption Dashboard')

page = st.sidebar.selectbox('Choose a page', ['Basic Info', 'Advanced Characteristics'])

if page == 'Basic Info':
    st.header('Basic Info')

    size_distribution = df['size'].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(x=size_distribution.index, y=size_distribution.values, ax=ax, palette='viridis')
    ax.set_title('Size Distribution')
    ax.set_xlabel('Size')
    ax.set_ylabel('Count')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

    age_distribution = df['age'].dropna()
    fig, ax = plt.subplots()
    sns.histplot(age_distribution, bins=20, kde=False, ax=ax, color='blue')
    ax.set_title('Age Distribution')
    ax.set_xlabel('Age')
    ax.set_ylabel('Count')
    st.pyplot(fig)

    sex_distribution = df['sex'].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(x=sex_distribution.index, y=sex_distribution.values, ax=ax, palette='rocket')
    ax.set_title('Sex Distribution')
    ax.set_xlabel('Sex')
    ax.set_ylabel('Count')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

elif page == 'Advanced Characteristics':
    st.header('Advanced Characteristics')

    heatmap_data = df.pivot_table(index='size', columns='coat', values='age', aggfunc='mean')
    fig, ax = plt.subplots()
    sns.heatmap(heatmap_data, cmap='coolwarm', annot=True, ax=ax)
    ax.set_title('Correlation of Coat Type and Size')
    st.pyplot(fig)

    sunburst_data = df.groupby(['sex', 'coat']).size().reset_index(name='count')
    fig = px.sunburst(sunburst_data, path=['sex', 'coat'], values='count', title='Pet Coat Type by Sex')
    st.plotly_chart(fig)

    fig = px.bar(df, x='breed', color='get_along_cats', title='Distribution of Get Along with Cats')
    st.plotly_chart(fig)

    fig = px.scatter(
        df, x='color', y='neutered', color='sex', size='age', animation_frame='year_found',
        title='Neutered Status by Color with Age and Sex'
    )
    st.plotly_chart(fig)

    fig = px.pie(df, names='housebroken', title='Housebroken Status Distribution')
    st.plotly_chart(fig)

    fig = px.scatter(df, x='age', y='neutered', color='sex', title='Age vs Neutered Status')
    st.plotly_chart(fig)