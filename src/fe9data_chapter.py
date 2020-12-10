import PySimpleGUI as sg

BlockLength = 0x5C # Bytes
# english has it at 0x60
# BlockLength = 0x60 # Bytes
NumberOfBlocks = None
CurrentOffset = None
OffsetDictionary = {}

ChapterList = []

# 0x1378C
StringDataDictionary = {
"ID": {"Offset": 0x0, "Length": 0x4, "Element": "ChapterNameInput"},
"unk1": {"Offset": 0x4, "Length": 0x4, "Element": "ChapterUnk1Input"},
"unk2": {"Offset": 0x8, "Length": 0x4, "Element": "ChapterUnk2Input"},
"unk3": {"Offset": 0xC, "Length": 0x4, "Element": "ChapterUnk3Input"},
"unk4": {"Offset": 0x10, "Length": 0x4, "Element": "ChapterUnk4Input"},
"unk5": {"Offset": 0x14, "Length": 0x4, "Element": "ChapterUnk5Input"},
# always 0
# "unk6": {"Offset": 0x18, "Length": 0x4, "Element": "ChapterUnk6Input"},
"unk7": {"Offset": 0x1C, "Length": 0x4, "Element": "ChapterUnk7Input"},
"unk8": {"Offset": 0x20, "Length": 0x4, "Element": "ChapterUnk8Input"},
"unk9": {"Offset": 0x24, "Length": 0x4, "Element": "ChapterUnk9Input"},
# always 0
# "unk10": {"Offset": 0x28, "Length": 0x4, "Element": "ChapterUnk10Input"},
"unk11": {"Offset": 0x2C, "Length": 0x4, "Element": "ChapterUnk11Input"},
"unk12": {"Offset": 0x30, "Length": 0x4, "Element": "ChapterUnk12Input"},
# always 0
# "unk13": {"Offset": 0x34, "Length": 0x4, "Element": "ChapterUnk13Input"},
"unk14": {"Offset": 0x38, "Length": 0x4, "Element": "ChapterUnk14Input"},
# i think this might be an int?
# these crash loading the english file so commenting out for now
# "unk16": {"Offset": 0x40, "Length": 0x4, "Element": "ChapterUnk16Input"},
"unk17": {"Offset": 0x44, "Length": 0x4, "Element": "ChapterUnk17Input"},
"unk18": {"Offset": 0x48, "Length": 0x4, "Element": "ChapterUnk18Input"},
"unk19": {"Offset": 0x4C, "Length": 0x4, "Element": "ChapterUnk19Input"},
}

IntegerDataDictionary = {
#"Unk20": {"Offset": 0x50, "Length": 0x1, "Element": "ChapterUnk20Input", "Signed": False},
"Unk20": {"Offset": 0x3C, "Length": 0x1, "Element": "ChapterUnk20Input", "Signed": False},
"Unk21": {"Offset": 0x50, "Length": 0x1, "Element": "ChapterUnk21Input", "Signed": False},
"Unk22": {"Offset": 0x51, "Length": 0x1, "Element": "ChapterUnk22Input", "Signed": False},
"Unk23": {"Offset": 0x52, "Length": 0x1, "Element": "ChapterUnk23Input", "Signed": False},
"Unk24": {"Offset": 0x53, "Length": 0x1, "Element": "ChapterUnk24Input", "Signed": False},
"Unk25": {"Offset": 0x54, "Length": 0x1, "Element": "ChapterUnk25Input", "Signed": False},
"Unk26": {"Offset": 0x55, "Length": 0x1, "Element": "ChapterUnk26Input", "Signed": False},
"Unk27": {"Offset": 0x56, "Length": 0x1, "Element": "ChapterUnk27Input", "Signed": False},
"Unk28": {"Offset": 0x57, "Length": 0x1, "Element": "ChapterUnk28Input", "Signed": False},
"Unk29": {"Offset": 0x58, "Length": 0x1, "Element": "ChapterUnk29Input", "Signed": False},
#0x3C is the "CXX" thing but just the number
# i think the next 2 bytes are padding
# then 0x3F is an int, it seems to be 0x02 multiple times

}

#-------------------------------------------------------------------------------
# GUI Layout
#-------------------------------------------------------------------------------
sg.ChangeLookAndFeel("SystemDefaultForReal")

ColumnChapterList = [
[
	sg.Listbox(key="ChapterListbox",
			   values=(""),
			   select_mode="LISTBOX_SELECT_MODE_SINGLE",
			   size=(24, 18),
			   disabled=True,
			   enable_events=True)
],
]

ColumnStrings = [
[
	sg.Text("Name", size=(12, 1)),
	sg.In(key="ChapterNameInput", size=(24, 1), disabled=True)
],
[
	sg.Text("Unknown 1", size=(12, 1)),
	sg.In(key="ChapterUnk1Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Unknown 2", size=(12, 1)),
	sg.In(key="ChapterUnk2Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Unknown 3", size=(12, 1)),
	sg.In(key="ChapterUnk3Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Unknown 4", size=(12, 1)),
	sg.In(key="ChapterUnk4Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Unknown 5", size=(12, 1)),
	sg.In(key="ChapterUnk5Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Unknown 7", size=(12, 1)),
	sg.In(key="ChapterUnk7Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Unknown 8", size=(12, 1)),
	sg.In(key="ChapterUnk8Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Unknown 9", size=(12, 1)),
	sg.In(key="ChapterUnk9Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Unknown 11", size=(12, 1)),
	sg.In(key="ChapterUnk11Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Unknown 12", size=(12, 1)),
	sg.In(key="ChapterUnk12Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Unknown 14", size=(12, 1)),
	sg.In(key="ChapterUnk14Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Unknown 16", size=(12, 1)),
	sg.In(key="ChapterUnk16Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Unknown 17", size=(12, 1)),
	sg.In(key="ChapterUnk17Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Unknown 18", size=(12, 1)),
	sg.In(key="ChapterUnk18Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Unknown 19", size=(12, 1)),
	sg.In(key="ChapterUnk19Input", size=(24, 1), disabled=True)
],
]

ColumnIntegers = [
[
		sg.Text("Unknown 20", size=(12, 1)),
		sg.In(key="ChapterUnk20Input", size=(6, 1), disabled=True),
],
[
		sg.Text("Unknown 21", size=(12, 1)),
		sg.In(key="ChapterUnk21Input", size=(6, 1), disabled=True),
],
[
		sg.Text("Unknown 22", size=(12, 1)),
		sg.In(key="ChapterUnk22Input", size=(6, 1), disabled=True),
],
[
		sg.Text("Unknown 23", size=(12, 1)),
		sg.In(key="ChapterUnk23Input", size=(6, 1), disabled=True),
],
[
		sg.Text("Unknown 24", size=(12, 1)),
		sg.In(key="ChapterUnk24Input", size=(6, 1), disabled=True),
],
[
		sg.Text("Unknown 25", size=(12, 1)),
		sg.In(key="ChapterUnk25Input", size=(6, 1), disabled=True),
],
[
		sg.Text("Unknown 26", size=(12, 1)),
		sg.In(key="ChapterUnk26Input", size=(6, 1), disabled=True),
],
[
		sg.Text("Unknown 27", size=(12, 1)),
		sg.In(key="ChapterUnk27Input", size=(6, 1), disabled=True),
],
[
		sg.Text("Unknown 28", size=(12, 1)),
		sg.In(key="ChapterUnk28Input", size=(6, 1), disabled=True),
],
[
		sg.Text("Unknown 29", size=(12, 1)),
		sg.In(key="ChapterUnk29Input", size=(6, 1), disabled=True),
],
[
	sg.Button("Apply Changes", key="ChapterApplyButton", disabled=True)
],
]

Tab = [
[
	sg.Column(layout=ColumnChapterList, vertical_alignment="top"),
	sg.Column(layout=ColumnStrings, vertical_alignment="top"),
	sg.Column(layout=ColumnIntegers, vertical_alignment="top"),
],
]
