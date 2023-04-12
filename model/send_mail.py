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
        """
        Method to send a DSR (Daily Status Report) mail with an attachment to the admin
        Sends an email from the support team's mail id to the administrators mail using
        the smtp.gmail.com server at port 587 along with a PDF attachment, as a payload.

        .. versionadded:: 1.2.0

        Parameters:
            None -> All variables are read from the system memory as per configruations

        Returns:
            None -> Sends an email with atttachment to the receivers mail id using SMTP

        NOTE: Credentials file holding the app key should be maintained in a secure env
        """
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
        body = "Hi " + user_first_name + ",\n\nWe hope this email finds you well. We appreciate you being amongst the first hundred users to try Jasper.\n\nPlease find below the predictions of colleges where you may get admission based on your KEAM rank. We have taken great care to ensure the accuracy of the predictions, and we hope they will be helpful in guiding you towards the right college for your academic and career goals.\n\nIf you have any questions or need further assistance, please do not hesitate to reach out to us. We are always here to help you.\n\nOnce again, thank you for using Jasper, and we wish you the best of luck in your college search journey.\n\nBest regards,\nJasper Community Team"

        email.attach(MIMEText(body, "plain"))  # Attach the body with the email instance

        filename = "college_predictions.pdf"  # open the file to be sent in the filename variable
        attachment = open("data/statements/college_predictions.pdf", "rb")  # pylint: disable=consider-using-with

        # Create an instance of MIMEBase and named as payload
        payload = MIMEBase("application", "octet-stream")
        payload.set_payload((attachment).read())  # Change the payload into encoded form

        encoders.encode_base64(payload)  # Encode the payload into base-64 form
        payload.add_header("Content-Disposition", "attachment; filename= %s" % filename)  # pylint: disable=consider-using-f-string

        email.attach(payload)  # Attach the instance 'payload' to the instance 'email'

        smtp_session = smtplib.SMTP("smtp.gmail.com", 587)  # Create an SMTP session
        smtp_session.starttls()  # Encrypt the connection using transport layer security

        # Authenticate the sender before sending the email to the receiver
        smtp_session.login(mail_credentials.SENDER_EMAIL_ID, mail_credentials.SENDER_EMAIL_PASSWORD)

        text = (
            email.as_string()
        )  # Converts the Multipart mail into a string & send the mail
        smtp_session.sendmail(
            mail_credentials.SENDER_EMAIL_ID, receiver_email_id, text
        )  # Perform entire mail transaction

        smtp_session.quit()  # Terminate the SMTP session after sending the mail