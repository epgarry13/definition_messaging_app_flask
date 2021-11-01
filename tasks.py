from flask.wrappers import Response
from celery import Celery
from celery.schedules import crontab
from time import sleep
from datatime import datetime, timedelta
from twilio.rest import Client
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

# TODO fill in twilio account info (os.environ)
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

app = Celery(
    'tasks', broker='amqps://bxrbsdmw:aFoX583lcV6MqY0Xh_Tevg2YPA-pEbOS@fish.rmq.cloudamqp.com/bxrbsdmw')

# Firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
requests_ref = db.collection('requests')


@app.task()
def reminder():

    # query database for requests in that have not been followed up
    requests = requests_ref.where(u'follow_up', u'==', False).stream()

    for request in requests:

        # Send follow-up
        resp_message = "Hey don't forget! %s means %s." % (
            request['word'], request['definition'])

        # TODO Fill in phone number
        message = client.messages.create(
            body=resp_message,
            from_='FILL THIS IN',
            to=request['phone_number']
        )

        # Make request as followed-up
        request['follow_up'] = True
        requests_ref.document(request['id']).update(request)

    return "Reminders sent."


# Scheduled to run job everyday at 11:00am (I think haha)
app.conf.beat_schedule = {
    'add-every-day': {
        'task': 'tasks.add',
        'schedule': crontab(minute=0, hour=11)
    }
}
