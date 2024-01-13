import streamlit as st
from st_pages import Page, add_page_title, show_pages


show_pages(
    [
        Page("app/aktual.py", "Aktual", "🏠"),
        Page("app/prakiraan.py", "Prakiraan 3 Hari", ":books:"),
        Page("app/wrhp.py", "Angin dan RASON", "📖"),
        Page("app/regional.py", "Parameter Regional", "✏️"),
        Page("app/rainrate.py", "Rainrate", "🧰"),
    ]
)

add_page_title()  # Optional method to add title and icon to current page


