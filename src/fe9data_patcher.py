import PySimpleGUI as sg
import xml.etree.ElementTree as et

from fe9data_io import *
import fe9LZ77
import cmpfile as cmp

# TODO: go through the data in fe9character, etc and properly document them all
import fe9data_character as fe9character
import fe9data_class as fe9class
import fe9data_item as fe9item

#-------------------------------------------------------------------------------
# Patch data
# Module: files such as fe9data_character or fe9data_class. they each contain
# dictionaries that describe the data stored in each type of data block
# data is split up between pointers to strings (StringDataDictionary)
# and integers (IntegerDataDictionary)
# ID: Which data block to modify
# Type: one entry in a data block. these are described in the DataDictionaries
# TODO: I should properly document them on a wiki page or something later though
# Data: What to write in that entry
#-------------------------------------------------------------------------------
def PatchData(Module, ID, Type, Data):
	global FE9DataContents
	global StringToPointer
	global StringsToAdd
	global PointerOffsetsToAdd

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
			print("No pointer offset for " + Type)
			AddedPointerOffsets = True
			PointerOffsetsToAdd.append(Offset - 0x20)

		if Data:
			# Strings are represented by a 4 byte long pointer to the string table
			# So we need to convert our string to that pointer
			if Data in StringToPointer:
				Data = StringToPointer[Data]

			# if a string isn't in this dictionary, we need to add it to the end of the file
			else:
				print(Data + " is not in the string table")
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
	print(Type, hex(int(Data)))
	Data = ConvertIntToByteArray(Data, Length, Signed)
	WriteBytesAtOffset(Data, FE9DataContents, Offset)

#-------------------------------------------------------------------------------
# GUI Layout
#-------------------------------------------------------------------------------
sg.ChangeLookAndFeel("SystemDefaultForReal")

layout = [
[
	sg.Text("Version:")
],
[
	sg.Drop(size=(14,1), default_value="Japan", values=["Japan", "North America", "Europe"], key="VersionDrop"),
],
[
	sg.Text("System.cmp file to patch:")
],
[
	sg.In("F:/Documents/GitHub/fe9-character-data-parser/src/system_jp_compressed.cmp", key="CMPFilePath"),
	sg.FileBrowse(file_types=(("CMP file", ".cmp"), ("All types", "*.*"))),
],
[
	sg.Text("Patch file:")
],
[
	sg.In("F:/Documents/GitHub/fe9-character-data-parser/src/patch.xml", key="XMLFilePath"),
	sg.FileBrowse(file_types=(("XML file", ".xml"), ("All types", "*.*"))),
],
[
	sg.Text("Save as...")
],
[
	sg.In("F:/Documents/GitHub/fe9-character-data-parser/tools/system.cmp", key="NewFilePath"),
	sg.FileSaveAs(file_types=(("CMP file", ".cmp"), ("All types", "*.*"))),
],
[
	sg.Button("Patch", key="PatchButton")
],
]

# TODO: Replace window title
window = sg.Window("Window Title", layout)

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
			sg.Popup("You forgot to add the path to the system.cmp file")
			continue

		PatchFile = values["XMLFilePath"]
		if not PatchFile:
			sg.Popup("You forgot to add the path to the patch file")
			continue

		NewFile = values["NewFilePath"]
		if not NewFile:
			sg.Popup("You forgot to add the path to the saved file")
			continue

		# TODO: check the checksum of the input file to make sure it's valid
		# you should also be able to determine what region to select without asking the user

		with open(OriginalFile, mode="rb") as File:
			File = File.read()
			File = bytearray(File)
			File = fe9LZ77.decompress(File)
			print("Decompressed file")
			CMPFile = cmp.CMPFile(File)

		FE9DataContents = CMPFile.GetFileByName("FE8Data.bin")

		# Read through the file to figure out where every data block is

		# header is 0x20 bytes long
		FileReadIndex = 0x4
		PointerOffsetTableAddress = ReadIntFromOffset(FE9DataContents, FileReadIndex, 0x4, False)
		FileReadIndex += 0x4
		PointerOffsetCount = ReadIntFromOffset(FE9DataContents, FileReadIndex, 0x4, False)
		# then some unimportant stuff until 0x2C
		FileReadIndex = 0x2C
		fe9character.NumberOfBlocks = ReadIntFromOffset(FE9DataContents, FileReadIndex, 0x4, False)
		FileReadIndex += 0x4

		# every character gets added to a dictionary,
		# with their PID as the key and their offset in the file as the value
		for i in range(fe9character.NumberOfBlocks):
			PIDPointer = ReadIntFromOffset(FE9DataContents, FileReadIndex, 0x4, False)
			PID = ReadStringFromPointer(FE9DataContents, PIDPointer, 0x20)
			fe9character.OffsetDictionary[PID] = FileReadIndex
			FileReadIndex += fe9character.BlockLength

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
		# TODO: Eventually calculate the start of this table dynamically
		Version = values["VersionDrop"]
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
		tree = et.parse(PatchFile)
		root = tree.getroot()

		# characters
		for character in root.iter('character'):
			PID = character.attrib["id"]
			print(PID)
			for child in character:
				PatchData(fe9character, PID, child.tag, child.text)

		# classes
		for job in root.iter('class'):
			JID = job.attrib["id"]
			print(JID)
			for child in job:
				PatchData(fe9class, JID, child.tag, child.text)

		# items
		for item in root.iter('item'):
			IID = item.attrib["id"]
			print(IID)
			for child in item:
				PatchData(fe9item, IID, child.tag, child.text)


		if PointerOffsetsToAdd:
			# get to the end of the pointer offset table
			FileReadIndex = PointerOffsetTableAddress + 0x20
			FileReadIndex += PointerOffsetCount * 0x4
			for i in PointerOffsetsToAdd:
				NewPointerOffset = ConvertIntToByteArray(i, 0x4, False)
				# Insert our new pointer offset and push everything down
				FE9DataContents[FileReadIndex:FileReadIndex] = NewPointerOffset
				FileReadIndex += 0x4
				print("Added pointer offset " + str(hex(i)))

			# Change the length of the pointer offset table in the header as well
			PointerOffsetCount += len(PointerOffsetsToAdd)
			PointerOffsetCountBytes = ConvertIntToByteArray(PointerOffsetCount, 0x4, False)
			WriteBytesAtOffset(PointerOffsetCountBytes, FE9DataContents, 0x8)

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
				print("Added string " + i)

		# If the filesize changed we have to modify the first 4 bytes
		NewLength = len(FE9DataContents)
		NewLengthBytes = ConvertIntToByteArray(NewLength, 0x4, False)
		WriteBytesAtOffset(NewLengthBytes, FE9DataContents, 0x0)

		# Insert our modified FE8Data.bin and rebuild the cmp file
		CMPFile.SetFile("FE8Data.bin", FE9DataContents, NewLength)
		CMPFile.Rebuild()

		# save the new cmp file
		with open(NewFile, mode="wb") as File:
			print("Compressing file...")
			FE9DataContents = fe9LZ77.compress(CMPFile.GetCMPFile())
			print("done")
			File.write(FE9DataContents)

		sg.Popup("Patched successfully")

#-------------------------------------------------------------------------------
# Exit
#-------------------------------------------------------------------------------
	if event == sg.WIN_CLOSED or event == 'Exit':
		break
window.close()
