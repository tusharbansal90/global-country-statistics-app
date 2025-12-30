import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Global Country Statistics Explorer", layout="wide")

DATA_PATH = os.path.join(os.path.dirname(__file__), "final_country_stats.csv")
df = pd.read_csv(DATA_PATH)



st.title("🌍 Global Country Statistics Explorer")
st.write("Explore, compare, and analyze key country statistics.")

country = st.sidebar.selectbox(
    "Select a Country",
    sorted(df["Country"].unique())
)

selected = df[df["Country"] == country].iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("Population", f"{int(selected['Population']):,}")
col2.metric("GDP per Capita", f"${selected['GDP ($ per capita)']:,.0f}")
col3.metric("Literacy Rate", f"{selected['Literacy (%)']}%")


avg_gdp = df["gdp_per_capita"].mean()
if selected["gdp_per_capita"] > avg_gdp:
    st.success("GDP per capita is above global average.")
else:
    st.warning("GDP per capita is below global average.")

top10 = df.sort_values("gdp_per_capita", ascending=False).head(10)

plt.figure(figsize=(8,4))
plt.barh(top10["country"], top10["gdp_per_capita"])
plt.xlabel("GDP per Capita")
plt.title("Top 10 Countries by GDP per Capita")
plt.gca().invert_yaxis()
st.pyplot(plt)
