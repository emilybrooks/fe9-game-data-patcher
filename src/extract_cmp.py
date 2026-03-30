import argparse
import cmp
import fe9LZ77
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument("input", help="The .cmp file to extract")
args = parser.parse_args()
input_file_path = pathlib.Path(args.input)

cmp_file = None
with input_file_path.open("rb") as cmp_bytes:
    cmp_bytes = cmp_bytes.read()
    cmp_bytes = bytearray(cmp_bytes)
    cmp_bytes = fe9LZ77.decompress(cmp_bytes)
    cmp_file = cmp.CMPFile(cmp_bytes)
    
# files will be placed in a folder that's named after the .cmp file
# folder will be in the same directory that the .cmp file is in
folder_name = input_file_path.name.split(".")[0]
working_folder = pathlib.Path(input_file_path.parent, folder_name)

for file_name in cmp_file.Header:
    file_path = pathlib.Path(working_folder, file_name)

    # make sub directories
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    contents = cmp_file.FileDictionary[file_name]
    with file_path.open("wb") as file:
        file.write(contents)
    
    print(f"{file_name}")

print(f"Extracted {cmp_file.NumberOfFiles} files successfully.")
