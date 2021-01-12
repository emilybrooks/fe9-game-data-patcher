BlockLength = 0x60 # Bytes
NumberOfBlocks = None
OffsetDictionary = {}

StringDataDictionary = {
"JID":            {"Offset": 0x00, "Length": 0x4},
"MIID":           {"Offset": 0x04, "Length": 0x4},
"MH_I":           {"Offset": 0x08, "Length": 0x4},
"Type1":          {"Offset": 0x0C, "Length": 0x4},
"Type2":          {"Offset": 0x10, "Length": 0x4},
"Rank":           {"Offset": 0x14, "Length": 0x4},
"Trait1":         {"Offset": 0x18, "Length": 0x4},
"Trait2":         {"Offset": 0x1C, "Length": 0x4},
"Trait3":         {"Offset": 0x20, "Length": 0x4},
"Trait4":         {"Offset": 0x24, "Length": 0x4},
"Trait5":         {"Offset": 0x28, "Length": 0x4},
"Trait6":         {"Offset": 0x2C, "Length": 0x4},
"EffectiveType1": {"Offset": 0x30, "Length": 0x4},
"EffectiveType2": {"Offset": 0x34, "Length": 0x4},
"EID1":           {"Offset": 0x38, "Length": 0x4},
"EID2":           {"Offset": 0x3C, "Length": 0x4},
}

IntegerDataDictionary = {
"Price":                  {"Offset": 0x40, "Length": 0x2, "Signed": False},
"Durability":             {"Offset": 0x42, "Length": 0x1, "Signed": False},
"Might":                  {"Offset": 0x43, "Length": 0x1, "Signed": False},
"Accuracy":               {"Offset": 0x44, "Length": 0x1, "Signed": False},
"Weight":                 {"Offset": 0x45, "Length": 0x1, "Signed": False},
"Critical":               {"Offset": 0x46, "Length": 0x1, "Signed": False},
"Min Range":              {"Offset": 0x47, "Length": 0x1, "Signed": False},
"Max Range":              {"Offset": 0x48, "Length": 0x1, "Signed": False},
"Icon":                   {"Offset": 0x49, "Length": 0x1, "Signed": False},
"Experience":             {"Offset": 0x4A, "Length": 0x1, "Signed": False},

"BonusHP":                {"Offset": 0x4B, "Length": 0x1, "Signed": False},
"BonusStrength":          {"Offset": 0x4C, "Length": 0x1, "Signed": False},
"BonusMagic":             {"Offset": 0x4D, "Length": 0x1, "Signed": False},
"BonusSkill":             {"Offset": 0x4E, "Length": 0x1, "Signed": False},
"BonusSpeed":             {"Offset": 0x4F, "Length": 0x1, "Signed": False},
"BonusLuck":              {"Offset": 0x50, "Length": 0x1, "Signed": False},
"BonusDefense":           {"Offset": 0x51, "Length": 0x1, "Signed": False},
"BonusResistance":        {"Offset": 0x52, "Length": 0x1, "Signed": False},

"Move Increase":          {"Offset": 0x53, "Length": 0x1, "Signed": False},
"Build Increase":         {"Offset": 0x54, "Length": 0x1, "Signed": False},

"FixedModeHP":            {"Offset": 0x55, "Length": 0x1, "Signed": True},
"FixedModeStrength":      {"Offset": 0x56, "Length": 0x1, "Signed": True},
"FixedModeMagic":         {"Offset": 0x57, "Length": 0x1, "Signed": True},
"FixedModeSkill":         {"Offset": 0x58, "Length": 0x1, "Signed": True},
"FixedModeSpeed":         {"Offset": 0x59, "Length": 0x1, "Signed": True},
"FixedModeLuck":          {"Offset": 0x5A, "Length": 0x1, "Signed": True},
"FixedModeDefense":       {"Offset": 0x5B, "Length": 0x1, "Signed": True},
"FixedModeResistance":    {"Offset": 0x5C, "Length": 0x1, "Signed": True},

"Unk_5D":                 {"Offset": 0x5D, "Length": 0x1, "Signed": False},
}
