import tkinter as tk
from tkinter import messagebox
from plyer import notification
import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def is_valid_email(email):
    """
    Check if the email address is valid.

    Parameters:
        email (str): Email address to be validated.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    import re
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email) is not None

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
        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Add body to the email
        msg.attach(MIMEText(body, 'plain'))

        # Determine SMTP server based on sender's email domain
        domain = sender_email.split('@')[1]
        smtp_servers = {
            'gmail.com': 'smtp.gmail.com',
            'outlook.com': 'smtp-mail.outlook.com',
            'hotmail.com': 'smtp-mail.outlook.com',
            'icloud.com': 'smtp.mail.me.com',
            'alexu.edu.eg': 'smtp.alexu.edu.eg',
            # Add more email providers and their SMTP servers here
        }

        if domain in smtp_servers:
            smtp_server = smtp_servers[domain]
        else:
            messagebox.showerror("Error", "Unsupported email provider")
            return

        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print("Error occurred while sending email:", e)

def receive_email(username, password):
    """
    Receive the latest email using IMAP protocol and print its body.

    Parameters:
        username (str): User's email username.
        password (str): User's email password.
    """
    try:
        # Determine IMAP server based on username's email domain
        domain = username.split('@')[1]
        imap_servers = {
            'gmail.com': 'imap.gmail.com',
            'outlook.com': 'outlook.office365.com',
            'hotmail.com': 'smtp-mail.outlook.com',
            'icloud.com': 'smtp.mail.me.com',
            #'alexu.edu.eg': 'smtp.alexu.edu.eg',
            # Add more email providers and their IMAP servers here
        }

        if domain in imap_servers:
            imap_server = imap_servers[domain]
        else:
            messagebox.showerror("Error", "Unsupported email provider")
            return

        # Connect to the IMAP server
        with imaplib.IMAP4_SSL(imap_server) as mail:
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
            # Send push notification
            notification.notify(
                title='New Email',
                message=f'From: {email_message["From"]}\nSubject: {email_message["Subject"]}',
                app_name='Email Client'
            )
    except Exception as e:
        print("Error occurred while receiving email:", e)

def send_email_gui():
    sender_email = sender_email_entry.get()
    sender_password = sender_password_entry.get()
    recipient_email = recipient_email_entry.get()
    subject = subject_entry.get()
    body = body_entry.get('1.0', 'end-1c')

    # Validate email format
    if not is_valid_email(sender_email):
        messagebox.showerror("Error", "Invalid sender email format")
        return
    if not is_valid_email(recipient_email):
        messagebox.showerror("Error", "Invalid recipient email format")
        return

    # Validate password
    if len(sender_password) < 6:
        messagebox.showerror("Error", "Password must be at least 6 characters long")
        return

    send_email(sender_email, sender_password, recipient_email, subject, body)

def receive_email_gui():
    sender_email = sender_email_entry.get()
    sender_password = sender_password_entry.get()

    # Validate email format
    if not is_valid_email(sender_email):
        messagebox.showerror("Error", "Invalid sender email format")
        return

    # Validate password
    if len(sender_password) < 6:
        messagebox.showerror("Error", "Password must be at least 6 characters long")
        return

    receive_email(sender_email, sender_password)

# GUI setup
root = tk.Tk()
root.title("Email Client")

# Sender Email
sender_email_label = tk.Label(root, text="Sender Email:")
sender_email_label.grid(row=0, column=0, padx=5, pady=5)
sender_email_entry = tk.Entry(root)
sender_email_entry.grid(row=0, column=1, padx=5, pady=5)

# Sender Password
sender_password_label = tk.Label(root, text="Sender Password:")
sender_password_label.grid(row=1, column=0, padx=5, pady=5)
sender_password_entry = tk.Entry(root, show="*")
sender_password_entry.grid(row=1, column=1, padx=5, pady=5)

# Recipient Email
recipient_email_label = tk.Label(root, text="Recipient Email:")
recipient_email_label.grid(row=2, column=0, padx=5, pady=5)
recipient_email_entry = tk.Entry(root)
recipient_email_entry.grid(row=2, column=1, padx=5, pady=5)

# Subject
subject_label = tk.Label(root, text="Subject:")
subject_label.grid(row=3, column=0, padx=5, pady=5)
subject_entry = tk.Entry(root)
subject_entry.grid(row=3, column=1, padx=5, pady=5)

# Body
body_label = tk.Label(root, text="Body:")
body_label.grid(row=4, column=0, padx=5, pady=5)
body_entry = tk.Text(root, height=5, width=30)
body_entry.grid(row=4, column=1, padx=5, pady=5)

# Send Button
send_button = tk.Button(root, text="Send Email", command=send_email_gui)
send_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="we")

# Receive Button
receive_button = tk.Button(root, text="Receive Email", command=receive_email_gui)
receive_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="we")

root.mainloop()
