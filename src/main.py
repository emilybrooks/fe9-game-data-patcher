import PySimpleGUI as sg
import xml.etree.ElementTree as et
import hashlib

from io_helpers import *
import fe9LZ77
import cmp

# TODO: go through the data and properly document them all
import fe9unit
import fe9class
import fe9item

Debug = False;

#-------------------------------------------------------------------------------
# Patch data
# Module: files such as fe9data_character or fe9data_class. they each contain
# dictionaries that describe the data stored in each type of data block
# data is split up between pointers to strings (StringDataDictionary)
# and integers (IntegerDataDictionary)
# ID: Which data block to modify
# Type: one entry in a data block. these are described in the DataDictionaries
# Data: What to write in that entry
#-------------------------------------------------------------------------------
def PatchData(Module, ID, Type, Data):
	global FE9DataContents
	global StringToPointer
	global StringsToAdd
	global PointerOffsetsToAdd
	global Debug

	Offset = Module.OffsetDictionary[ID]

	# strings
	if Type in Module.StringDataDictionary:
		Offset += Module.StringDataDictionary[Type]["Offset"]
		Length = Module.StringDataDictionary[Type]["Length"]
		Signed = False

		# TODO: I want to try and clean up this if logic

		# if there's no pointer offset for this entry in the original file,
		# we need to add it to the pointer offset table or it won't be read by the game
		OriginalPointer = ReadIntFromOffset(FE9DataContents, Offset, 0x4, False)
		if not OriginalPointer:
			if Debug: print("No pointer offset for " + Type)
			AddedPointerOffsets = True
			PointerOffsetsToAdd.append(Offset - 0x20)

		if Data:
			# Strings are represented by a 4 byte long pointer to the string table
			# So we need to convert our string to that pointer
			if Data in StringToPointer:
				Data = StringToPointer[Data]

			# if a string isn't in this dictionary, we need to add it to the end of the file
			else:
				if Debug: print(Data + " is not in the string table")
				# Keep track of which offsets to write the new string's pointers to in a list
				if Data not in StringsToAdd:
					StringsToAdd[Data] = []
				StringsToAdd[Data].append(Offset)
				AddedStrings = True

				# don't write anything for now
				return
		else:
			# if we're replacing this string with nothing
			# just write 0x00000000
			Data = 0x0

	# integers
	elif Type in Module.IntegerDataDictionary:
		Offset += Module.IntegerDataDictionary[Type]["Offset"]
		Length = Module.IntegerDataDictionary[Type]["Length"]
		Signed = Module.IntegerDataDictionary[Type]["Signed"]

	else:
		# TODO: error handling
		raise Exception(Type + " isn't a valid tag")

	# Modify the FE9Data file with the new change
	if Debug: print(Type, hex(int(Data)))
	Data = ConvertIntToByteArray(Data, Length, Signed)
	WriteBytesAtOffset(Data, FE9DataContents, Offset)

#-------------------------------------------------------------------------------
# print only if Debug is True
#-------------------------------------------------------------------------------
def DebugPrint(String):
	if Debug:
		print(String)

#-------------------------------------------------------------------------------
# GUI Layout
#-------------------------------------------------------------------------------
sg.ChangeLookAndFeel("SystemDefaultForReal")

layout = [
[
	sg.Text("System.cmp file to patch:")
],
[
	sg.In("", key="CMPFilePath"),
	sg.FileBrowse(file_types=(("CMP file", ".cmp"), ("All types", "*.*"))),
],
[
	sg.Text("Patch file:")
],
[
	sg.In("", key="XMLFilePath"),
	sg.FileBrowse(file_types=(("XML file", ".xml"), ("All types", "*.*"))),
],
[
	sg.Button("Patch", key="PatchButton")
],
[
	sg.Output(size=(55, 10), key="Output")
],
]

window = sg.Window("fe9 game data patcher", layout)

#-------------------------------------------------------------------------------
# Program Start (Event Loop)
#-------------------------------------------------------------------------------
while True:
	event, values = window.read()

#-------------------------------------------------------------------------------
# Patch
#-------------------------------------------------------------------------------
	if event == "PatchButton":
		FE9DataContents = None
		StringToPointer = {}
		StringsToAdd = {}
		PointerOffsetsToAdd = []

		OriginalFile = values["CMPFilePath"]
		if not OriginalFile:
			print("Error: No CMP file provided")
			continue

		PatchFile = values["XMLFilePath"]
		if not PatchFile:
			print("Error: No patch file provided")
			continue

		NewFile = OriginalFile
		NewFile = NewFile[:-4] + "_patched" + NewFile[-4:]

		with open(OriginalFile, mode="rb") as File:
			File = File.read()
			# the game data file is slightly different for each build of the game
			# figure out which version by calculating the checksum
			# this is also handy for verifying that a valid system.cmp was provided
			Checksum = hashlib.sha256(File)
			Checksum = Checksum.hexdigest()
			DebugPrint(f"System.cmp checksum: {Checksum}")

			Version = ""
			if Checksum == "2d7e1ba67022aa50c9c67e5544288c447654014434960caba97134a3b884c1b4":
				Version = "Japan"
			if Checksum == "fd6d9fc346c86f478c0c3acbf9c621b189ec633965f5617e943d26213f697137":
				Version = "North America"
			if Checksum == "0b7929179b0ad1d4898d763665e9a3120e6b38d3aa0dc8f5e4759c9969ea269e":
				Version = "Europe"

			# TODO: Can I word this error in a better way?
			if Version == "":
				print("The system.cmp file is invalid")
				continue
			print(f"System.cmp version: {Version}")

			File = bytearray(File)
			print("Decompressing...")
			File = fe9LZ77.decompress(File)
			CMPFile = cmp.CMPFile(File)

		FE9DataContents = CMPFile.GetFileByName("FE8Data.bin")

		# Read through the file to figure out where every data block is
		print("Parsing system.cmp")

		# header is 0x20 bytes long
		FileReadIndex = 0x4
		PointerOffsetTableAddress = ReadIntFromOffset(FE9DataContents, FileReadIndex, 0x4, False)
		FileReadIndex += 0x4
		PointerOffsetCount = ReadIntFromOffset(FE9DataContents, FileReadIndex, 0x4, False)
		# then some unimportant stuff until 0x2C
		FileReadIndex = 0x2C
		fe9unit.NumberOfBlocks = ReadIntFromOffset(FE9DataContents, FileReadIndex, 0x4, False)
		FileReadIndex += 0x4

		# every character gets added to a dictionary,
		# with their PID as the key and their offset in the file as the value
		for i in range(fe9unit.NumberOfBlocks):
			PIDPointer = ReadIntFromOffset(FE9DataContents, FileReadIndex, 0x4, False)
			PID = ReadStringFromPointer(FE9DataContents, PIDPointer, 0x20)
			fe9unit.OffsetDictionary[PID] = FileReadIndex
			FileReadIndex += fe9unit.BlockLength

		fe9class.NumberOfBlocks = ReadIntFromOffset(FE9DataContents, FileReadIndex, 0x4, False)
		FileReadIndex += 0x4

		# parse classes
		for i in range(fe9class.NumberOfBlocks):
			JIDPointer = ReadIntFromOffset(FE9DataContents, FileReadIndex, 0x4, False)
			JID = ReadStringFromPointer(FE9DataContents, JIDPointer, 0x20)
			fe9class.OffsetDictionary[JID] = FileReadIndex
			FileReadIndex += fe9class.BlockLength

		fe9item.NumberOfBlocks = ReadIntFromOffset(FE9DataContents, FileReadIndex, 0x4, False)
		FileReadIndex += 0x4

		# parse items
		for i in range(fe9item.NumberOfBlocks):
			IIDPointer = ReadIntFromOffset(FE9DataContents, FileReadIndex, 0x4, False)
			IID = ReadStringFromPointer(FE9DataContents, IIDPointer, 0x20)
			fe9item.OffsetDictionary[IID] = FileReadIndex
			FileReadIndex += fe9item.BlockLength

		# Parse the table of strings to keep track of their pointers
		if Version == "Japan":
			FileReadIndex = 0x14774
		if Version == "North America":
			FileReadIndex = 0x1484C
		if Version == "Europe":
			FileReadIndex = 0x1484C

		while True:
			Pointer = FileReadIndex - 0x20
			String = bytearray()
			for i in range(0xFF):
				ReadByte = FE9DataContents[FileReadIndex]
				FileReadIndex += 1
				# end of the string is marked by a 0x00 byte
				if ReadByte == 0x0:
					break
				String.append(ReadByte)
			String = String.decode(encoding="shift-jis")
			# end of the table is two 0x00 bytes
			if not String:
				break
			StringToPointer[String] = Pointer

		# Parse the xml file
		print("Parsing patch file")
		tree = et.parse(PatchFile)
		root = tree.getroot()

		# units
		for unit in root.iter('unit'):
			PID = unit.attrib["id"]
			DebugPrint(PID)
			for child in unit:
				PatchData(fe9unit, PID, child.tag, child.text)
		print("Patched unit entries")

		# classes
		# "class" is a keyword in python so job is used instead
		for job in root.iter('class'):
			JID = job.attrib["id"]
			DebugPrint(JID)
			for child in job:
				PatchData(fe9class, JID, child.tag, child.text)
		print("Patched class entries")

		# items
		for item in root.iter('item'):
			IID = item.attrib["id"]
			DebugPrint(IID)
			for child in item:
				PatchData(fe9item, IID, child.tag, child.text)
		print("Patched item entries")

		if PointerOffsetsToAdd:
			# get to the end of the pointer offset table
			FileReadIndex = PointerOffsetTableAddress + 0x20
			FileReadIndex += PointerOffsetCount * 0x4
			for i in PointerOffsetsToAdd:
				NewPointerOffset = ConvertIntToByteArray(i, 0x4, False)
				# Insert our new pointer offset and push everything down
				FE9DataContents[FileReadIndex:FileReadIndex] = NewPointerOffset
				FileReadIndex += 0x4
				DebugPrint("Added pointer offset " + str(hex(i)))

			# Change the length of the pointer offset table in the header as well
			PointerOffsetCount += len(PointerOffsetsToAdd)
			PointerOffsetCountBytes = ConvertIntToByteArray(PointerOffsetCount, 0x4, False)
			WriteBytesAtOffset(PointerOffsetCountBytes, FE9DataContents, 0x8)
			print("Updated pointer offsets")

		# do this after adding pointer offsets because it shifts the rest of the file forward,
		# which would mess up pointer calculation
		if StringsToAdd:
			for i in StringsToAdd:
				# write the pointers to this string where it's referenced
				NewStringPointer = len(FE9DataContents) - 0x20
				NewStringPointer = ConvertIntToByteArray(NewStringPointer, 0x4, False)
				for Offset in StringsToAdd[i]:
					WriteBytesAtOffset(NewStringPointer, FE9DataContents, Offset)

				# add the string to the end of the file
				FE9DataContents += ConvertStringToByteArray(i)
				# add a 0x00 byte as a terminator
				FE9DataContents += bytearray(0x1)
				DebugPrint("Added string " + i)
			print("Updated string table")

		# If the filesize changed we have to modify the first 4 bytes
		NewLength = len(FE9DataContents)
		NewLengthBytes = ConvertIntToByteArray(NewLength, 0x4, False)
		WriteBytesAtOffset(NewLengthBytes, FE9DataContents, 0x0)

		# Insert our modified FE8Data.bin and rebuild the cmp file
		CMPFile.SetFile("FE8Data.bin", FE9DataContents, NewLength)
		CMPFile.Rebuild()
		print("Rebuilt the CMP file")

		# save the new cmp file
		with open(NewFile, mode="wb") as File:
			print("Compressing file...")
			FE9DataContents = fe9LZ77.compress(CMPFile.GetCMPFile())
			File.write(FE9DataContents)
		print(f"Wrote to {NewFile}")
		print("Patched successfully")

#-------------------------------------------------------------------------------
# Exit
#-------------------------------------------------------------------------------
	if event == sg.WIN_CLOSED or event == 'Exit':
		break
window.close()
