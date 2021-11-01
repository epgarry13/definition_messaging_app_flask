
To set up environment:

python3 -m venv venv 
source venv/bin/activate
pip install -r requirements.txt

-----------------------
Make sure to include serviceAccountKey.json in root.

To deploy to heroku:

Login with credentials.

git add .
git commit -am "commit message"
git push heroku master
git ps:scale web=1
heroku logs --tail (to check if deployed, should say the app is "Up" and not "Crashed").

