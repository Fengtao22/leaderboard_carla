#!/usr/bin/env python

# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""
This module provides a dummy agent to control the ego vehicle
"""

from __future__ import print_function

import carla

from leaderboard.autoagents.autonomous_agent import AutonomousAgent, Track
import pygame ### to display current window

from leaderboard.autoagents.human_agent import HumanInterface 
from srunner.scenariomanager.carla_data_provider import CarlaDataProvider
import os.path
import json 

def get_entry_point():
    return 'feng'

class feng(AutonomousAgent):

    """
    Dummy autonomous agent to control the ego vehicle
    """

    def setup(self, path_to_conf_file):
        """
        Setup the agent parameters
        """
        self.track = Track.SENSORS #MAP

        self.camera_width = 1280
        self.camera_height = 720
        self._side_scale = 0.3
        self._left_mirror = False
        self._right_mirror = False

        self._hic = HumanInterface(
            self.camera_width,
            self.camera_height,
            self._side_scale,
            self._left_mirror,
            self._right_mirror
        )
        self._prev_timestamp = 0
        self._clock = pygame.time.Clock()

    def sensors(self):
        """
        Define the sensor suite required by the agent

        :return: a list containing the required sensors in the following format:

        [
            {'type': 'sensor.camera.rgb', 'x': 0.7, 'y': -0.4, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0,
                      'width': 300, 'height': 200, 'fov': 100, 'id': 'Left'},

            {'type': 'sensor.camera.rgb', 'x': 0.7, 'y': 0.4, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0,
                      'width': 300, 'height': 200, 'fov': 100, 'id': 'Right'},

            {'type': 'sensor.lidar.ray_cast', 'x': 0.7, 'y': 0.0, 'z': 1.60, 'yaw': 0.0, 'pitch': 0.0, 'roll': 0.0,
             'id': 'LIDAR'}
        ]
        """

        sensors = [
            {'type': 'sensor.camera.rgb', 'x': 0.7, 'y': 0.0, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0,
             'width': 800, 'height': 600, 'fov': 100, 'id': 'Center'},
        ]  ## {'type': 'sensor.opendrive_map', 'reading_frequency': 1, 'id': 'OpenDRIVE'}

        return sensors

    def run_step(self, input_data, timestamp):
        """
        Execute one step of navigation.
        """
        self._clock.tick_busy_loop(20)  ### pygame frequency
        self._hic.run_interface(input_data)  ## for visulizing purpose comme
        ###########################################################################
        ##### insert autopilot function here to get a smart control action ########
        ###########################################################################
        actor_list = CarlaDataProvider.get_world().get_actors().filter('vehicle.*') ### include cars and bikes
        walker_list = CarlaDataProvider.get_world().get_actors().filter('walker.*') ### pedestrians 
        print('vehicle number: ', len(actor_list))  ### parked cars are not included!!!! To do
        print('walker number: ', len(walker_list))
        print('type of the actor: ', type(actor_list[0]))


        #### continuing writing to json file
        current_timestamp = CarlaDataProvider.get_world().get_snapshot().timestamp
        frame_ = current_timestamp.frame
        lane_num = 4 ## To do
        intent = 'unknown'

        agent_dic = {}
        for i, actor in enumerate(actor_list):
            agent_id = actor.id
            agent_type = actor.type_id #'kEgoVehicle'
            x, y, z = actor.get_location().x, actor.get_location().y, actor.get_location().z
            ax, ay, az = actor.get_acceleration().x, actor.get_acceleration().y, actor.get_acceleration().z
            agent_dic[i] = {'agent_id': agent_id, 'agent_type_class': agent_type, 'agent_speed': (x, y, z), 'agent_acceleration': (ax,ay,az), 'agent_intent': intent}

        for j, actor in enumerate(walker_list):
            agent_id = actor.id
            agent_type = actor.type_id #'kEgoVehicle'
            x, y, z = actor.get_location().x, actor.get_location().y, actor.get_location().z
            ax, ay, az = actor.get_acceleration().x, actor.get_acceleration().y, actor.get_acceleration().z
            agent_dic[i+j] = {'agent_id': agent_id, 'agent_type_class': agent_type, 'agent_speed': (x, y, z), 'agent_acceleration': (ax,ay,az), 'agent_intent': intent}

        frame_details ={ 
            "info" : {'timestamp': timestamp, 'sequence_number': frame_}, 
            "agents": agent_dic, 
            "map": {'num_drivable_lanes': lane_num} 
        } 
            
        # Convert and write JSON object to file
        if os.path.isfile('sample.json'):
            with open("sample.json", "a") as outfile: 
                json.dump(frame_details, outfile)
        else:    
            with open("sample.json", "w") as outfile: 
                json.dump(frame_details, outfile)


        for actor in actor_list:
            print(actor)
        print("=====================>")
        for key, val in input_data.items():
            if hasattr(val[1], 'shape'):
                shape = val[1].shape
                print("[{} -- {:06d}] with shape {}".format(key, val[0], shape))
            else:
                print("[{} -- {:06d}] ".format(key, val[0]))
        print("<=====================")

        # DO SOMETHING SMART

        # RETURN CONTROL
        control = carla.VehicleControl()
        control.steer = 0.0
        control.throttle = 0.0
        control.brake = 0.0
        control.hand_brake = False
        ###########################################################################

        self._prev_timestamp = timestamp
        return control
