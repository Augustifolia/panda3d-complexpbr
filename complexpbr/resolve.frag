#version 430

#pragma include "common.glsl"

uniform usampler2D oit_FragmentHeads;

out vec4 p3d_FragColor;

void main() {
  uint head = texelFetch(oit_FragmentHeads, ivec2(gl_FragCoord.xy), 0).r;
  if (head == 0) {
    discard;
  }

  // Alpha component stores the transmission
  vec4 outfrag = vec4(0, 0, 0, 1);

  // Read the linked list into an array, sorted front-to-back so that the
  // rearmost surfaces will drop off the end of the array.
  uint next;
  uint count = 1;
  const uint maxcount = OIT_MAX_OVERDRAW;
  oit_Fragment fragments[maxcount];
  {
    oit_FragmentListNode node = oit_Fragments[head - 1];
    fragments[0] = node.frag;
    outfrag.w = node.frag.color.w;
    next = node.next;
  }

  //For some reason, amdgpu crashed if this is a while loop instead and there are too many layers of transparency
  for (int n = 0; n < 100; n++) {
     if (next <= 0) {
       break;
     }
  //}
  //while (next > 0) {
    oit_FragmentListNode node = oit_Fragments[next - 1];
    outfrag.w *= node.frag.color.w;

    // Find where to insert this.
    uint i = 0;
    while (i < count && node.frag.depth > fragments[i].depth) {
      ++i;
    }

    if (i < maxcount) {
      if (count < maxcount) {
        fragments[count] = fragments[count - 1];
        ++count;
      }

      for (uint j = count - 1; j > i; --j) {
        fragments[j] = fragments[j - 1];
      }

      fragments[i] = node.frag;
    }

    next = node.next;
  }

  // Now do the blending, back-to-front.
  while (count > 0) {
    --count;
    outfrag.rgb = fma(outfrag.rgb, vec3(fragments[count].color.w), fragments[count].color.rgb);
  }

  p3d_FragColor = outfrag;
}
