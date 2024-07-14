import streamlit as st
from streamlit_ui import create_ui
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        create_ui()
    except Exception as e:
        logger.error(f"An error occurred while running the application: {str(e)}")
        st.error("An unexpected error occurred. Please try again later.")