import openai
import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Streamlit UI components for API key input:
api_key = st.text_input("Enter your OpenAI API Key:", type="password")
client = openai.OpenAI(api_key=api_key)

if api_key:
  openai.api_key = api_key
  # Set up Streamlit layout
  st.title('Merch AI Designer: Revolutionizing Merchandise Creation')

  # User Inputs in the sidebar
  description_input = st.sidebar.text_area("Describe your merchandise idea", "Type here...")
  merch_type = st.sidebar.selectbox("Select merchandise type", ["T-Shirt", "Mug", "Poster", "Tote Bag"])
  submit_button = st.sidebar.button('Generate Design')

  # Processing User Inputs
  if submit_button:
      # Define API URL and headers
      headers = {
          'Authorization': f'Bearer {api_key}',
          'Content-Type': 'application/json'
      }
      data = {
          "model": "dall-e-3",
          "prompt": f"{description_input} as a {merch_type}",
          "size": "1024x1024",
          "quality": "standard",
          "n": 1
      }

      # Send a post request to the OpenAI API      
      response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=data)
      response_data = response.json()      

      # Get the image URL from the response
      image_url = response_data['data'][0]['url']

      # Download the image and display it in Streamlit
      image_response = requests.get(image_url)
      image = Image.open(BytesIO(image_response.content))
      st.image(image, caption=f'Your Custom {merch_type}', use_column_width=True)
  else:    
    st.warning("Please enter your API key to proceed.")