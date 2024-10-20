#version 430

#pragma include "ibl_v.vert"
//#pragma include "sum_sines.vert"

//uniform mat4 p3d_ProjectionMatrix;
//uniform mat4 p3d_ModelViewMatrix;
//uniform mat3 p3d_NormalMatrix;
//uniform mat4 p3d_TextureMatrix;

uniform vec4 p3d_ColorScale;

//in vec4 p3d_Vertex;
//in vec4 p3d_Color;
//in vec3 p3d_Normal;
//in vec2 p3d_MultiTexCoord0;

//out vec2 v_texcoord;
out vec3 v_normal;
//out vec4 v_color;

void main() {
  gl_Position = p3d_ProjectionMatrix * (p3d_ModelViewMatrix * p3d_Vertex);
  v_texcoord = (p3d_TextureMatrix * vec4(p3d_MultiTexCoord0, 0, 1)).xy;
  v_normal = normalize(p3d_NormalMatrix * p3d_Normal);
  v_color = p3d_Color * p3d_ColorScale;
  vec4 position = c_vert();
  //gl_Position = position;
}
