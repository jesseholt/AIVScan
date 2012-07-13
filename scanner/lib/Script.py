#!/usr/bin/python

__author__ =  'ketchup'
__version__=  '0.1'
__modified_by = 'ketchup'

import sys
import xml.dom.minidom

class Script:
	scriptId = ''
	output = ''
	
	def __init__( self, ScriptNode ):
		if not (ScriptNode is None):
			self.scriptId = ScriptNode.getAttribute('id')
			self.output = ScriptNode.getAttribute('output')
			

if __name__ == '__main__':

	dom = xml.dom.minidom.parse('/tmp/test_pwn01.xml')

	scriptNode = dom.getElementsByTagName('script')[0]
		
	
	
	script = Script( scriptNode )
	print script.scriptId
	print script.output
	
