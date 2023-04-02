#version 330 core

#ifndef MAX_LIGHTS
    #define MAX_LIGHTS 5
#endif

uniform mat4 p3d_ProjectionMatrix;
uniform mat4 p3d_ModelViewMatrix;
uniform mat3 p3d_NormalMatrix;
uniform mat4 p3d_TextureMatrix;

in vec3 p3d_Normal;
in vec4 p3d_Vertex;
in vec4 p3d_Color;
in vec4 p3d_Tangent;
in vec2 p3d_MultiTexCoord0;

out vec3 v_position;
out vec4 v_color;
out mat3 v_tbn;
out vec2 v_texcoord;

uniform struct p3d_LightSourceParameters {
    vec4 position;
    vec4 diffuse;
    vec4 specular;
    vec3 attenuation;
    vec3 spotDirection;
    float spotCosCutoff;
    sampler2DShadow shadowMap;
    mat4 shadowViewMatrix;
} p3d_LightSource[MAX_LIGHTS];

out vec4 v_shadow_pos[MAX_LIGHTS];

void main()
{
    // Transform vertex position and normal to world space
    v_position = vec3(p3d_ModelViewMatrix * p3d_Vertex);
    vec3 normal = normalize(p3d_NormalMatrix * p3d_Normal);
    vec3 tangent = normalize(p3d_NormalMatrix * p3d_Tangent.xyz);
    vec3 bitangent = cross(normal, tangent) * p3d_Tangent.w;

    // Calculate the tangent space matrix
    v_tbn = mat3(tangent, bitangent, normal);
	
    for (int i = 0; i < p3d_LightSource.length(); ++i) {
        v_shadow_pos[i] = p3d_LightSource[i].shadowViewMatrix * vec4(v_position,1);
    }

    // Pass the color, texture coordinates, and clip space position to the fragment shader
    v_color = p3d_Color;
    v_texcoord = (p3d_TextureMatrix * vec4(p3d_MultiTexCoord0, 0.0, 1.0)).xy;
    gl_Position = p3d_ProjectionMatrix * p3d_ModelViewMatrix * p3d_Vertex;
}