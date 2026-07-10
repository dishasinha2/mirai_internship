import streamlit as st
import math

st.set_page_config(
    page_title="Scientific Calculator",
    page_icon="🧮",
    layout="centered"
)

st.title("🧮 Scientific Calculator")

st.write("Perform basic and scientific calculations.")

mode = st.radio(
    "Angle Mode",
    ["Degrees", "Radians"],
    horizontal=True
)

st.divider()

operation = st.selectbox(
    "Select Operation",
    [
        "Addition (+)",
        "Subtraction (-)",
        "Multiplication (×)",
        "Division (÷)",
        "Power (x^y)",
        "Square (x²)",
        "Square Root (√x)",
        "Reciprocal (1/x)",
        "Modulus (%)",
        "Sine (sin)",
        "Cosine (cos)",
        "Tangent (tan)",
        "Log Base 10",
        "Natural Log (ln)",
        "Factorial",
        "Absolute Value"
    ]
)

binary_operations = [
    "Addition (+)",
    "Subtraction (-)",
    "Multiplication (×)",
    "Division (÷)",
    "Power (x^y)",
    "Modulus (%)"
]

if operation in binary_operations:
    col1, col2 = st.columns(2)

    with col1:
        num1 = st.number_input("First Number", value=0.0)

    with col2:
        num2 = st.number_input("Second Number", value=0.0)

else:
    num1 = st.number_input("Enter Number", value=0.0)

if st.button("Calculate", use_container_width=True):

    try:

        if operation == "Addition (+)":
            result = num1 + num2

        elif operation == "Subtraction (-)":
            result = num1 - num2

        elif operation == "Multiplication (×)":
            result = num1 * num2

        elif operation == "Division (÷)":
            if num2 == 0:
                st.error("Cannot divide by zero.")
                st.stop()
            result = num1 / num2

        elif operation == "Power (x^y)":
            result = math.pow(num1, num2)

        elif operation == "Square (x²)":
            result = num1 ** 2

        elif operation == "Square Root (√x)":
            if num1 < 0:
                st.error("Square root of a negative number is not real.")
                st.stop()
            result = math.sqrt(num1)

        elif operation == "Reciprocal (1/x)":
            if num1 == 0:
                st.error("Cannot divide by zero.")
                st.stop()
            result = 1 / num1

        elif operation == "Modulus (%)":
            result = num1 % num2

        elif operation == "Sine (sin)":
            angle = math.radians(num1) if mode == "Degrees" else num1
            result = math.sin(angle)

        elif operation == "Cosine (cos)":
            angle = math.radians(num1) if mode == "Degrees" else num1
            result = math.cos(angle)

        elif operation == "Tangent (tan)":
            angle = math.radians(num1) if mode == "Degrees" else num1
            result = math.tan(angle)

        elif operation == "Log Base 10":
            if num1 <= 0:
                st.error("Log is only defined for positive numbers.")
                st.stop()
            result = math.log10(num1)

        elif operation == "Natural Log (ln)":
            if num1 <= 0:
                st.error("Natural log is only defined for positive numbers.")
                st.stop()
            result = math.log(num1)

        elif operation == "Factorial":
            if num1 < 0 or int(num1) != num1:
                st.error("Factorial is only defined for non-negative integers.")
                st.stop()
            result = math.factorial(int(num1))

        elif operation == "Absolute Value":
            result = abs(num1)

        st.success("Calculation Completed")
        st.metric("Result", result)

    except Exception as e:
        st.error(f"Error: {e}")

st.divider()

st.caption("Developed using Python + Streamlit")