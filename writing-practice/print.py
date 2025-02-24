import streamlit as st
import logging
import sys
from datetime import datetime

# Set up file logging
logging.basicConfig(
    filename='streamlit_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(message)s'
)

# Test multiple logging approaches
print("Test print", flush=True)
logging.debug("Test debug log")
logging.info("Test info log")

with open('debug_output.txt', 'a') as f:
    f.write(f"{datetime.now()} - Direct file write test\n")

st.write("Browser output working")


# streamlit run print.py
# python -m streamlit run print.py
# streamlit run print.py --server.headless true