# Chat-Server
This is a Python based TCP Server.
>>Module used --> socket, threading and sys.

>>It has 2 modes:

1.) Online mode: For communicating between two different machine around the globe.
2.) Offline mode: For communicating within the same machine (localhost).

>>How to set-up the Server ?

Step 1.) Run Server.puy

Step 2.) Choose Online or Offline mode as per your use.

Step 3.) Create a Admin name and password (for master control login in future).

Step 4.) Note the IPV4 address given by the program.

Step 5.) In Client.py fill the IPV4 address (the one given by Server.py) in string variable named "host".

Step 6.) Run Client.py and Choose a nickname.

You are all done. Enjoy!

[ Note: To Login as admin you have to enter the admin name (you created while setting up the server) as "//admin_name" i.e. using double forward slash. Then enter password.
All commands are given using double forward slash like : //kick and //clients.]
