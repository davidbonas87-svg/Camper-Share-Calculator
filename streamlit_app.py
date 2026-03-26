import streamlit as st

st.set_page_config(page_title="Camper Share Calculator", layout="centered")

st.title("Camper Share Financial Model")

st.subheader("Inputs")

campers = st.number_input("Number of campers", min_value=1, value=4, step=1)
members = st.number_input("Members per camper", min_value=1, value=30, step=1)
price = st.number_input("Avg revenue per member (€)", min_value=0, value=200, step=10)

leasing = st.number_input("Leasing per camper (€)", min_value=0, value=1100, step=50)
insurance = st.number_input("Insurance per camper (€)", min_value=0, value=250, step=10)
maintenance = st.number_input("Maintenance per camper (€)", min_value=0, value=200, step=10)
parking = st.number_input("Parking / infra per camper (€)", min_value=0, value=200, step=10)
software = st.number_input("Software per camper (€)", min_value=0, value=150, step=10)
variable = st.number_input("Variable cost per camper (€)", min_value=0, value=400, step=10)
platform = st.number_input("Platform fixed cost (€)", min_value=0, value=2000, step=50)

st.subheader("Results")

revenue_per_camper = members * price
total_revenue = campers * revenue_per_camper

fixed_cost_per_camper = leasing + insurance + maintenance + parking + software
total_cost = campers * (fixed_cost_per_camper + variable) + platform

monthly_profit = total_revenue - total_cost
annual_profit = monthly_profit * 12

break_even_members = (fixed_cost_per_camper + variable + (platform / campers)) / price if price > 0 else 0

st.metric("Revenue per camper", f"€{revenue_per_camper:,.0f}")
st.metric("Total revenue", f"€{total_revenue:,.0f}")
st.metric("Total monthly cost", f"€{total_cost:,.0f}")
st.metric("Monthly profit", f"€{monthly_profit:,.0f}")
st.metric("Annual profit", f"€{annual_profit:,.0f}")
st.metric("Break-even members per camper", f"{break_even_members:.1f}")

st.subheader("Summary")

st.write(f"Fixed cost per camper: €{fixed_cost_per_camper:,.0f}")
st.write(f"Total members: {campers * members}")
