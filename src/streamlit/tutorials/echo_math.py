import streamlit as st
import pandas as pd

st.title('This is my title')

with st.echo():
    x = 50

with st.echo():
    y = 20

with st.echo():
    z = x + y
    st.write(z)
