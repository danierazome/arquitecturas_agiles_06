import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError


class Email:

    SCOPES = [
        "https://www.googleapis.com/auth/gmail.send"
    ]
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    service = build('gmail', 'v1', credentials=creds)

    def send_email(self, email):
        message = MIMEText(
            'Usuario fue bloqueado por 3 intentos fallidos en autenticación')
        message['subject'] = 'Usuario bloqueado ABC jobs'
        message['to'] = email

        create_message = {'raw': base64.urlsafe_b64encode(
            message.as_bytes()).decode()}

        try:
            message = (self.service.users().messages().send(
                userId="me", body=create_message).execute())
            print("Mensaje enviado")
        except HTTPError as error:
            print(F'An error occurred: {error}')
