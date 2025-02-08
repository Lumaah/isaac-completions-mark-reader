import argparse


characters = [
    "Isaac", "Maggy", "Cain", "Judas", "???", "Eve", "Samson", "Azazel", 
    "Lazarus", "Eden", "The Lost", "Lilith", "Keeper", "Apollyon", "Forgotten", "Bethany",
    "Jacob & Esau", "T Isaac", "T Maggy", "T Cain", "T Judas", "T ???", "T Eve", "T Samson", "T Azazel", 
    "T Lazarus", "T Eden", "T Lost", "T Lilith", "T Keeper", "T Apollyon", "T Forgotten", "T Bethany",
    "T Jacob"
]

checklist_order = [
    "Mom Heart", "Isaac", "Satan", "Boss Rush", "Chest", 
    "Dark Room", "Mega Satan", "Greed", "Hush", "Delirium", "Mother", "Beast"
]


def getInt(data, offset, debug=False, num_bytes=2):
    if debug:
        print(f"Value read from {offset} (on {num_bytes} bytes) : {int.from_bytes(data[offset:offset+num_bytes], 'little', signed=False)}")
    return int.from_bytes(data[offset:offset+num_bytes], 'little')


def getSectionOffsets(data):
    ofs = 0x14
    sectData = [-1, -1, -1]
    entryLens = [1, 4, 4, 1, 1, 1, 1, 4, 4, 1]
    sectionOffsets = [0] * 10
    for i in range(len(entryLens)):
        for j in range(3):
            sectData[j] = int.from_bytes(data[ofs:ofs+2], 'little', signed=False)
            ofs += 4
        if sectionOffsets[i] == 0:
            sectionOffsets[i] = ofs
        for j in range(sectData[2]):
            ofs += entryLens[i]
    return sectionOffsets


def getChecklistUnlocks(data, char_index):
    checklist_data = []
    if char_index == 14:
        clu_ofs = getSectionOffsets(data)[1] + 0x32C
        for i in range(12):
            current_ofs = clu_ofs + i * 4
            checklist_data.append(getInt(data, current_ofs))
            if i == 8:
                clu_ofs += 0x4
            if i == 9:
                clu_ofs += 0x37C
            if i == 10:
                clu_ofs += 0x84
    elif char_index > 14:
        clu_ofs = getSectionOffsets(data)[1] + 0x31C
        for i in range(12):
            current_ofs = clu_ofs + char_index * 4 + i * 19 * 4
            checklist_data.append(getInt(data, current_ofs))
            if i == 8:
                clu_ofs += 0x4C
            if i == 9:
                clu_ofs += 0x3C
            if i == 10:
                clu_ofs += 0x3C
    else:
        clu_ofs = getSectionOffsets(data)[1] + 0x6C
        for i in range(12):
            current_ofs = clu_ofs + char_index * 4 + i * 14 * 4
            checklist_data.append(getInt(data, current_ofs))
            if i == 5:
                clu_ofs += 0x14
            if i == 8:
                clu_ofs += 0x3C
            if i == 9:
                clu_ofs += 0x3B0
            if i == 10:
                clu_ofs += 0x50
    return checklist_data


def missing_completions_marks(data, char_index):
    checklist = getChecklistUnlocks(data, char_index)
    missings = []
    for idx, val in enumerate(checklist):
        if val == 0:
            missings.append(checklist_order[idx])
    return missings


def main():
    parser = argparse.ArgumentParser(
        description="tool to have a list of all missing completions marks on the binding of isaac repentance +."
    )
    parser.add_argument("file", help="path to file")
    args = parser.parse_args()

    try:
        with open(args.file, "rb") as f:
            data = f.read()
    except Exception as e:
        print(f"error while loading file {e}")
        return

    print("list of all completions marks :\n")
    for idx, char_name in enumerate(characters):
        try:
            missings = missing_completions_marks(data, idx)
        except Exception as e:
            print(f"impossible to read {char_name} (index {idx}) : {e}")
            continue

        if missings:
            print(f"• {char_name} (index {idx}) is missing : {', '.join(missings)}")
        else:
            print(f"• {char_name} (index {idx}) has everything unlocked")
            

if __name__ == "__main__":
    main()
