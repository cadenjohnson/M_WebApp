

Start virtual environment via 
--------------------------------*******************************************************************************************************************
.\M_env\Scripts\activate

run app via
------------------------
python main.py




Setting up Heroku hosting on the cloud
-----------------------------------------
install heroku cli
install git (obviously)
install gunicorn
freeze requirements
git init
git add .
git commit -m "Innit app"
heroku login
heroku create ----------
https://mckrakenwebapp.herokuapp.com/
https://git.heroku.com/mckrakenwebapp.git
git push heroku master
----should be created, but forgot procfile

------to update and commit to heroku------ ********************************************************************************************************
git add .
git commit -m "added procfile"
git push heroku master


-----------View Heroku Logs---------------
heroku logs --tail
-----------View Heroku Dynos--------------
heroku ps




update database via
-----------------------
flask db migrate
or
flask db upgrade     ?



Please update me thx



to update and backup to github
go to source control
--------------------------------*******************************************************************************************************************
commit changes
pull/push --> Push to...
choose the right repo
you good dawg




recources:
https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

https://flask-login.readthedocs.io/en/latest/

https://www.youtube.com/watch?v=uNmWxvvyBGU

https://www.youtube.com/watch?v=2dEM-s3mRLE

https://www.youtube.com/watch?v=8d2KfERrb5Q

https://www.youtube.com/watch?v=pjVhrIJFUEs

https://getbootstrap.com/docs/4.0/components/navbar/

https://github.com/cadenjohnson/M_WebApp

https://www.sachinsf.com/how-to-push-the-code-from-vs-code-to-github/#:~:text=Step%201%3A%20Open%20your%20Github,(optional)%20for%20the%20repository.




integrate Spotify auth and simple request/display of playlists

update blog to accept posts (make blog post form on new template (new, update, delete))

add more models/blueprints (calendar, weather, then maybe spotify)

implement flask security

add remember me to login

add admin portal to see all users, add, remove, etc
    view number of accounts
        view all accounts listed username - name - email
    delete accounts
    update accounts
    view number of tasks for each account

add mock billing page

update DB tables to have many to one / many to many relationships

Design key goals
-functionalities/capabilities
-what data i want available
-how to summarize data for dashboard


VULNERABILITIES
passwords in plain text
