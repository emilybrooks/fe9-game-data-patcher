import PySimpleGUI as sg

BlockLength = 0x60 # Bytes
NumberOfBlocks = None
CurrentOffset = None
OffsetDictionary = {}

IIDList = []

StringDataDictionary = {
"JID": {"Offset": 0x0, "Length": 0x4, "Element": "ItemIIDInput"},
"MIID": {"Offset": 0x4, "Length": 0x4, "Element": "ItemMIIDInput"},
"MH_I": {"Offset": 0x8, "Length": 0x4, "Element": "ItemMH_IInput"},
"Type1": {"Offset": 0xC, "Length": 0x4, "Element": "ItemType1Input"},
"Type2": {"Offset": 0x10, "Length": 0x4, "Element": "ItemType2Input"},
"Rank": {"Offset": 0x14, "Length": 0x4, "Element": "ItemRankInput"},
# i think trait 1 is what weapon rank is required to use it
"Trait1": {"Offset": 0x18, "Length": 0x4, "Element": "ItemTrait1Input"},
# type 2 affects if it does physical or magical
# it might affects weapon triangle?
"Trait2": {"Offset": 0x1C, "Length": 0x4, "Element": "ItemTrait2Input"},
"Trait3": {"Offset": 0x20, "Length": 0x4, "Element": "ItemTrait3Input"},
"Trait4": {"Offset": 0x24, "Length": 0x4, "Element": "ItemTrait4Input"},
"Trait5": {"Offset": 0x28, "Length": 0x4, "Element": "ItemTrait5Input"},
"Trait6": {"Offset": 0x2C, "Length": 0x4, "Element": "ItemTrait6Input"},
"EffectiveType1": {"Offset": 0x30, "Length": 0x4, "Element": "ItemEffectiveType1Input"},
"EffectiveType2": {"Offset": 0x34, "Length": 0x4, "Element": "ItemEffectiveType2Input"},
"EID1": {"Offset": 0x38, "Length": 0x4, "Element": "ItemEID1Input"},
"EID2": {"Offset": 0x3C, "Length": 0x4, "Element": "ItemEID2Input"},
}

IntegerDataDictionary = {
"Price": {"Offset": 0x40, "Length": 0x2, "Element": "ItemPriceInput", "Signed": False},
"Durability": {"Offset": 0x42, "Length": 0x1, "Element": "ItemDurabilityInput", "Signed": False},
"Might": {"Offset": 0x43, "Length": 0x1, "Element": "ItemMightInput", "Signed": False},
"Accuracy": {"Offset": 0x44, "Length": 0x1, "Element": "ItemAccuracyInput", "Signed": False},
"Weight": {"Offset": 0x45, "Length": 0x1, "Element": "ItemWeightInput", "Signed": False},
"Critical": {"Offset": 0x46, "Length": 0x1, "Element": "ItemCriticalInput", "Signed": False},
"Min Range": {"Offset": 0x47, "Length": 0x1, "Element": "ItemMinRangeInput", "Signed": False},
"Max Range": {"Offset": 0x48, "Length": 0x1, "Element": "ItemMaxRangeInput", "Signed": False},
"Icon": {"Offset": 0x49, "Length": 0x1, "Element": "ItemIconInput", "Signed": False},
"Experience": {"Offset": 0x4A, "Length": 0x1, "Element": "ItemExperienceInput", "Signed": False},
"BonusHP": {"Offset": 0x4B, "Length": 0x1, "Element": "ItemBonusHPInput", "Signed": False},
"BonusStrength": {"Offset": 0x4C, "Length": 0x1, "Element": "ItemBonusStrengthInput", "Signed": False},
"BonusMagic": {"Offset": 0x4D, "Length": 0x1, "Element": "ItemBonusMagicInput", "Signed": False},
"BonusSkill": {"Offset": 0x4E, "Length": 0x1, "Element": "ItemBonusSkillInput", "Signed": False},
"BonusSpeed": {"Offset": 0x4F, "Length": 0x1, "Element": "ItemBonusSpeedInput", "Signed": False},
"BonusLuck": {"Offset": 0x50, "Length": 0x1, "Element": "ItemBonusLuckInput", "Signed": False},
"BonusDefense": {"Offset": 0x51, "Length": 0x1, "Element": "ItemBonusDefenseInput", "Signed": False},
"BonusResistance": {"Offset": 0x52, "Length": 0x1, "Element": "ItemBonusResistanceInput", "Signed": False},
# still a big gap at the end
}

#-------------------------------------------------------------------------------
# GUI Layout
#-------------------------------------------------------------------------------
sg.ChangeLookAndFeel("SystemDefaultForReal")

ColumnIIDList = [
[
	sg.Listbox(key="ItemListbox",
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
	sg.In(key="ItemIIDInput", size=(24, 1), disabled=True)
],
[
	sg.Text("Name", size=(12, 1)),
	sg.In(key="ItemMIIDInput", size=(24, 1), disabled=True)
],
[
	sg.Text("Description", size=(12, 1)),
	sg.In(key="ItemMH_IInput", size=(24, 1), disabled=True)
],
[
	sg.Text("Type 1", size=(12, 1)),
	sg.In(key="ItemType1Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Type 2", size=(12, 1)),
	sg.In(key="ItemType2Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Rank", size=(12, 1)),
	sg.In(key="ItemRankInput", size=(24, 1), disabled=True)
],
[
	sg.Text("Trait 1", size=(12, 1)),
	sg.In(key="ItemTrait1Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Trait 2", size=(12, 1)),
	sg.In(key="ItemTrait2Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Trait 3", size=(12, 1)),
	sg.In(key="ItemTrait3Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Trait 4", size=(12, 1)),
	sg.In(key="ItemTrait4Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Trait 5", size=(12, 1)),
	sg.In(key="ItemTrait5Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Trait 6", size=(12, 1)),
	sg.In(key="ItemTrait6Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Effective Type 1", size=(12, 1)),
	sg.In(key="ItemEffectiveType1Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Effective Type 2", size=(12, 1)),
	sg.In(key="ItemEffectiveType2Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Animation 1", size=(12, 1)),
	sg.In(key="ItemEID1Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Animation 2", size=(12, 1)),
	sg.In(key="ItemEID2Input", size=(24, 1), disabled=True)
],
]

FrameBonusStats = [
[
	sg.Text("HP ", size=(3, 1)),
	sg.In(key="ItemBonusHPInput", size=(4, 1), disabled=True),
	sg.Text("Spd", size=(3, 1)),
	sg.In(key="ItemBonusSpeedInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Str", size=(3, 1)),
	sg.In(key="ItemBonusStrengthInput", size=(4, 1), disabled=True),
	sg.Text("Lck", size=(3, 1)),
	sg.In(key="ItemBonusLuckInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Mag", size=(3, 1)),
	sg.In(key="ItemBonusMagicInput", size=(4, 1), disabled=True),
	sg.Text("Def", size=(3, 1)),
	sg.In(key="ItemBonusDefenseInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Skl", size=(3, 1)),
	sg.In(key="ItemBonusSkillInput", size=(4, 1), disabled=True),
	sg.Text("Res", size=(3, 1)),
	sg.In(key="ItemBonusResistanceInput", size=(4, 1), disabled=True),
]
]

ColumnThree = [
[
		sg.Text("Unit Price", size=(12, 1)),
		sg.In(key="ItemPriceInput", size=(6, 1), disabled=True),
],
[
		sg.Text("Durability", size=(12, 1)),
		sg.In(key="ItemDurabilityInput", size=(4, 1), disabled=True),
],
[
		sg.Text("Might", size=(12, 1)),
		sg.In(key="ItemMightInput", size=(4, 1), disabled=True),
],
[
		sg.Text("Accuracy", size=(12, 1)),
		sg.In(key="ItemAccuracyInput", size=(4, 1), disabled=True),
],
[
		sg.Text("Weight", size=(12, 1)),
		sg.In(key="ItemWeightInput", size=(4, 1), disabled=True),
],
[
		sg.Text("Critical", size=(12, 1)),
		sg.In(key="ItemCriticalInput", size=(4, 1), disabled=True),
],
[
		sg.Text("Minimum Range", size=(12, 1)),
		sg.In(key="ItemMinRangeInput", size=(4, 1), disabled=True),
],
[
		sg.Text("Maximum Range", size=(12, 1)),
		sg.In(key="ItemMaxRangeInput", size=(4, 1), disabled=True),
],
[
		sg.Text("Icon Index", size=(12, 1)),
		sg.In(key="ItemIconInput", size=(4, 1), disabled=True),
],
[
		sg.Text("Experience", size=(12, 1)),
		sg.In(key="ItemExperienceInput", size=(4, 1), disabled=True),
],
[
	sg.Frame(title="Stat Bonuses", layout=FrameBonusStats),
],
[
	sg.Button("Apply Changes", key="ItemApplyButton", disabled=True)
],
]

Tab = [
[
	sg.Column(layout=ColumnIIDList, vertical_alignment="top"),
	sg.Column(layout=ColumnStrings, vertical_alignment="top"),
	sg.Column(layout=ColumnThree, vertical_alignment="top"),
],
]
