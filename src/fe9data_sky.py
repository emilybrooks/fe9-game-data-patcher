import PySimpleGUI as sg

BlockLength = 0x4 # Bytes
NumberOfBlocks = None
CurrentOffset = None
OffsetDictionary = {}

SkyList = []

# 0x14760 start of entries
StringDataDictionary = {
"Sky ID": {"Offset": 0x0, "Length": 0x4, "Element": "SkyIDInput"},
}
