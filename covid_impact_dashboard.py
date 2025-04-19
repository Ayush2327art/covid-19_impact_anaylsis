
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Covid-19 Economic Impact Dashboard", layout="wide")
st.title("📊 Covid-19 Impacts on Global Economy (2020–2022)")

@st.cache_data
def load_data():
    covid_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    covid = pd.read_csv(covid_url)
    economic = pd.read_csv("economic_data_sample.csv")
    return covid, economic

covid_df, eco_df = load_data()

covid_df = covid_df.drop(columns=['Province/State', 'Lat', 'Long'])
covid_df = covid_df.melt(id_vars=['Country/Region'], var_name='Date', value_name='Confirmed')
covid_df['Date'] = pd.to_datetime(covid_df['Date'])
covid_df['Year'] = covid_df['Date'].dt.year
covid_df = covid_df[covid_df['Year'].isin([2020, 2021, 2022])]

eco_df['Year'] = eco_df['Year'].astype(int)
merged_df = pd.merge(covid_df, eco_df, left_on=['Country/Region', 'Year'], right_on=['Country', 'Year'], how='inner')

st.sidebar.header("📅 Select Year")
selected_year = st.sidebar.radio("Year", [2020, 2021, 2022])
filtered_df = merged_df[merged_df['Year'] == selected_year]

st.subheader(f"📈 Covid-19 Confirmed Cases Trend - {selected_year}")
top_countries = filtered_df.groupby('Country/Region')['Confirmed'].max().nlargest(5).index
line_data = filtered_df[filtered_df['Country/Region'].isin(top_countries)]
fig_line = px.line(line_data, x="Date", y="Confirmed", color="Country/Region", title="Top 5 Countries - Covid-19 Spread")
st.plotly_chart(fig_line, use_container_width=True)

st.subheader(f"💹 GDP Comparison by Country - {selected_year}")
bar_data = filtered_df.groupby('Country/Region')['GDP'].mean().nlargest(10).reset_index()
fig_bar = px.bar(bar_data, x="Country/Region", y="GDP", color="Country/Region", title="Top 10 Countries by GDP")
st.plotly_chart(fig_bar, use_container_width=True)

st.subheader(f"🧑‍💼 Unemployment Rate Distribution - {selected_year}")
pie_data = filtered_df.groupby('Country/Region')['Unemployment'].mean().nlargest(6).reset_index()
fig_pie = px.pie(pie_data, values='Unemployment', names='Country/Region', title='Top 6 Unemployment Rates')
st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("📊 Correlation: Covid-19 vs Economic Indicators")
corr_df = filtered_df[['Confirmed', 'GDP', 'Unemployment']].corr()
fig_corr, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(corr_df, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
st.pyplot(fig_corr)

st.markdown("---")
st.caption("Data Source: Johns Hopkins University & Sample Economic Data | Developed with Streamlit")
