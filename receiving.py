import tkinter as tk
from tkinter import messagebox,ttk
from plyer import notification
import imaplib
import email

def is_valid_email(email): #checking if email format is valid
    """
    Parameters:
        email (str): Email address to be validated.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    import re
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email) is not None

def process_email_body(message): # process email body and return text content.
    """ Parameters:
        message (email.message.Message): Email message object.

    Returns:
        str: Text content of the email body.
    """
    if message.is_multipart():
        #if msg is multipart, iterate through each part and process it
        body = ""
        for part in message.get_payload():
            charset = part.get_content_charset()
            if part.get_content_type() == "text/plain":
                body += part.get_payload(decode=True).decode(charset or 'utf-8')
    else:
        #if msg is not multipart, directly process body
        charset = message.get_content_charset()
        body = message.get_payload(decode=True).decode(charset or 'utf-8')
    return body

def receive_email(username, password):
    """
    Receive the latest email using IMAP protocol and print its body.

    Parameters:
        username (str): User's email username.
        password (str): User's email password.
    """
    try:
        #determining IMAP server 
        domain = username.split('@')[1]
        imap_servers = {   #we can add more email providers and their IMAP servers 
            'gmail.com': 'imap.gmail.com',
            'outlook.com': 'outlook.office365.com',
            'hotmail.com': 'smtp-mail.outlook.com',
            'icloud.com': 'smtp.mail.me.com',
            #'alexu.edu.eg': 'smtp.alexu.edu.eg',
           
        }
        if domain in imap_servers:
            imap_server = imap_servers[domain]
        else:
            messagebox.showerror("Error", "Unsupported email provider")
            return
        
         #connecting to IMAP server
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
            #print(email_message.get_payload())
            print(process_email_body(email_message))  #in my terminal

            #sending push notification
            notification.notify(
                title='New Email',
                message=f'From: {email_message["From"]}\nSubject: {email_message["Subject"]}',
                app_name='Email Client'
            )
    except Exception as e:
        messagebox.showerror("Error", f"Error occurred while receiving email: {e}")

def receive_email_gui():
    username = username_entry.get()
    password = password_entry.get()

    if not is_valid_email(username):
        messagebox.showerror("Error", "Invalid sender email format")
        return

    receive_email(username, password)

# GUI 
root = tk.Tk()
root.title("Receive Email")

#Stylinggg
root.configure(bg="#A1C398")
style = ttk.Style()
style.configure("TButton", background="#FA7070", foreground="black")
style.map("TButton", background=[('pressed', '#FA7070'), ('active', '#FA7070')])
style.configure("TEntry", background="#C6EBC5", foreground="black")
style.configure("TLabel", background="#A1C398", foreground="black")

#username
username_label = tk.Label(root, text="Username (Email Address):")
username_label.grid(row=0, column=0, padx=5, pady=5)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=5, pady=5)

#password
password_label = tk.Label(root, text="Password:")
password_label.grid(row=1, column=0, padx=5, pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

#receive Button
receive_button = tk.Button(root, text="Receive Email", command=receive_email_gui)
receive_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="we")

root.mainloop()