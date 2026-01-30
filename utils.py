from settings import *



def get_distance(position1, position2):
    wx1, wy1, wz1 = position1
    wx2, wy2, wz2 = position2

    return int(math.sqrt((wx1 - wx2) ** 2 + (wy1 - wy2) ** 2 + (wz1 - wz2) ** 2))



def is_solid(block_type):
    return True if not (block_type in [0, TORCH]) else False

def is_breakable(block_type):
    return False if block_type in  [BEDROCK, COMMAND_BLOCK] and GAMEMODE != CREATIVE else True

def calc_yaw_pitch(position1:glm.vec3, position2:glm.vec3):
    vector = position1 - position2

    pitch = math.atan2(-vector.x, math.sqrt(vector.y ** 2 + vector.z ** 2))
    yaw = math.atan2(vector.y, vector.z)

    return pitch, yaw

def r_to_r1x0(value, max_val, min_val=0) -> float:
    if value > max_val: value = max_val
    if value < min_val: value = min_val

    if max_val == 0: return 0.0

    return value / max_val

def con_range(x:float, in_min:float, in_max:float, out_min:float,out_max:float):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def round_vec3_x(vec:glm.vec3):
    x = vec.x

    if x - float(int(x)) >= 0.7:
        return glm.vec3(int(x) + 1, vec.yz)
    return glm.vec3(glm.ivec3(vec))
def round_vec3_z(vec:glm.vec3):
    z = vec.z

    if z - float(int(z)) >= 0.7:
        return glm.vec3(int(z) + 1, vec.yz)
    return glm.vec3(glm.ivec3(vec))


@njit
def is_climbable(x):
    return False

def to_surival_mined(block):
    if block == GRASS: return DIRT
    return block

def sun_value(sun_angle):

    angle = int(360 - sun_angle)
    angle += 91
    angle %= 361
    angle -= 180
    angle = glm.abs(angle)

    if sun_angle > 180:
        return -(angle / 180 - 1.0)
    
    return angle / 180


@njit
def is_light(x):
    return x == TORCH

def is_number(string: str):
    for i in string:
        if not i in "1234567890-+":
            return False
        
    return True

def valid_cmd_position_spec(string: str):
    if string == "~":
        return True
    if string.startswith("~") and string.count("~") == 1: 
        string = string.replace("~", "")


    return is_number(string) and string != ""
@njit
def get_xyz(index):
    y = index // CHUNK_AREA
    for x in range(CHUNK_SIZE):
        for z in range(CHUNK_SIZE):
            if x + CHUNK_SIZE * z + CHUNK_AREA * y == index:
                return (x, y ,z)
            
    return (-1, -1, -1)



@njit
def _numpyindex(array, item):
    r = list(np.where(array == item))
    return r[0]

@njit
def numpyindex(array, item):
    if isinstance(item, list):
        res = np.zeros(0)
        for i in item:
            res = np.append(_numpyindex(array, i), res)
        return res
    else:
        return _numpyindex(array, item)

@njit
def get_light(x):
    if x == TORCH:
        return TORCH_LIGHT
    else: 
        return 0

def get_floatpart_fromfloat(x:float):
    return x - float(int(x))

@njit
def is_transparent(x):
    if x in [0, TORCH, GLASS]: return True
    else: return False

@njit
def can_bcm_block(x:int):
    if x in [TORCH, GLASS]: return False
    else: return True


def get_block_size(x:int):
    if x == TORCH:
        return glm.vec3(0.23, 0.9, 0.23)
    else:
        return glm.vec3(1, 1, 1)
    
