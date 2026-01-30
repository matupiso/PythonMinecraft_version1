from settings import *
from noise import noise2, noise3
from meshes.chunk_mesh_builder import get_index



# @njit
# def get_height(x, z):
#     # island mask
#     island = 1 / (pow(0.0025 * math.hypot(x - CENTER_X, z - CENTER_Z), 20) + 0.0001)
#     island = min(island, 1)

#     # amplitude
#     a1 = CENTER_Y
#     a2, a4, a8 = a1 * 0.5, a1 * 0.25, a1 * 0.125

#     # frequency
#     f1 = 0.0035 # 0.005
#     f2, f4, f8 = f1 * 2, f1 * 4, f1 * 8

#     if noise2(0.1 * x, 0.1 * z) < 0:
#         a1 /= 1.02

#     height = 0
#     height += noise2(x * f1, z * f1) * a1 + a1
#     height += noise2(x * f2, z * f2) * a2 - a2
#     height += noise2(x * f4, z * f4) * a4 + a4
#     height += noise2(x * f8, z * f8) * a8 - a8

#     height = max(height,  noise2(x * f8, z * f8) + 2)
#     height *= island

#     return int(height) + 32


@njit
def _get_height(x, z):

    h1 = noise2(x * 0.09, z * 0.09)
    h2 = noise2(x * 0.18, z * 0.18)
    h3 = noise2(x * 0.0902, z * 0.0902)
    h4 = noise2(x * 0.04, z * 0.04)

    height = 0
    if h2 < h1: height = h2
    elif h1 < h2: height = h1
    else:
        height = 2 * h1
    return int(height * 32)  + (int(90 * (h3 - 0.3) if h3 > 0.46 else 0) if h4 > 0.44 and h4 < 0.6 else 0) + 56

@njit
def get_height(x, z):
    h_select = noise2(x * 0.002, z * 0.002)
    if h_select > 0.6:
        return _get_height(x, z)
    else:
        return int((h_select - 0.31) * 32) + 65



@njit
def abs_float(x:float):
    if x >= 0.0: return x
    elif x < 0.0: return float(-x)
    return 0.0

@njit
def get_temperature(x, z):
    raw_temp = noise2(x * 0.001, z * 0.001)


    indicator = 1 if raw_temp > 0.005 else -1
    if raw_temp  == 0.005: indicator = 0
    raw_temp = abs_float(raw_temp)
    raw_temp *= 100
    raw_temp = int(raw_temp)
    


    temp = raw_temp + (indicator if x % (z // 10 + 1) > 10 else -1)

    return temp

@njit
def get_humdity(x, z):
    wh = get_height(x, z)
    raw_hum = noise2(x * 0.002, z * 0.0002)
    raw_hum = int(raw_hum * 100)
    if wh > 100: ind = 0.005
    else: ind  = 0.0001

    ind *= int(noise2(x, z) * 100)
    ind += random.randrange(0, 10) / 10

    hum = raw_hum + ind
    hum = abs_float(hum)
    return hum

def get_biome(x, z):
    world_height = get_height(x, z)
    temperature = get_temperature(x, z)
    humdity = get_humdity(x, z, world_height)
    biome = 0

    if world_height > MOUNTIN_MIN_HEIGHT:
        if temperature > 20:
            biome = MOUNTIN_HOT

        else:
            biome = MOUNTIN_COLD


    elif world_height <= MOUNTIN_LVL and world_height > PLAIN_MIN_HEIGHT:
        if temperature > 40:
            biome = DESERT

        else:
            biome = PLAINS

    elif world_height <= PLAIN_MIN_HEIGHT and world_height > SEA_MIN_HEIGHT:
        biome = 0


    return biome


@njit
def noise_int(x, z, f, a, b):
    n = noise2(x * f, z * f)
    n += 1
    n /= 2
    r = (n * (b - a)) + a
    if r > b: r= b
    if r < a: r = a
    return r


@njit
def coal_ore_vein(x, y, z):
    p = noise3(x * 0.201, y * 0.201, z * 0.201)
    if y < COAL_ORE_LEVEL_B and y > COAL_ORE_LEVEL_A:
        p *= 1.1

    return p > 0.5
        



@njit
def get_VH_height(x, z, plus, minus):

    

    freq = 1.56

    height = noise2(x * freq, z * freq)
    height *= freq + 1
    height = int(height * 4.19)
    height = min(plus, height)
    height = max(minus, height)
    return height

@njit
def set_voxel_id_plains(voxels, x, y, z, wx, wy, wz):
    voxels[get_index(x, y, z)] = GRASS


@njit
def set_voxel_id_desert(voxels, x, y, z, wx, wy, wz):
    voxels[get_index(x, y, z)] = SAND


@njit
def set_voxel_id_mountin_hot(voxels, x, y, z, wx, wy, wz):
    voxels[get_index(x, y, z)] = STONE


@njit
def set_voxel_id_mountin_cold(voxels, x, y, z, wx, wy, wz):
    voxels[get_index(x, y, z)] = SNOW

@njit
def math_abs(x):
    return x if x > 0 else -x

@njit
def cave_near(wx, wy, wz):
    world_height = get_height(wx, wz)
    for x in range(wx - 5, wx + 5):
        for y in range(wy - 15,wy + 9):
            for z in range(wz - 5, wz + 5):
                if (noise3(x * 0.19, y * 0.19, z * 0.19) > 0.17 and
                (noise2(x * 0.1, z * 0.1) * 3 + 3 < y < world_height + 2 or y > MOUNTIN_LVL)):
                    return noise2(wx * 0.1, wz * 0.1) > 0.6 
    return False



@njit
def set_voxel_id(voxels, x, y, z, wx, wy, wz):

    world_height = get_height(wx, wz)
    if wy == 0:
        voxel_id = BEDROCK
    elif wy >= MOUNTIN_LVL + get_VH_height(wx, wz, MOUNTIN_PLUS, MOUNTIN_MINUS) and wy < SNOW_LVL + get_VH_height(wx, wz, SNOW_PLUS, SNOW_MINUS):
        voxel_id = STONE if random.random() > 0.1 else COAL_ORE

    elif wy >= MOUNTIN_LVL + get_VH_height(wx, wz, MOUNTIN_PLUS, MOUNTIN_MINUS) and wy >= SNOW_LVL + get_VH_height(wx, wz, SNOW_PLUS, SNOW_MINUS):
        voxel_id = SNOW
    
    

    elif wy == world_height - 1:
        voxel_id = SAND if (get_temperature(wx, wz) > 64) else GRASS if not cave_near(wx, wy, wz) else 0
    elif wy < world_height - 1 and wy > noise_int(x, z, 0.95, world_height - 10, world_height - 4):
        voxel_id = SAND if (get_temperature(wx, wz) > 64) else DIRT if not cave_near(wx, wy, wz) else 0

    else:
        if (noise3(wx * 0.19, wy * 0.19, wz * 0.19) > 0.17 and
                (noise2(wx * 0.1, wz * 0.1) * 3 + 3 < wy < world_height + 2 or wy > MOUNTIN_LVL)):
            if  wy < world_height - 2: voxel_id = 0 
            if  wy < world_height - 2 and y > 1 and wy < MOUNTIN_LVL and noise_int(x, z, 0.34, 0, 90) < 45:
                voxels[get_index(x, y-1, z)] = WOOD 
                voxel_id = TORCH

        else:
            voxel_id = COAL_ORE if coal_ore_vein(wx, wy, wz) else STONE





    if voxel_id == GRASS and wy >= MOUNTIN_LVL + get_VH_height(wx, wz, MOUNTIN_PLUS, MOUNTIN_MINUS):
        voxel_id = STONE


    if voxel_id == GRASS:
        if noise_int(x, z, 0.99, 0,  100) / 100 < TREE_PROPAB:
            if noise_int(x, z, 0.09, 0,  100) < 3: place_bush(voxels, x, y, z, wy)
            else:place_tree(voxels, x, y, z, wy)



    
    voxels[get_index(x, y, z)] = voxel_id


@njit
def place_tree(voxels, x, y, z,  wy):
    TREE_HEIGHT = random.randint(TREE_MIN_HEIGHT, TREE_MAX_HEIGHT)
    TREE_H_HEIGHT = TREE_HEIGHT // 2  
    TREE_H_WIDTH = random.randint(TREE_MIN_WIDTH, TREE_MAX_WIDTH) // 2

    rnd = random.random()
        
    if y + TREE_HEIGHT >= CHUNK_SIZE:
        return None
    if x - TREE_H_WIDTH < 0 or x + TREE_H_WIDTH >= CHUNK_SIZE:
        return None
    if z - TREE_H_WIDTH < 0 or z + TREE_H_WIDTH >= CHUNK_SIZE:
        return None
    if wy > MOUNTIN_LVL - MOUNTIN_VARIABILITY - 1:
        return None

    # wood under the tree





    # leaves
    m = 0
    for n, iy in enumerate(range(TREE_H_HEIGHT, TREE_HEIGHT - 1)):
        k = iy % 2
        rng = int(random.random() * 2)
        for ix in range(-TREE_H_WIDTH + m, TREE_H_WIDTH - m * rng):
            for iz in range(-TREE_H_WIDTH + m * rng, TREE_H_WIDTH - m):
                if (ix + iz) % 4:
                    voxels[get_index(x + ix + k, y + iy, z + iz + k)] = LEAVES
        m += 1 if n > 0 else 3 if n > 1 else 0

    # tree trunk
    for iy in range(1, TREE_HEIGHT - 2):
        voxels[get_index(x, y + iy, z)] = WOOD

    # top
    voxels[get_index(x, y + TREE_HEIGHT - 2, z)] = LEAVES



@njit
def place_bush(voxels, x, y, z,  wy):
    TREE_HEIGHT = BUSH_HEIGHT
    TREE_H_HEIGHT = TREE_HEIGHT // 2  
    TREE_H_WIDTH = random.randint(TREE_MIN_WIDTH, TREE_MAX_WIDTH) // 2

    rnd = random.random()
        
    if y + TREE_HEIGHT >= CHUNK_SIZE:
        return None
    if x - TREE_H_WIDTH < 0 or x + TREE_H_WIDTH >= CHUNK_SIZE:
        return None
    if z - TREE_H_WIDTH < 0 or z + TREE_H_WIDTH >= CHUNK_SIZE:
        return None
    if wy > MOUNTIN_LVL - MOUNTIN_VARIABILITY - 1:
        return None

    # wood under the tree





    # leaves
    m = 0
    for n, iy in enumerate(range(TREE_H_HEIGHT, TREE_HEIGHT - 1)):
        k = iy % 2
        rng = int(random.random() * 2)
        for ix in range(-TREE_H_WIDTH + m, TREE_H_WIDTH - m * rng):
            for iz in range(-TREE_H_WIDTH + m * rng, TREE_H_WIDTH - m):
                if (ix + iz) % 4:
                    voxels[get_index(x + ix + k, y + iy, z + iz + k)] = LEAVES
        m += 1 if n > 0 else 3 if n > 1 else 0

    # tree trunk
    for iy in range(1, TREE_HEIGHT - 2):
        voxels[get_index(x, y + iy, z)] = WOOD

    # top
    voxels[get_index(x, y + TREE_HEIGHT - 2, z)] = LEAVES


