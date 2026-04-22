import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date
sns.set_theme(
    style="darkgrid",   # clean background with grid
    palette="muted",      # nice default colors
    font_scale=1.1       # slightly bigger text
)

# =====================
# PAGE CONFIGURATION
# =====================
st.set_page_config(
    page_title="Nigerian Incidence Dashboard",
    layout="wide"
)

# =====================
# LOAD DATA
# =====================
df = pd.read_csv("zhul.csv")

df["Start date"] = pd.to_datetime(df["Start date"])
df["End date"] = pd.to_datetime(df["End date"])
df["Duration"] = (df["End date"] - df["Start date"]).dt.days

# =====================
# SIDEBAR
# =====================
st.sidebar.title("User Profile")
st.sidebar.write("Abdulakeem Suliyat Opeyemi")
st.sidebar.write("Data Analyst")

st.sidebar.header("Filters")

selected_states = st.sidebar.multiselect(
    "Select State(s)",
    sorted(df["State"].dropna().unique())
)

start_date = st.sidebar.date_input(
    "Start Date",
    value=df["Start date"].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    value=df["Start date"].max().date()
)

# =====================
# APPLY FILTERS
# =====================
filtered_df = df.copy()

if selected_states:
    filtered_df = filtered_df[filtered_df["State"].isin(selected_states)]

filtered_df = filtered_df[
    (filtered_df["Start date"] >= pd.to_datetime(start_date)) &
    (filtered_df["Start date"] <= pd.to_datetime(end_date))
]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# =====================
# TITLE
# =====================
st.title("Nigerian Incidence Dashboard")
st.markdown("### Professional Notebook-Style Analytics Dashboard")

# =====================
# KPIs
# =====================
total_incidents = filtered_df["Incident"].count()
total_deaths = filtered_df["Number of deaths"].sum()
avg_deaths = filtered_df["Number of deaths"].mean()
max_deaths = filtered_df["Number of deaths"].max()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Incidents", total_incidents)
col2.metric("Total Deaths", total_deaths)
col3.metric("Avg Deaths", round(avg_deaths, 2))
col4.metric("Highest Death Toll", max_deaths)

# =====================
# CHART 1
# =====================
st.header("1. Incidents Causing Most Deaths")
data = filtered_df.groupby("Incident")["Number of deaths"].sum().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(8,5))
data.plot(kind="barh", ax=ax)
color=sns.color_palette("Reds_r")
sns.despine()
st.pyplot(fig) 
st.markdown(" Insights :" 
" Shift in risk profile: The chart suggests everyday risks (like road accidents) may currently outweigh high-profile insurgency incidents in terms of frequency.")
# CHART 2
# =====================
st.header("2. Cumulative Deaths Over Time")
df_sorted = filtered_df.sort_values("Start date")
df_sorted["cumulative_deaths"] = df_sorted["Number of deaths"].cumsum()

fig, ax = plt.subplots(figsize=(8,5))
ax.plot(df_sorted["Start date"], df_sorted["cumulative_deaths"],linewidth=2)
sns.despine()
st.pyplot(fig)
st.markdown(" Insights :" 
" No dips or volatility are visible, which points to consistent expansion rather than short-term fluctuations.")
# =====================
# CHART 3
# =====================
st.header("3. Median Deaths per Incident by State")
data = filtered_df.groupby("State")["Number of deaths"].median()

fig, ax = plt.subplots()
data.plot(kind="bar", ax=ax)
st.pyplot(fig)
st.markdown(" Insights :" 
" The data reveals that Cross River is the most critical focus area, with Zamfara and Rivers also requiring attention.")
# =====================
# CHART 4
# =====================
st.header("4. States with Highest Total Deaths")
data = filtered_df.groupby("State")["Number of deaths"].sum().sort_values(ascending=False)

fig, ax = plt.subplots()
data.plot(kind="bar", ax=ax)
st.pyplot(fig)
st.markdown(" Insights :" 
" The chart highlights regional concentration — Borno is the clear epicenter, overshadowing all other states.")
# =====================
# CHART 5
# =====================
st.header("5. Incidents with Fewer than 5 Deaths")
few = (filtered_df["Number of deaths"] < 5).sum()
many = (filtered_df["Number of deaths"] >= 5).sum()

fig, ax = plt.subplots()
ax.pie([few, many], labels=["<5 Deaths", "≥5 Deaths"], autopct="%1.1f%%")
st.pyplot(fig)
st.markdown(" Insights :" 
" The majority of cases (79.1%) involve fewer than five deaths, showing that most incidents are relatively low-fatality.")

# =====================
# CHART 6
# =====================
st.header("6. Monthly Deaths Trend")
data = filtered_df.groupby(
    filtered_df["Start date"].dt.to_period("M")
)["Number of deaths"].sum()

fig, ax = plt.subplots()
data.plot(kind="line", ax=ax)
st.pyplot(fig)
st.markdown(" Insights :" 
" The chart reflects a highly variable trend, not a smooth progression.")

# =====================
# CHART 7
# =====================
st.header("7. Variance in Deaths by State")
data = filtered_df.groupby("State")["Number of deaths"].var()

fig, ax = plt.subplots()
data.plot(kind="bar", ax=ax)
st.pyplot(fig)
st.markdown(" Insights :" 
" The chart reflects a concentration of activity or impact in Bayelsa, making it the primary hotspot.")

# =====================
# CHART 8
# =====================
st.header("8. Distribution of Deaths")
fig, ax = plt.subplots()
filtered_df["Number of deaths"].plot(kind="hist", bins=20, ax=ax)
st.pyplot(fig)
st.markdown(" Insights :" 
" The dataset is dominated by small values, meaning most occurrences fall in the lower range.")
# =====================
# CHART 9
# =====================
st.header("9. Incidents Ended per Year")
data = filtered_df.groupby(filtered_df["End date"].dt.year).size()

fig, ax = plt.subplots()
data.plot(kind="line", ax=ax)
st.pyplot(fig)
st.markdown(" Insights :" 
" The initial rise suggests positive momentum or expansion in the early period.")

# =====================
# CHART 10
# =====================
st.header("10. Top States by Incident Count")
data = filtered_df.groupby("State").size().sort_values(ascending=False).head(10)

fig, ax = plt.subplots()
data.plot(kind="bar", ax=ax)
st.pyplot(fig)
st.markdown(" Insights :" 
"The chart suggests that Lagos is the primary hotspot, far ahead of other states in the dataset.")
