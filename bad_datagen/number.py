import json

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
    "orange_dye_sack",
]


def generate_states(start_index, models):
    result = {}
    current_index = start_index

    for i in range(len(models)):
        state = create_note_block(i)
        if state is not None:
            result[state] = {"model": f"gauntlet:block/{models[i]}", "index": current_index}
            current_index += 1

    return result


def create_note_block(index):
    id = 0
    for i in range(len(INSTRUMENTS)):
        for j in range(25):
            if id == index:
                return f'instrument={INSTRUMENTS[i].lower()},note={j},powered=false'
            id += 1
            if id == index:
                return f'instrument={INSTRUMENTS[i].lower()},note={j},powered=true'
            id += 1


def create_redstone_wire(index):
    west = index % 3
    south = (index // 3) % 3
    north = (index // 9) % 3
    east = (index // 27) % 3
    power = (index // 81) % 16  # Modulo by 16 to keep power within 0-15

    direction_map = {0: 'none', 1: 'side', 2: 'up'}
    west_str = direction_map[west]
    south_str = direction_map[south]
    north_str = direction_map[north]
    east_str = direction_map[east]

    return f"power={power},east={east_str},north={north_str},south={south_str},west={west_str}"



def create_mushroom_block(index):
    west = index % 2
    south = index // 2 % 2
    north = index // 4 % 2
    east = index // 8 % 2
    up = index // 16 % 2
    down = index // 32

    if down > 1:
        raise Exception(f"Index {index} exceeds maximum value")

    return f"east={bool(east)},north={bool(north)},south={bool(south)},west={bool(west)},up={bool(up)},down={bool(down)}"


def create_waterlog_glow_lichen(index):
    west = index % 2
    south = index // 2 % 2
    north = index // 4 % 2
    east = index // 8 % 2
    up = index // 16 % 2
    down = index // 32

    if down > 1:
        raise Exception(f"Index {index} exceeds maximum value")

    return f"waterlogged=true,down={bool(down)},up={bool(up)},east={bool(east)},north={bool(north)},south={bool(south)},west={bool(west)}"


def create_leaves(block, index):
    index += 1
    distance = 1 + (index % 7)
    persistent = index // 7

    if persistent > 1:
        raise Exception(f"Index {index} exceeds maximum value")

    return f"distance={distance},persistent={bool(persistent)}"


def create_note_block(index):
    id = 0
    for i in range(len(INSTRUMENTS)):
        for j in range(25):
            if id == index:
                return f'instrument={INSTRUMENTS[i].lower()},note={j},powered=false'
            id += 1
            if id == index:
                return f'instrument={INSTRUMENTS[i].lower()},note={j},powered=true'
            id += 1


def create_redstone_wire(index):
    west = index % 3
    south = (index // 3) % 3
    north = (index // 9) % 3
    east = (index // 27) % 3
    power = (index // 81) % 16  # Modulo by 16 to keep power within 0-15

    direction_map = {0: 'none', 1: 'side', 2: 'up'}
    west_str = direction_map[west]
    south_str = direction_map[south]
    north_str = direction_map[north]
    east_str = direction_map[east]

    return f"power={power},east={east_str},north={north_str},south={south_str},west={west_str}"



def create_mushroom_block(index):
    west = index % 2
    south = (index // 2) % 2
    north = (index // 4) % 2
    east = (index // 8) % 2
    up = (index // 16) % 2
    down = (index // 32) % 2

    return f"east={bool(east)},north={bool(north)},south={bool(south)},west={bool(west)},up={bool(up)},down={bool(down)}"


def create_waterlog_glow_lichen(index):
    west = index % 2
    south = (index // 2) % 2
    north = (index // 4) % 2
    east = (index // 8) % 2
    up = (index // 16) % 2
    down = (index // 32) % 2

    return f"waterlogged=true,down={bool(down)},up={bool(up)},east={bool(east)},north={bool(north)},south={bool(south)},west={bool(west)}"


def create_leaves(index):
    distance = 1 + (index % 7)
    persistent = (index // 7) % 2

    return f"distance={distance},persistent={bool(persistent)}"


def generate_custom_block(block_type, start_index, models):
    block_map = {
        'note_block': create_note_block,
        'redstone_wire': create_redstone_wire,
        'mushroom_block': create_mushroom_block,
        'waterlog_glow_lichen': create_waterlog_glow_lichen,
        'leaves': create_leaves
    }

    if block_type not in block_map:
        raise Exception(f"Invalid block type: {block_type}")

    block_func = block_map[block_type]
    result = {}

    for i, model in enumerate(models):
        state = block_func(i)
        if state is not None:
            result[state] = {"model": f"gauntlet:block/{model}", "index": start_index + i}

    return result

# Usage
with open('../customblocks.json') as f:
    data = json.load(f)

start_index = data[list(data.keys())[-1]]['index'] + 1
block_type = 'redstone_wire'
data = generate_custom_block(block_type, start_index, MODELS)
print(json.dumps(data, indent=4))