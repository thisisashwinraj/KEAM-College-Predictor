import numpy as np
import streamlit as st
import pandas as pd
import time

from model.predictor import CollegePredictor
from model.chatbot import Chatbot
from model.reports import PredictionsReport
from model.send_mail import CollegeListMailer, BugReportMail

from streamlit_star_rating import st_star_rating
from bokeh.models.widgets import Div


# Set the title and favicon for the streamlit web application
st.set_page_config(
    page_title="Jasper",
    page_icon="assets/favicon/jasper-favicon.jpg",
)

# Remove the extra padding from the top margin of the web app
st.markdown(
    """
        <style>
               .block-container {
                    padding-top: 1rem;
					padding-bottom: 1rem;
                }
        </style>
        """,
    unsafe_allow_html=True,
)

# Hide streamlit's default image expanders from app interface
hide_img_fs = """
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
"""
st.markdown(hide_img_fs, unsafe_allow_html=True)  # Allow HTML parsing

# Hide the streamlit menu and default footer from the app's front-end
HIDE_MENU_STYLE = """
<style>
#MainMenu  {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(HIDE_MENU_STYLE, unsafe_allow_html=True)  # Allow HTML tags in mkd


def apply_style_to_sidebar_button(file_name):
    with open(file_name, encoding="utf-8") as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)


def college_predictor():
    st.title(":dart: KEAM College Predictor")
    user_input_full_name_warning = False
    user_input_email_id_warning = False

    user_input_full_name = st.text_input("Full Name:")

    if len(user_input_full_name) < 1:
        st.warning("Full Name is a required field", icon="⚠️")
        user_input_full_name_warning = True
    else:
        user_input_full_name_warning = False

    col1, col2 = st.columns(2)

    with col1:
        user_input_email_id = st.text_input("E-Mail Id:")

    if len(user_input_email_id) < 1:
        st.warning("E-Mail Id is a required field", icon="⚠️")
        user_input_email_id_warning = True
    else:
        user_input_email_id_warning = False

    if (
        user_input_email_id_warning == False
        and CollegeListMailer.is_valid_email(user_input_email_id) == False
    ):
        st.warning("Please enter a valid email id", icon="⚠️")
        user_input_email_id_warning = True
    else:
        user_input_email_id_warning = False

    course_list = (
        "Electronics and Communication Engineering",
        "Civil Engineering",
        "Mechanical Engineering",
        "Electrical and Electronics Engineering",
        "Computer Science and Engineering",
        "Chemical Engineering",
        "Information Technology",
        "Applied Electronics",
        "Bio Technology and Biochemical Engineering",
        "Artificial Intelligence",
        "Automobile Engineering",
        "Electronics and Instrumentation",
        "Food Technology",
        "Aeronautical Engineering",
        "Mechatronics Engineering",
        "Production Engineering",
        "Dairy Technology",
        "Robotics and Automation",
        "Safety and Fire Engineering",
        "Naval Architecture and Ship Building",
        "Agricultural Engineering",
        "Metallurgical and Materials Engineering",
        "Polymer Engineering",
        "Printing Technology",
    )

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
        user_input_rank = st.number_input(
            "Enter Your Rank:", min_value=1, max_value=5000000
        )

    category_hashmap = {
        "State Merit (SM)": "SM",
        "Ezhava (EZ)": "EZ",
        "Muslim (MU)": "MU",
        "Other Backward Hindu (BH)": "BH",
        "Latin Catholic & Anglo Indian (LA)": "LA",
        "Dheevara & Related (DV)": "DV",
        "Viswakarma & Related (VK)": "VK",
        "Other Backward Christian (BX)": "BX",
        "Kudumbi (KU)": "KU",
        "Kusavan & Related (KN)": "KN",
        "Scheduled Caste (SC)": "SC",
        "Scheduled Tribe (ST)": "ST",
    }

    with col4:
        category_selectbox = st.selectbox(
            "Select Category:", list(category_hashmap.keys())
        )
        user_input_category = category_hashmap[category_selectbox]

    college_type_hashmap = {
        "Government (G)": "G",
        "Government Controlled (N)": "N",
        "Private/Self-Financing (S)": "S",
    }

    with col5:
        college_type_selectbox = st.selectbox(
            "Select College Type:", list(college_type_hashmap.keys())
        )
        user_input_college_type = college_type_hashmap[college_type_selectbox]

    accept_terms_and_conditions = st.checkbox(
        "By using the college predictor I accept the terms and conditions & I consent "
        + "to be contacted in future"
    )

    isDisabled = (
        user_input_email_id_warning
        or user_input_full_name_warning
        or (not accept_terms_and_conditions)
    )

    if st.button("Predict Colleges for Me", disabled=isDisabled):
        predicted_colleges = CollegePredictor.keam_college_predictor(
            user_input_course,
            user_input_college_type,
            user_input_category,
            user_input_rank,
        )

        hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
        # Inject CSS with Markdown
        st.markdown(hide_table_row_index, unsafe_allow_html=True)

        PredictionsReport.college_predictions_report(predicted_colleges)

        CollegeListMailer.send_college_predictions_mail(
            user_input_full_name, user_input_email_id
        )

        # predicted_colleges = predicted_colleges.drop("College Name", axis = 'columns')
        # st.sidebar.table(predicted_colleges.head())

        email_sent_alert = st.success(
            "An e-mail with a list of eligible colleges has been mailed to you",
            icon="✅",
        )

        time.sleep(5)
        email_sent_alert.empty()

    st.sidebar.markdown("""---""")
    apply_style_to_sidebar_button("assets/style.css")

    user_input_chatbot_query = st.sidebar.text_input("Have doubts? Ask Jasper:")

    if st.sidebar.button("Send Message"):
        chatbot_response = Chatbot.enquiry(user_input_chatbot_query)

        chatbot_message_alert = st.sidebar.warning(chatbot_response, icon="⚠️")

        time.sleep(5)
        chatbot_message_alert.empty()
    st.sidebar.info("This feature is still in development", icon="ℹ️")

    for _ in range(15):
        st.sidebar.markdown("\n\n")

    st.sidebar.success("This application is created by Ashwin Raj")


def about_page():
    # Display a markdown title for the about section with an emoji
    st.markdown("# :dart: About Jasper - College Predictor")

    # Display a paragraph with basic information about CroMa and it's features
    st.markdown(
        "<p align = 'justify'>Welcome to the KEAM College Predictor Tool, a "
        + "powerful tool built by Ashwin Raj that helps students predict the "
        + "colleges where they are likely to get admission, based on their rank "
        + "in KEAM's Engineering Test</p>",
        unsafe_allow_html=True,
    )

    # Display paragraph with information about ticketing machine and real-time database
    st.markdown(
        "<p align = 'justify'>KEAM, or Kerala Engineering Architecture Medical, "
        + "is a state-level entrance examination conducted by the Commissioner "
        + "for Entrance Examinations (CEE) in Kerala, India. This exam is taken "
        + "by thousands of students every year, for getting admission to some of the "
        + "pioneers colleges in the state. However, predicting the best option from "
        + "150+ colleges can be a daunting task. That's where Jasper comes in handy</p>",
        unsafe_allow_html=True,
    )

    # Display another paragraph with information about CroMa's database structure and rules
    st.markdown(
        "<p align = 'justify'>Using data from the past six years, the KEAM College "
        + "Predictor Tool analyzes trends and patterns to predict the colleges where "
        + "students are likely to get admission based on their rank. This "
        + "can be incredibly valuable for students who want to plan their "
        + "applications and make informed decisions about their future</p>",
        unsafe_allow_html=True,
    )

    # Add an input box for the user to enter their email ID for subscribing to newsletter
    newsletter_user_email_id = st.sidebar.text_input("Enter your Email Id")
    if (
        len(newsletter_user_email_id) > 0
        and CollegeListMailer.is_valid_email(newsletter_user_email_id) == False
    ):
        st.sidebar.warning("Please enter a valid email id", icon="⚠️")

    # Apply the CSS styles defined in the parameter file to the sidebar buttons
    apply_style_to_sidebar_button("assets/style.css")

    # Add a button for the user to subscribe to the newsletter
    newsletter_mailing_list_user_email_id = st.sidebar.button(
        "Subscribe to our Newsletter"
    )

    if newsletter_mailing_list_user_email_id:
        # Display a success message when user subscribes to receive our newsletters
        newsletter_subscribed_alert = st.sidebar.success(
            "You have subscribed to newsletter", icon="✅"
        )

        time.sleep(3)  # Hold the execution for the next three seconds
        newsletter_subscribed_alert.empty()  # Clear the star_rating_alert from the UI

    st.sidebar.markdown("""---""")  # Add a horizontal line to the web app's sidebar

    # Create an expander widget for Contact the CroMa Team section
    contact_dev_team_expander = st.sidebar.expander("Contact the Development Team")

    # Add text input fields for the user to enter their name, email, and message
    contact_dev_team_expander.text_input("Enter your Full Name:")
    contact_dev_team_user_email_id = contact_dev_team_expander.text_input(
        "Enter your E-Mail Id:"
    )
    if (
        len(contact_dev_team_user_email_id) > 0
        and CollegeListMailer.is_valid_email(newsletter_user_email_id) == False
    ):
        contact_dev_team_expander.warning("Please enter a valid email id", icon="⚠️")

    contact_dev_team_expander.text_area("Enter your Message:")

    # Add a button to allow the user to send their message
    send_message_to_dev_team_button = contact_dev_team_expander.button("Send Message")

    if send_message_to_dev_team_button:
        # Display a success message when user sends a message to CroMa's dev team
        contact_dev_team_alert = contact_dev_team_expander.success(
            "Your message has been sent", icon="✅"
        )

        time.sleep(3)  # Hold the execution for the next three seconds
        contact_dev_team_alert.empty()  # Clear the star_rating_alert from the UI

    # Add 13 new lines to create space between sections in the sidebar
    for _ in range(13):
        st.sidebar.write("\n\n")

    # Add a section to rate the user's experience with CroMa using st_star_rating
    with st.sidebar:
        st.write("Found Jasper helpful? Rate your experience:")
        # Add a 5-star rating widget to allow the user to rate their experience
        star_rating = st_star_rating("", 5, 3, 54)

        # Check if star rating has been altered by the user
        if star_rating != 3:
            # Display a success message when a new star rating has been given
            star_rating_alert = st.success(
                "Thanks for sharing your experience", icon="✅"
            )

            time.sleep(3)  # Hold the execution for the next three seconds
            star_rating_alert.empty()  # Clear the star_rating_alert from the UI


def send_bug_report():
    # Display a markdown title for the bug report  with a bug emoji
    br_full_name_warning = False
    br_email_id_warning = False

    st.markdown("# :ladybug: Send Bug Report")

    # Display a message to users who wish to report a bug
    st.markdown(
        "<p align = 'justify'>If you believe that you have discovered any "
        + "vulnerability in Jasper, please fill in thr form below with a thorough "
        + "explanation of the vulnerability. We will revert back to you after due "
        + "diligence of your bug report</p>",
        unsafe_allow_html=True,
    )
    # Create two columns to hold text input fields
    col1, col2 = st.columns(2)

    # Define context managers to set the current column for the following input fields
    with col1:
        # Create a text input field in the first column to read user's full name
        br_full_name = st.text_input("Full Name:")

    if len(br_full_name) < 1:
        st.warning("Full Name is a required field", icon="⚠️")
        br_full_name_warning = True
    else:
        br_full_name_warning = False

    with col2:
        # Create a text input field in the second column to read user's email id
        br_email_id = st.text_input("E-Mail Id:")

    if len(br_email_id) < 1:
        st.warning("E-Mail Id is a required field", icon="⚠️")
        br_email_id_warning = True
    else:
        br_email_id_warning = False

    if (
        br_email_id_warning == False
        and CollegeListMailer.is_valid_email(br_email_id) == False
    ):
        st.warning("Please enter a valid email id", icon="⚠️")
        br_email_id_warning = True
    else:
        br_email_id_warning = False

    # Create two columns to hold input dropdown fields
    col3, col4 = st.columns(2)

    # Define context managers to set the current column for selectbox input field
    with col3:
        # Create a selectbox input field in the third column to read the bug location
        br_bug_in_page = st.selectbox("Which page is the bug in?", page_list)

    # Tuple of strings that represent different types of bugs for users to select from
    bug_types = (
        "General Bug/Error",
        "Access Token/API Key Disclosure",
        "Memory Corruption",
        "Database Injection",
        "Code Execution",
        "Denial of Service",
        "Privacy/Authorization",
    )

    # Define context managers to set the current column for selectbox input field
    with col4:
        # Create a selectbox input field in the fourth column to read the bug type
        br_bug_type = st.selectbox("What type of bug is it?", bug_types)

    # Create a text area where users can describe the bug and steps to reproduce it
    br_bug_description = st.text_area(
        "Describe the issue in detail (include steps to reproduce the issue):"
    )

    # Widget to upload relevant attachments, such as screenshots, charts, and reports.
    # The file uploader widget is set to accept multiple files (limit: 200mb per file)
    br_uploaded_files = st.file_uploader(
        "Include any relevant attachments such as screenshots, or reports:",
        accept_multiple_files=True,
    )

    # Checkbox that user must check to indicate that they accept terms & conditions
    bug_report_terms_and_conditions = st.checkbox(
        "I accept the terms and conditions and I consent to be contacted in future by "
        + "the CroMa support team"
    )

    isDisabled = (
        br_email_id_warning
        or br_full_name_warning
        or (not bug_report_terms_and_conditions)
    )

    # Create a button that the users can click to send the bug reports to the CroMa team
    # Disabled argument enables the button only if the user has checked the T&C checkbox
    if st.button("Send Bug Report", disabled=isDisabled):
        # Call send_bug_report_mail method of the BugReportMail object to send the mail
        BugReportMail.send_bug_report_mail(
            br_full_name,
            br_email_id,
            br_bug_in_page,
            br_bug_type,
            br_bug_description,
            br_uploaded_files,
        )

        # Displays a success message to user indicating that their report has been sent
        bug_report_sent_alert = st.success("Your bug report has been sent!", icon="✅")

        time.sleep(3)  # Hold the execution for the next three seconds
        bug_report_sent_alert.empty()  #  Clear the bug_report_sent_alert from the frontend

    # Create an expander to display the FAQs regarding bug reports in the sidebar
    faq_expander = st.sidebar.expander("Frequently Asked Questions", True)

    # Display the various frequently asked questions in the sidebar expander
    faq_expander.write(
        "Q: Do you offer any kind of bug bounty?\nA: No, we do not offer any bug bounties."
    )  # FAQ Question 1
    faq_expander.write(
        "Q: How long does it takes to hear back?\nA: You'll hear back from us within 3 days."
    )  # FAQ Question 2
    faq_expander.write(
        "Q: Can we share our reports with others?\nA: We expect you don't share any report."
    )  # FAQ Question 3

    # Add some empty lines to the sidebar to place the button on the bottom section
    for _ in range(16):
        st.sidebar.write("\n\n")

    # Apply the CSS styles defined in the parameter file to the sidebar buttons
    apply_style_to_sidebar_button("assets/style.css")

    # Create a button to redirect to CroMa's social media handles
    # NOTE: Streamlit is still implementing redirection features. This is only a workaround.
    if st.sidebar.button("Join our Community Handle"):
        # Open a new window/tab on user's default web browser
        javascript = "window.open('https://www.streamlit.io/')"

        # Trigger the JavaScript code when it fails to load an image
        html = f"img src onerror={javascript}"

        div = Div(text=html)  # Create a bokeh div with HTML
        st.bokeh_chart(
            div
        )  # Display the div object as a Bokeh chart in the Streamlit app

        # On rsuccesfully opening the tab, display a success message
        st.sidebar.success("Redirecting you to community handle")


# Create a dictionary of different pages of thew web app, along with their corresponding functions
page_list = {
    "College Predictor": college_predictor,
    "About Jasper": about_page,
    "Send Bug Report": send_bug_report,
}

# Create a dropdown menu for selecting a page from the page_list, passing the dictionary key
selected_page = st.sidebar.selectbox("Navigate Within WebApp:", page_list.keys())

page_list[
    selected_page
]()  # Call function corresponding to the page keeping key as an index
