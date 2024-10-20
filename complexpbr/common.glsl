#pragma once

// Maximum number of pixels behind each other
#define OIT_MAX_OVERDRAW 8

struct oit_Fragment {
  // This can be optimized further, with packHalf2x16 for example
  // Be sure to
  // Note: color w component is transmittance, not opacity!
  vec4 color;
  float depth;
};

struct oit_FragmentListNode {
  oit_Fragment frag;
  uint next;
};

layout(std430, binding=0) buffer oit_FragmentBuffer {
  uint oit_FragmentCount;
  oit_FragmentListNode oit_Fragments[];
};
