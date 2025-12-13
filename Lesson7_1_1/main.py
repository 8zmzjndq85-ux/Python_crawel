import streamlit as st
import pandas as pd
import json

def load_rate():
    with open("rate.json", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

# 之後的邏輯同你原本的 Streamlit 程式