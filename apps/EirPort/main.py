import streamlit as st
import requests

st.logo("images/IrishSetterIcon.png", size="large")

st.title("Welcome to the EirPort!")
st.text("Here you'll find the latest and greatest of our dog Eir's health metrics")
# %%
st.image("images/IrishSetter.png")

# # Station actions
# st.header("Station Actions")
# st.write("Here you can select the action you want to perform")

# # Sidebar
# st.sidebar.title("Select an action")
# identifier = st.sidebar.selectbox("Read a scale", ["water_bowl", "food_bowl"])

# # Read scale
# response = requests.get(
#     f"http://localhost:8001/read/{identifier}?unit=kg",
#     headers={"accept": "application/json"},
# )
