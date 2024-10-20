#version 430

layout(early_fragment_tests) in;

#pragma include "common.glsl"
//#pragma include "sum_sines.frag"
#pragma include "ibl_f.frag"

//uniform sampler2D p3d_Texture0;

layout(r32ui) uniform uimage2D oit_FragmentHeads;

//in vec2 v_texcoord;
in vec3 v_normal;
//in vec4 v_color;

void main() {
  //vec4 color = texture(p3d_Texture0, v_texcoord) * v_color;
  //vec4 color = shade_water();
  vec4 color = c_frag();

  if (color.a > 0.001) {
    oit_FragmentListNode node;
    node.frag.color.rgb = color.rgb * color.a; // premultiply
    node.frag.color.w = 1 - color.a; // store transmission, not opacity!
    node.frag.depth = gl_FragCoord.z;

    uint head = atomicAdd(oit_FragmentCount, 1);
    node.next = imageAtomicExchange(oit_FragmentHeads, ivec2(gl_FragCoord.xy), head + 1);

    oit_Fragments[head] = node;
  }

  discard;
}
