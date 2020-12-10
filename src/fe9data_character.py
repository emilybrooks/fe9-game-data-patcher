import PySimpleGUI as sg

BlockLength = 0x54 # Bytes
NumberOfBlocks = None
CurrentOffset = None
OffsetDictionary = {}

PIDList = []

StringDataDictionary = {
"PID": {"Offset": 0x0, "Length": 0x4, "Element": "CharacterPIDInput"},
"MPID": {"Offset": 0x4, "Length": 0x4, "Element": "CharacterMPIDInput"},
# supposedly 0x8 to 0xB is always 0
"FID": {"Offset": 0xC, "Length": 0x4, "Element": "CharacterFIDInput"},
"JID": {"Offset": 0x10, "Length": 0x4, "Element": "CharacterJIDInput"},
"Affinity": {"Offset": 0x14, "Length": 0x4, "Element": "CharacterAffinityInput"},
"WeaponRank": {"Offset": 0x18, "Length": 0x4, "Element": "CharacterWeaponRankInput"},
"SID1": {"Offset": 0x1C, "Length": 0x4, "Element": "CharacterSID1Input"},
"SID2": {"Offset": 0x20, "Length": 0x4, "Element": "CharacterSID2Input"},
"SID3": {"Offset": 0x24, "Length": 0x4, "Element": "CharacterSID3Input"},
"AID1": {"Offset": 0x28, "Length": 0x4, "Element": "CharacterAID1Input"},
"AID2": {"Offset": 0x2C, "Length": 0x4, "Element": "CharacterAID2Input"},
}

IntegerDataDictionary = {
# this seems like it's a unique number for every unit in the game, maybe it's a unit id or something
# ike is 1, titania is 2, oscar is 3, boyd is 4, rhys is 5
"Unit Index": {"Offset": 0x30, "Length": 0x2, "Element": "CharacterUnk4Input", "Signed": False},

# always 0
#"Unk6": {"Offset": 0x32, "Length": 0x1, "Element": "CharacterUnk6Input", "Signed": False},

"Unk7": {"Offset": 0x33, "Length": 0x1, "Element": "CharacterUnk7Input", "Signed": False},

# this is what their gauge is when they first join your party
# after that it just carries over between maps
"LaguzGauge": {"Offset": 0x34, "Length": 0x1, "Element": "CharacterLaguzGaugeInput", "Signed": False},

# this seems to be 30 (0x1E) for every character
#"Unk8": {"Offset": 0x35, "Length": 0x1, "Element": "CharacterUnk8Input", "Signed": False},
"Level": {"Offset": 0x36, "Length": 0x1, "Element": "CharacterLevelInput", "Signed": False},
"Build": {"Offset": 0x37, "Length": 0x1, "Element": "CharacterBuildInput", "Signed": True},
"Weight": {"Offset": 0x38, "Length": 0x1, "Element": "CharacterWeightInput", "Signed": True},

# these should be signed
"BaseHP": {"Offset": 0x39, "Length": 0x1, "Element": "CharacterBaseHPInput", "Signed": True},
"BaseStrength": {"Offset": 0x3A, "Length": 0x1, "Element": "CharacterBaseStrengthInput", "Signed": True},
"BaseMagic": {"Offset": 0x3B, "Length": 0x1, "Element": "CharacterBaseMagicInput", "Signed": True},
"BaseSkill": {"Offset": 0x3C, "Length": 0x1, "Element": "CharacterBaseSkillInput", "Signed": True},
"BaseSpeed": {"Offset": 0x3D, "Length": 0x1, "Element": "CharacterBaseSpeedInput", "Signed": True},
"BaseLuck": {"Offset": 0x3E, "Length": 0x1, "Element": "CharacterBaseLuckInput", "Signed": True},
"BaseDefense": {"Offset": 0x3F, "Length": 0x1, "Element": "CharacterBaseDefenseInput", "Signed": True},
"BaseResistance": {"Offset": 0x40, "Length": 0x1, "Element": "CharacterBaseResistanceInput", "Signed": True},

# these should be unsigned, as ena can have a 145 strength growth
"GrowthHP": {"Offset": 0x41, "Length": 0x1, "Element": "CharacterGrowthHPInput", "Signed": False},
"GrowthStrength": {"Offset": 0x42, "Length": 0x1, "Element": "CharacterGrowthStrengthInput", "Signed": False},
"GrowthMagic": {"Offset": 0x43, "Length": 0x1, "Element": "CharacterGrowthMagicInput", "Signed": False},
"GrowthSkill": {"Offset": 0x44, "Length": 0x1, "Element": "CharacterGrowthSkillInput", "Signed": False},
"GrowthSpeed": {"Offset": 0x45, "Length": 0x1, "Element": "CharacterGrowthSpeedInput", "Signed": False},
"GrowthLuck": {"Offset": 0x46, "Length": 0x1, "Element": "CharacterGrowthLuckInput", "Signed": False},
"GrowthDefense": {"Offset": 0x47, "Length": 0x1, "Element": "CharacterGrowthDefenseInput", "Signed": False},
"GrowthResistance": {"Offset": 0x48, "Length": 0x1, "Element": "CharacterGrowthResistanceInput", "Signed": False},

"FixedModeHP": {"Offset": 0x49, "Length": 0x1, "Element": "CharacterFixedModeHPInput", "Signed": False},
"FixedModeStrength": {"Offset": 0x4A, "Length": 0x1, "Element": "CharacterFixedModeStrengthInput", "Signed": False},
"FixedModeMagic": {"Offset": 0x4B, "Length": 0x1, "Element": "CharacterFixedModeMagicInput", "Signed": False},
"FixedModeSkill": {"Offset": 0x4C, "Length": 0x1, "Element": "CharacterFixedModeSkillInput", "Signed": False},
"FixedModeSpeed": {"Offset": 0x4D, "Length": 0x1, "Element": "CharacterFixedModeSpeedInput", "Signed": False},
"FixedModeLuck": {"Offset": 0x4E, "Length": 0x1, "Element": "CharacterFixedModeLuckInput", "Signed": False},
"FixedModeDefense": {"Offset": 0x4F, "Length": 0x1, "Element": "CharacterFixedModeDefenseInput", "Signed": False},
"FixedModeResistance": {"Offset": 0x50, "Length": 0x1, "Element": "CharacterFixedModeResistanceInput", "Signed": False},
# supposedly these are always 0
# "Unk17": {"Offset": 0x51, "Length": 0x1, "Element": "", "Signed": False},
# "Unk18": {"Offset": 0x52, "Length": 0x1, "Element": "", "Signed": False},
# "Unk19": {"Offset": 0x53, "Length": 0x1, "Element": "", "Signed": False},
}

#-------------------------------------------------------------------------------
# GUI Layout
#-------------------------------------------------------------------------------
sg.ChangeLookAndFeel("SystemDefaultForReal")

ColumnPIDList = [
[
	sg.Listbox(key="CharacterListbox",
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
	sg.In(key="CharacterPIDInput", size=(24, 1), disabled=True)
],
[
	sg.Text("Name", size=(12, 1)),
	sg.In(key="CharacterMPIDInput", size=(24, 1), disabled=True)
],
[
	sg.Text("Portrait", size=(12, 1)),
	sg.In(key="CharacterFIDInput", size=(24, 1), disabled=True)
],
[
	sg.Text("Class", size=(12, 1)),
	sg.In(key="CharacterJIDInput", size=(24, 1), disabled=True)
],
[
	sg.Text("Affinity", size=(12, 1)),
	sg.In(key="CharacterAffinityInput", size=(24, 1), disabled=True)
],
[
	sg.Text("Weapon Ranks", size=(12, 1)),
	sg.In(key="CharacterWeaponRankInput", size=(24, 1), disabled=True)
],
[
	sg.Text("Skill 1", size=(12, 1)),
	sg.In(key="CharacterSID1Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Skill 2", size=(12, 1)),
	sg.In(key="CharacterSID2Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Skill 3", size=(12, 1)),
	sg.In(key="CharacterSID3Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Model 1", size=(12, 1)),
	sg.In(key="CharacterAID1Input", size=(24, 1), disabled=True)
],
[
	sg.Text("Model 2", size=(12, 1)),
	sg.In(key="CharacterAID2Input", size=(24, 1), disabled=True)
],
]

FrameBaseStats = [
[
	sg.Text("HP ", size=(3, 1)),
	sg.In(key="CharacterBaseHPInput", size=(4, 1), disabled=True),
	sg.Text("Spd", size=(3, 1)),
	sg.In(key="CharacterBaseSpeedInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Str", size=(3, 1)),
	sg.In(key="CharacterBaseStrengthInput", size=(4, 1), disabled=True),
	sg.Text("Lck", size=(3, 1)),
	sg.In(key="CharacterBaseLuckInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Mag", size=(3, 1)),
	sg.In(key="CharacterBaseMagicInput", size=(4, 1), disabled=True),
	sg.Text("Def", size=(3, 1)),
	sg.In(key="CharacterBaseDefenseInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Skl", size=(3, 1)),
	sg.In(key="CharacterBaseSkillInput", size=(4, 1), disabled=True),
	sg.Text("Res", size=(3, 1)),
	sg.In(key="CharacterBaseResistanceInput", size=(4, 1), disabled=True),
]
]

FrameGrowths =[
[
	sg.Text("HP ", size=(3, 1)),
	sg.In(key="CharacterGrowthHPInput", size=(4, 1), disabled=True),
	sg.Text("Spd", size=(3, 1)),
	sg.In(key="CharacterGrowthSpeedInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Str", size=(3, 1)),
	sg.In(key="CharacterGrowthStrengthInput", size=(4, 1), disabled=True),
	sg.Text("Lck", size=(3, 1)),
	sg.In(key="CharacterGrowthLuckInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Mag", size=(3, 1)),
	sg.In(key="CharacterGrowthMagicInput", size=(4, 1), disabled=True),
	sg.Text("Def", size=(3, 1)),
	sg.In(key="CharacterGrowthDefenseInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Skl", size=(3, 1)),
	sg.In(key="CharacterGrowthSkillInput", size=(4, 1), disabled=True),
	sg.Text("Res", size=(3, 1)),
	sg.In(key="CharacterGrowthResistanceInput", size=(4, 1), disabled=True),
]
]

FrameFixedMode =[
[
	sg.Text("HP ", size=(3, 1)),
	sg.In(key="CharacterFixedModeHPInput", size=(4, 1), disabled=True),
	sg.Text("Spd", size=(3, 1)),
	sg.In(key="CharacterFixedModeSpeedInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Str", size=(3, 1)),
	sg.In(key="CharacterFixedModeStrengthInput", size=(4, 1), disabled=True),
	sg.Text("Lck", size=(3, 1)),
	sg.In(key="CharacterFixedModeLuckInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Mag", size=(3, 1)),
	sg.In(key="CharacterFixedModeMagicInput", size=(4, 1), disabled=True),
	sg.Text("Def", size=(3, 1)),
	sg.In(key="CharacterFixedModeDefenseInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Skl", size=(3, 1)),
	sg.In(key="CharacterFixedModeSkillInput", size=(4, 1), disabled=True),
	sg.Text("Res", size=(3, 1)),
	sg.In(key="CharacterFixedModeResistanceInput", size=(4, 1), disabled=True),
]
]

ColumnStats = [
[
	sg.Text("Level"),
	sg.In(key="CharacterLevelInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Build"),
	sg.In(key="CharacterBuildInput", size=(4, 1), disabled=True),
	sg.Text("Wt.  "),
	sg.In(key="CharacterWeightInput", size=(4, 1), disabled=True),
],
[
	sg.Frame(title="Base Stats", layout=FrameBaseStats),
],
[
	sg.Frame(title="Growths", layout=FrameGrowths)
],
[
	sg.Frame(title="Fixed Mode Initial Points", layout=FrameFixedMode)
],
[
	sg.Text("Unit Index", size=(12, 1)),
	sg.In(key="CharacterUnk4Input", size=(4, 1), disabled=True),
],
[
	sg.Text("Unknown 7", size=(12, 1)),
	sg.In(key="CharacterUnk7Input", size=(4, 1), disabled=True),
],
[
	sg.Text("Laguz Gauge Initial Value"),
	sg.In(key="CharacterLaguzGaugeInput", size=(4, 1), disabled=True),
],
[
	sg.Text("Unknown 8", size=(12, 1)),
	sg.In(key="CharacterUnk8Input", size=(4, 1), disabled=True),
],
[
	sg.Button("Apply Changes", key="CharacterApplyButton", disabled=True)
],
]

Tab = [
[
	sg.Column(layout=ColumnPIDList, vertical_alignment="top"),
	sg.Column(layout=ColumnStrings, vertical_alignment="top"),
	sg.Column(layout=ColumnStats, vertical_alignment="top"),
],
]
