from meshes.base_mesh import BaseMesh
from meshes.chunk_mesh_builder import build_chunk_mesh, build_chunk_mesh_special, get_index
from settings import *


class ChunkMesh(BaseMesh):
    def __init__(self, chunk):
        super().__init__()

        self.voxels = chunk.voxels
        self.chunk = chunk
        self.ctx = chunk.app.ctx
        self.app = chunk.app
        self.attrs = ("in_position", "voxel_id", "face_id", "ao_id", "light_id")
        self.vbo_format = "3u1 1u1 1u1 1u1 1u1"
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        self.program = chunk.app.shader_program.chunk
        self.vao = self.get_vao()

    def get_vertex_data(self):
        return build_chunk_mesh(
            chunk_voxels=self.voxels,
            format_size=self.format_size,
            chunk_position=self.chunk.position,
            world_voxels=self.chunk.world.voxels,
            light_map=np.array(np.multiply(self.chunk.light_map, 100), dtype="uint8") 
        )
    

class ComplicatedChunkMesh(BaseMesh):
    def __init__(self, chunk):
        super().__init__()

        self.voxels = chunk.voxels
        self.chunk = chunk
        self.ctx = chunk.app.ctx
        self.app = chunk.app
        self.attrs = ("in_position", "tex_type", "in_uv")
        self.vbo_format = "3f 1f 2f"
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        self.program = chunk.app.shader_program.complicated_chunk
        self.vao = self.get_vao() if TORCH in self.voxels else None
       

                        

    def render(self):
        if self.vao: super().render()

    def get_vertex_data(self):
        return build_chunk_mesh_special(
            chunk_voxels=self.voxels,
            format_size=self.format_size,
            torch_index = self.chunk.world.torch_index

        )