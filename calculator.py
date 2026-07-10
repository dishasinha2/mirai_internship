import streamlit as st

st.set_page_config(
    page_title="Calculator",
    page_icon="🧮",
    layout="centered"
)

st.title("🧮 Streamlit Calculator")
st.write("Perform basic arithmetic operations.")

col1, col2 = st.columns(2)

with col1:
    num1 = st.number_input("First Number", value=0.0)

with col2:
    num2 = st.number_input("Second Number", value=0.0)

operation = st.radio(
    "Select Operation",
    ["+", "-", "×", "÷"],
    horizontal=True
)

if st.button("Calculate", use_container_width=True):

    if operation == "+":
        result = num1 + num2

    elif operation == "-":
        result = num1 - num2

    elif operation == "×":
        result = num1 * num2

    elif operation == "÷":
        if num2 == 0:
            st.error("Cannot divide by zero.")
            st.stop()
        result = num1 / num2

    st.metric("Result", result)