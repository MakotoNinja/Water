#!/usr/bin/env python

'''
 ' A farmware for a custom tool for Farmbot
'''

import os, sys, json, Qualify
from random import randint
from farmware_tools import device, app, get_config_value
from Coordinate import Coordinate

PIN_LIGHTS = 7
PKG = 'Water Plants'

PLANT_TYPE = get_config_value(PKG, 'plant_type', str).lower()
TRANSLATE_HMEIGHT = Qualify.integer(PKG, 'translate_height')
WATER_HEIGHT = Qualify.integer(PKG, 'water_height')

tool_water_retrieve_sequence_id = Qualify.sequence(PKG, 'tool_water_retrieve')
tool_water_return_sequence_id = Qualify.sequence(PKG, 'tool_water_return')

if len(Qualify.errors):
	for err in Qualify.errors:
		device.log(err, 'error', ['toast'])
	sys.exit()
else:
	device.log('No config errors detected')

all_plants = app.get_plants()
target_plants = [];
for plant in all_plants:
	if plant['name'].lower() == PLANT_TYPE:
		target_plants.append(plant)

if not len(target_plants):
	device.log('No plants found with name: "{}"'.format(PLANT_TYPE))
	sys.exit()
else :
	print(json.dumps(target_plants))

device.write_pin(PIN_LIGHTS, 1, 0)

#device.execute(tool_water_retrieve_sequence_id)
#bot = Coordinate(device.get_current_position('x'), device.get_current_position('y'), Z_TRANSLATE)
#bot.move_abs()

#device.execute(tool_water_return_sequence_id)

device.home('all')
device.write_pin(PIN_LIGHTS, 0, 0)
