import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Global Country Statistics Explorer",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
DATA_PATH = os.path.join(os.path.dirname(__file__), "final_country_stats.csv")
df = pd.read_csv(DATA_PATH)

# ---------------- SAFE FLOAT FUNCTION ----------------
def safe_float(val):
    try:
        return float(val)
    except:
        return 0.0

# ---------------- TITLE ----------------
st.title("🌍 Global Country Statistics Explorer")
st.write("Explore, compare, and analyze key country statistics.")

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔎 Select Countries")

country_list = sorted(df["Country"].unique())

country1 = st.sidebar.selectbox("Country 1", country_list, index=0)
country2 = st.sidebar.selectbox("Country 2", country_list, index=1)

c1 = df[df["Country"] == country1].iloc[0]
c2 = df[df["Country"] == country2].iloc[0]

# ---------------- MAIN METRICS ----------------
st.markdown("---")
st.subheader("📊 Key Metrics Comparison")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### {country1}")
    st.metric("Population", f"{int(c1['Population']):,}")
    st.metric("GDP per Capita", f"${safe_float(c1['GDP ($ per capita)']):,.0f}")
    st.metric("Literacy Rate", f"{safe_float(c1['Literacy (%)']):.1f}%")

with col2:
    st.markdown(f"### {country2}")
    st.metric("Population", f"{int(c2['Population']):,}")
    st.metric("GDP per Capita", f"${safe_float(c2['GDP ($ per capita)']):,.0f}")
    st.metric("Literacy Rate", f"{safe_float(c2['Literacy (%)']):.1f}%")

# ---------------- DEMOGRAPHICS ----------------
st.markdown("---")
st.subheader("📈 Demographics")

d1, d2 = st.columns(2)

with d1:
    st.markdown(f"#### {country1}")
    st.metric("Population Density", f"{safe_float(c1['Pop. Density (per sq. mi.)']):.2f}")
    st.metric("Birth Rate", f"{safe_float(c1['Birthrate']):.2f}")
    st.metric("Death Rate", f"{safe_float(c1['Deathrate']):.2f}")
    st.metric("Infant Mortality", f"{safe_float(c1['Infant mortality (per 1000 births)']):.2f}")

with d2:
    st.markdown(f"#### {country2}")
    st.metric("Population Density", f"{safe_float(c2['Pop. Density (per sq. mi.)']):.2f}")
    st.metric("Birth Rate", f"{safe_float(c2['Birthrate']):.2f}")
    st.metric("Death Rate", f"{safe_float(c2['Deathrate']):.2f}")
    st.metric("Infant Mortality", f"{safe_float(c2['Infant mortality (per 1000 births)']):.2f}")

# ---------------- GDP INSIGHT ----------------
st.markdown("---")
avg_gdp = df["GDP ($ per capita)"].apply(safe_float).mean()

if safe_float(c1["GDP ($ per capita)"]) > avg_gdp:
    st.success(f"{country1} has GDP per capita above global average.")
else:
    st.warning(f"{country1} has GDP per capita below global average.")

# ---------------- TOP 10 GDP CHART ----------------
st.markdown("---")
st.subheader("💰 Top 10 Countries by GDP per Capita")

top10 = (
    df.assign(gdp=df["GDP ($ per capita)"].apply(safe_float))
    .sort_values("gdp", ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(top10["Country"], top10["gdp"])
ax.set_xlabel("GDP per Capita")
ax.set_title("Top 10 Countries by GDP per Capita")
ax.invert_yaxis()

st.pyplot(fig)
