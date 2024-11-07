import streamlit as st
import google.generativeai as genai
import requests

# Pre-set API keys and Custom Search Engine ID
genai_api_key = "AIzaSyBzP_urPbe1zBnZwgjhSlVl-MWtUQMEqQA"
google_search_api_key = "AIzaSyAf_74VcMcZu0tZ0B1VJ-T67qTb_vA28ZE"
google_cse_id = "10a125a1f8ed84071"

# Streamlit App Title and Description
st.title("Essay Generator with Google Generative AI")
st.write("Enter a topic, and this app will generate a detailed essay for you.")

# Input for the topic
platform = st.text_input("Enter the social media post to write for")
topic = st.text_input("Enter the topic to write for")

# Function to fetch statistics related to the topic using Google Custom Search
def fetch_statistics(topic, cse_id, api_key):
    url = f"https://www.googleapis.com/customsearch/v1?q={topic}+statistics&cx={cse_id}&key={api_key}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            statistics = []
            for item in data.get("items", []):
                snippet = item.get("snippet")
                if snippet:
                    statistics.append(snippet)
            return statistics
        else:
            st.error("Failed to fetch statistics. Please check your API key or CSE ID.")
            return None
    except Exception as e:
        st.error(f"An error occurred while fetching statistics: {str(e)}")
        return None

# Button to trigger fetching statistics and generating the essay
if st.button("Generate Essay"):
    if not topic:
        st.error("Please enter a topic for the essay.")
    else:
        # Fetch statistics related to the topic
        statistics = fetch_statistics(topic, google_cse_id, google_search_api_key)
        statistics_text = ""
        
        if statistics:
            # Combine statistics into a single string for prompt
            statistics_text = "Here are some statistics related to your topic:\n" + "\n".join(statistics)

        # Configure the Google Generative AI API
        genai.configure(api_key=genai_api_key)

        try:
            # Create the GenerativeModel instance
            model = genai.GenerativeModel("gemini-1.5-flash")

            # Generate content based on the user-defined topic, with statistics if available
            prompt = (
                f"Write a post for {platform} on {topic}"
                f"Use simple, confident language that shows solid understanding. "
                f"Make the essay as comprehensive and detailed as possible."
                f"here are some statistics I believe you'll need:".join(statistics)
            )
            response = model.generate_content(prompt)

            # Display the generated essay in Streamlit
            if response.text:
                st.subheader("Generated Essay:")
                st.write(response.text)
            else:
                st.error("No content generated. Please try again.")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
