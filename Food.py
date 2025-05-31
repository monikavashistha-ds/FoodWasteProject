import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="Food Waste Management", layout="wide")

# Loading  Data
@st.cache_data
def load_data():
    providers = pd.read_csv("C:/Users/Monika Vashishth/Documents/providers_data.csv")
    receivers = pd.read_csv("C:/Users/Monika Vashishth/Documents/receivers_data.csv")
    claims = pd.read_csv("C:/Users/Monika Vashishth/Documents/claims_data.csv")
    listings = pd.read_csv("C:/Users/Monika Vashishth/Documents/food_listings_data.csv")

 
    # Merge provider name into listings
    listings = listings.merge(
        providers[['Provider_ID', 'Name']], 
        on='Provider_ID', 
        how='left'
    )
    listings.rename(columns={'Name': 'Provider_Name'}, inplace=True)

    return providers, receivers, claims, listings

# Load the data
providers, receivers, claims, listings = load_data()

# Sidebar Navigation
page = st.sidebar.radio("Navigate", ["Home", "Query Outputs", "Filters", "Provider Contacts"])

# ----------------------------------
if page == "Home":
    st.title("Welcome to Food Waste Management System")
    st.image("food_donation.jpg", use_column_width=True)
    st.markdown("""
    This platform reduces food waste by connecting food providers (like households and restaurants)
    with those in need. Use the navigation to explore queries, apply filters, or contact providers.
    """)

# ----------------------------------
elif page == "Query Outputs":
    st.title("📊 SQL Query Results")
    merged = claims.merge(listings, on="Food_ID").merge(receivers, on="Receiver_ID")

    queries = {
        "1. Number of Providers by Type": providers.groupby("Type").size().reset_index(name="Count"),
        "2. Total Claimed Food Quantity by City": merged.groupby("City")["Quantity"].sum().reset_index(),
        "3. Most Claimed Meal Types": listings.groupby("Meal_Type")["Quantity"].sum().reset_index().sort_values(by="Quantity", ascending=False),
        "4. Top 5 Receivers by Claims": claims.groupby("Receiver_ID").size().sort_values(ascending=False).head(5).reset_index(name="Total Claims"),
        "5. Food Quantity by Food Type": listings.groupby("Food_Type")["Quantity"].sum().reset_index(),
        "6. Providers with the Most Listings": listings.groupby("Provider_Name").size().sort_values(ascending=False).head(5).reset_index(name="Listings Count"),
        "7. Receivers by City": receivers.groupby("City").size().reset_index(name="Receiver Count"),
        "8. Claims per Meal Type": merged.groupby("Meal_Type").size().reset_index(name="Total Claims"),
        "9. Total Listings by Location": listings.groupby("Location").size().reset_index(name="Total Listings"),
        "10. Food Listings Quantity per Provider Type": listings.merge(providers[['Provider_ID', 'Type']], on="Provider_ID").groupby("Type")["Quantity"].sum().reset_index(),
        "11. Most Active Receiver (by Quantity)": merged.groupby("Receiver_ID")["Quantity"].sum().reset_index().sort_values(by="Quantity", ascending=False).head(1),
        "12. Total Claims by Food Type": merged.groupby("Food_Type").size().reset_index(name="Total Claims"),
        "13. Average Quantity Listed per Meal Type": listings.groupby("Meal_Type")["Quantity"].mean().reset_index(name="Average Quantity"),
        "14. Number of Unique Providers per City": providers.groupby("City")["Provider_ID"].nunique().reset_index(name="Unique Providers"),
        "15. Most Frequent Listing Location": listings["Location"].value_counts().reset_index().rename(columns={"index": "Location", "Location": "Count"}).head(1),
    }

    for i, (desc, df) in enumerate(queries.items(), start=1):
        st.markdown(f"""---\n### {desc}""")
        st.dataframe(df)

# ----------------------------------
elif page == "Filters":
    st.title("🔍 Filter Food Listings")

    city = st.selectbox("Select Location", options=["All"] + sorted(listings["Location"].dropna().unique()))
    provider_name = st.selectbox("Select Provider Name", options=["All"] + sorted(providers["Name"].dropna().unique()))
    food_type = st.selectbox("Select Food Type", options=["All"] + sorted(listings["Food_Type"].dropna().unique()))
    meal_type = st.selectbox("Select Meal Type", options=["All"] + sorted(listings["Meal_Type"].dropna().unique()))

    filtered = listings.copy()
    if city != "All":
        filtered = filtered[filtered["Location"] == city]
    if provider_name != "All":
        filtered = filtered[filtered["Provider_Name"] == provider_name]
    if food_type != "All":
        filtered = filtered[filtered["Food_Type"] == food_type]
    if meal_type != "All":
        filtered = filtered[filtered["Meal_Type"] == meal_type]

    st.dataframe(filtered)

# ----------------------------------
elif page == "Provider Contacts":
    st.title("📞 Provider Contact List")
    st.dataframe(providers[["Name", "Type", "City", "Contact"]])
