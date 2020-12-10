import PySimpleGUI as sg

BlockLength = 0x28 # Bytes
NumberOfBlocks = None
CurrentOffset = None
OffsetDictionary = {}

SIDList = []

Listbox1 = []
Listbox2 = []

StringDataDictionary = {
"ID": {"Offset": 0x0, "Length": 0x4, "Element": "SkillSIDInput"},
# appears to be the name written in japanese
"Unk1": {"Offset": 0x4, "Length": 0x4, "Element": "SkillUnk1Input"},
"Name": {"Offset": 0x8, "Length": 0x4, "Element": "SkillMSIDInput"},
"Help Text 1": {"Offset": 0xC, "Length": 0x4, "Element": "SkillHelp1Input"},
"Help Text 2": {"Offset": 0x10, "Length": 0x4, "Element": "SkillHelp2Input"},
"Animation": {"Offset": 0x14, "Length": 0x4, "Element": "SkillEIDInput"},
}

IntegerDataDictionary = {
# an index of some sort, it counts up 1 every entry
"unk4": {"Offset": 0x18, "Length": 0x1, "Element": "SkillUnk4Input", "Signed": False},
# icon index?
"unk5": {"Offset": 0x19, "Length": 0x1, "Element": "SkillUnk5Input", "Signed": False},
"Skill Points Required": {"Offset": 0x1A, "Length": 0x1, "Element": "SkillCostInput", "Signed": False},
# seems to always be 0
"unk9": {"Offset": 0x1D, "Length": 0x1, "Element": "SkillUnk9Input", "Signed": False},
# seems to always be 0
"unk10": {"Offset": 0x1E, "Length": 0x1, "Element": "SkillUnk10Input", "Signed": False},
# telgnosis has this set to 5
# maybe this is line of sight in fog?
# "This skill increases its user's Hit Rate by 20 and his/her sight in Fog of War maps by 5 tiles."
"unk11": {"Offset": 0x1F, "Length": 0x1, "Element": "SkillUnk11Input", "Signed": False},
}

#-------------------------------------------------------------------------------
# GUI Layout
#-------------------------------------------------------------------------------
sg.ChangeLookAndFeel("SystemDefaultForReal")

ColumnSIDList = [
[
	sg.Listbox(key="SkillListbox",
			   values=(""),
			   select_mode="LISTBOX_SELECT_MODE_SINGLE",
			   size=(24, 18),
			   disabled=True,
			   enable_events=True)
],
]

ColumnStrings = [
[
	sg.Text("ID", size=(12, 1)),
	sg.In(key="SkillSIDInput", size=(24, 1), disabled=True)
],
[
	sg.Text("Unknown 1", size=(12, 1)),
	sg.In(key="SkillUnk1Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Name", size=(12, 1)),
	sg.In(key="SkillMSIDInput", size=(24, 1), disabled=True)
],
[
	sg.Text("Help Text 1", size=(12, 1)),
	sg.In(key="SkillHelp1Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Help Text 2", size=(12, 1)),
	sg.In(key="SkillHelp2Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Animation", size=(12, 1)),
	sg.In(key="SkillEIDInput", size=(24, 1), disabled=True)
],
[
	sg.Button("Apply Changes", key="SkillApplyButton", disabled=True)
],
]

ColumnIntegers = [
[
	sg.Text("Unknown 4", size=(12, 1)),
	sg.In(key="SkillUnk4Input", size=(6, 1), disabled=True),
],
[
	sg.Text("Unknown 5", size=(12, 1)),
	sg.In(key="SkillUnk5Input", size=(6, 1), disabled=True),
],
[
	sg.Text("Skill Points Required", size=(12, 1)),
	sg.In(key="SkillCostInput", size=(6, 1), disabled=True),
],
[
	sg.Text("Unknown 9", size=(12, 1)),
	sg.In(key="SkillUnk9Input", size=(6, 1), disabled=True),
],
[
	sg.Text("Unknown 10", size=(12, 1)),
	sg.In(key="SkillUnk10Input", size=(6, 1), disabled=True),
],
[
	sg.Text("Unknown 11", size=(12, 1)),
	sg.In(key="SkillUnk11Input", size=(6, 1), disabled=True),
],
[
	sg.Text("Unknown 20", size=(12, 1)),
	sg.In(key="SkillUnk20Input", size=(6, 1), disabled=True),
],
[
	sg.Text("Item required to learn", size=(24, 1)),
],
[
	sg.Listbox(key="SkillFirstListbox", values=(""), size=(24, 5)),
],
[
	sg.Text("Units that can learn", size=(24, 1)),
],
[
	sg.Listbox(key="SkillSecondListbox", values=(""), size=(24, 5)),
],
]

Tab = [
[
	sg.Column(layout=ColumnSIDList, vertical_alignment="top"),
	sg.Column(layout=ColumnStrings, vertical_alignment="top"),
	sg.Column(layout=ColumnIntegers, vertical_alignment="top"),
],
]
