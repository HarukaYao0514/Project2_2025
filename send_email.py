# Name: Yao Yao
# Student ID: 202283890009
# Date: 20/4/25

import smtplib
from email.message import EmailMessage

# Set the sender email and password and recipient email
from_email_addr = "3389632376@qq.com"  # My QQ email address
from_email_pass = "yjihuwitupbbdacg"  # My QQ email app password
to_email_addr = "3389632376@qq.com"  # My QQ email address

# Create a message object
msg = EmailMessage()

# Set the email body
body = "Hello from Raspberry Pi"
msg.set_content(body)

# Set sender and recipient
msg['From'] = from_email_addr
msg['To'] = to_email_addr

# Set your email subject
msg['Subject'] = 'TEST EMAIL'

# Connecting to server and sending email
server = smtplib.SMTP('smtp.qq.com',587)

# Enable TLS encryption
server.starttls()

# Login to the SMTP server
server.login(from_email_addr, from_email_pass)

# Send the message
server.send_message(msg)

print('Email sent')

# Disconnect from the Server
server.quit()
