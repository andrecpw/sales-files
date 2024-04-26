
from notion_client import Client
import streamlit as st


def initialize_notion_client():
    return Client(auth=st.secrets["notion_token"])

def add_form_data_to_notion(notion, form_data):
    properties = {}
    for key, value in form_data.items():
        if isinstance(value, str):
            properties[key] = {
                "title" if key == "CLIENTE" else "rich_text": [{"text": {"content": value}}]
            }

    notion.pages.create(parent={"database_id": st.secrets["database_id"]}, properties=properties)