//#pragma once

// waves stuff
#define num_waves 32

uniform float amplitude[num_waves];
uniform float wavelength[num_waves];
uniform float phase[num_waves];
uniform vec2 direction[num_waves];
uniform bool circular[num_waves];

uniform float osg_FrameTime;

// other stuff
//in vec4 p3d_Vertex;
//uniform mat3 p3d_NormalMatrix;
uniform mat4 p3d_ModelViewProjectionMatrix;

//out mat3 v_tbn;


float rand(vec2 co){
    return fract(sin(dot(co, vec2(12.9898, 78.233))) * 43758.5453);
}


vec4 sum_sines() {
    vec2 pos = p3d_Vertex.xy;
    float height = 0.;

    float dx = 0.;
    float dy = 0.;

    for (int i = 0; i < num_waves; i++) {
        float amp = amplitude[i];
        float wave = wavelength[i];
        float ph = phase[i];
        vec2 dir = direction[i];
        bool cir = circular[i];

        if (cir) {
            dir = ((pos - dir) / length(pos - dir));
        }
        // calculate the wave height
        float offset = rand(dir) * 20;
        float w = amp * sin(dot(dir, pos) * wave + ph * osg_FrameTime + rand(dir) * 50);
        height = height + w;

        // calculate the wave normal
        dx = dx + wave * dir.x * amp * cos(dot(dir, pos) * wave + osg_FrameTime * ph + rand(dir) * 50);
        dy = dy + wave * dir.y * amp * cos(dot(dir, pos) * wave + osg_FrameTime * ph + rand(dir) * 50);

    }
    vec3 tangent = vec3(0., 1., dy);
    vec3 bitangent = vec3(1., 0., dx);
    vec3 normal = vec3(-dx, -dy, 1.);
    tangent = p3d_NormalMatrix * tangent;
    bitangent = p3d_NormalMatrix * bitangent;
    normal = p3d_NormalMatrix * normal;
    v_tbn = mat3(tangent, bitangent, normal);

    height = height / num_waves;
    vec4 position = p3d_Vertex + vec4(0, 0, height, 0);
    position = p3d_ModelViewProjectionMatrix * position;
    return position;
}
