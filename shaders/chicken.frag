#version 330 core

layout (location = 0) out vec4 fragColor;


flat in int t;

void main(){
    
    fragColor = vec4((t % 20) * 0.05,  (20 - (t % 20)) * 0.05, 0.4 , 1) ;
}