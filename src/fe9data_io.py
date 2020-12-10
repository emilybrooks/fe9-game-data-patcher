#-------------------------------------------------------------------------------
# Returns a byte array
# ByteArray: Where to grab the data from
# Offset: Start location, in bytes
# Length: Amount of data to read, in bytes
#-------------------------------------------------------------------------------
def ReadBytesFromOffset(ByteArray, Offset, Length):
	EndPoint = Offset + Length
	return ByteArray[Offset:EndPoint]

#-------------------------------------------------------------------------------
# Copy bytes from an array sequentially until a terminating character is reached
# Returns a string
# ByteArray: Where to grab the data from
# Pointer: Pointer to read from, it should be an int
# Offset: sometimes the pointer starts from the beginning of a bundled file,
# or you have to add 0x20 to account for the header
#-------------------------------------------------------------------------------
def ReadStringFromPointer(ByteArray, Pointer, Offset = 0x0):
	if Pointer == 0:
		return None

	Output = bytearray()
	ReadIndex = Pointer

	## just using 0xFF as a safeguard so it doesn't loop infinitely
	for i in range(0xFF):
		ReadByte = (ByteArray[ReadIndex + Offset])
		ReadIndex += 1

		# read until the null terminator (0), then stop
		if ReadByte == 0x0:
			break

		Output.append(ReadByte)

	Output = Output.decode(encoding="shift-jis")
	return Output

#-------------------------------------------------------------------------------
# Returns an integer
# ByteArray: Where to grab the data from
# Offset: Start location, in bytes
# Length: Amount of data to read, in bytes
# Signed: How to interpret the bytes, eg 0 to 255 or -128 to 127
#-------------------------------------------------------------------------------
def ReadIntFromOffset(ByteArray, Offset, Length, Signed=False):
	EndPoint = Offset + Length
	Output = ByteArray[Offset:EndPoint]
	Output = int.from_bytes(Output, byteorder="big", signed=Signed)
	return Output

#-------------------------------------------------------------------------------
# Input: What to write
# Destination: ByteArray that will be modified
# Offset: Where to start writing
#-------------------------------------------------------------------------------
def WriteBytesAtOffset(Input, Destination, Offset):
	WriteIndex = Offset
	for i in Input:
		Destination[WriteIndex] = i
		WriteIndex += 1

#-------------------------------------------------------------------------------
# Take an integer and return it encoded as a bytearray
# Integer: What to encode
# Length: Length of the bytearray
# Signed: How to write the data, eg. from -128 to 127 or 0 to 255
#-------------------------------------------------------------------------------
def ConvertIntToByteArray(Integer, Length, Signed):
	# Make sure it's an int and not a string
	Integer = int(Integer)
	Integer = Integer.to_bytes(Length, "big", signed=Signed)
	return bytearray(Integer)

#-------------------------------------------------------------------------------
# Take an string and return it encoded as a bytearray
# String: What to encode
#-------------------------------------------------------------------------------
def ConvertStringToByteArray(String):
	StingBytes = String.encode("shift-jis")
	return bytearray(StingBytes)
