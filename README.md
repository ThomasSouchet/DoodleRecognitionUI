# DoodleRecognitionUI
Doodle Recognition UI

# Git commands to intialize and create repo on GitHub:

- git init
- gh repo create
- git remote -v
- git add .
- git commit -m "Initial commit"
- git push origin master

# Heroku commands to build UI and deploy it on Heroku

- heroku login
- *optional:* heroku apps:destroy --app=doodle-recognition --confirm doodle-recognition
- *optional:* heroku create doodle-recognition --region eu
- git push heroku master
- *Start the application on Heroku:* heroku ps:scale web=1
- *Stop the application on Heroku:* heroku ps:scale web=0
