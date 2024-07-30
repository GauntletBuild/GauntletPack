#version 150

#moj_import <fog.glsl>

in vec3 Position;
in vec4 Color;
in vec2 UV0;
in ivec2 UV2;

uniform sampler2D Sampler0;
uniform sampler2D Sampler2;

uniform mat4 ModelViewMat;
uniform mat4 ProjMat;
uniform int FogShape;

out float vertexDistance;
out vec4 vertexColor;
out vec2 texCoord0;
out float custom;

void main() {
    vec3 position = Position;
    vec4 color = Color;
    texCoord0 = UV0;
    vec4 screenPos;
    custom = 0.0;

    if (color.r == 4.0/255.0) {
        if (color.b == 0.0/255.0) {
            // Arbitrary y offset
            position.y += color.g * 255.0 - 128.0;
            color.rgb = vec3(1.0, 1.0, 1.0);
	    screenPos = ProjMat * ModelViewMat * vec4(position, 1.0);
        } else if (color.b == 1.0/255.0) {
            // Item pickup animation
            position.y += 120 - color.g * 20.0;
            color.a = 1.0 - color.g;
            color.rgb = vec3(1.0, 1.0, 1.0);
            
            if (abs(mod(position.z, 1.0) - 0.01) < 0.001) {
                position.y -= 16;
            }
	    screenPos = ProjMat * ModelViewMat * vec4(position, 1.0);
        } else if (color.b == 2.0/255.0) {
            // Arbitrary y offset (small)
            position.y += color.g * 16.0;
            color.rgb = vec3(1.0, 1.0, 1.0);
	    screenPos = ProjMat * ModelViewMat * vec4(position, 1.0);
        } else if (color.b == 3.0/255.0) {
	    screenPos = ProjMat * ModelViewMat * vec4(position, 1.0);
            vertexDistance = fog_distance(Position, FogShape);
            if (color.g == 0.0/255.0) {
                custom = 1.0;
                color.rgb = vec3(1.0, 1.0, 1.0);
            } else if (color.g == 1.0/255.0) {
                custom = 1.0;
                color.rgb = vec3(1.0, 0.831, 0.478);
            } else if (color.g == 2.0/255.0) {
                custom = 2.0;
                color.rgb = vec3(1.0, 1.0, 1.0);
            }

	    if (custom != 0.0 && screenPos.w > 0.0) {
		screenPos.xyz /= screenPos.w;
		screenPos.w = 1.0;
		screenPos.z = custom * 0.0001 - 1.0;
	    }

            if (vertexDistance > 12.0) {
                gl_Position = vec4(0.0/0.0);
                return;
            }
            if (vertexDistance > 4.0) {
                color.a *= 1.0 - (vertexDistance - 4.0) / 8.0;
            }
	} else if (color.b == 4.0/255.0) {
	    screenPos = ProjMat * ModelViewMat * vec4(position, 1.0);
            color.rgb = vec3(1.0, 1.0, 1.0);
    
	    screenPos.xyz /= abs(screenPos.w);
	    
	    float aspect = ProjMat[1][1] / ProjMat[0][0];
            float sizeX = 0.05;
            float sizeY = sizeX * aspect;
	    float minX = -1.0 + sizeX;
	    float maxX = 1.0 - sizeX;
	    float minY = -1.0;
	    float maxY = 1.0 - 2.0*sizeY;
		
            float sectionSize = 16.0;
	    float sectionX = sectionSize;
	    float sectionY = sectionSize;

	    if (screenPos.w < 0.0) {
		if (screenPos.x < 0.0) {
		    screenPos.xy *= minX / screenPos.x;
                    sectionX = 0.0;
		} else {
		    screenPos.xy *= maxX / screenPos.x;
                    sectionX = 2.0*sectionSize;
		}
	    } else if (screenPos.x < minX) {
		screenPos.xy *= minX / screenPos.x;
                sectionX = 0.0;
	    } else if (screenPos.x > maxX) {
		screenPos.xy *= maxX / screenPos.x;
                sectionX = 2.0*sectionSize;
	    }

            if (screenPos.w < 0.0 && screenPos.y < minY) {
                screenPos.y = minY;
                sectionY = 2.0*sectionSize;
            } else if (screenPos.y < minY) {
		screenPos.xy *= minY / screenPos.y;
                sectionY = 2.0*sectionSize;

                if (screenPos.x > -0.5 && screenPos.x < 0.5) {
		     sectionX = sectionSize;
		}
	    } else if (screenPos.y > maxY) {
		screenPos.xy *= maxY / screenPos.y;
                sectionY = 0.0;
                
                if (screenPos.x > -0.5 && screenPos.x < 0.5) {
		     sectionX = sectionSize;
		}
	    }
	    
	    screenPos.z = 0.0;
	    screenPos.w = 1.0;
	    
            ivec2 size = textureSize(Sampler0, 0);
	    vec2 texelSize = 1.0 / vec2(size);


	    if (gl_VertexID == 0) {
		screenPos.x -= sizeX;
		screenPos.y += 2.0*sizeY;
                texCoord0.x += sectionX * texelSize.x;
                texCoord0.y += sectionY * texelSize.y;
	    } else if (gl_VertexID == 1) {
		screenPos.x -= sizeX;
                texCoord0.x += sectionX * texelSize.x;
                texCoord0.y += (sectionY - 2.0*sectionSize) * texelSize.y;
	    } else if (gl_VertexID == 2) {
		screenPos.x += sizeX;
                texCoord0.x += (sectionX - 2.0*sectionSize) * texelSize.x;
                texCoord0.y += (sectionY - 2.0*sectionSize) * texelSize.y;
	    } else if (gl_VertexID == 3) {
		screenPos.x += sizeX;
		screenPos.y += 2.0*sizeY;
                texCoord0.x += (sectionX - 2.0*sectionSize) * texelSize.x;
                texCoord0.y += sectionY * texelSize.y;
	    }
        } else {
            color.rgb = vec3(1.0, 1.0, 1.0);
	    screenPos = ProjMat * ModelViewMat * vec4(position, 1.0);
        }
    } else if (color.r == 1.0/255.0) {
        color.a = 0.0;
	screenPos = ProjMat * ModelViewMat * vec4(position, 1.0);
    } else {
	screenPos = ProjMat * ModelViewMat * vec4(position, 1.0);
    }

    gl_Position = screenPos;

    vertexDistance = fog_distance(position, FogShape);
    vertexColor = color * texelFetch(Sampler2, UV2 / 16, 0);
}
