git add --all
git commit -m "commit ultimul"
git push origin main
git push heroku main
heroku ps:restart
heroku logs
