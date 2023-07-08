import json

START_INDEX = 26
END_INDEX = 100

INSTRUMENTS = [
    "HARP",
    "BASEDRUM",
    "SNARE",
    "HAT",
    "BASS",
    "FLUTE",
    "BELL",
    "GUITAR",
    "CHIME",
    "XYLOPHONE",
    "IRON_XYLOPHONE",
    "COW_BELL",
    "DIDGERIDOO",
    "BIT",
    "BANJO",
    "PLING",
    "ZOMBIE",
    "SKELETON",
    "CREEPER",
    "DRAGON",
    "WITHER_SKELETON",
    "PIGLIN",
    "CUSTOM_HEAD",
]

MODELS = [
    "yellow_dye_sack",
    "white_dye_sack",
    "red_dye_sack",
    "purple_dye_sack",
    "pink_dye_sack",
    "orange_dye_sack",
    "magenta_dye_sack",
    "lime_dye_sack",
    "light_gray_dye_sack",
    "light_blue_dye_sack",
    "green_dye_sack",
    "gray_dye_sack",
    "cyan_dye_sack",
    "brown_dye_sack",
    "blue_dye_sack",
    "black_dye_sack"
]

def get_state(number):
    id = 0
    for i in range(len(INSTRUMENTS)):
        for j in range(25):
            if id == number:
                return f'instrument={INSTRUMENTS[i].lower()},note={j},powered=false'
            id += 1
            if id == number:
                return f'instrument={INSTRUMENTS[i].lower()},note={j},powered=true'
            id += 1

result = {}

for i in range(min(END_INDEX, len(MODELS))):
    state = get_state(i+START_INDEX)
    if state is not None:
        result[state] = {"model": f"gauntlet:block/{MODELS[i]}"}

print(json.dumps(result, indent=4))
