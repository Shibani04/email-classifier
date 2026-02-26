import imapclient
import email
from email.header import decode_header

def fetch_emails(host, username, password, num_emails=10):
    emails = []
    
    try:
        # Connect to email server
        client = imapclient.IMAPClient(host, ssl=True)
        client.login(username, password)
        client.select_folder('INBOX')
        
        # Fetch latest emails
        messages = client.search(['ALL'])
        latest = messages[-num_emails:]
        
        for uid in latest:
            raw = client.fetch([uid], ['RFC822'])
            msg = email.message_from_bytes(raw[uid][b'RFC822'])
            
            # Decode subject
            subject = decode_header(msg['subject'])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode(errors='ignore')
            
            # Extract body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(errors='ignore')
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors='ignore')
            
            emails.append({
                "from": msg.get("from", "Unknown"),
                "subject": subject or "No Subject",
                "body": body[:500]
            })
        
        client.logout()
        
    except Exception as e:
        print(f"Error: {e}")
    
    return emails