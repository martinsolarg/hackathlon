How to run; 
````
From parernt directory of /server/ :
$ export FLASK_APP=server/run_server.py
$ flask run
 * Running on http://127.0.0.1:5000/
 ````
 
 Initialize DB (removes all data)
 
 ````
curl -X POST  http://127.0.0.1:5000/init_db
````
 
 Creating a user
 
 ````
 curl -X POST  http://127.0.0.1:5000/create_user -d '{"id": "<user_id>"  ,"name": "<nickname>"}' -H 'Content-Type: application/json'
 ````
 Requesting for all users
 ````
curl -X GET  http://127.0.0.1:5000/get_users
````
Call bot 

 ````
curl -X GET  http://127.0.0.1:5000/coach <text>
using bot coach (outgoing webhook)
enroll - enroll tournament 
leave - leave tournament
give - wait for a quick game
help - print help
````
