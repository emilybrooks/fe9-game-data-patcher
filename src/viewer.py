import PySimpleGUI as sg

from io_helpers import *
import fe9LZ77
import cmp

import fe9unit
import fe9class
import fe9item
import fe9skill

#-------------------------------------------------------------------------------
# init
#-------------------------------------------------------------------------------
FE9DataContents = None
StringToPointer = {}
StringsToAdd = {}
PointerOffsetsToAdd = []

PIDList = []
JIDList = []
IIDList = []
SIDList = []

GameDataFile = "F:\\Documents\\GitHub\\fe9-game-data-patcher\\ignore\\system_jp_compressed.cmp"
with open(GameDataFile, mode="rb") as File:
	File = File.read()
	File = bytearray(File)
	File = fe9LZ77.decompress(File)
	CMPFile = cmp.CMPFile(File)

FE9DataContents = CMPFile.GetFileByName("FE8Data.bin")
FileReadIndex = 0x2C

# parse unit data
fe9unit.NumberOfBlocks = ReadIntFromOffset(FE9DataContents, FileReadIndex, 0x4, False)
FileReadIndex += 0x4
for i in range(fe9unit.NumberOfBlocks):
	PIDPointer = ReadIntFromOffset(FE9DataContents, FileReadIndex, 0x4, False)
	PID = ReadStringFromPointer(FE9DataContents, PIDPointer, 0x20)
	fe9unit.OffsetDictionary[PID] = FileReadIndex
	PIDList.append(PID)
	FileReadIndex += fe9unit.BlockLength

# parse class data
fe9class.NumberOfBlocks = ReadIntFromOffset(FE9DataContents, FileReadIndex, 0x4, False)
FileReadIndex += 0x4
for i in range(fe9class.NumberOfBlocks):
	JIDPointer = ReadIntFromOffset(FE9DataContents, FileReadIndex, 0x4, False)
	JID = ReadStringFromPointer(FE9DataContents, JIDPointer, 0x20)
	fe9class.OffsetDictionary[JID] = FileReadIndex
	JIDList.append(JID)
	FileReadIndex += fe9class.BlockLength

# parse item data
fe9item.NumberOfBlocks = ReadIntFromOffset(FE9DataContents, FileReadIndex, 0x4, False)
FileReadIndex += 0x4
for i in range(fe9item.NumberOfBlocks):
	IIDPointer = ReadIntFromOffset(FE9DataContents, FileReadIndex, 0x4, False)
	IID = ReadStringFromPointer(FE9DataContents, IIDPointer, 0x20)
	fe9item.OffsetDictionary[IID] = FileReadIndex
	IIDList.append(IID)
	FileReadIndex += fe9item.BlockLength

# parse skill data

# there's a collection of strings right after the skill blocks
# they're used for what item is required to learn a skill, and who can learn it
# I need to get to the end of that list, so i'm keeping track of how many items are referenced
SkillListLength = 0

fe9skill.NumberOfBlocks = ReadIntFromOffset(FE9DataContents, FileReadIndex, 0x4, False)
FileReadIndex += 0x4
for i in range(fe9skill.NumberOfBlocks):
	SIDPointer = ReadIntFromOffset(FE9DataContents, FileReadIndex, 0x4, False)
	SID = ReadStringFromPointer(FE9DataContents, SIDPointer, 0x20)
	fe9skill.OffsetDictionary[SID] = FileReadIndex
	SIDList.append(SID)
	Count1 = ReadIntFromOffset(FE9DataContents, FileReadIndex + 0x1B, 0x1, False)
	Count2 = ReadIntFromOffset(FE9DataContents, FileReadIndex + 0x1C, 0x1, False)
	SkillListLength = SkillListLength + Count1 + Count2
	FileReadIndex += fe9skill.BlockLength

#-------------------------------------------------------------------------------
# GUI Layout
#-------------------------------------------------------------------------------
sg.ChangeLookAndFeel("SystemDefaultForReal")

ListboxWidth = 24
ListboxHeight = 45
TabUnit = [[sg.Listbox(key="UnitListbox",values=(PIDList),select_mode="LISTBOX_SELECT_MODE_SINGLE",size=(ListboxWidth, ListboxHeight),enable_events=True),],]
TabClass = [[sg.Listbox(key="ClassListbox", values=(JIDList), select_mode="LISTBOX_SELECT_MODE_SINGLE", size=(ListboxWidth, ListboxHeight), enable_events=True), ],]
TabItem = [[sg.Listbox(key="ItemListbox", values=(IIDList), select_mode="LISTBOX_SELECT_MODE_SINGLE", size=(ListboxWidth, ListboxHeight), enable_events=True),],]
TabSkill = [[sg.Listbox(key="SkillListbox", values=(SIDList), select_mode="LISTBOX_SELECT_MODE_SINGLE", size=(ListboxWidth, ListboxHeight), enable_events=True),],]

TabGroup = [
[
	sg.Tab(layout=TabUnit, title="Unit"),
	sg.Tab(layout=TabClass, title="Class"),
	sg.Tab(layout=TabItem, title="Item"),
	sg.Tab(layout=TabSkill, title="Skill"),
],
]

layout = [
[
	sg.TabGroup(TabGroup, tab_location="topleft"),
	sg.Output(size=(60, 45), key="Output"),
],
]

window = sg.Window("system.cmp viewer", layout)

#-------------------------------------------------------------------------------
# Program Start (Event Loop)
#-------------------------------------------------------------------------------
while True:
	event, values = window.read()

#-------------------------------------------------------------------------------
# Selecting a unit entry
#-------------------------------------------------------------------------------
	if event == "UnitListbox":
		Selection = values["UnitListbox"]
		if not Selection:
			continue
		Selection = Selection[0]

		# clear the console
		window['Output'].update('')

		CurrentOffset = fe9unit.OffsetDictionary[Selection]

		# strings
		for Item in fe9unit.StringDataDictionary:
			Offset = fe9unit.StringDataDictionary[Item]["Offset"]
			Offset += CurrentOffset
			Length = fe9unit.StringDataDictionary[Item]["Length"]
			Pointer = ReadIntFromOffset(FE9DataContents, Offset, Length)
			if Pointer:
				String = ReadStringFromPointer(FE9DataContents, Pointer, 0x20)
			else:
				String = ""
			print(f"{Item}: {String}")

		# integers
		for Item in fe9unit.IntegerDataDictionary:
			Offset = fe9unit.IntegerDataDictionary[Item]["Offset"]
			Offset += CurrentOffset
			Length = fe9unit.IntegerDataDictionary[Item]["Length"]
			Signed = fe9unit.IntegerDataDictionary[Item]["Signed"]
			Integer = ReadIntFromOffset(FE9DataContents, Offset, Length, Signed)
			print(f"{Item}: {Integer}")

#-------------------------------------------------------------------------------
# Selecting a class entry
#-------------------------------------------------------------------------------
	if event == "ItemListbox":
		Selection = values["ItemListbox"]
		if not Selection:
			continue
		Selection = Selection[0]

		# clear the console
		window['Output'].update('')

		CurrentOffset = fe9item.OffsetDictionary[Selection]

		# strings
		for Item in fe9item.StringDataDictionary:
			Offset = fe9item.StringDataDictionary[Item]["Offset"]
			Offset += CurrentOffset
			Length = fe9item.StringDataDictionary[Item]["Length"]
			Pointer = ReadIntFromOffset(FE9DataContents, Offset, Length)
			if Pointer:
				String = ReadStringFromPointer(FE9DataContents, Pointer, 0x20)
			else:
				String = ""
			print(f"{Item}: {String}")

		# integers
		for Item in fe9item.IntegerDataDictionary:
			Offset = fe9item.IntegerDataDictionary[Item]["Offset"]
			Offset += CurrentOffset
			Length = fe9item.IntegerDataDictionary[Item]["Length"]
			Signed = fe9item.IntegerDataDictionary[Item]["Signed"]
			Integer = ReadIntFromOffset(FE9DataContents, Offset, Length, Signed)
			print(f"{Item}: {Integer}")

#-------------------------------------------------------------------------------
# Selecting an item entry
#-------------------------------------------------------------------------------
	if event == "ClassListbox":
		Selection = values["ClassListbox"]
		if not Selection:
			continue
		Selection = Selection[0]

		# clear the console
		window['Output'].update('')

		CurrentOffset = fe9class.OffsetDictionary[Selection]

		# strings
		for Item in fe9class.StringDataDictionary:
			Offset = fe9class.StringDataDictionary[Item]["Offset"]
			Offset += CurrentOffset
			Length = fe9class.StringDataDictionary[Item]["Length"]
			Pointer = ReadIntFromOffset(FE9DataContents, Offset, Length)
			if Pointer:
				String = ReadStringFromPointer(FE9DataContents, Pointer, 0x20)
			else:
				String = ""
			print(f"{Item}: {String}")

		# integers
		for Item in fe9class.IntegerDataDictionary:
			Offset = fe9class.IntegerDataDictionary[Item]["Offset"]
			Offset += CurrentOffset
			Length = fe9class.IntegerDataDictionary[Item]["Length"]
			Signed = fe9class.IntegerDataDictionary[Item]["Signed"]
			Integer = ReadIntFromOffset(FE9DataContents, Offset, Length, Signed)
			print(f"{Item}: {Integer}")

#-------------------------------------------------------------------------------
# Selecting a skill entry
#-------------------------------------------------------------------------------
	if event == "SkillListbox":
		Selection = values["SkillListbox"]
		if not Selection:
			continue
		Selection = Selection[0]

		# clear the console
		window['Output'].update('')

		CurrentOffset = fe9skill.OffsetDictionary[Selection]

		# strings
		for Item in fe9skill.StringDataDictionary:
			Offset = fe9skill.StringDataDictionary[Item]["Offset"]
			Offset += CurrentOffset
			Length = fe9skill.StringDataDictionary[Item]["Length"]
			Pointer = ReadIntFromOffset(FE9DataContents, Offset, Length)
			if Pointer:
				String = ReadStringFromPointer(FE9DataContents, Pointer, 0x20)
			else:
				String = ""
			print(f"{Item}: {String}")

		# integers
		for Item in fe9skill.IntegerDataDictionary:
			Offset = fe9skill.IntegerDataDictionary[Item]["Offset"]
			Offset += CurrentOffset
			Length = fe9skill.IntegerDataDictionary[Item]["Length"]
			Signed = fe9skill.IntegerDataDictionary[Item]["Signed"]
			Integer = ReadIntFromOffset(FE9DataContents, Offset, Length, Signed)
			print(f"{Item}: {Integer}")

		# each block has pointers to 2 lists, and a count of how many items are in those lists
		ItemRequiredCount = ReadIntFromOffset(FE9DataContents, CurrentOffset + 0x1B, 0x1)
		ItemRequiredPointer = ReadIntFromOffset(FE9DataContents, CurrentOffset + 0x20, 0x4)
		UnitRestrictionCount = ReadIntFromOffset(FE9DataContents, CurrentOffset + 0x1C, 0x1)
		UnitRestrictionPointer = ReadIntFromOffset(FE9DataContents, CurrentOffset + 0x24, 0x4)

		print()
		print("Item required to learn:")
		i = 0
		while i < ItemRequiredCount:
			# The lists contain pointers to strings, 0x4 bytes for each pointer
			# the 0x20 offset still applies
			Offset = ItemRequiredPointer + (i * 0x4) + 0x20
			Pointer = ReadIntFromOffset(FE9DataContents, Offset, 0x4)
			String = ReadStringFromPointer(FE9DataContents, Pointer, 0x20)
			print(String)
			i += 1

		print()
		print("Units able to learn:")
		i = 0
		while i < UnitRestrictionCount:
			Offset = UnitRestrictionPointer + (i * 0x4) + 0x20
			Pointer = ReadIntFromOffset(FE9DataContents, Offset, 0x4)
			String = ReadStringFromPointer(FE9DataContents, Pointer, 0x20)
			print(String)
			i += 1

#-------------------------------------------------------------------------------
# Exit
#-------------------------------------------------------------------------------
	if event == sg.WIN_CLOSED or event == 'Exit':
		break
window.close()
