#version 430

#pragma include "common.glsl"

const vec2 triangle[3] = {
  {-3.0, -3.0},
  { 3.0, -3.0},
  { 0.0,  3.0},
};

void main() {
  gl_Position = vec4(triangle[gl_VertexID], 0.0f, 1.0f);

  // Need to reset this for the next frame, might as well do it here, because
  // we have no good way to clear it from the CPU - see #1389
  oit_FragmentCount = 0;
}
