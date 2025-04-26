# Program Title: Agile Raspberry Pi Plant Moisture Sensor with Email Notification
# Program Description: Regularly check the moisture status of plants and send out email notifications based on the detection results.
# Name: Yao Yao
# Student ID: 202283890009
# Course & Year: Project Semester 3
# Date: 20/4/25

#!/usr/bin/python
import RPi.GPIO as GPIO
import smtplib
from email.message import EmailMessage
import time
from datetime import datetime, timedelta

# Setup for GPIO and sensor
channel = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
    if GPIO.input(channel):
        return "No Water Detected! Please water your plant."
    else:
        return "Water Detected! Water NOT needed."

def send_email(status):
    # Set the sender email and password and recipient email
    from_email_addr = "3389632376@qq.com"  # My QQ email address
    from_email_pass = "yjihuwitupbbdacg"  # My QQ email app password
    to_email_addr = "3389632376@qq.com"  # Recipient's email address

    # Create a message object
    msg = EmailMessage()

    # Set the email body
    body = f"Plant status: {status}"
    msg.set_content(body)

    # Set sender and recipient
    msg['From'] = from_email_addr
    msg['To'] = to_email_addr

    # Set your email subject
    msg['Subject'] = 'Detection of Plant Soil Moisture'

    # Connecting to server and sending email
    server = smtplib.SMTP('smtp.qq.com', 587)
    server.starttls()

    # Login to the SMTP server
    server.login(from_email_addr, from_email_pass)

    # Send the message
    server.send_message(msg)
    print('Email sent')

    # Disconnect from the Server
    server.quit()

def record_log(status):
    with open("email_log.txt", "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp} - Plant status: {status}\n")

def main():
    current_time = datetime.now()
    today = current_time.date()

    # Define the scheduled times in 24-hour format
    scheduled_times = [datetime.combine(today, datetime.strptime(t, "%H").time()) for t in ["08", "10", "12", "14"]]

    # Find the next scheduled time that is greater than the current time
    next_check_time = min([t for t in scheduled_times if t > current_time], default=None)

    if next_check_time is None:
        # If all scheduled times have passed for today, set it to the first time of the next day
        next_check_time = datetime.combine(today + timedelta(days=1), datetime.strptime("08", "%H").time())

    while True:
        sleep_duration = (next_check_time - datetime.now()).total_seconds()
        if sleep_duration > 0:
            time.sleep(sleep_duration)

        status = callback(channel)
        send_email(status)
        record_log(status)

        # Calculate the next scheduled time for the same day or the next day if necessary
        today = datetime.now().date()
        scheduled_times_today = [datetime.combine(today, datetime.strptime(t, "%H").time()) for t in ["08", "10", "12", "14"]]
        future_times = [t for t in scheduled_times_today if t > datetime.now()]

        if future_times:
            next_check_time = min(future_times)
        else:
            # If no more scheduled times left for today, set it to the first time of the next day
            next_check_time = datetime.combine(today + timedelta(days=1), datetime.strptime("08", "%H").time())

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
