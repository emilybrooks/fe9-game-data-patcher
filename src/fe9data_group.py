import PySimpleGUI as sg

BlockLength = 0x4 # Bytes
NumberOfBlocks = None
CurrentOffset = None
OffsetDictionary = {}

GroupIDList = []

# 0x14760 start of entries
StringDataDictionary = {
"Group ID": {"Offset": 0x0, "Length": 0x4, "Element": "GroupMGInput"},
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
