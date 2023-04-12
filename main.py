import numpy as np
import streamlit as st
import pandas as pd
import time

from model.predictor import CollegePredictor
from model.chatbot import Chatbot
from model.reports import PredictionsReport
from model.send_mail import CollegeListMailer


# Set the title and favicon for the streamlit web application
st.set_page_config(
    page_title="Jasper",
    page_icon="hardware/assets/croma-favicon.png",
)

# Hide the streamlit menu and default footer from the app's front-end
HIDE_MENU_STYLE = """
<style>
#MainMenu  {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(HIDE_MENU_STYLE, unsafe_allow_html=True)  # Allow HTML tags in mkd


def apply_style_to_sidebar_button(file_name):
    """
    Function to apply CSS style specified in the parameter to the sidebar button.
    The function takes a CSS file as a parameter and applies the customized style
    to all the buttons widgets on the sidebar of the croma_hw_playground web page
    Read more in the :ref:`Styling the CroMa Web Application`.
    .. versionadded:: 1.2.0
    Parameters:
        [css file] file_name: CSS file holding style to be applied on the buttons
    Returns:
        None -> Applies the style specified in the CSS file to all sidebar button
    """
    with open(file_name, encoding="utf-8") as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)


def college_predictor():
    st.title(":dart: KEAM College Predictor")
    user_input_full_name_warning = False
    user_input_email_id_warning = False

    user_input_full_name = st.text_input("Full Name:")

    if len(user_input_full_name) < 1:
        st.warning("This is a required field", icon="⚠️")
        user_input_full_name_warning = True
    else:
        user_input_full_name_warning = False

    col1, col2 = st.columns(2)

    with col1:
        user_input_email_id = st.text_input("E-Mail Id:")

    if len(user_input_email_id) < 1:
        st.warning("This is a required field", icon="⚠️")
        user_input_email_id_warning = True
    else:
        user_input_email_id_warning = False

    if user_input_email_id_warning == False and CollegeListMailer.is_valid_email(user_input_email_id) == False:
        st.warning("Please enter a valid email id", icon="⚠️")
        user_input_email_id_warning = True
    else:
        user_input_email_id_warning = False

    course_list = ('Electronics and Communication Engineering', 'Civil Engineering', 'Mechanical Engineering', 'Electrical and Electronics Engineering', 'Computer Science and Engineering', 'Chemical Engineering', 'Information Technology', 'Applied Electronics', 'Bio Technology and Biochemical Engineering', 'Artificial Intelligence', 'Automobile Engineering', 'Electronics and Instrumentation', 'Food Technology', 'Aeronautical Engineering', 'Mechatronics Engineering', 'Production Engineering', 'Dairy Technology', 'Robotics and Automation', 'Safety and Fire Engineering', 'Naval Architecture and Ship Building', 'Agricultural Engineering', 'Metallurgical and Materials Engineering', 'Polymer Engineering', 'Printing Technology')

    with col2:
        user_input_course = st.selectbox("Select Course:", course_list)

    col3, col4, col5 = st.columns(3)
    
    # st.markdown("""
    # <style>
    #     button.step-up {display: none;}
    #     button.step-down {display: none;}
    #     div[data-baseweb] {border-radius: 4px;}
    # </style>""",
    # unsafe_allow_html=True)

    with col3: 
        user_input_rank = st.number_input("Enter Your Rank:", min_value=1, max_value=5000000)

    category_hashmap = {'State Merit (SM)': 'SM', 'Ezhava (EZ)': 'EZ', 'Muslim (MU)': 'MU', 'Other Backward Hindu (BH)': 'BH', 'Latin Catholic & Anglo Indian (LA)': 'LA', 'Dheevara & Related (DV)': 'DV', 'Viswakarma & Related (VK)': 'VK', 'Other Backward Christian (BX)': 'BX', 'Kudumbi (KU)': 'KU', 'Kusavan & Related (KN)': 'KN', 'Scheduled Caste (SC)': 'SC', 'Scheduled Tribe (ST)': 'ST'}

    with col4:
        category_selectbox = st.selectbox("Select Category:", list(category_hashmap.keys()))
        user_input_category = category_hashmap[category_selectbox]

    college_type_hashmap = {'Government (G)': 'G', 'Government Controlled (N)': 'N', 'Private/Self-Financing (S)': 'S'}

    with col5:
        college_type_selectbox = st.selectbox("Select College Type:", list(college_type_hashmap.keys()))
        user_input_college_type = college_type_hashmap[college_type_selectbox]

    accept_terms_and_conditions = st.checkbox(
        "By using the college predictor I accept the terms and conditions & I consent " 
        + "to be contacted in future"
    )

    isDisabled = user_input_email_id_warning or user_input_full_name_warning or (not accept_terms_and_conditions)

    if st.button("Predict Colleges for Me", disabled = isDisabled):
        predicted_colleges = CollegePredictor.keam_college_predictor(user_input_course,user_input_college_type,user_input_category,user_input_rank)
        
        hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
        # Inject CSS with Markdown
        st.markdown(hide_table_row_index, unsafe_allow_html=True)

        PredictionsReport.college_predictions_report(predicted_colleges)

        CollegeListMailer.send_college_predictions_mail(user_input_full_name, user_input_email_id)

        # predicted_colleges = predicted_colleges.drop("College Name", axis = 'columns')
        # st.sidebar.table(predicted_colleges.head())

        email_sent_alert = st.success("An e-mail with a list of eligible colleges has been mailed to you", icon="✅")

        time.sleep(5)
        email_sent_alert.empty()

    st.sidebar.markdown("""---""")
    apply_style_to_sidebar_button("assets/style.css")

    user_input_chatbot_query = st.sidebar.text_input("Enter your Query:")

    if st.sidebar.button("Send Message"):
        chatbot_response = Chatbot.enquiry(user_input_chatbot_query)

        chatbot_message_alert = st.sidebar.info(chatbot_response, icon="✅")

        time.sleep(5)
        chatbot_message_alert.empty()

def about_page():
    pass

def send_bug_report():
    pass

# Create a dictionary of different pages of thew web app, along with their corresponding functions
page_list = {
    "College Predictor": college_predictor,
    "About Jasper": about_page,
    "Send Bug Report": send_bug_report,
}

# Create a dropdown menu for selecting a page from the page_list, passing the dictionary key
selected_page = st.sidebar.selectbox("Navigate Within Pages:", page_list.keys())

page_list[
    selected_page
]()  # Call function corresponding to the page keeping key as an index