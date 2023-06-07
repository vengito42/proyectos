import email.utils
from email.mime.text import MIMEText

SENDER = < CORREO DEL AUTOR >
PASSWORD = < PASSWORD DE SEGURIDAD DEL CORREO >
toList = < LISTA DE CORREOS DESTINATARIOS >


# Create the message

def createEmail(subject, body, author, destination):
    msg = MIMEText(body)
    msg['To'] = email.utils.formataddr(('', str(destination).replace('[', '').replace(']', '').replace("'", '')))
    msg['From'] = email.utils.formataddr((subject, author))
    msg['Subject'] = subject
    return msg


# Inicializando y enviando el correo
import smtplib


def sendMail(msg, sender):
    conection = smtplib.SMTP_SSL(host='smtp.gmail.com')
    conection.login(user=sender, password=PASSWORD)
    conection.sendmail(sender, toList, msg.as_string())
    conection.quit()


msg = createEmail('Email de prueba', 'Este es el cuerpo del correo', SENDER, toList)
sendMail(msg)
