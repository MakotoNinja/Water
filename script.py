#!/usr/bin/env python

'''
 ' A farmware for a custom tool for Farmbot
'''

import os, sys, json, Qualify
from random import randint
from farmware_tools import device, app, get_config_value
from Coordinate import Coordinate

def bite():
	for i in range(3):
		device.set_servo_angle(SERVO_PIN, HOLE_OPEN_ANGLE)
		device.wait(100)
		device.set_servo_angle(SERVO_PIN, HOLE_CLOSE_ANGLE)
		device.wait(100)

def chomp():
	for i in range(NUM_BITES):
		device.log('Pass {} of {}'.format(i+1, NUM_BITES))
		device.set_servo_angle(SERVO_PIN, HOLE_OPEN_ANGLE)						# open mouth
		bot.set_axis_position('z', BED_HEIGHT - (i * BITE_ADVANCE))				# move down to bed
		bite()																	# bite!
		bot.set_axis_position('z', BED_HEIGHT + BITE_RETRACT)					# retract from hole
		bot.set_offset_axis_position(DUMP_OFFSET['axis'], DUMP_OFFSET['value'])	# offset to dump soil
		device.set_servo_angle(SERVO_PIN, HOLE_OPEN_ANGLE)						# dump soil
		device.wait(BITE_TIMEOUT)												# give time for dump to finish
		bot.set_offset_axis_position(DUMP_OFFSET['axis'], 0)					# reposition over hole

def deploy():
	for plant in target_plants:
		device.set_servo_angle(SERVO_PIN, PLANT_OPEN_ANGLE)						# open mouth
		bot.set_axis_position('z', Z_TRANSLATE)									# move to translate height
		bot.set_offset(0, 0, 0, move_abs=False)									# reset offset if any
		bot.set_coordinate(PLANT_STAGE['x'], PLANT_STAGE['y'])					# move above plant stage
		bot.set_axis_position('z', PLANT_STAGE['z'])							# move down to plant stage
		device.set_servo_angle(SERVO_PIN, PLANT_CLOSE_ANGLE)					# bite down on plant
		bot.set_axis_position('z', Z_TRANSLATE)									# move to translate height
		bot.set_coordinate(plant['x'], plant['y'])								# move above current plant
		bot.set_axis_position('z', BED_HEIGHT - (BITE_ADVANCE * NUM_BITES - 2))	# lower into hole
		device.set_servo_angle(SERVO_PIN, HOLE_OPEN_ANGLE)						# drop payload
		bot.set_axis_position('z', BED_HEIGHT + BITE_RETRACT)
		device.set_servo_angle(SERVO_PIN, HOLE_CLOSE_ANGLE)
		bot.set_offset(x=INFILL_RADIUS)
		bot.set_axis_position('z', BED_HEIGHT)
		for i in range(NUM_BITES):
			r = INFILL_RADIUS-(i*BITE_ADVANCE)
			bot.set_offset(x=r, y=r)
			bot.set_offset(x=-r, y=r)
			bot.set_offset(x=-r, y=-r)
			bot.set_offset(x=r, y=-r)
			bot.set_offset(x=r, y=0)
		bot.set_axis_position('z', Z_TRANSLATE)									# move to translate height

PIN_LIGHTS = 7
PKG = 'Audrey II'

SERVO_PIN = Qualify.integer(PKG, 'servo_pin')
HOLE_OPEN_ANGLE = Qualify.integer(PKG, 'hole_open_angle')
HOLE_CLOSE_ANGLE = Qualify.integer(PKG, 'hole_close_angle')
PLANT_OPEN_ANGLE = Qualify.integer(PKG, 'plant_open_angle')
PLANT_CLOSE_ANGLE = Qualify.integer(PKG, 'plant_close_angle')
PLANT_TYPE = get_config_value(PKG, 'plant_type', str).lower()
Z_TRANSLATE = Qualify.integer(PKG, 'z_translate')
BED_HEIGHT = Qualify.integer(PKG, 'bed_height')
NUM_BITES = Qualify.integer(PKG, 'num_bites')
BITE_ADVANCE = Qualify.integer(PKG, 'bite_advance')
BITE_RETRACT = Qualify.integer(PKG, 'bite_retract')
BITE_TIMEOUT = Qualify.integer(PKG, 'bite_timeout')
DUMP_OFFSET = Qualify.combo(PKG, 'dump_offset')
INFILL_RADIUS = Qualify.integer(PKG, 'infill_radius')
PLANT_STAGE_ID = Qualify.integer(PKG, 'plant_stage_id')
PLANT_STAGE = Qualify.get_tool(PLANT_STAGE_ID)

audrey_retrieve_sequence_id = Qualify.sequence(PKG, 'audrey_retrieve')
audrey_return_sequence_id = Qualify.sequence(PKG, 'audrey_return')

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

device.write_pin(PIN_LIGHTS, 1, 0)

device.execute(audrey_retrieve_sequence_id)
bot = Coordinate(device.get_current_position('x'), device.get_current_position('y'), Z_TRANSLATE)
bot.move_abs()
for site in target_plants:
	bot.set_coordinate(site['x'], site['y'], Z_TRANSLATE)
	bot.move_abs()
	chomp()
	bot.set_axis_position('z', Z_TRANSLATE)
	bot.move_abs()

deploy()
device.set_servo_angle(SERVO_PIN, HOLE_CLOSE_ANGLE)
device.execute(audrey_return_sequence_id)

device.home('all')
device.write_pin(PIN_LIGHTS, 0, 0)
