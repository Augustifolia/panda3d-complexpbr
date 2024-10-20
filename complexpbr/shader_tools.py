

def include(base_shader, included_shader):
    ...


def strip_version(file: str):
    lines = file.split("\n")
    for line in lines:
        if line.startswith("#version "):
            lines.remove(line)
            break

    return "\n".join(lines)


def remove_duplicate_defines(file: str):
    defines = []
    lines = file.split("\n")
    for line in lines:
        if line.startswith(("in ", "out ", "uniform ")):
            command = line.split(";")[0]
            if command not in defines:
                defines.append(command)
            else:
                lines.remove(line)

    return "\n".join(lines)


def add_define(file: str, string: str):
    v_line = 0
    lines = file.split("\n")
    for index, line in enumerate(lines):
        if line.startswith("#version "):
            v_line = index
            break

    lines.insert(v_line + 1, string)
    return "\n".join(lines)


if __name__ == '__main__':
    shader = """
#version 430

uniform sampler2D scene_tex;  // albedo
uniform sampler2D scene_tex;  // al
uniform sampler2D depth_tex;  // depth
uniform sampler2D normal_tex;  // normal
uniform vec2 window_size;
uniform mat4 p3d_ViewMatrix;
uniform mat4 p3d_ProjectionMatrixInverse;

// SSAO parameters with default values
const float radius = 0.5;
const float bias = 0.025;
    """

    # print(add_define(shader, "some new string"))
    # print(remove_duplicate_defines(shader))
    print(strip_version(shader))
