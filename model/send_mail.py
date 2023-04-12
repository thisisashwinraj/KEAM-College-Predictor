import re
import smtplib
from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

from email import encoders
from email.mime.application import MIMEApplication

from config import mail_credentials


class CollegeListMailer:
    def is_valid_email(email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def send_college_predictions_mail(user_full_name, receiver_email_id):
        email = MIMEMultipart()  # Create an instance of MIMEMultipart

        # Store the senders email address in the To field
        email["From"] = mail_credentials.SENDER_EMAIL_ID
        # Store the receivers email address in the from field
        email["To"] = receiver_email_id

        # Get the user's first name
        user_first_name = ""
        for i in user_full_name:
            if i == " ":
                break
            else:
                user_first_name = user_first_name + i

        email["Subject"] = user_first_name + ", your college predictions are ready!"

        # Store the body of the mail in the function variable named body
        body = (
            "Hi "
            + user_first_name
            + ",\n\nWe hope this email finds you well. We appreciate you being amongst the first hundred users to try Jasper.\n\nPlease find below the predictions of colleges where you may get admission based on your KEAM rank. We have taken great care to ensure the accuracy of the predictions, and we hope they will be helpful in guiding you towards the right college for your academic and career goals.\n\nIf you have any questions or need further assistance, please do not hesitate to reach out to us. We are always here to help you.\n\nOnce again, thank you for using Jasper, and we wish you the best of luck in your college search journey.\n\nBest regards,\nJasper Community Team"
        )

        email.attach(MIMEText(body, "plain"))  # Attach the body with the email instance

        filename = "college_predictions.pdf"  # open the file to be sent in the filename variable
        attachment = open(
            "data/statements/college_predictions.pdf", "rb"
        )  # pylint: disable=consider-using-with

        # Create an instance of MIMEBase and named as payload
        payload = MIMEBase("application", "octet-stream")
        payload.set_payload((attachment).read())  # Change the payload into encoded form

        encoders.encode_base64(payload)  # Encode the payload into base-64 form
        payload.add_header(
            "Content-Disposition", "attachment; filename= %s" % filename
        )  # pylint: disable=consider-using-f-string

        email.attach(payload)  # Attach the instance 'payload' to the instance 'email'

        smtp_session = smtplib.SMTP("smtp.gmail.com", 587)  # Create an SMTP session
        smtp_session.starttls()  # Encrypt the connection using transport layer security

        # Authenticate the sender before sending the email to the receiver
        smtp_session.login(
            mail_credentials.SENDER_EMAIL_ID, mail_credentials.SENDER_EMAIL_PASSWORD
        )

        text = (
            email.as_string()
        )  # Converts the Multipart mail into a string & send the mail
        smtp_session.sendmail(
            mail_credentials.SENDER_EMAIL_ID, receiver_email_id, text
        )  # Perform entire mail transaction

        smtp_session.quit()  # Terminate the SMTP session after sending the mail


class BugReportMail:  # pylint: disable=too-few-public-methods
    def send_bug_report_mail(
        br_full_name,
        br_email_id,
        br_bug_in_page,
        br_bug_type,
        br_bug_description,
        attachment=None,
    ):  # pylint: disable=no-self-argument
        # Receiver's email id is fixed as the developer team's email id
        RECEIVER_EMAIL_ID = "rajashwin733@gmail.com"

        message = MIMEMultipart()  # Create an instance of MIMEMultipart

        message[
            "To"
        ] = RECEIVER_EMAIL_ID  #  Store the receivers mail id in the To field

        message[
            "From"
        ] = (
            mail_credentials.SENDER_EMAIL_ID
        )  # Store the senders mail id in the From field

        message[
            "Subject"
        ] = "Jasper Bug Report"  # Store the subject of the mail in the subject field

        br_mail_body = (
            "Hello team,\n\nA new bug report has been raised for Jasper. "
            + "Please find the details as mentioned below.\n\nSubmitted by: "
            + br_full_name
            + "\n\nE-Mail Id: "
            + br_email_id
            + "\n\nBug Reported In: "
            + br_bug_in_page
            + "\n\nType of Bug: "
            + br_bug_type
            + "\n\nDescription: "
            + br_bug_description
            + "\n\nRegards,\nJasper Support Team"
        )  # Store the body of the mail in the function variable named br_mail_body

        message.attach(
            MIMEText(br_mail_body, "plain", "utf-8")
        )  # Attach body with email instance

        # Check if a file is provided as an attachment to be sent across
        if attachment:
            att = MIMEApplication(
                attachment.read()  # pylint: disable=no-member
            )  # Read the attachment using read method
            att.add_header(
                "Content-Disposition",
                "attachment",
                filename=attachment.name,  # pylint: disable=no-member
            )
            message.attach(att)  # Attach the file to the email

        server = smtplib.SMTP(
            "smtp.gmail.com", 587
        )  # Create an SMTP session at Port 587
        server.starttls()  # Encrypt the connection using transport layer security
        server.ehlo()  # Hostname to send for this command defaults to the FQDN of the local host.

        # Authenticate the sender before sending the email to the receiver
        server.login(
            mail_credentials.SENDER_EMAIL_ID, mail_credentials.SENDER_EMAIL_PASSWORD
        )
        text = (
            message.as_string()
        )  # Converts the Multipart mail into a string & send the mail

        # Perform entire mail transaction
        server.sendmail(mail_credentials.SENDER_EMAIL_ID, RECEIVER_EMAIL_ID, text)
        server.quit()  # Terminate the SMTP session after sending the mail
