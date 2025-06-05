import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk

# ----------------------------
# Page Setup
# ----------------------------
st.set_page_config(page_title="U.S. Border Crossing Dashboard", layout="wide")

# ----------------------------
# Load Data
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Border_Crossing_Entry_Data.csv")
    df["Date"] = pd.to_datetime(df["Date"], format="%b %Y")  # For "Jan 2024" format
    return df

df = load_data()

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("🔎 Filter Data")

# State selection
all_states = sorted(df["State"].dropna().unique())
select_all_states = st.sidebar.checkbox("Select All States", value=True)
selected_states = st.sidebar.multiselect("States:", all_states, default=all_states if select_all_states else [])

# Measure selection
all_measures = sorted(df["Measure"].dropna().unique())
select_all_measures = st.sidebar.checkbox("Select All Measures", value=True)
selected_measures = st.sidebar.multiselect("Measures:", all_measures, default=all_measures if select_all_measures else [])

# Date range
min_date = df["Date"].min()
max_date = df["Date"].max()
start_date, end_date = st.sidebar.date_input("Select Date Range:", [min_date, max_date], min_value=min_date, max_value=max_date)

# ----------------------------
# Filtered Data
# ----------------------------
filtered_df = df[
    (df["State"].isin(selected_states)) &
    (df["Measure"].isin(selected_measures)) &
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date))
]

# ----------------------------
# Metrics + Map + About
# ----------------------------
total_crossings = int(filtered_df["Value"].sum())
unique_ports = filtered_df["Port Name"].nunique()
states_covered = filtered_df["State"].nunique()
top_measure = df.groupby("Measure")["Value"].sum().idxmax()

st.title("🛂 U.S. Border Crossing Entry Dashboard")
metrics_col, map_col, about_col = st.columns([1.5, 3, 1.2])

with metrics_col:
    st.markdown("### 📊 Metrics")
    st.markdown(f"**Total Crossings:** `{total_crossings:,}`")
    st.markdown(f"**Unique Ports:** `{unique_ports}`")
    st.markdown(f"**States Covered:** `{states_covered}`")
    st.markdown(f"**Top Measure:** `{top_measure}`")

with about_col:
    st.subheader("ℹ️ About")
    st.markdown("""
    **Data Source**: [data.gov](https://data.gov)  
    This dashboard visualizes U.S. border crossing entries by state, measure, and time.
    """)

with map_col:
    st.subheader("🗺️ Map of Ports")

    map_df = (
        filtered_df.groupby(["Port Name", "Latitude", "Longitude"], as_index=False)["Value"]
        .sum()
    )

    # Dropdown to focus on a specific port
    top_ports = (
        filtered_df.groupby("Port Name")["Value"]
        .sum()
        .sort_values(ascending=False)
        .head(20)
        .reset_index()
    )
    top_port_names = top_ports["Port Name"].tolist()
    selected_port = st.selectbox("🔍 Highlight a Port on the Map:", ["All Ports"] + top_port_names)

    # Optional zoom into specific port
    if selected_port != "All Ports":
        map_df = map_df[map_df["Port Name"] == selected_port]

    if map_df.empty:
        st.warning("No ports match the selected filters.")
    else:
        avg_lat = map_df["Latitude"].mean()
        avg_lon = map_df["Longitude"].mean()
        zoom_level = 6 if len(map_df) <= 5 else 4

        map_layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position='[Longitude, Latitude]',
            get_radius="Value / 2000",
            get_fill_color='[255, 100, 100, 160]',
            pickable=True,
        )

        map_view = pdk.ViewState(
            latitude=avg_lat,
            longitude=avg_lon,
            zoom=zoom_level,
            pitch=0,
        )

        st.pydeck_chart(
            pdk.Deck(
                layers=[map_layer],
                initial_view_state=map_view,
                tooltip={"text": "{Port Name}\nCrossings: {Value}"}
            )
        )

# ----------------------------
# Bar + Line Chart Side by Side
# ----------------------------
st.markdown("### 📊 Port Activity Overview")
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("#### 🚏 Top Ports")
    bar_fig = px.bar(
        top_ports,
        x="Port Name",
        y="Value",
        labels={"Value": "Total Crossings"},
        height=400
    )
    bar_fig.update_traces(marker_color='lightskyblue', width=0.4)
    bar_fig.update_layout(xaxis_tickangle=45, margin=dict(l=10, r=10, t=30, b=60))
    st.plotly_chart(bar_fig, use_container_width=True)

with col2:
    st.markdown("#### 📈 Monthly Trend")
    monthly = filtered_df.groupby("Date")["Value"].sum().reset_index()
    line_fig = px.line(
        monthly,
        x="Date",
        y="Value",
        labels={"Value": "Total Crossings"},
        height=400
    )
    line_fig.update_layout(margin=dict(l=10, r=10, t=30, b=40))
    st.plotly_chart(line_fig, use_container_width=True)