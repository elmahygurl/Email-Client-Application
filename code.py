import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(sender_email, sender_password, recipient_email, subject, body):
    """
    Send an email using SMTP protocol.

    Parameters:
        sender_email (str): Sender's email address.
        sender_password (str): Sender's email password.
        recipient_email (str): Recipient's email address.
        subject (str): Email subject.
        body (str): Email body.
    """
    try:
        #creating a multipart message to include email objects
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain')) # Adding body to the email

        #if using an Outlook's SMTP server
        with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print("Error occurred while sending email:", e)
    #     #if using a Gmail's SMTP server
    #      with smtplib.SMTP('smtp.gmail.com', 587) as server:
    #         server.starttls()
    #         server.login(sender_email, sender_password)
    #         server.send_message(msg)
    #         print("Email sent successfully!")
    # except Exception as e:
    #     print("Error occurred while sending email:", e)


def receive_email(username, password):
    """
    Receive the latest email using IMAP protocol and print its body.

    Parameters:
        username (str): User's email username.
        password (str): User's email password.
    """
    try:
        #if using an outlook IMAP server
        with imaplib.IMAP4_SSL('outlook.office365.com') as mail:
        #if using a Gmail's IMAP server    
        #with imaplib.IMAP4_SSL('imap.gmail.com') as mail:
            mail.login(username, password)
            mail.select('inbox')
            result, data = mail.search(None, 'ALL')
            latest_email_id = data[0].split()[-1]
            result, data = mail.fetch(latest_email_id, '(RFC822)')
            raw_email = data[0][1]
            email_message = email.message_from_bytes(raw_email)
            print('From:', email_message['From'])
            print('Subject:', email_message['Subject'])
            print('Body:')
            print(email_message.get_payload())
    except Exception as e:
        print("Error occurred while receiving email:", e)


#testing example
if __name__ == "__main__":
    
    sender_email = 'email@outlook.com'
    sender_password = 'pass'
    recipient_email = 'email@outlook.com'
    subject = 'Test Email'
    body = 'This is a test email.'

    send_email(sender_email, sender_password, recipient_email, subject, body)

    receive_email(sender_email, sender_password)
