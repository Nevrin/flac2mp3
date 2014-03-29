#!/usr/bin/env python3
#
#  flac2mp3.py
#  
#  Copyright 2014 Jakub Tauchman <j.tauchman@email.cz>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

"""converts folder with flacs to mp3s

arguments:
Arguments can be listed with running script with -h
./flac2mp3.py -h
"""

import argparse
import re
import os
import tempfile
import subprocess
import pprint


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='flac2mp3')
	parser.add_argument('folder', help="folder with flacs to convert")
	args = parser.parse_args()
	
	work_dir = args.folder
	
	try:
		os.mkdir(str(work_dir) + "/flac2mp3_converted")
	except FileExistsError:
		pass
		print("Converted folder exists, yet coverted?")
		#exit(1)
		
	pprint.pprint(sorted(os.listdir(work_dir)))
	
	
	


