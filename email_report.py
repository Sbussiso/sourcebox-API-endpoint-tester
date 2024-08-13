import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()


def report(endpoint, success, response_message=None):
    # Combine name, email, and message into a single string to return
    if success == True:
        full_message = f"""
        ENDPOINT SUCCESS: {endpoint}

        The endpoint {endpoint} PASSED automated testing. No further action needed.

        GITHUB REPO: {os.getenv('GITHUB_REPO')}

        BASE API URL: {os.getenv('BASE_URL')}

        Full API URL (endpoint included): {os.getenv('BASE_URL')}{endpoint}

        MESSAGE: {response_message}
        """
    else:
        full_message = f"""
        FAILURE OF ENDPOINT: {endpoint}

        The endpoint {endpoint} has Failed automated testing. Please investigate the issue and resolve it as soon as possible.

        GITHUB REPO: {os.getenv('GITHUB_REPO')}

        BASE API URL: {os.getenv('BASE_URL')}

        Full API URL (endpoint included): {os.getenv('BASE_URL')}{endpoint}

        ERROR MESSAGE: {response_message}
        """

    try:
        # Create the email content
        msg = MIMEMultipart()
        msg['From'] = os.getenv('GMAIL_USERNAME')
        msg['To'] = os.getenv('GMAIL_USERNAME')
        msg['Subject'] = f"Sourcebox API Endpoint Test Report for {endpoint} endpoint"

        # Attach the message
        msg.attach(MIMEText(full_message, 'plain'))

        # Connect to the server and send the email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(os.getenv('GMAIL_USERNAME'), os.getenv('GOOGLE_PASSWORD'))  # Hide before GitHub push
        server.send_message(msg)
        server.quit()

    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")
