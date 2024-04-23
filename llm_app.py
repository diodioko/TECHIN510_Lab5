import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Load API key from environment
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key not found. Please check your .env file.")
    st.stop()

# Configure the API
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

# Template for the AI to generate travel plans
prompt_template = """
You are an expert at planning oversea trips.

Please take the users request and plan a comprehensive trip for them.

Please include the following details:
- The destination
- The duration of the trip
- The activities that will be done
- The accommodation

The user's request is:
{prompt}
"""

def generate_content(user_prompt):
    full_prompt = prompt_template.format(prompt=user_prompt)
    response = model.generate_content(full_prompt)
    return response.text

# Streamlit user interface
st.title("✈️ Travel Planner")
st.write("Enter details about your next travel including destination, budget, and desired activities:")

# User inputs
location = st.text_input("Destination (e.g., Tokyo, Paris):")
budget = st.number_input("Budget in USD:", min_value=100, max_value=10000, value=1500)
days = st.slider("Number of days:", min_value=1, max_value=30, value=7)
activities = st.text_input("Activities (e.g., skiing, sightseeing):")

# Create a structured prompt for the model
user_prompt = f"Location: {location}, Budget: ${budget}, Days: {days}, Activities: {activities}"
if st.button("Plan My Trip!"):
    if location and activities:
        reply = generate_content(user_prompt)
        st.write("Here's your AI-generated travel plan:")
        st.write(reply)
    else:
        st.warning("Please fill in all the fields to generate a travel plan.")

