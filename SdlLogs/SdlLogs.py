import sublime
import sublime_plugin
import json
import re
from os import path
import shutil 

# settings
sourcePath = "source_path"

#Regulars for columns:
dateRegex       = "\\[\\s?[0-9]{1,2} \\s?[A-Z][a-z]{2} [0-9]{4} [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2},[0-9]{0,3}]"
junkRegex       = " /(.*)/sdl_core/src/" 
componentRegex  = "\\[[A-Z][a-zA-z]{3,26}] "
threadEnter     = ".(cc|h):[0-9]{1,5} (.*): Enter"
threadExit      = " Exit"
threadRegex     = "\\[0x[a-zA-Z0-9]{12}]"
pathRegex       = "sdl_core/src/(.*).(cc|h):[0-9]{1,5}" 

#flags for commands
actThreadFlag    = False
actDateFlag      = False
actPathFlag      = False
actComponentFlag = False

def getSelectedText(self):
	#array of selection regions
	selText = self.view.sel()
	#selected string
	selText = self.view.substr(selText[0])
	return selText


#Hide date of all traces from log
class HideDateCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global actDateFlag
		trcRegions = self.view.find_all(dateRegex)

		if actDateFlag is False:
			self.view.fold(trcRegions)
			actDateFlag = True
		else:
			self.view.unfold(trcRegions)
			actDateFlag = False


class FunctionCallCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		posFatal = 0
		enterRegex = "initial fake value"

		while enterRegex is not "":

			enterRegion = self.view.find(threadEnter, posFatal)
			enterRegex = self.view.substr(enterRegion)
			enterRegex = enterRegex[enterRegex.find(" ")+1:]
			enterRegex = enterRegex[:enterRegex.find(" ")]

			print (enterRegex)

			if enterRegex is not "":
				exitRegion = self.view.find(enterRegex+threadExit, posFatal)
				print (self.view.substr(exitRegion))

				if exitRegion.size() is not 0:
					posFatal = enterRegion.b
				else:
					self.view.show(enterRegion)
					posFatal = enterRegion.b
					break




class HideThreadAdressCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global actThreadFlag
		trcRegions = self.view.find_all(threadRegex)

		if actThreadFlag is False:
			self.view.fold(trcRegions)
			actThreadFlag = True
		else:
			self.view.unfold(trcRegions)
			actThreadFlag = False


class HideComponentCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global actComponentFlag
		trcRegions = self.view.find_all(componentRegex)

		if actComponentFlag is False:
			self.view.fold(trcRegions)
			actComponentFlag = True
		else:
			self.view.unfold(trcRegions)
			actComponentFlag = False


class HideExtraPathCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global actPathFlag
		trcRegions = self.view.find_all(junkRegex)

		if actPathFlag is False:
			self.view.fold(trcRegions)
			actPathFlag = True
		else:
			self.view.unfold(trcRegions)
			actPathFlag = False


class FilterByValueCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		selTextRegex = getSelectedText(self)
		if selTextRegex is not "":
			trcRegions = self.view.find_all(selTextRegex)
			cutRegion = sublime.Region(0, 0)
			leftBorder = 0

			for i in range (0, len(trcRegions)):
				trcRegions[i] = self.view.full_line(trcRegions[i])
				trcRegions[i] = self.view.substr(trcRegions[i])

			self.view.erase(edit, sublime.Region(0, self.view.size()))
			leftBorder = 0

			for i in range (0, len(trcRegions)):
				leftBorder+= self.view.insert(edit, leftBorder, trcRegions[i])


class JumpToFileCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		FULL_PATH_FILE	= "(/.*)(/sdl_core/src/.{0,}\\.(cc|h|cpp|hpp)):(\\d{1,})"
		CORRECTED_PATH  = "(/[^/ ]*)+/?"

		primaryPath = re.search(FULL_PATH_FILE, self.view.substr(self.view.line(self.view.sel()[0])))
		isItPath = re.search(CORRECTED_PATH, self.view.substr(self.view.line(self.view.sel()[0])))

		if self.view.settings().get(sourcePath) != "": 
			if primaryPath :
				file = self.view.settings().get(sourcePath) + primaryPath.group(2)
				if path.isfile(file) : 
					self.view.window().open_file(file + ":" + primaryPath.group(4), sublime.ENCODED_POSITION)
				else:
					sublime.error_message("File '{0}' not found. Maybe path to source files in your settings is incorrect or file really absent".format(file))
			elif isItPath:
				sublime.error_message("Expected '/sdl_core/src/' in '{0}' ".format(isItPath.group(0)))
		else:
			if primaryPath :
				file = primaryPath.group(1) + primaryPath.group(2)
				if path.isfile(file): 
					self.view.window().open_file(file + ":" + primaryPath.group(4), sublime.ENCODED_POSITION)
				else:
					sublime.error_message("File '{0}' not found. You can write path to source files in settings and try again. Or file really absent".format(file))
			elif isItPath:
				sublime.error_message("Expected '/sdl_core/src/' in '{0}' ".format(isItPath.group(0)))