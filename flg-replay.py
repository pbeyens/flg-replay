#!/usr/bin/python

import sys
import socket
import string
import select

def start():
	global move, sgf_nodes, flsgf
	move = 0
	flsgf = []
	return ';SZ[19]'+sgf_nodes[move]

def next():
	global move, sgf_nodes
	move = move + 1
	return ';'+sgf_nodes[move]

def prev():
	global move, flsgf
	if move == 0:
		return ""
	data = flsgf[move-1]
	if data.find("AB") != -1:
		data = data.replace("AE","AW")
		data = data.replace("AB","AE")
	elif data.find("AW") != -1:
		data = data.replace("AE","AB")
		data = data.replace("AW","AE")
	move = move - 1
	return data

# read sgf and split into separate command
sgf = sys.stdin.read()
sgf_nodes = string.split(sgf,';')

# this is the expanded sgf from flgoban
move = 0
flsgf = []

# setup communication
flgoban = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
flgoban.connect(('localhost', 5000))

# start
flgoban.send(start())

input = [flgoban] 
while True:
	inputready,outputready,exceptready = select.select(input,[],[],0)

	for s in inputready:
		if s == flgoban:
			data = s.recv(1024)
			if data == "":
				sys.exit(0)
			print "IN"+data,
			print "->"+str(move)+'-'+str(len(flsgf))
			if data.find(";KEY[g]") != -1:
				s.send(start())
			elif data.find(";KEY[j]") != -1:
				s.send(next())
			elif data.find(";KEY[k]") != -1:
				s.send(prev())
			elif data.find(";KEY[") != -1:
				pass
			elif data.find(";MOU[") != -1:
				pass
			elif move == len(flsgf)+1:
				flsgf.append(data)
	
s.close()

sys.exit(0)
