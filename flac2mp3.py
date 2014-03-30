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

"""converts folder with flacs to mp3s perserving ID3 tags

Script creates new folder with transcoded mp3s in argumented folder.
Works on UNIX using flac and lame. Deconding and encoding works
in paralel.

arguments:
Arguments can be listed with running script with -h
./flac2mp3.py -h
"""

import argparse
import os
import tempfile
import subprocess


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='flac2mp3')
	
	parser.add_argument('input_folder', help="folder with flacs to convert")
	parser.add_argument('output_folder', help="folder with output mp3s")
	parser.add_argument('-p', type=int, default=2, help="number of paralel processes")
	parser.add_argument('-a', type=int, default=256, help="value of ABR")
	
	args = parser.parse_args()
	
	work_dir = args.input_folder
	out_dir = str(os.path.abspath(args.output_folder))
		
	flacs2con = []
	for file_in_dir in sorted(os.listdir(work_dir)):
		if file_in_dir.endswith(".flac"):
			flacs2con.append(file_in_dir)
	
	with tempfile.TemporaryDirectory() as tmpdir:
		os.chdir(tmpdir)
		FNULL = open('/dev/null', 'w')
		
		proc_list = list()
		
		#decode flacs to wavs
		for flac_file in flacs2con:
			
			f_name = flac_file.rsplit('.',1)[0]
			id3_file = f_name + '.id3'
			wav_file = f_name + '.wav'
			
			#extract metadata for id3 tags
			id3_p = subprocess.Popen(['metaflac', "--export-tags-to={0}".format(id3_file), work_dir + flac_file], stdout=FNULL, stderr=FNULL)
			#decode flacs to wavs
			flac_p = subprocess.Popen(['flac', '-d', work_dir + flac_file, '-o', wav_file], stdout=FNULL, stderr=FNULL)
			print("Decoding", flac_file, "...")
			proc_list.append(flac_p)
			
			if len(proc_list) >= args.p:
				proc_list[0].wait()
				del proc_list[0]		
			id3_p.wait()
	
		for proc in proc_list:
			proc.wait()
		
		wavs2con = []
		for file_in_dir in sorted(os.listdir(tmpdir)):
			if file_in_dir.endswith(".wav"):
				wavs2con.append(file_in_dir)
		
		#encode wavs to mp3s
		for wav_file in wavs2con:
			f_name = wav_file.rsplit('.',1)[0]
			mp3_file = f_name + '.mp3'
			id3_file = f_name + '.id3'
			
			id3_tags = {"TITLE":"", "ARTIST":"", "ALBUM":"", "ALBUM":"", "DATE":"", "TRACKNUMBER":"0"}
			
			#generate id3 from file
			with open(id3_file, encoding='utf-8') as opened_id3_file:
				for line in opened_id3_file:
					id3_tags[line.split('=',1)[0]] = line.split('=',1)[1].strip('\n')
			
			id3_tags_arg = []
			
			#encode wav to mp3 with id3 tags
			p = subprocess.Popen(['lame', '-h', '--abr', str(args.a), "--tt",
			id3_tags['TITLE'], "--ta", id3_tags['ARTIST'], '--tl', id3_tags['ALBUM'], 
			'--ty', id3_tags['DATE'], '--tn', id3_tags['TRACKNUMBER'],
			tmpdir + '/' + wav_file, out_dir + '/' + mp3_file], stdout=FNULL, stderr=FNULL)
			
			print("Encoding", mp3_file, "...")
			proc_list.append(p)
			
			if len(proc_list) >= args.p:
				proc_list[0].wait()
				del proc_list[0]
		
		#wait for remaining runnig processes
		for proc in proc_list:
			proc.wait()
		
		FNULL.close()
