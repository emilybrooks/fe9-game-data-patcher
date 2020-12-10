import PySimpleGUI as sg

BlockLength = 0x64 # Bytes
NumberOfBlocks = None
CurrentOffset = None
OffsetDictionary = {}

JIDList = []

StringDataDictionary = {
"JID": {"Offset": 0x0, "Length": 0x4, "Element": "ClassJIDInput"},
"MJID": {"Offset": 0x4, "Length": 0x4, "Element": "ClassMJIDInput"},
"MH_J": {"Offset": 0x8, "Length": 0x4, "Element": "ClassMH_JInput"},
"Promote": {"Offset": 0xC, "Length": 0x4, "Element": "ClassPromoteInput"},
"DefaultWeapon": {"Offset": 0x10, "Length": 0x4, "Element": "ClassDefaultWeaponInput"},
"WeaponRank": {"Offset": 0x14, "Length": 0x4, "Element": "ClassWeaponRankInput"},
"SID1": {"Offset": 0x18, "Length": 0x4, "Element": "ClassSID1Input"},
"SID2": {"Offset": 0x1C, "Length": 0x4, "Element": "ClassSID2Input"},
"SID3": {"Offset": 0x20, "Length": 0x4, "Element": "ClassSID3Input"},
# gap?
"Race": {"Offset": 0x2C, "Length": 0x4, "Element": "ClassRaceInput"},
"Type": {"Offset": 0x30, "Length": 0x4, "Element": "ClassTypeInput"},
# gap?
"AID": {"Offset": 0x38, "Length": 0x4, "Element": "ClassAIDInput"},
}

IntegerDataDictionary = {
"Build": {"Offset": 0x3C, "Length": 0x1, "Element": "ClassBuildInput", "Signed": True},
"Weight": {"Offset": 0x3D, "Length": 0x1, "Element": "ClassWeightInput", "Signed": True},
"Move": {"Offset": 0x3E, "Length": 0x1, "Element": "ClassMoveInput", "Signed": True},
# gap?
"Skill Capacity": {"Offset": 0x40, "Length": 0x1, "Element": "ClassSkillCapacityInput", "Signed": False},
# gap?
"BaseHP": {"Offset": 0x44, "Length": 0x1, "Element": "ClassBaseHPInput", "Signed": True},
"BaseStrength": {"Offset": 0x45, "Length": 0x1, "Element": "ClassBaseStrengthInput", "Signed": True},
"BaseMagic": {"Offset": 0x46, "Length": 0x1, "Element": "ClassBaseMagicInput", "Signed": True},
"BaseSkill": {"Offset": 0x47, "Length": 0x1, "Element": "ClassBaseSkillInput", "Signed": True},
"BaseSpeed": {"Offset": 0x48, "Length": 0x1, "Element": "ClassBaseSpeedInput", "Signed": True},
"BaseLuck": {"Offset": 0x49, "Length": 0x1, "Element": "ClassBaseLuckInput", "Signed": True},
"BaseDefense": {"Offset": 0x4A, "Length": 0x1, "Element": "ClassBaseDefenseInput", "Signed": True},
"BaseResistance": {"Offset": 0x4B, "Length": 0x1, "Element": "ClassBaseResistanceInput", "Signed": True},
"MaxHP": {"Offset": 0x4C, "Length": 0x1, "Element": "ClassMaxHPInput", "Signed": True},
"MaxStrength": {"Offset": 0x4D, "Length": 0x1, "Element": "ClassMaxStrengthInput", "Signed": True},
"MaxMagic": {"Offset": 0x4E, "Length": 0x1, "Element": "ClassMaxMagicInput", "Signed": True},
"MaxSkill": {"Offset": 0x4F, "Length": 0x1, "Element": "ClassMaxSkillInput", "Signed": True},
"MaxSpeed": {"Offset": 0x50, "Length": 0x1, "Element": "ClassMaxSpeedInput", "Signed": True},
"MaxLuck": {"Offset": 0x51, "Length": 0x1, "Element": "ClassMaxLuckInput", "Signed": True},
"MaxDefense": {"Offset": 0x52, "Length": 0x1, "Element": "ClassMaxDefenseInput", "Signed": True},
"MaxResistance": {"Offset": 0x53, "Length": 0x1, "Element": "ClassMaxResistanceInput", "Signed": True},
"GrowthHP": {"Offset": 0x54, "Length": 0x1, "Element": "ClassGrowthHPInput", "Signed": True},
"GrowthStrength": {"Offset": 0x55, "Length": 0x1, "Element": "ClassGrowthStrengthInput", "Signed": True},
"GrowthMagic": {"Offset": 0x56, "Length": 0x1, "Element": "ClassGrowthMagicInput", "Signed": True},
"GrowthSkill": {"Offset": 0x57, "Length": 0x1, "Element": "ClassGrowthSkillInput", "Signed": True},
"GrowthSpeed": {"Offset": 0x58, "Length": 0x1, "Element": "ClassGrowthSpeedInput", "Signed": True},
"GrowthLuck": {"Offset": 0x59, "Length": 0x1, "Element": "ClassGrowthLuckInput", "Signed": True},
"GrowthDefense": {"Offset": 0x5A, "Length": 0x1, "Element": "ClassGrowthDefenseInput", "Signed": True},
"GrowthResistance": {"Offset": 0x5B, "Length": 0x1, "Element": "ClassGrowthResistanceInput", "Signed": True},
}

# apparently there's laguz data at 0x5C for 8 bytes

#-------------------------------------------------------------------------------
# GUI Layout
#-------------------------------------------------------------------------------
sg.ChangeLookAndFeel("SystemDefaultForReal")

ColumnJIDList = [
[
	sg.Listbox(key="ClassListbox",
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
	sg.In(key="ClassJIDInput", size=(24, 1), disabled=True)
],
[
	sg.Text("Name", size=(12, 1)),
	sg.In(key="ClassMJIDInput", size=(24, 1), disabled=True)
],
[
	sg.Text("Description", size=(12, 1)),
	sg.In(key="ClassMH_JInput", size=(24, 1), disabled=True)
],
[
	sg.Text("Promoted Class", size=(12, 1)),
	sg.In(key="ClassPromoteInput", size=(24, 1), disabled=True)
],
[
	sg.Text("Default Weapon", size=(12, 1)),
	sg.In(key="ClassDefaultWeaponInput", size=(24, 1), disabled=True)
],
[
	sg.Text("Weapon Rank", size=(12, 1)),
	sg.In(key="ClassWeaponRankInput", size=(24, 1), disabled=True)
],
[
	sg.Text("Skill 1", size=(12, 1)),
	sg.In(key="ClassSID1Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Skill 2", size=(12, 1)),
	sg.In(key="ClassSID2Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Skill 3", size=(12, 1)),
	sg.In(key="ClassSID3Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Race", size=(12, 1)),
	sg.In(key="ClassRaceInput", size=(24, 1), disabled=True)
],
[
	sg.Text("Type", size=(12, 1)),
	sg.In(key="ClassTypeInput", size=(24, 1), disabled=True)
],
[
	sg.Text("Model", size=(12, 1)),
	sg.In(key="ClassAIDInput", size=(24, 1), disabled=True)
],
[
	sg.Text("Build", size=(12, 1)),
	sg.In(key="ClassBuildInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Weight", size=(12, 1)),
	sg.In(key="ClassWeightInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Move", size=(12, 1)),
	sg.In(key="ClassMoveInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Skill Capacity", size=(12, 1)),
	sg.In(key="ClassSkillCapacityInput", size=(4, 1), disabled=True),
],
]

FrameBaseStats = [
[
	sg.Text("HP ", size=(3, 1)),
	sg.In(key="ClassBaseHPInput", size=(4, 1), disabled=True),
	sg.Text("Spd", size=(3, 1)),
	sg.In(key="ClassBaseSpeedInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Str", size=(3, 1)),
	sg.In(key="ClassBaseStrengthInput", size=(4, 1), disabled=True),
	sg.Text("Lck", size=(3, 1)),
	sg.In(key="ClassBaseLuckInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Mag", size=(3, 1)),
	sg.In(key="ClassBaseMagicInput", size=(4, 1), disabled=True),
	sg.Text("Def", size=(3, 1)),
	sg.In(key="ClassBaseDefenseInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Skl", size=(3, 1)),
	sg.In(key="ClassBaseSkillInput", size=(4, 1), disabled=True),
	sg.Text("Res", size=(3, 1)),
	sg.In(key="ClassBaseResistanceInput", size=(4, 1), disabled=True),
]
]

FrameMaxStats = [
[
	sg.Text("HP ", size=(3, 1)),
	sg.In(key="ClassMaxHPInput", size=(4, 1), disabled=True),
	sg.Text("Spd", size=(3, 1)),
	sg.In(key="ClassMaxSpeedInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Str", size=(3, 1)),
	sg.In(key="ClassMaxStrengthInput", size=(4, 1), disabled=True),
	sg.Text("Lck", size=(3, 1)),
	sg.In(key="ClassMaxLuckInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Mag", size=(3, 1)),
	sg.In(key="ClassMaxMagicInput", size=(4, 1), disabled=True),
	sg.Text("Def", size=(3, 1)),
	sg.In(key="ClassMaxDefenseInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Skl", size=(3, 1)),
	sg.In(key="ClassMaxSkillInput", size=(4, 1), disabled=True),
	sg.Text("Res", size=(3, 1)),
	sg.In(key="ClassMaxResistanceInput", size=(4, 1), disabled=True),
]
]

FrameGrowths = [
[
	sg.Text("HP ", size=(3, 1)),
	sg.In(key="ClassGrowthHPInput", size=(4, 1), disabled=True),
	sg.Text("Spd", size=(3, 1)),
	sg.In(key="ClassGrowthSpeedInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Str", size=(3, 1)),
	sg.In(key="ClassGrowthStrengthInput", size=(4, 1), disabled=True),
	sg.Text("Lck", size=(3, 1)),
	sg.In(key="ClassGrowthLuckInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Mag", size=(3, 1)),
	sg.In(key="ClassGrowthMagicInput", size=(4, 1), disabled=True),
	sg.Text("Def", size=(3, 1)),
	sg.In(key="ClassGrowthDefenseInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Skl", size=(3, 1)),
	sg.In(key="ClassGrowthSkillInput", size=(4, 1), disabled=True),
	sg.Text("Res", size=(3, 1)),
	sg.In(key="ClassGrowthResistanceInput", size=(4, 1), disabled=True),
]
]

ColumnStats = [
[
	sg.Frame(title="Base Stats", layout=FrameBaseStats),
],
[
	sg.Frame(title="Stat Caps", layout=FrameMaxStats),
],
[
	sg.Frame(title="Growths", layout=FrameGrowths),
],
[
	sg.Button("Apply Changes", key="ClassApplyButton", disabled=True)
],
]

Tab = [
[
	sg.Column(layout=ColumnJIDList, vertical_alignment="top"),
	sg.Column(layout=ColumnStrings, vertical_alignment="top"),
	sg.Column(layout=ColumnStats, vertical_alignment="top"),
],
]
