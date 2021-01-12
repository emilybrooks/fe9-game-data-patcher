BlockLength = 0x54 # Bytes
NumberOfBlocks = None
OffsetDictionary = {}

StringDataDictionary = {
"PID":        {"Offset": 0x00, "Length": 0x4},
"MPID":       {"Offset": 0x04, "Length": 0x4},
"FID":        {"Offset": 0x0C, "Length": 0x4},
"JID":        {"Offset": 0x10, "Length": 0x4},
"Affinity":   {"Offset": 0x14, "Length": 0x4},
"WeaponRank": {"Offset": 0x18, "Length": 0x4},
"SID1":       {"Offset": 0x1C, "Length": 0x4},
"SID2":       {"Offset": 0x20, "Length": 0x4},
"SID3":       {"Offset": 0x24, "Length": 0x4},
"AID1":       {"Offset": 0x28, "Length": 0x4},
"AID2":       {"Offset": 0x2C, "Length": 0x4},
}

IntegerDataDictionary = {
"UnitIndex":           {"Offset": 0x30, "Length": 0x2, "Signed": False},

# TODO: what does 0x33 control?
"Unk_33":              {"Offset": 0x33, "Length": 0x1, "Signed": False},
"LaguzGauge":          {"Offset": 0x34, "Length": 0x1, "Signed": False},
# TODO: what does 0x35 control?
"Unk_35":              {"Offset": 0x35, "Length": 0x1, "Signed": False},
"Level":               {"Offset": 0x36, "Length": 0x1, "Signed": False},
"Build":               {"Offset": 0x37, "Length": 0x1, "Signed": True},
"Weight":              {"Offset": 0x38, "Length": 0x1, "Signed": True},

"BaseHP":              {"Offset": 0x39, "Length": 0x1, "Signed": True},
"BaseStrength":        {"Offset": 0x3A, "Length": 0x1, "Signed": True},
"BaseMagic":           {"Offset": 0x3B, "Length": 0x1, "Signed": True},
"BaseSkill":           {"Offset": 0x3C, "Length": 0x1, "Signed": True},
"BaseSpeed":           {"Offset": 0x3D, "Length": 0x1, "Signed": True},
"BaseLuck":            {"Offset": 0x3E, "Length": 0x1, "Signed": True},
"BaseDefense":         {"Offset": 0x3F, "Length": 0x1, "Signed": True},
"BaseResistance":      {"Offset": 0x40, "Length": 0x1, "Signed": True},

"GrowthHP":            {"Offset": 0x41, "Length": 0x1, "Signed": False},
"GrowthStrength":      {"Offset": 0x42, "Length": 0x1, "Signed": False},
"GrowthMagic":         {"Offset": 0x43, "Length": 0x1, "Signed": False},
"GrowthSkill":         {"Offset": 0x44, "Length": 0x1, "Signed": False},
"GrowthSpeed":         {"Offset": 0x45, "Length": 0x1, "Signed": False},
"GrowthLuck":          {"Offset": 0x46, "Length": 0x1, "Signed": False},
"GrowthDefense":       {"Offset": 0x47, "Length": 0x1, "Signed": False},
"GrowthResistance":    {"Offset": 0x48, "Length": 0x1, "Signed": False},

"FixedModeHP":         {"Offset": 0x49, "Length": 0x1, "Signed": False},
"FixedModeStrength":   {"Offset": 0x4A, "Length": 0x1, "Signed": False},
"FixedModeMagic":      {"Offset": 0x4B, "Length": 0x1, "Signed": False},
"FixedModeSkill":      {"Offset": 0x4C, "Length": 0x1, "Signed": False},
"FixedModeSpeed":      {"Offset": 0x4D, "Length": 0x1, "Signed": False},
"FixedModeLuck":       {"Offset": 0x4E, "Length": 0x1, "Signed": False},
"FixedModeDefense":    {"Offset": 0x4F, "Length": 0x1, "Signed": False},
"FixedModeResistance": {"Offset": 0x50, "Length": 0x1, "Signed": False},
}
