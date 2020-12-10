import PySimpleGUI as sg

BlockLength = 0xC # Bytes
NumberOfBlocks = None
CurrentOffset = None
OffsetDictionary = {}



# 0x147E0 start of entries
StringDataDictionary = {
"PID 1": {"Offset": 0x0, "Length": 0x4, "Element": "RelationsPID1Input"},
"PID 2": {"Offset": 0x4, "Length": 0x4, "Element": "RelationsPID2Input"},
}

IntegerDataDictionary = {
# "type" of boost, 1 is critical boost, 2 is crit negation
"Unk 1": {"Offset": 0x8, "Length": 0x1, "Element": "RelationsUnk1Input", "Signed": False},
# if type 1, how much critical boost?
"Unk 2": {"Offset": 0x9, "Length": 0x1, "Element": "RelationsUnk2Input", "Signed": False},
}

#-------------------------------------------------------------------------------
# GUI Layout
#-------------------------------------------------------------------------------
sg.ChangeLookAndFeel("SystemDefaultForReal")

ColumnGroupList = [
[
	sg.Listbox(key="GroupListbox",
			   values=(""),
			   select_mode="LISTBOX_SELECT_MODE_SINGLE",
			   size=(24, 18),
			   disabled=True,
			   enable_events=True)
],
]

Tab = [
[
	sg.Column(layout=ColumnGroupList, vertical_alignment="top"),
],
]
