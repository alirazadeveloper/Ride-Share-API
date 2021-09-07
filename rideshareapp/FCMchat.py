import firebase_admin
from firebase_admin import credentials, messaging
cred = credentials.Certificate(r"Rideshare-key.json")
firebase_admin.initialize_app(cred)
def sendPush(title, msg, registration_token, dataObject=None):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=msg
        ),
        data=dataObject,
        token=registration_token,
    )
    response = messaging.send(message)
    return response
        