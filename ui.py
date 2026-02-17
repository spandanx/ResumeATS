import logging

import streamlit as st

import asyncio
from src.main import process_resume, authenticate

import pandas as pd
import random
# from numpy.random import default_rng as rng
# import plotly.express as px
import plotly.graph_objects as go
# from pages.login_page_2 import login_page_2_func

# from streamlit_cookies_controller import CookieController
# from datetime import datetime, timedelta
# if 'controller' not in st.session_state:
#     logging.info("Setting cookie controller in session state")
#     st.session_state.controller = CookieController()
# else:
#     logging.info("Cookie controller is already set")
#
# controller = st.session_state.controller
# controller = CookieController()

# from streamlit_local_storage import LocalStorage
# if 'local_storage' in st.session_state:
#     logging.info("LocalStorage variable Found and setting")
#     localS = st.session_state['local_storage']
# else:
#     logging.info("LocalStorage variable not Found and setting")
#     localS = LocalStorage()
#     st.session_state["local_storage"] = localS

# from streamlit_ws_localstorage import injectWebsocketCode, getOrCreateUID
# conn = injectWebsocketCode()
# conn.setLocalStorageVal(key='persistent_data', val='some_data') # Save
# logging.info("Setting in localstorage")
# ret = conn.getLocalStorageVal(key='persistent_data')
# logging.info("Value set in localstorage")

# import sys
# sys.path.append('src.components.schemas')
# import sys
# sys.path.append('src')

def generate_random_color():
    return f'#{random.randint(0, 0xFFFFFF):06x}'

st.set_page_config(page_title="Resume ATS Application")

# st.title("Resume ATS scorer")
st.set_page_config(layout="wide")
# st.markdown("""
# This application calculates resume score and gets you suggestion on the possible changes in the resume.
# It also reads job descriptions and calculates similarity score.
# Version: 1.6
# """)


####### Login Page

def login_page():
    # Define a placeholder for the login form
    login_placeholder = st.empty()

    # Hardcoded credentials for demonstration
    # ACTUAL_USERNAME = "user"
    # ACTUAL_PASSWORD = "password"

    # Check if the user is already logged in
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        with login_placeholder.form("login_form"):
            st.markdown("### Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")

            if submit_button:
                response = asyncio.run(authenticate(username=username, password=password))
                logging.info("Response - ")
                logging.info(response)

                if response is not None and response is not False:
                    logging.info("Logging In")
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    login_placeholder.empty()  # Clear the login form
                    # st.success("Login successful!")
                    # logging.info("Setting cache")
                    # all_cache = controller.getAll()
                    # logging.info(all_cache)
                    # controller.set('username', username)
                    # controller.set('token', response)
                    # controller.set('my_cookie', 'my_value', expires_at=expires_at)
                    # controller.set('my_cookie', 'my_value', expires=expires_at)
                    # localS.setItem('my_key_custom', 'my_value')
                    logging.info("Setting cache done")
                    st.rerun()
                else:
                    logging.info("Failed to login")
                    # st.error("Invalid username or password.")
    # else:
    #     st.write("Welcome, you are logged in!")
    #     if st.button("Logout"):
    #         st.session_state.logged_in = False
    #         # st.experimental_rerun() # Rerun to show login page again
    #         st.rerun()

# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
#
dummy_tab_1, dummy_tab_2, logout_tab = st.columns([1, 1, 0.2]) # Adjust ratios as needed

with logout_tab:
    if ('logged_in' in st.session_state) and st.session_state.logged_in:
        if st.button("Logout", key="logout_button_small"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            # st.experimental_rerun() # Rerun to show login page again
            st.rerun()

if ('logged_in' not in st.session_state) or (('logged_in' in st.session_state) and (not st.session_state.logged_in)):
    login_page()
# else:
#     st.write("Welcome, you are logged in!")
#     # Display your application content here
#     if st.button("Logout", key="logout_button_large"):
#         st.session_state.logged_in = False
#         st.rerun()

####### Login Page

# input_tab, analytics_tab = st.tabs(["Resume Input", "Analytics"])
# full_page, logout_button = st.columns([2, 0.1]) # Adjust ratios as needed
#
# with logout_button:
#     if st.button("My Button"):
#         st.write("Button clicked!")

# dummy_tab_1, dummy_tab_2, logout_tab = st.columns([1, 1, 0.1])
#
# if logout_tab:
#     if st.button("Logout", key="logout_button_small"):
#         st.session_state.logged_in = False
#         st.rerun()

def switch_tab(tab_index):
    js = f"""
    <script>
    function clickTab() {{
        var tabGroup = window.parent.document.getElementsByClassName("stTabs")[0];
        if (tabGroup) {{
            var tabs = tabGroup.getElementsByTagName("button");
            if (tabs.length > {tab_index}) {{
                tabs[{tab_index}].click();
                return true;
            }}
        }}
        return false;
    }}
    // Try immediately and with a small delay
    if (!clickTab()) {{
        setTimeout(clickTab, 100);
    }}
    </script>
    """
    st.components.v1.html(js, height=0)

# with full_page:
if ('logged_in' in st.session_state) and st.session_state.logged_in:

    input_tab, analytics_tab = st.tabs(["Resume Input", "Analytics"])

    response = {}

    username = "default_user"
    if 'username' in st.session_state:
        username = st.session_state['username']

    logging.info("Current user - ")
    logging.info(username)

    with input_tab:

        uploaded_resume_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])

        job_description = st.text_area("Enter your job description:", "")

        if st.button("Calculate Score"):
            if not uploaded_resume_file:
                st.markdown(":red[File Not found]")
            else:
                try:
                    response = asyncio.run(process_resume(resume_file_path=uploaded_resume_file, raw_job_description=job_description, username=username))
                    # st.markdown(response)
                    switch_tab(1)
                except Exception as e:
                    st.markdown(f":red[Something is wrong! Could not perform the analysis] \n {e}")

    with analytics_tab:
        if "components" in response and len(response["components"]) == 2:
            resume_tab, similaity_tab = st.tabs(["Resume Score", "Similarity Score"])

            with resume_tab:
                # st.write(response["resume_score_description"])
                # resume_dict = response["resume_component_wise_score"]

                ############### Donut chart ###############

                # labels = [label["category"] for label in response["resume_component_wise_score"]]
                labels = ["Resume score", "Scope of improvements"]
                # labels.append("scope of improvements")
                # labels = ['resume score', 'scope of improvements']

                # values = [label["score"] for label in response["resume_component_wise_score"]]
                values = [response["resume_total_score"], 100 - response["resume_total_score"]]
                # values.append(100 - response["resume_total_score"])
                # values = [response["resume_total_score"], 100 - response["resume_total_score"]]
                colors = ['rgb(43, 171, 103)', 'rgb(138, 150, 144)']

                # colors = [generate_random_color() for _ in range(2)]

                # Use `hole` to create a donut-like pie chart
                # fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker_colors=colors)])
                resume_donut_chart_column, resume_line_chart_column = st.columns([1, 1])

                with resume_donut_chart_column:
                    ############### Donut chart ###############
                    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker_colors=colors)])
                    fig.update_traces(hoverinfo='label+percent', textinfo='none', hole=.8)
                    fig.update_layout(
                        annotations=[dict(text=(str(round(response["resume_total_score"], 2))), x=0.5, y=0.5,
                                          font_size=20, showarrow=False, xanchor="center"),
                                     dict(text="TOTAL", x=0.5, y=0.4,
                                          font_size=20, showarrow=False, xanchor="center")
                                     ])
                    st.plotly_chart(fig)
                    ############### Donut chart ###############

                with resume_line_chart_column:

                    ############### Line chart ################
                    df = pd.DataFrame(
                        {
                            "Sections": [section["category"] for section in response["resume_component_wise_score"]],
                            "Scores": [section["score"] for section in
                                       response["resume_component_wise_score"]],
                            "Colors": [generate_random_color() for _ in range(len(response["resume_component_wise_score"]))]
                        }
                    )

                    # st.bar_chart(df, x="Features", y="Scores")
                    st.bar_chart(df, x="Sections", y="Scores", color="Colors")

                    ############### Line chart ################

                ############## Columns ##############
                st.divider()
                for resume_section in response["resume_component_wise_score"]:
                    line_col, description_col = st.columns([0.2, 0.8])

                    with line_col:
                        st.progress(int(resume_section["score"]) * 10, text=resume_section["category"] + " | Score - :red[" + str(int(resume_section["score"])) + "]")
                        # st.markdown("")

                    with description_col:
                        st.markdown(resume_section["justification"])

                        with st.expander("Suggestions"):
                            st.write('\n'.join([" - " + suggestion for suggestion in resume_section["improvement_suggestions"]]))

                    st.divider()

            with similaity_tab:
                labels = [section["category"] for section in response["component_wise_score_similarity"]]

                values = [section["similarity_score"] for section in response["component_wise_score_similarity"]]
                # colors = ['rgb(33, 75, 99)', 'rgb(18, 36, 37)']

                fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
                fig.update_traces(hoverinfo="label+value", textinfo='label+value', hole=.8)
                fig.update_layout(
                    annotations=[dict(text=(str(round(response["similarity_total_score"], 2))), x=0.5, y=0.5,
                                      font_size=20, showarrow=False, xanchor="center"),
                                 dict(text="OVERALL", x=0.5, y=0.4,
                                      font_size=20, showarrow=False, xanchor="center")
                                 ])
                st.plotly_chart(fig)

                ################ Suggestions ##############
                st.divider()
                for resume_section in response["component_wise_score_similarity"]:
                    line_col, description_col = st.columns([0.2, 0.8])

                    with line_col:
                        st.progress(int(resume_section["similarity_score"]) * 10,
                                    text=resume_section["category"] + " | Score - :red[" + str(
                                        int(resume_section["similarity_score"])) + "]")
                        # st.markdown("")

                    with description_col:
                        st.markdown(resume_section["justification"])

                        with st.expander("Suggestions"):
                            st.write(
                                '\n'.join([" - " + suggestion for suggestion in resume_section["suggestions"]]))

                    st.divider()
                ################ Suggestions ##############

        elif "components" in response and len(response["components"]) == 0:
            st.markdown(":red[Could not analyse the resume]")

        elif "components" in response and "resume_description" in response["components"]:
            st.header("Resume Score")
            st.write(response["resume_score_description"])

        elif "components" in response and "similarity_description" in response["components"]:
            st.header("Similarity Score")
            st.write(response["similarity_score_description"])


