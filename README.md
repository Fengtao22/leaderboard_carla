This repo is obtained from leaderboard-2.0 and we focus on carla version 0.9.14

To run the data collection:

* First, start the carla simulator by: 
/*sh CarlaUE4.sh -RenderOffScreen*/ here "RenderOffScreen" works for remote server  
* run the test_run.sh file by:
/*sh test_run.sh */ In this bash file, I select feng.py as the agent for ego car and the data saving process is conducted within feng.py
## Things to do:
1. modify feng.py in the autoagents folder