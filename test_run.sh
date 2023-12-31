export CARLA_ROOT=$CARLA_ROOT/home/volvo/Desktop/CARLA/CARLA_Leaderboard_20 
export SCENARIO_RUNNER_ROOT=$SCENARIO_RUNNER_ROOT/home/volvo/Desktop/CARLA/scenario_runner
export LEADERBOARD_ROOT=$LEADERBOARD_ROOT/home/volvo/Desktop/CARLA/leaderboard
export PYTHONPATH="${CARLA_ROOT}/PythonAPI/carla/":"${SCENARIO_RUNNER_ROOT}":"${LEADERBOARD_ROOT}":"${CARLA_ROOT}/PythonAPI/carla/dist/carla-0.9.14-py3.7-linux-x86_64.egg":${PYTHONPATH}


# export SCENARIOS=${LEADERBOARD_ROOT}/data/all_towns_traffic_scenarios_public.json  ### maybe the new version wra
# Parameterization settings. These will be explained in 2.2. Now simply copy them to run the test.
export ROUTES=${LEADERBOARD_ROOT}/data/routes_validation.xml  #routes_devtest.xml
export REPETITIONS=1 
export DEBUG_CHALLENGE=1
export CHECKPOINT_ENDPOINT=${LEADERBOARD_ROOT}/results.json
#export TEAM_AGENT=${LEADERBOARD_ROOT}/leaderboard/autoagents/team_code/sensor_agent.py #feng.py #human_agent.py
#export TEAM_CONFIG=/home/volvo/Desktop/CARLA/carla_garage/pretrained_models/leaderboard/tfpp_wp_all_0

#export TEAM_AGENT=${LEADERBOARD_ROOT}/leaderboard/autoagents/bradyz/auto_pilot.py

export TEAM_AGENT=${LEADERBOARD_ROOT}/team_code/image_agent.py
export TEAM_CONFIG=${LEADERBOARD_ROOT}/team_code/epoch=24.ckpt
export HAS_DISPLAY=1  

export SAVE_PATH=${LEADERBOARD_ROOT}/leaderboard/myEval
export CHALLENGE_TRACK_CODENAME=SENSORS  ##MAP

./scripts/run_evaluation.sh




