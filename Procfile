web: gunicorn app:app --log-file=-

beat: celery -A tasks beat --loglevel=info
worker: celery -A tasks worker

# to start:
# heroku ps:scale worker=1
# heroku ps:scale beat=1

# to stop:
# heroku ps:scale worker=0
# heroku ps:scale beat=0