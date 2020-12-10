import PySimpleGUI as sg

BlockLength = 0xC # Bytes
NumberOfBlocks = None
CurrentOffset = None
OffsetDictionary = {}

TerrainList = []

StringDataDictionary = {
"Terrain Name": {"Offset": 0x0, "Length": 0x4, "Element": "TerrainNameInput"},
"MT": {"Offset": 0x4, "Length": 0x4, "Element": "TerrainMTInput"},
}

IntegerDataDictionary = {
# these might be a pointer?
"Unk1": {"Offset": 0x8, "Length": 0x4, "Element": "TerrainUnk1Input", "Signed": False},
}
# data from the above pointer
# length: 0x17

# these might be tile bonuses?
# 0x00 avoid bonus
# 0x01 defense bonus
# 0x02 光の守り has this set to 3
# 0x03
# 0x04 光の守り has this set to 3
# 0x05 光の守り has this set to 3
# 0x06 recovery bonus
# 0x07 gate and castle have this set to 1

# i think the rest are movement cost
# 0x08 medium build
# 0x09 medium build
# 0x0A desert:3 bush:2
# 0x0B knight
# 0x0C desert:3 bush:2
# 0x0D light build
# 0x0E light build
# 0x0F horse knight
# 0x10 paladin / valkyrie
# 0x11 flier
# 0x12 light build
# 0x13 bandit / berserker
# 0x14 tiger / lion / cat
# 0x15 light build
# 0x16 medium build

#-------------------------------------------------------------------------------
# GUI Layout
#-------------------------------------------------------------------------------
sg.ChangeLookAndFeel("SystemDefaultForReal")

ColumnTerrainList = [
[
	sg.Listbox(key="TerrainListbox",
			   values=(""),
			   select_mode="LISTBOX_SELECT_MODE_SINGLE",
			   size=(24, 18),
			   disabled=True,
			   enable_events=True)
],
]

ColumnStrings = [
[
	sg.Text("Terrain Name", size=(12, 1)),
	sg.In(key="TerrainNameInput", size=(24, 1), disabled=True)
],
[
	sg.Text("MT", size=(12, 1)),
	sg.In(key="TerrainMTInput", size=(24, 1), disabled=True)
],
]

ColumnIntegers = [
[
	sg.Text("Unknown 1"),
	sg.In(key="TerrainUnk1Input", size=(6, 1), disabled=True),
],
[
	sg.Button("Apply Changes", key="TerrainApplyButton", disabled=True)
],
]

Tab = [
[
	sg.Column(layout=ColumnTerrainList, vertical_alignment="top"),
	sg.Column(layout=ColumnStrings, vertical_alignment="top"),
	sg.Column(layout=ColumnIntegers, vertical_alignment="top"),
],
]
