import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email:

    def send_email(self, email):
        # Configurar el remitente y las credenciales
        rem_email = 'ssierraoxxonv@gmail.com'
        rem_pass = 'qceo xvdw bwyc jtut'

        # Configurar el destinatario y el mensaje
        rec_email = email
        subj = 'Usuario bloqueado ABC jobs'
        txt_msg = 'Usuario fue bloqueado por 3 intentos fallidos en autenticación'

        try:
            # Iniciar una conexión SMTP con el servidor de correo
            servidor_smtp = smtplib.SMTP("smtp.gmail.com", 587)
            servidor_smtp.starttls()
            servidor_smtp.login(rem_email, rem_pass)

            # Crear el mensaje MIME
            msg = MIMEMultipart()
            msg["From"] = rem_email
            msg["To"] = rec_email
            msg["Subject"] = subj
            msg.attach(MIMEText(txt_msg, 'plain'))

            # Enviar el correo electrónico
            servidor_smtp.sendmail(rem_email, rec_email, msg.as_string())
            servidor_smtp.quit()
            print("Correo electrónico enviado correctamente")
        except Exception as e:
            print(f"Error al enviar el correo electrónico: {str(e)}")
