import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ✅ Updated scopes for both reading and sending
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def get_latest_email():
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', maxResults=1, labelIds=['INBOX']).execute()
    message = results.get('messages', [])[0]
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    return msg['snippet']

def search_emails_by_query(query):
    service = get_gmail_service()
    response = service.users().messages().list(userId='me', q=query, maxResults=5).execute()
    messages = response.get('messages', [])
    results = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['Subject', 'Date']).execute()
        headers = {h['name']: h['value'] for h in msg_data['payload']['headers']}
        snippet = msg_data['snippet']
        results.append({
            'subject': headers.get('Subject', 'No Subject'),
            'date': headers.get('Date', 'No Date'),
            'snippet': snippet
        })
    return results

def send_email(recipient, subject, body):
    service = get_gmail_service()
    message_text = f"To: {recipient}\nSubject: {subject}\n\n{body}"
    message = {
        'raw': base64.urlsafe_b64encode(message_text.encode("utf-8")).decode("utf-8")
    }
    try:
        send_result = service.users().messages().send(userId='me', body=message).execute()
        return send_result
    except Exception as e:
        return f"Error sending email: {e}"

if __name__ == '__main__':
    print(get_latest_email())
