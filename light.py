from settings import *
from meshes.chunk_mesh_builder import get_index, get_chunk_index
from utils import is_transparent


@njit 
def set_light(light_map, pos, light):
    wx, wy, wz = pos
    cx, cy, cz = wx // CHUNK_SIZE, wy // CHUNK_SIZE, wz // CHUNK_SIZE
    cx *= CHUNK_SIZE
    cy *= CHUNK_SIZE
    cz*= CHUNK_SIZE
    lx, ly, lz = wx - cx, wy - cy, wz - cz
    light_map[get_chunk_index(pos)][get_index(lx, ly, lz)] += light
@njit 
def get_block(world_map, pos):
    wx, wy, wz = pos
    cx, cy, cz = wx // CHUNK_SIZE, wy // CHUNK_SIZE, wz // CHUNK_SIZE
    cx *= CHUNK_SIZE
    cy *= CHUNK_SIZE
    cz*= CHUNK_SIZE
    lx, ly, lz = wx - cx, wy - cy, wz - cz
    return world_map[get_chunk_index(pos)][get_index(lx, ly, lz)]

@njit 
def chunk_set_light(light_map, pos, light):
    light_map[int(get_index(*pos))] += light
    return light_map
@njit 
def chunk_get_block(chunk_map, pos):
    return chunk_map[int(get_index(*pos))]




@njit
def emit_light(world_map, light_map, emit_pos, emit_light):
    directions = [
        (0, 1, 0), (0, -1, 0),
        (1, 0, 0), (-1, 0, 0),
        (0, 0, 1), (0, 0, -1)
    ]
    visited = []
    visit = [(emit_pos, emit_light)]

    index = -1
    while len(visit) > 0:
        index += 1
        if index < len(visit):
            (x, y, z), el = visit[index] 
            visited.append((x, y, z))
        else:
            break
        set_light(light_map, (x, y, z), el)

        if not is_transparent(get_block(world_map, (x, y, z))):
            continue

        el -= LIGHT_DECREASE

        if el <= 0:
            continue

        for direction in directions:
            ax, ay, az = direction
            if x + ax >= 0 and x + ax < WORLD_W * CHUNK_SIZE and y + ay >= 0 and y + ay < WORLD_H * CHUNK_SIZE and z + az >= 0 and z + az < WORLD_D * CHUNK_SIZE:
                if not (x + ax, y + ay, z + az) in visited:
                    visit.append(((x + ax, y + ay, z + az), el))



        

    return light_map




@njit
def chunk_emit_light(chunk_map, light_map, emit_pos, emit_light):
    directions = [
        (0, 1, 0), (0, -1, 0),
        (1, 0, 0), (-1, 0, 0),
        (0, 0, 1), (0, 0, -1)
    ]
    visited = []
    visit = [(emit_pos, emit_light)]

    index = -1
    while len(visit) > 0:
        index += 1
        if index < len(visit):
            (x, y, z), el = visit[index] 
            visited.append((x, y, z))
        else:
            break
        light_map = chunk_set_light(light_map, (x, y, z), el)

        if not is_transparent(chunk_get_block(chunk_map, (x, y, z))) and index != 0:
            continue

        el -= LIGHT_DECREASE

        if el <= 0:
            continue

        for direction in directions:
            ax, ay, az = direction
            if x + ax >= 0 and x + ax < CHUNK_SIZE and y + ay >= 0 and y + ay < CHUNK_SIZE and z + az >= 0 and z + az < CHUNK_SIZE:
                if not (x + ax, y + ay, z + az) in visited:
                    visit.append(((x + ax, y + ay, z + az), el))



        

    return light_map



z = np.zeros(CHUNK_VOL)
a = chunk_emit_light(z, z, (0,0,0), 0.2)

print_info("light_initialized")




