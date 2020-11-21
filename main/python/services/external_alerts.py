from flask import current_app
from flask_mail import Mail, Message


def alert_flood():
    try:
        mail_message = "A quien corresponda,\n\nSe le envia este mail dado que se ha detectado que en la próxima hora en Durazno se producirá una inundación.\nPor lo tanto se recomienda que evacúe a los ciudadanos.\n\nEquipo KitCentinela"
        sender = "kitcentinela@gmail.com"
        recipient = "vkunze6@gmail.com"
        subject = "INUNDACIÓN!!"
        send_email(mail_message, sender, recipient, subject)
        return "exito"
    except Exception as e:
        return "error: " + str(e)


def alert_rain():
    try:
        mail_message = "Querido vecino,\n\nSe le envia este mail para recordarle que envíe sus datos de lluvia al " \
                       "siguiente link: \n\nMuchas gracias, que tenga un buen día!\nEquipo KitCentinela :)"
        sender = "kitcentinela@gmail.com"
        recipient = "vkunze6@gmail.com"
        subject = "Recuerde colaborar con sus datos de lluvia!"
        send_email(mail_message, sender, recipient, subject)
        return "exito"
    except Exception as e:
        return "error: " + str(e)


def send_email(message, sender_email, recipient_email, subject):
    with current_app.app_context():
        mail = Mail(current_app)
        msg = Message(subject, sender=sender_email, recipients=[recipient_email])
        msg.body = message
        mail.send(msg)
        return "Sent"
