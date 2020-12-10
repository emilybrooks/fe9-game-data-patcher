import PySimpleGUI as sg

BlockLength = 0xC # Bytes
NumberOfBlocks = None
CurrentOffset = None
OffsetDictionary = {}

AffinityList = []

StringDataDictionary = {
"ID": {"Offset": 0x0, "Length": 0x4, "Element": "AffinityIDInput"},
}

IntegerDataDictionary = {
"BonusAttack": {"Offset": 0x4, "Length": 0x1, "Element": "AffinityBonusAttackInput", "Signed": False},
"BonusDefense": {"Offset": 0x5, "Length": 0x1, "Element": "AffinityBonusDefenseInput", "Signed": False},
"BonusAccuracy": {"Offset": 0x6, "Length": 0x1, "Element": "AffinityBonusAccuracyInput", "Signed": False},
"BonusAvoid": {"Offset": 0x7, "Length": 0x1, "Element": "AffinityBonusAvoidInput", "Signed": False},
"Unk5": {"Offset": 0x8, "Length": 0x1, "Element": "AffinityUnk5Input", "Signed": False},
"Unk6": {"Offset": 0x9, "Length": 0x1, "Element": "AffinityUnk6Input", "Signed": False},
"Unk7": {"Offset": 0xA, "Length": 0x1, "Element": "AffinityUnk7Input", "Signed": False},
"Unk8": {"Offset": 0xB, "Length": 0x1, "Element": "AffinityUnk8Input", "Signed": False},
}

#-------------------------------------------------------------------------------
# GUI Layout
#-------------------------------------------------------------------------------
sg.ChangeLookAndFeel("SystemDefaultForReal")

ColumnAffinityList = [
[
	sg.Listbox(key="AffinityListbox",
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
	sg.In(key="AffinityIDInput", size=(24, 1), disabled=True)
],
[
	sg.Button("Apply Changes", key="AffinityApplyButton", disabled=True)
],
]

ColumnIntegers = [
[
		sg.Text("Attack Bonus", size=(12, 1)),
		sg.In(key="AffinityBonusAttackInput", size=(6, 1), disabled=True),
],
[
		sg.Text("Defense Bonus", size=(12, 1)),
		sg.In(key="AffinityBonusDefenseInput", size=(6, 1), disabled=True),
],
[
		sg.Text("Accuracy Bonus", size=(12, 1)),
		sg.In(key="AffinityBonusAccuracyInput", size=(6, 1), disabled=True),
],
[
		sg.Text("Avoid Bonus", size=(12, 1)),
		sg.In(key="AffinityBonusAvoidInput", size=(6, 1), disabled=True),
],
[
		sg.Text("Unknown 5", size=(12, 1)),
		sg.In(key="AffinityUnk5Input", size=(6, 1), disabled=True),
],
[
		sg.Text("Unknown 6", size=(12, 1)),
		sg.In(key="AffinityUnk6Input", size=(6, 1), disabled=True),
],
[
		sg.Text("Unknown 7", size=(12, 1)),
		sg.In(key="AffinityUnk7Input", size=(6, 1), disabled=True),
],
[
		sg.Text("Unknown 8", size=(12, 1)),
		sg.In(key="AffinityUnk8Input", size=(6, 1), disabled=True),
],
]

Tab = [
[
	sg.Column(layout=ColumnAffinityList, vertical_alignment="top"),
	sg.Column(layout=ColumnStrings, vertical_alignment="top"),
	sg.Column(layout=ColumnIntegers, vertical_alignment="top"),
],
]
