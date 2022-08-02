import streamlit as st
#from scripts.utils import read_flipside
from landing import landing_page

from beautify import flipside_logo, discord_logo, set_bg_hack_url
import os


st.set_page_config(page_title="Flipside Polygon Mega Dashboard", layout="wide")
set_bg_hack_url()
landing_page()

st.sidebar.markdown("#### About")
discord_logo(os.getenv('DISCORD_USERNAME'))
flipside_logo()
flipside_logo(url="https://flipsidecrypto.xyz/kipto-1822")
