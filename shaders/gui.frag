#version 330 core

layout (location = 0) out vec4 fragColor;


in vec2 uv;

uniform sampler2D image;
uniform int tfi;

void main() {
    vec4 tex = texture(image, uv); 
    if (tex.r == 0){
        fragColor = vec4(0, 0, 0, 0);
    }else{
        fragColor = tex;
    }
}

