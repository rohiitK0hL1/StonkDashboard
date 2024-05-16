import streamlit as st
from streamlit_option_menu import option_menu

import accounts, dashboard

st.set_page_config(
    page_title="Stonk Dashboard",
)

class MultiApp:
    def __init__(self):
        self.apps=[]
    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })
    def run():
        with st.sidebar:
            app=option_menu(
                menu_title='Stonk Dashboard',
                options=['Accounts','Dashboard'],
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color":"white", "font-size": "20px","text-align":"left", "margin":"0px"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )
            
            if app == 'Account':
                accounts.app()
            if app == 'Dashboard':
                dashboard.app()

    run()