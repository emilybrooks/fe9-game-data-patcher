BlockLength = 0x64 # Bytes
NumberOfBlocks = None
OffsetDictionary = {}

StringDataDictionary = {
"JID":           {"Offset": 0x00, "Length": 0x4},
"MJID":          {"Offset": 0x04, "Length": 0x4},
"MH_J":          {"Offset": 0x08, "Length": 0x4},
"Promote":       {"Offset": 0x0C, "Length": 0x4},
"DefaultWeapon": {"Offset": 0x10, "Length": 0x4},
"WeaponRank":    {"Offset": 0x14, "Length": 0x4},
"SID1":          {"Offset": 0x18, "Length": 0x4},
"SID2":          {"Offset": 0x1C, "Length": 0x4},
"SID3":          {"Offset": 0x20, "Length": 0x4},
# gap?
"Race":          {"Offset": 0x2C, "Length": 0x4},
"Type":          {"Offset": 0x30, "Length": 0x4},
# gap?
"AID":           {"Offset": 0x38, "Length": 0x4},
}

IntegerDataDictionary = {
"Build":            {"Offset": 0x3C, "Length": 0x1, "Signed": True},
"Weight":           {"Offset": 0x3D, "Length": 0x1, "Signed": True},
"Move":             {"Offset": 0x3E, "Length": 0x1, "Signed": True},
# gap?
"Skill Capacity":   {"Offset": 0x40, "Length": 0x1, "Signed": False},
# gap?
"BaseHP":           {"Offset": 0x44, "Length": 0x1, "Signed": True},
"BaseStrength":     {"Offset": 0x45, "Length": 0x1, "Signed": True},
"BaseMagic":        {"Offset": 0x46, "Length": 0x1, "Signed": True},
"BaseSkill":        {"Offset": 0x47, "Length": 0x1, "Signed": True},
"BaseSpeed":        {"Offset": 0x48, "Length": 0x1, "Signed": True},
"BaseLuck":         {"Offset": 0x49, "Length": 0x1, "Signed": True},
"BaseDefense":      {"Offset": 0x4A, "Length": 0x1, "Signed": True},
"BaseResistance":   {"Offset": 0x4B, "Length": 0x1, "Signed": True},

"MaxHP":            {"Offset": 0x4C, "Length": 0x1, "Signed": True},
"MaxStrength":      {"Offset": 0x4D, "Length": 0x1, "Signed": True},
"MaxMagic":         {"Offset": 0x4E, "Length": 0x1, "Signed": True},
"MaxSkill":         {"Offset": 0x4F, "Length": 0x1, "Signed": True},
"MaxSpeed":         {"Offset": 0x50, "Length": 0x1, "Signed": True},
"MaxLuck":          {"Offset": 0x51, "Length": 0x1, "Signed": True},
"MaxDefense":       {"Offset": 0x52, "Length": 0x1, "Signed": True},
"MaxResistance":    {"Offset": 0x53, "Length": 0x1, "Signed": True},

"GrowthHP":         {"Offset": 0x54, "Length": 0x1, "Signed": True},
"GrowthStrength":   {"Offset": 0x55, "Length": 0x1, "Signed": True},
"GrowthMagic":      {"Offset": 0x56, "Length": 0x1, "Signed": True},
"GrowthSkill":      {"Offset": 0x57, "Length": 0x1, "Signed": True},
"GrowthSpeed":      {"Offset": 0x58, "Length": 0x1, "Signed": True},
"GrowthLuck":       {"Offset": 0x59, "Length": 0x1, "Signed": True},
"GrowthDefense":    {"Offset": 0x5A, "Length": 0x1, "Signed": True},
"GrowthResistance": {"Offset": 0x5B, "Length": 0x1, "Signed": True},
# apparently there's laguz data at 0x5C for 8 bytes
}
