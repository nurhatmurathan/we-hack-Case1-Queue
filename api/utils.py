import requests


def send_email(emails):
    url = 'https://us-central1-carbon-zone-417117.cloudfunctions.net/mail-sender'
    data = {
        "html_content": "<h1>Your HTML Content Here</h1>",
        "heading": "Your Email Subject",
        "emails": emails
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=data, headers=headers)

    return response
