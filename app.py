import streamlit as st
st.write('# Streamlit Calculator')

num1 = st.number_input('number 1')
num2 = st.number_input('number 2')
num3 = num1 + num2

st.write('# Answer is ',num3)
