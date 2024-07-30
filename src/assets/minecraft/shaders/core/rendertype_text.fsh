#version 150

#moj_import <fog.glsl>

uniform sampler2D Sampler0;

uniform vec4 ColorModulator;
uniform float FogStart;
uniform float FogEnd;
uniform vec4 FogColor;

in float vertexDistance;
in vec4 vertexColor;
in vec2 texCoord0;
in float custom;

out vec4 fragColor;

void main() {
    if (custom == 2.0) {
        vec4 color = texture(Sampler0, texCoord0) * vertexColor * ColorModulator;
        if (color.a < 0.01) {
            discard;
        }
        fragColor = color;
    } else if (custom == 1.0) {
        vec4 color = texture(Sampler0, texCoord0) * vertexColor * ColorModulator;
        if (color.a >= 0.01) {
            fragColor = color;
        } else {
            vec2 leftCoords = texCoord0 - vec2(0.99/textureSize(Sampler0, 0).x, 0.0);
            vec4 left = texture(Sampler0, leftCoords);
            if (left.a >= 0.01 && left.r > 0.5 && left.g > 0.5 && left.b > 0.5) {
                fragColor = vec4(0.22, 0.22, 0.22, 1.0);
            } else {
                discard;
            }
        }
    } else {
        vec4 color = texture(Sampler0, texCoord0) * vertexColor * ColorModulator;
	if (color.a < 0.01 && custom == 5.0) {
		fragColor = vec4(1.0, 0.0, 0.0, 1.0);
		return;
	}

        if (color.a < 0.01) {
            discard;
        }
        fragColor = linear_fog(color, vertexDistance, FogStart, FogEnd, FogColor);
    }
}
