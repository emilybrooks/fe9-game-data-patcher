BlockLength = 0x28 # Bytes
NumberOfBlocks = None
OffsetDictionary = {}

StringDataDictionary = {
"SID":             {"Offset": 0x00, "Length": 0x4},
"Name":            {"Offset": 0x04, "Length": 0x4},
"MSID":            {"Offset": 0x08, "Length": 0x4},
"Mess_Help":       {"Offset": 0x0C, "Length": 0x4},
"Mess_Help2":      {"Offset": 0x10, "Length": 0x4},
"Animation":       {"Offset": 0x14, "Length": 0x4},
}

IntegerDataDictionary = {
"SkillIndex":      {"Offset": 0x18, "Length": 0x1, "Signed": False},
"IconIndex":       {"Offset": 0x19, "Length": 0x1, "Signed": False},
"SkillPoints":     {"Offset": 0x1A, "Length": 0x1, "Signed": False},
"Unk_1F":          {"Offset": 0x1F, "Length": 0x1, "Signed": False},
}

ItemRequiredCount = {"Offset": 0x1B, "Length": 0x1}
ItemRequiredPointer = {"Offset": 0x20, "Length": 0x4}
UnitRestrictionsCount = {"Offset": 0x1C, "Length": 0x1}
UnitRestrictionsPointer = {"Offset": 0x24, "Length": 0x4}
