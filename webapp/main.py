
import streamlit as st
import pandas as pd


def is_good(s):
    return ['background-color: green'] * len(s) if s.good_prediction else ['background-color: red'] * len(s)


pct = st.empty()
test = st.empty()

while True:
    dff = pd.read_csv("/data/dataset.csv")
    test.dataframe(dff.style.apply(is_good, axis=1))
    pct.write(f"Percentage of good predictions: {dff['good_prediction'].mean() * 100:.2f}%")
