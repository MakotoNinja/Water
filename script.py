#!/usr/bin/env python

'''
 ' A plant watering Farmware
'''

import os, sys, json, Qualify
from random import randint
from farmware_tools import device, app, get_config_value
from Coordinate import Coordinate

PIN_LIGHTS = 7
PKG = 'Water Plants'

PLANT_TYPES = Qualify.get_csv(PKG, 'plant_types')
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
'''
device.log('PLANT_TYPES: {}'.format(json.dumps(PLANT_TYPES)))
all_plants = app.get_plants()
target_plants = [];
for plant in all_plants:
	plant_name = ''.join(plant['name'].split()).lower()
	device.log('plant_name: {}, PLANT_TYPES: {}'.format(plant_name, json.dumps(PLANT_TYPES))
	if plant_name in PLANT_TYPES:
		target_plants.append(plant)

if len(target_plants):
	print(json.dumps(target_plants))
else :
	device.log('No plants found with name: "{}"'.format(PLANT_TYPE))
	sys.exit()

device.write_pin(PIN_LIGHTS, 1, 0)
'''
#device.execute(tool_water_retrieve_sequence_id)
#bot = Coordinate(device.get_current_position('x'), device.get_current_position('y'), Z_TRANSLATE)
#bot.move_abs()

#device.execute(tool_water_return_sequence_id)

device.home('all')
device.write_pin(PIN_LIGHTS, 0, 0)
