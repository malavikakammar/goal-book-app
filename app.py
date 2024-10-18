from dotenv import load_dotenv
load_dotenv()  # Take environment variables from .env.

import streamlit as st
import os
import google.generativeai as genai

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Streamlit app
st.set_page_config(page_title="Goal Writer & Q&A Application")

st.header("Goal Writer")

# Initialize session state if it doesn't exist
if 'step' not in st.session_state:
    st.session_state.step = 0  # Track the current step of the conversation
    st.session_state.salary_hike = None
    st.session_state.role_change = None
    st.session_state.other_reason = None
    st.session_state.change_timing = None
    st.session_state.final_statement = None  # To store the final statement

# Function to generate responses based on user input
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

# Step-based conversation
if st.session_state.step == 0:
    # Input section for goals
    goal_input = st.text_input("Input your goal: ", key="goal_input")
    goal_submit = st.button("Submit Goal")

    # If the submit button for the goal is clicked
    if goal_submit:
        goal_response = get_gemini_response(goal_input)
        st.subheader("AI Response:")
        #st.write(goal_response)

        # Check for job change
        if "I want to change my job" in goal_input:
            st.session_state.step = 1  # Move to next step
            st.subheader("Why do you want to change your job?");
            reasons = [
                "Seeking better salary",
                "Looking for more growth opportunities",
                "Wanting a better work-life balance",
                "Relocation for personal reasons",
                "Other"
            ]
            st.session_state.reason = st.selectbox("Select an option:", reasons)

elif st.session_state.step == 1:
    # Asking follow-up based on the reason selected
    if st.session_state.reason == "Seeking better salary":
        st.subheader("How much salary are you looking for?");
        st.session_state.salary_hike = st.text_input("Enter the expected salary hike (%):")
        if st.button("Submit Salary"):
            st.write(f"Got it! You're looking for a salary hike of: {st.session_state.salary_hike}%.")
            st.session_state.step = 3  # Move to next step

    elif st.session_state.reason == "Other":
        st.subheader("Please state your reason:")
        st.session_state.other_reason = st.text_input("Enter the reason:")
        if st.button("Submit Reason"):
            st.write(f"Thanks for sharing! Your reason for wanting to change is: {st.session_state.other_reason}.")
            st.session_state.step = 3  # Move to next step

    elif st.session_state.reason == "Looking for more growth opportunities":
        st.subheader("What role are you looking for?");
        st.session_state.role_change = st.text_input("Enter the desired role:")
        if st.button("Submit Role"):
            st.write(f"Great choice! You're looking for a role in: {st.session_state.role_change}.")
            st.session_state.step = 3  # Move to next step

    elif st.session_state.reason == "Relocation for personal reasons":
        st.subheader("Which location do you want to relocate to?");
        st.session_state.role_change = st.text_input("Enter the location:")
        if st.button("Submit Location"):
            st.write(f"Got it! You're considering relocating to: {st.session_state.role_change}.")
            st.session_state.step = 3  # Move to next step

elif st.session_state.step == 3:
    # Asking the final question
    st.subheader("When do you want to change?")
    change_timing = st.selectbox("Select a timeframe:", ["Immediately", "Within 3 months", "Within 6 months", "Unsure"])
    
    if st.button("Submit Timing"):
        st.session_state.change_timing = change_timing

        # Create a summary statement
        summary = "I want to change my job"
        if st.session_state.reason == "Seeking better salary":
            summary += f" because of a salary hike of {st.session_state.salary_hike}%."
        elif st.session_state.reason == "Looking for more growth opportunities":
            summary += f" to pursue a role in {st.session_state.role_change}."
        elif st.session_state.reason == "Other":
            summary += f" because: {st.session_state.other_reason}."
        elif st.session_state.reason == "Relocation for personal reasons":
            summary += f" to relocate to {st.session_state.role_change}."

        # Adjust wording for "Immediately"
        if st.session_state.change_timing == "Immediately":
            summary += " You want to change your job immediately."
        else:
            summary += f" You want to change your job by {st.session_state.change_timing}."

        st.session_state.final_statement = summary  # Store the final statement
        st.subheader("Your Summary:")
        st.write(st.session_state.final_statement)

# Optionally, include a reset button to clear session state
if st.button("Reset"):
    st.session_state.clear()
