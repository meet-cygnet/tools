#
#

import smtplib
import ssl
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587  # or 465 for SSL
USERNAME = "your_email@example.com"
PASSWORD = "your_password"
TO_EMAIL = "recipient@example.com"

def send_email():
    try:
        # Email content
        msg = MIMEMultipart()
        msg["From"] = USERNAME
        msg["To"] = TO_EMAIL
        msg["Subject"] = "Test Email"
        msg.attach(MIMEText("Hello, this is a test email.", "plain"))

        # Connection
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            print("[INFO] Connecting to server...")
            server.ehlo()

            if SMTP_PORT == 587:
                print("[INFO] Starting TLS...")
                server.starttls(context=context)
                server.ehlo()

            print("[INFO] Logging in...")
            server.login(USERNAME, PASSWORD)

            print("[INFO] Sending email...")
            server.sendmail(USERNAME, TO_EMAIL, msg.as_string())

        print("[SUCCESS] Email sent successfully.")

    except smtplib.SMTPAuthenticationError as e:
        print("[ERROR] Authentication failed:", e.smtp_error.decode() if e.smtp_error else e)
    except smtplib.SMTPConnectError as e:
        print("[ERROR] Connection failed:", e)
    except smtplib.SMTPServerDisconnected as e:
        print("[ERROR] Server unexpectedly disconnected:", e)
    except smtplib.SMTPResponseException as e:
        print(f"[ERROR] SMTP error code {e.smtp_code}: {e.smtp_error.decode() if e.smtp_error else e}")
    except smtplib.SMTPSenderRefused as e:
        print(f"[ERROR] Sender refused: {e}")
    except smtplib.SMTPRecipientsRefused as e:
        print(f"[ERROR] Recipient refused: {e}")
    except smtplib.SMTPDataError as e:
        print(f"[ERROR] SMTP data error: {e}")
    except smtplib.SMTPHeloError as e:
        print(f"[ERROR] HELO failed: {e}")
    except socket.gaierror as e:
        print(f"[ERROR] Network/DNS issue: {e}")
    except socket.timeout as e:
        print(f"[ERROR] Network timeout: {e}")
    except ConnectionRefusedError as e:
        print(f"[ERROR] Connection refused (possible firewall): {e}")
    except ssl.SSLError as e:
        print(f"[ERROR] SSL/TLS error: {e}")
    except Exception as e:
        print(f"[ERROR] Unknown error occurred: {e}")

if __name__ == "__main__":
    send_email()
