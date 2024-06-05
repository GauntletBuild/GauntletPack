#version 150

#moj_import <fog.glsl>

in vec3 Position;
in vec2 UV0;
in vec4 Color;
in ivec2 UV2;

uniform sampler2D Sampler0;
uniform sampler2D Sampler2;

uniform mat4 ModelViewMat;
uniform mat4 ProjMat;
uniform int FogShape;

out float vertexDistance;
out vec2 texCoord0;
out vec4 vertexColor;
out float custom;

void main() {
    if (Color.g <= 0.2 && Color.b == 0.0) {
        gl_Position = vec4(0.0/0.0);
        return;
    }
    
    gl_Position = ProjMat * ModelViewMat * vec4(Position, 1.0);
    vertexDistance = fog_distance(Position, FogShape);
    texCoord0 = UV0;

    vec4 color = Color;
    if (color.a == 0.0) {
        custom = 1.0;
        color.a = 0.5;
        
        if (vertexDistance > 12.0) {
            gl_Position = vec4(0.0/0.0);
            return;
        }
        if (vertexDistance > 4.0) {
            color.a *= 1.0 - (vertexDistance - 4.0) / 8.0;
        }
    } else {
        custom = 0.0;
    }

    vertexColor = color * texelFetch(Sampler2, UV2 / 16, 0);
}
