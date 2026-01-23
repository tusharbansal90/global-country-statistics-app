import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Global Country Statistics Explorer", layout="wide")

DATA_PATH = os.path.join(os.path.dirname(__file__), "final_country_stats.csv")
df = pd.read_csv(DATA_PATH)

def safe_float(value):
    try:
        return float(str(value).replace(",", "."))
    except:
        return 0.0

st.title("🌍 Global Country Statistics Explorer")
st.write("Explore, compare, and analyze key country statistics.")

country = st.sidebar.selectbox(
    "Select a Country",
    sorted(df["Country"].unique())
)

selected = df[df["Country"] == country].iloc[0]

col1, col2, col3 = st.columns(3)
c1.metric(
    "Population",
    f"{int(selected['Population']):,}"
)

c2.metric(
    "GDP per Capita",
    f"${safe_float(selected['GDP ($ per capita)']):,.0f}"
)

c3.metric(
    "Literacy Rate",
    f"{safe_float(selected['Literacy (%)']):.1f}%"
)

st.markdown("---")
st.subheader("📊 Demographics")

d1, d2, d3, d4 = st.columns(4)

d1.metric(
    "Population Density",
    f"{safe_float(selected['Pop. Density (per sq. mi.)']):.2f}"
)

d2.metric(
    "Birth Rate",
    f"{safe_float(selected['Birthrate']):.2f}"
)

d3.metric(
    "Death Rate",
    f"{safe_float(selected['Deathrate']):.2f}"
)


d4.metric(
    "Infant Mortality",
    f"{safe_float(selected['Infant mortality (per 1000 births)']):.2f}"
)


st.markdown("---")

avg_gdp = df["GDP ($ per capita)"].apply(safe_float).mean()

if safe_float(selected["GDP ($ per capita)"]) > avg_gdp:
    st.success("GDP per capita is above global average.")
else:
    st.warning("GDP per capita is below global average.")

# ---------------- TOP 10 GDP CHART ----------------
st.subheader("💰 Top 10 Countries by GDP per Capita")

top10 = (
    df.assign(gdp=df["GDP ($ per capita)"].apply(safe_float))
      .sort_values("gdp", ascending=False)
      .head(10)
)

plt.figure(figsize=(8, 4))
plt.barh(top10["Country"], top10["gdp"])
plt.xlabel("GDP per Capita (USD)")
plt.title("Top 10 Countries by GDP per Capita")
plt.gca().invert_yaxis()

st.pyplot(plt)
