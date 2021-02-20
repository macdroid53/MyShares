#!/usr/bin/env python
# -*- coding: utf-8 -*-
DEBUG = False
if DEBUG:
	import ptvsd
	print("Waiting for debugger attach")
	# 5678 is the default attach port in the VS Code debug configurations
	ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
	ptvsd.wait_for_attach()

import re
import math
import itertools

outfile = "/home/mac/SharedData/Projects/adamis/wire003.dat"
file = open(outfile, "w")

if Gui.ActiveDocument.getInEdit() is not None:
	print('In edit mode')
	print('---------------------------------------')
	"""
	Implication here is that the selection object is an open sketch and the selected items are SubElements in the sketch object
	So, the actual selected edges must be extracted from the selection
	Not sure what other things can be in edit mode...
	But below checks to see if the active document has an open sketch
	"""
	if Gui.ActiveDocument.getInEdit().Object.TypeId == 'Sketcher::SketchObject':
		print('Container type: ', Gui.ActiveDocument.getInEdit().Object.TypeId)
		print('Container object: ', Gui.ActiveDocument.getInEdit().Object.Name) #prints the name of the container that contains the selected edges
		"""
		since in a sketch:
			find the names of the selected edges
			and add them to list of 
		"""
		SelEx=Gui.Selection.getSelectionEx()[0].SubElementNames
		print('Selected edges in container: ', SelEx) #print the names of the selected edges
		#print('---------------------------------------')
		
		#This line is the same:
		#-------------------------------
		#edges = [ActiveSketch.Geometry[int(re.findall(r'\d+',Elem)[0])-1] for Elem in SelEx if Elem.find('Edge') == 0]
		#-------------------------------
		#as these lines:
		#-------------------------------
		edges = [] # create an empty list
		for Elem in SelEx: # loop for all elements in the string-list SelEx
			if Elem.find('Edge') == 0: # the string starts with the substring 'Edge'
				Number = re.findall(r'\d+',Elem)[0] # Number becomes the float of the first numbers (0..9) found in the string Elem
				Index = int(Number)-1 # convert to integer and decrease by one. Lists start numbering with 0, the edge-numbers start with 1
				edges.append(ActiveSketch.Geometry[Index]) # append next element at end of the list (= top of the stack)
		#-------------------------------
		"""
		now loop through the list and display info
		"""
		for edge, simplename in zip(edges, SelEx):
			print('---------------------------------------')
			print('Processing: ', simplename)
			print('Selected edge type: ', edge.TypeId)
			if edge.TypeId == 'Part::GeomArcOfCircle':
				print('Radius: ', edge.Radius)
				print('Arc Length: ', edge.length())
				arcang = edge.length()/(2*math.pi*edge.Radius)*360
				print('Arc angle: ', arcang)
				print('Center X: ', edge.Center.x, ' Y: ', edge.Center.y, ' Z: ', edge.Center.z)
			else:
				print('Length: ', edge.length())
			print('Vert X: ', edge.EndPoint.x, ' Y: ', edge.EndPoint.y, ' Z: ', edge.EndPoint.z)
			print('Vert X: ', edge.StartPoint.x, ' Y: ', edge.StartPoint.y, ' Z: ', edge.StartPoint.z)
			file.write(' '.join([edge.StartPoint.x, edge.StartPoint.y, edge.StartPoint.z]))
			file.write('\n')

else:
	print('Not edit in edit mode')
	"""
	
	"""
	for sel in FreeCADGui.Selection.getSelectionEx():
		print('---------------------------------------')
		print('Container type: ', sel.Object) #prints the ???
		print('Container object: ', sel.ObjectName) #prints the name of the container that contains the selected edges
		print('Container user label: ', sel.Object.Label)
		SelNams = sel.SubElementNames
		print('Selected edges in container: ', SelNams) #print the names of the selected edges
		#print('---------------------------------------')
		#print(sel.SubObjects)   #prints the tuple containing the Edge object/s
		for selectededges, simplename in zip(sel.SubObjects, SelNams):
			print('---------------------------------------')
			print('Processing: ', simplename)    #how to get the Edge# name here???
			print('Selected edge type: ', selectededges.Curve.TypeId)
			if selectededges.Curve.TypeId == 'Part::GeomCircle':
				print('Radius: ', selectededges.Curve.Radius)
				print('Arc length: ', selectededges.Length)
				arcang = selectededges.Length/(2*math.pi*selectededges.Curve.Radius)*360
				print('Arc angle: ', arcang)
			else:
				print('Length: ', selectededges.Length)
			print('Edge verts: ', selectededges.Vertexes)
			for vert in selectededges.Vertexes:
				print('Vert X ',vert.X, ' Y: ', vert.Y, ' Z: ', vert.Z)
				file.write(' '.join([str(vert.X), str(vert.Y), str(vert.Z)]))
				file.write('\n')

file.close()