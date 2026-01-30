#version 330 core

layout (location = 0) out vec4 fragColor;


const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;

uniform sampler2DArray u_texture_array_0;
uniform vec3 sun_light;




in vec2 uv;
in vec3 ao_value;
in vec3 voxel_color;

flat in int Voxel_id;
flat in int Face_id;
flat in int light;

void main(){
    vec2 face_uv = uv;
    face_uv.x = uv.x / 3.0 - min(Face_id, 2) / 3.0;

    vec3 tex_col = texture(u_texture_array_0, vec3(face_uv, Voxel_id)).rgb;



    //tex_col *= voxel_color;
    tex_col = pow(tex_col, gamma);
    tex_col *= sun_light;
    tex_col *= ao_value;
    tex_col = pow(tex_col, inv_gamma);
    tex_col *= clamp(((light /  100) + 0.25), 0, 1);
    if (Voxel_id == 13 && tex_col.x == 0){
        fragColor = vec4(tex_col, 0.01);
    }else{
        fragColor = vec4(tex_col, 1);
    }
  

    
   
}   