import streamlit as st
import google.generativeai as genai

# Configure Gemini API
def configure_gemini(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    return model

def is_agriculture_related(prompt):
    agriculture_keywords = [
        'farm', 'crop', 'plant', 'soil', 'harvest', 'fertilizer', 'irrigation',
        'pesticide', 'seed', 'agriculture', 'farming', 'livestock', 'organic',
        'garden', 'yield', 'weather', 'season', 'greenhouse', 'sustainable',
        'dairy', 'cultivation', 'pest', 'weed', 'nutrient', 'compost'
    ]
    return any(keyword in prompt.lower() for keyword in agriculture_keywords)

def get_chatbot_response(model, prompt):
    context = ("You are an agricultural expert chatbot. Provide concise responses (under 100 words) "
              "to agriculture-related queries in a polite and professional manner. "
              "Focus on practical, accurate information for farmers and gardeners.")
    
    if not is_agriculture_related(prompt):
        return "I apologize, but I can only assist with agriculture-related questions. Please feel free to ask me about farming, crops, soil, livestock, or any other agricultural topics."
    
    try:
        response = model.generate_content(context + "\n\nUser: " + prompt)
        return response.text[:300]  # Limiting response to ~100 words
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    st.set_page_config(page_title="Agricultural Assistant", page_icon="🌾")
    
    # Add custom CSS for styling
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(rgba(255,255,255,0.5), rgba(255,255,255,0.5)), 
                        url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80');
            background-size: cover;
            background-position: center;
        }
        .stTextInput > div > div > input {
            background-color: rgba(255, 255, 255, 0.9);
        }
        .stMarkdown {
            background-color: rgba(255, 255, 255, 0.7);
            padding: 10px;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🌾 Agricultural Assistant")
    
    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # API key input
    api_key = st.sidebar.text_input("Enter your Gemini API key", type="password")
    
    if api_key:
        try:
            model = configure_gemini(api_key)
            
            # Chat interface
            user_input = st.text_input("Ask me anything about agriculture:", key="user_input")
            
            if st.button("Send"):
                if user_input:
                    response = get_chatbot_response(model, user_input)
                    st.session_state.chat_history.append(("user", user_input))
                    st.session_state.chat_history.append(("bot", response))
            
            # Display chat history
            for role, message in st.session_state.chat_history:
                with st.container():
                    if role == "user":
                        st.markdown(f"**You:** {message}")
                    else:
                        st.markdown(f"**Agricultural Assistant:** {message}")
                    st.markdown("---")
        except Exception as e:
            st.error(f"Error initializing the model: {str(e)}")
    else:
        st.warning("Please enter your Gemini API key in the sidebar to start chatting.")

if __name__ == "__main__":
    main()