from fe9data_io import *

class CMPFile:
	# the entire cmp file
	FileContents = None
	NumberOfFiles = None
	Header = {}
	# each individual file that's stored in the cmp file
	FileDictionary = {}

	def __init__(self, ByteArray):
			self.FileContents = ByteArray
			FileReadIndex = 0x0

			# The first four bytes should be "pack",
			# otherwise the file is probably incorrect or it's still compressed
			if not ReadBytesFromOffset(self.FileContents, FileReadIndex, 0x4) == bytearray(b"pack"):
				# TODO: Error Handling
				print("Failed to read 'pack'")

			FileReadIndex += 0x4
			self.NumberOfFiles = ReadIntFromOffset(self.FileContents, FileReadIndex, 0x2, False)

			FileReadIndex += 0x4
			for i in range(self.NumberOfFiles):
				FileReadIndex += 0x4 # For some reason these bytes are always 0
				NamePointer = ReadIntFromOffset(self.FileContents, FileReadIndex, 0x4, False)
				Name = ReadStringFromPointer(self.FileContents, NamePointer)
				self.Header[Name] = {}

				FileReadIndex += 0x4
				self.Header[Name]["StartPointer"] = ReadIntFromOffset(self.FileContents, FileReadIndex, 0x4, False)

				FileReadIndex += 0x4
				self.Header[Name]["Length"] = ReadIntFromOffset(self.FileContents, FileReadIndex, 0x4, False)

				FileReadIndex += 0x4

			for i in self.Header:
				Pointer = self.Header[i]["StartPointer"]
				Length = self.Header[i]["Length"]
				Contents = ReadBytesFromOffset(self.FileContents, Pointer, Length)
				self.FileDictionary[i] = Contents

	def GetFileByName(self, Name):
		return self.FileDictionary[Name]

	def SetFile(self, Name, Contents, Length):
		self.FileDictionary[Name] = Contents
		self.Header[Name]["Length"] = Length

	def GetCMPFile(self):
		return self.FileContents

#-------------------------------------------------------------------------------
# If a file was modified, we need to reconstruct the cmp archive and the header
#-------------------------------------------------------------------------------
	def Rebuild(self):
		self.FileContents = bytearray()
		self.FileContents += bytearray(b"pack")
		self.FileContents += ConvertIntToByteArray(self.NumberOfFiles, 0x2, False)
		self.FileContents += bytearray(0x2)

		# file definitions
		for i in self.Header:
			# 4 empty bytes per file definition
			self.FileContents += bytearray(0x4)
			# this data isn't known yet, so fill it with empty bytes for now
			# File Name
			self.FileContents += bytearray(0x4)
			# Start pointer
			self.FileContents += bytearray(0x4)
			# File length
			self.FileContents += bytearray(0x4)

		# filename table
		FileIndex = 0
		for i in self.Header:
			FileNamePointer = ConvertIntToByteArray(len(self.FileContents), 0x4, False)
			self.FileContents += ConvertStringToByteArray(i)
			# empty byte seperates the strings
			self.FileContents += bytearray(0x1)
			# write the pointer to this in the file definition table
			WriteBytesAtOffset(FileNamePointer, self.FileContents, 0xC + 0x10 * FileIndex)
			FileIndex += 1

		# iterate through each file to add to the cmp archive
		FileIndex = 0
		for i in self.Header:
			# each file needs to start on a multiple of 0x20
			# add empty bytes to fill in the gap
			BytesToAdd = 0x20 - (len(self.FileContents) % 0x20)
			if BytesToAdd != 0x20:
				self.FileContents += bytearray(BytesToAdd)

			StartPointer = len(self.FileContents)

			# update the header dictionary
			self.Header[i]["StartPointer"] = StartPointer

			# update the file definition table
			StartPointerBytes = ConvertIntToByteArray(StartPointer, 0x4, False)
			WriteBytesAtOffset(StartPointerBytes, self.FileContents, 0x10 + 0x10 * FileIndex)

			Length = self.Header[i]["Length"]
			LengthBytes = ConvertIntToByteArray(Length, 0x4, False)
			WriteBytesAtOffset(LengthBytes, self.FileContents, 0x14 + 0x10 * FileIndex)

			# add the file's contents
			self.FileContents += self.FileDictionary[i]

			FileIndex += 1
