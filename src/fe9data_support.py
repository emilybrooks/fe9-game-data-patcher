import PySimpleGUI as sg

NumberOfBlocks = None
CurrentOffset = None
OffsetDictionary = {}

SupportList = []

#-------------------------------------------------------------------------------
# GUI Layout
#-------------------------------------------------------------------------------
sg.ChangeLookAndFeel("SystemDefaultForReal")

ColumnSupportList = [
[
	sg.Listbox(key="SupportListbox",
			   values=(""),
			   select_mode="LISTBOX_SELECT_MODE_SINGLE",
			   size=(24, 18),
			   disabled=True,
			   enable_events=True)
],
]

Tab = [
[
	sg.Column(layout=ColumnSupportList, vertical_alignment="top"),
],
]
