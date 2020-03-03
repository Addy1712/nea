import smtplib, ssl
password = input("Type your password and press enter: ")
while True:
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "ad17ha12@gmail.com"  # Enter your address
    receiver_email = "018433@durhamsixthformcentre.org.uk"  # Enter receiver address
    message = """\
    Subject: PYTHON

    This message is sent from dsfc"""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

