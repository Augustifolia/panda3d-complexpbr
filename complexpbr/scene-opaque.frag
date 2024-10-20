#version 430

uniform sampler2D p3d_Texture0;

in vec2 v_texcoord;
in vec3 v_normal;
in vec4 v_color;

out vec4 p3d_FragColor;

void main() {
  vec4 color = texture(p3d_Texture0, v_texcoord) * v_color;
  p3d_FragColor = color;
}
