
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

deviceToken = "device token"
content = "custom content"

firebase_admin.initialize_app(
    credentials.Certificate('serviceAccountKey.json'))

registration_token = deviceToken

_apsAlert = messaging.ApsAlert(
    title='New message',
    body=json.dumps(content))

_aps = messaging.Aps(
    alert=_apsAlert,
    sound="default",
    badge=1,
    mutable_content=True,
    available=True)

_apsPayload = messaging. APNSPayload(aps=_aps)

_apns = messaging.APNSConfig(payload=_apsPayload)

message = messaging.Message(
    data = {
        'content': json.dumps(content),
    }, token=registration_token, apns=_apns,
)

response = messaging. send(message)
