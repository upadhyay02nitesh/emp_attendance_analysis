# import streamlit as st
# import requests
# import os





# def convert_currency(amount, to_currency):
#     url = f"https://open.er-api.com/v6/latest/INR"
#     response = requests.get(url)
#     print(response.json())
#     if response.status_code == 200:
#         return response.json()["rates"][to_currency] * amount
#     return None

# # Streamlit UI
# st.set_page_config(page_title="💱 INR Currency Converter", layout="centered")
# st.title("💱 Convert INR to Other Currencies")

# with st.form("convert_form"):
#     amount = st.number_input("Enter amount in INR", min_value=1.0, step=1.0)
#     currency_options = ["USD", "EUR", "GBP", "INR", "JPY", "AUD"]
#     to_currency = st.selectbox("Convert to (Currency Code)", options=currency_options, index=0, help="Select currency")
#     submit = st.form_submit_button("Convert")

# if submit:
#     converted = convert_currency(amount, to_currency.upper())
    
#     if converted is not None:
#         st.success(f"{amount} INR = {converted:.2f} {to_currency.upper()}")
#     else:
#         st.error("Failed to fetch exchange rate.")



import streamlit as st
import requests
import os





def convert_currency(amount,from_currency, to_currency):
    url = f"https://open.er-api.com/v6/latest/{from_currency}"
    response = requests.get(url)
    # print(response.json()
    if response.status_code == 200:
        return response.json()["rates"][to_currency] * amount
    return None

# Streamlit UI
st.set_page_config(page_title="💱  Currency Converter", layout="centered")
st.title("💱 Convert One Currency to Other Currencies")

with st.form("convert_form"):
    currency_options = ["USD", "EUR", "GBP", "INR", "JPY", "AUD"]
    amount = st.number_input("Enter amount in ", min_value=1.0, step=1.0)
    from_currency = st.selectbox("Convert from (Currency Code)", options=currency_options, index=0, help="Select currency")
    to_currency = st.selectbox("Convert to (Currency Code)", options=currency_options, index=0, help="Select currency")
    submit = st.form_submit_button("Convert")

if submit:
    converted = convert_currency(amount,from_currency, to_currency.upper())
    
    if converted is not None:
        st.success(f"{amount} {from_currency} = {converted:.2f} {to_currency.upper()}")
    else:
        st.error("Failed to fetch exchange rate.")
