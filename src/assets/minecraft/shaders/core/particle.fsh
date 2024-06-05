#version 150

#moj_import <fog.glsl>

uniform sampler2D Sampler0;

uniform vec4 ColorModulator;
uniform float FogStart;
uniform float FogEnd;
uniform vec4 FogColor;

in float vertexDistance;
in vec2 texCoord0;
in vec4 vertexColor;
in float custom;

out vec4 fragColor;

vec4 biLinearTex2D(sampler2D sampler, vec2 uv) {
	vec2 res = vec2(textureSize(sampler, 0));
    vec2 st = uv * res - 0.5;

    vec2 iuv = floor( st );
    vec2 fuv = fract( st );

    vec4 a = texture(sampler, (iuv+vec2(0.5,0.5))/res );
    vec4 b = texture(sampler, (iuv+vec2(1.5,0.5))/res );
    vec4 c = texture(sampler, (iuv+vec2(0.5,1.5))/res );
    vec4 d = texture(sampler, (iuv+vec2(1.5,1.5))/res );

    return mix(
        mix( a, b, fuv.x),
        mix( c, d, fuv.x), fuv.y
    );
}

void main() {
    if (custom == 1.0) {
        vec4 color = biLinearTex2D(Sampler0, texCoord0) * vertexColor * ColorModulator;
        if (color.a < 0.01) {
             discard;
        }
        fragColor = linear_fog(color, vertexDistance, FogStart, FogEnd, FogColor);
        gl_FragDepth = 0.0;
    } else {
        vec4 color = texture(Sampler0, texCoord0) * vertexColor * ColorModulator;
        if (color.a < 0.1) {
             discard;
        }
        fragColor = linear_fog(color, vertexDistance, FogStart, FogEnd, FogColor);
        gl_FragDepth = gl_FragCoord.z;
    }
}

