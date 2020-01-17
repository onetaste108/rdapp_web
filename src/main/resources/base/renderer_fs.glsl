#version 120
#define MAX_STEP 1024*36*2
#define MAX_OCTAVES 8

varying vec2 v_pos;

precision highp sampler2D;
precision highp float;

// Textures
uniform sampler2D u_tex_blit;
uniform sampler2D u_tex_blur;
uniform sampler2D u_tex_depth;
uniform sampler2D u_tex_norm;
uniform sampler2D u_tex_beauty;
// Internal
uniform vec2 u_res;
uniform vec2 u_ren_res;
uniform vec4 u_viewport;
uniform int u_tex_mode;

// Common
uniform float u_min_depth;
uniform float u_max_depth;
uniform float u_stop_dist;

uniform float u_time;
uniform float u_cam_fov;
uniform mat4 u_cam_mat;
uniform float u_cam_crop;
uniform float u_cam_mode;
uniform mat4 u_tex_mat;

uniform int u_octaves;
uniform float u_amp[MAX_OCTAVES];
uniform float u_freq[MAX_OCTAVES];
uniform vec3 u_pos[MAX_OCTAVES];

uniform float u_bump;
uniform vec3 u_bump_val;
uniform vec3 u_bump_off;
uniform float u_speed;
uniform float u_seed;
uniform float u_rand_strength;

uniform bool u_mirror;
uniform int u_shape;

uniform float u_scan_pos;
uniform float u_scan_size;

// Materials
uniform float u_ref_strength;
uniform float u_ref_point;
uniform float u_ref_smooth;
uniform float u_ref_metallic;
uniform int u_material;
uniform vec3 u_material_mix;

// Texture Control
uniform float u_tex_scale;
uniform vec2 u_tex_ref_mat;
uniform vec2 u_tex_dif_mat;


// Render
uniform int u_max_step;
uniform float u_step_scale;
uniform bool u_render;
uniform bool u_ren_bounds;

// Constants


const float PI = 3.1415926535897932384626433832795;
const float EPS = 0.001;

// Functions

vec2 pack(float x){
  float fix = 255.0/256.0;
  vec2 y = vec2(fract(x*fix*1.0), fract(x*fix*255.0));
  // y = fract(y*255.0)/255.0;
  return y;
}

float unpack(vec2 x) {
  float fix = 256.0/255.0;
  return x.x*fix/1.0+x.y*fix/255.0;
}

float rand(float n){return fract(sin(n) * 43758.5453123);}
vec3 rand3(float n){return vec3(rand(n),rand(n+0.333),rand(n+0.666));}
float noise(float p){
	float fl = floor(p);
  float fc = fract(p);
	return mix(rand(fl), rand(fl + 1.0), smoothstep(0.0, 1.0, fc))*2.0-1.0;
}


vec2 ctos(vec3 p) {
  p = normalize(p);
  float phi = atan(p.z, p.x) / PI / 2.0 + 0.5;
  float the = acos(p.y) / PI;
  return vec2(phi, the);
}
//
// vec2 ctos(vec3 p) {
//   p = normalize(p);
//   float phi = atan(p.z, p.x)/PI/2 + 0.5;
//   float the = atan(length(p.xz), p.y)/PI;
//   return vec2(phi, the);
// }

vec3 stoc(vec2 uv) {
  vec3 p;
  float phi = (uv.x - 0.5) * PI * 2.0;
  float the = uv.y * PI;
  p.x = sin(the)*cos(phi);
  p.y = cos(the);
  p.z = sin(the)*sin(phi);
  return p;
}

vec2 ctob(vec3 p) {
  float absX = abs(p.x);
  float absY = abs(p.y);
  float absZ = abs(p.z);

  bool isXPositive = p.x > 0;
  bool isYPositive = p.y > 0;
  bool isZPositive = p.z > 0;

  float maxAxis;
  vec2 uv;
  if (isXPositive && absX >= absY && absX >= absZ) {
    maxAxis = absX;
    uv.x = p.z;
    uv.y = p.y;
  }
  if (!isXPositive && absX >= absY && absX >= absZ) {
    maxAxis = absX;
    uv.x = -p.z;
    uv.y = p.y;
  }
  if (isYPositive && absY >= absX && absY >= absZ) {
    maxAxis = absY;
    uv.x = -p.x;
    uv.y = -p.z;
  }
  if (!isYPositive && absY >= absX && absY >= absZ) {
    maxAxis = absY;
    uv.x = -p.x;
    uv.y = p.z;
  }
  if (isZPositive && absZ >= absX && absZ >= absY) {
    maxAxis = absZ;
    uv.x = p.x;
    uv.y = p.y;
  }
  if (!isZPositive && absZ >= absX && absZ >= absY) {
    maxAxis = absZ;
    uv.x = -p.x;
    uv.y = p.y;
  }
  uv = 0.5 * (uv / maxAxis + 1.0);
  return uv;
}

float norm_depth(float depth) {
  return depth / u_max_depth;
}
float denorm_depth(float depth) {
  return depth * u_max_depth;
}
vec3 norm_norm(vec3 norm) {
  return norm;
  return norm / 2.0 + 0.5;
}
vec3 denorm_norm(vec3 norm) {
  return norm;
  return norm * 2.0 - 1.0;
}




float sdSphere( vec3 p, float s )
{
  return length(p)-s;
}
float sdPosSphere( vec3 p, vec3 pos, float s )
{
  return length(p-pos)-s;
}


vec3 opTwist(vec3 p )
{
    float k = 2.0; // or some other amount
    float c = cos(k*p.y);
    float s = sin(k*p.y);
    mat2  m = mat2(c,-s,s,c);
    vec3  q = vec3(m*p.xz,p.y);
    return q;
}

float sdEllipsoid( vec3 p, vec3 r )
{
    float k0 = length(p/r);
    float k1 = length(p/(r*r));
    return k0*(k0-1.0)/k1;
}
float sdTorus( vec3 p, vec2 t )
{
  vec2 q = vec2(length(p.xz)-t.x,p.y);
  return length(q)-t.y;
}

float opSmoothUnion( float d1, float d2, float k ) {
    float h = clamp( 0.5 + 0.5*(d2-d1)/k, 0.0, 1.0 );
    return mix( d2, d1, h ) - k*h*(1.0-h); }

float opSmoothSubtraction( float d1, float d2, float k ) {
    float h = clamp( 0.5 - 0.5*(d2+d1)/k, 0.0, 1.0 );
    return mix( d2, -d1, h ) + k*h*(1.0-h); }


// Texture Sampling

vec4 pt(sampler2D tex, vec2 uv) {
  vec2 uvi = fract(uv/2.0)*2.0;
  if (uvi.x > 1.0) uv.x = (1.0-fract(uv.x));
  else uv.x = fract(uv.x);
  if (uvi.y > 1.0) uv.y = (1.0-fract(uv.y));
  else uv.y = fract(uv.y);

  return texture2D(tex, (uv-0.5)*0.9+0.5);
}


vec4 ptr(sampler2D tex, vec2 uv) {
  vec2 uvi = fract(uv/2.0)*2.0;
  if (uvi.x >= 1.0) uv.x = (1.0-fract(uv.x));
  if (uvi.y >= 1.0) uv.y = (1.0-fract(uv.y));
  return texture2D(tex, uv);
}

vec4 sample_reflection(vec3 p) {
  return pt(u_tex_blit, ctob(p)*vec2(1.0,1.0));
}

vec4 sample_diffuse(vec3 p) {
  if (u_shape == 4) {
    return pt(u_tex_blur, p.xy*0.1*vec2(u_tex_scale)*vec2(1.0, -1.0)+0.5);
  } else {
    return pt(u_tex_blur, ctob((mat3(u_tex_mat)*p)*vec3(1.0, -1.0, 1.0))*vec2(u_tex_scale));
  }
}

vec3 distort_sin(vec3 p, float s, float f, float t) {
  p.xyz += 1.000*sin(2.0*(f)*p.yzx+t)*s;
  p.xyz += 0.500*sin(4.0*(f)*p.yzx+t)*s;
  p.xyz += 0.250*sin(8.0*(f)*p.yzx+t)*s;
  p.xyz += 0.050*sin(16.0*(f)*p.yzx+t)*s;
  return p;
}



vec3 distort(vec3 p, float s, float f) {
  p = s*sin(f*p.yzx*PI*2);
  return p;
}

vec3 distort_oct(vec3 p) {
  for (int i = 0; i < MAX_OCTAVES; i++) {
    if (i >= u_octaves) break;
    p += distort(p+u_pos[i], u_amp[i], u_freq[i]);

  }

  return p;
}

vec3 mirror(vec3 p) {
  p.x = abs(p.x);
  float d = 0.1;
  if (p.x < d) p.x = mix(p.x, 0, smoothstep(0,1,1-p.x/d));
  return p;
}

vec3 mapP(vec3 p) {
  if (u_mirror) p = mirror(p);
  p = distort_oct(p);
  return p;
}

float bump(vec3 p) {
  vec3 tex = sample_diffuse(p).rgb;
  tex = (tex-0.5+u_bump_off)*u_bump_val;
  tex += 0.5;
  float val = (tex.r + tex.g + tex.b) / 3.0 * u_bump;
  return val;
}

float get_shape(vec3 p) {
  float dist;
  float b = bump(p);
  vec3 cam = (u_cam_mat * vec4(0.0,0.0,0.0,1.0)).xyz;
  float cam_rad = sdSphere(cam, 1.3);
  if (u_shape == 0) {
    dist = sdSphere( p, 1.0 ) - b;
  }
  if (u_shape == 1) {
    dist = -sdSphere( p, 4.0 ) + b;
  }
  if (u_shape == 2) {
    float a = sdSphere( p, 1.0 ) - b;
    float b = -sdSphere( p, 4.0 ) - b;
    dist = opSmoothUnion(a, b, 0.1);
  }
  if (u_shape == 3) {
    float a = sdSphere( p, 1.0 ) - b;
    if (u_mirror) cam.x = abs(cam.x);
    float b = -sdPosSphere( p, cam, length(cam) ) - b;
    dist = opSmoothUnion(a, b, 0.5);
  }
  if (u_shape == 4) {
    dist = -p.z-b;
  }

  return dist;
}


float map(vec3 p) {
  vec3 _p = p;
  p = mapP(p);
  float dist = get_shape(p);
  vec3 cam = (u_cam_mat * vec4(0.0,0.0,0.0,1.0)).xyz;
  float cam_sphere = sdPosSphere(_p, cam, u_cam_crop);
  dist = opSmoothSubtraction(cam_sphere, dist, 0.3);
  return dist;
}

vec3 normal(vec3 p) {
  return normalize(vec3(
      map(vec3(p.x+EPS,p.y,p.z))-map(vec3(p.x-EPS,p.y,p.z)),
      map(vec3(p.x,p.y+EPS,p.z))-map(vec3(p.x,p.y-EPS,p.z)),
      map(vec3(p.x,p.y,p.z+EPS))-map(vec3(p.x,p.y,p.z-EPS))
    ));
}

float raymarch(vec3 eye, vec3 dir) {

  float dist;
  float depth = 0.001;
  for (int i = 0; i < MAX_STEP; i++) {
    dist = map(eye + depth * dir);
    depth += dist * u_step_scale;
    if ((dist <= u_stop_dist) || (depth >= u_max_depth)) break;
  }
  if (dist > u_stop_dist) {
    depth = 0.0;
  }
  return depth;
}

float reflection_raymarch(vec3 eye, vec3 dir) {
  float dist;
  float depth = u_min_depth;
  for (int i = 0; i < MAX_STEP; i++) {
    dist = abs(map(eye + depth * dir));
    depth += dist * u_step_scale;
    if ((dist <= u_stop_dist) || (depth >= u_max_depth) || (i >= u_max_step)) break;
  }
  if (dist > u_stop_dist) {
    depth = u_max_depth;
  }
  return depth;
}

vec3 raydir(float fov, vec2 p) {
  vec3 forward = vec3(0.0,0.0,1.0);
  vec3 right = vec3(1.0,0.0,0.0);
  vec3 up = vec3(0.0,1.0,0.0);
  vec3 rd = normalize(forward + fov * p.x * right + fov * p.y * up);
  return rd;
}

float material_mix(vec3 color) {
  color = color * 2.0 - 1.0;
  color = color * normalize(u_material_mix);
  color = color * 0.5 + 0.5;
  float bw = (color.x + color.y + color.z) / 3.0;
  return smoothstep(0.4, 0.6, bw);
}


vec3 fresnel(float cosTheta, vec3 F0) {
    return F0 + (1.0 - F0) * pow(1.0 - cosTheta, 5.0);
}


struct Cam {
  vec3 eye;
  vec3 ray;
};

Cam get_cam(vec2 uv) {
  Cam cam;

  if (u_cam_mode == 0) {
    vec4 eye4 = vec4(0.0,0.0,0.0,1.0);
    vec4 ray4 = vec4(raydir(u_cam_fov, uv), 1.0);
    vec3 eye = (u_cam_mat * eye4).xyz;
    vec3 ray = (u_cam_mat * ray4).xyz - eye;
    cam.eye = eye;
    cam.ray = ray;
  }

  if (u_cam_mode == 1) {
    vec4 eye4 = vec4(uv*u_cam_fov,0.0,1.0);
    vec3 ray = mat3(u_cam_mat) * vec3(0.0,0.0,1.0);
    vec3 eye = (u_cam_mat * eye4).xyz;
    cam.eye = eye;
    cam.ray = ray;
  }

  return cam;
}


vec4 render_scan(vec3 p) {
  vec3 mp = mapP(p);
  float d = max(min(map(p),0.5),-0.5)+0.5;
  return vec4(d, ctos(normalize(mp)), 0.0);
}

float render_depth(vec2 uv) {
  Cam cam = get_cam(uv);

  float depth = raymarch(cam.eye, cam.ray);

  return depth;
}

vec3 render_norm(vec2 uv) {
  Cam cam = get_cam(uv);

  float depth = texture2D(u_tex_depth, v_pos*0.5+0.5).r;
  if (depth == 1.0) return vec3(0.0);

  depth = denorm_depth(depth);
  vec3 p = cam.eye + cam.ray * depth;
  vec3 norm = normal(p);

  return norm;
}

vec4 render_beauty(vec2 uv) {
  Cam cam = get_cam(uv);

  float depth = texture2D(u_tex_depth, v_pos*0.5+0.5).r;
  if (depth == 0.0) return vec4(0.0);
  // if (depth == 1.0) return texture2D(u_tex_blit, project_sphere(eye + ray * denorm_depth(depth))).rgb;
  depth = denorm_depth(depth);


  vec3 norm = texture2D(u_tex_norm, v_pos*0.5+0.5).rgb;
  norm = denorm_norm(norm);

  vec3 p = cam.eye + cam.ray * depth;
  vec3 mp = mapP(p);
  // mp = normalize(distort_oct(mp, 1.7, 0.3, 0.0, 0.0));



  vec3 diffuse = sample_diffuse(mp).rgb;

  vec3 ref_ray = reflect(cam.ray, norm);
  vec3 ref_color = pt(u_tex_blit, ctos(mat3(u_tex_mat)*ref_ray)*vec2(2.0,2.0)).rgb;
  vec3 F = fresnel(max(dot(norm, -cam.ray), 0.0), vec3(0.0));
  float mmix = material_mix(diffuse);
  float metallic = u_ref_metallic;

  vec3 beauty;
  if (u_material == 0) beauty = diffuse;
  if (u_material == 1) beauty = mix(diffuse, ref_color, F);
  if (u_material == 2) beauty = ref_color;
  if (u_material == 3) beauty = mix(diffuse, ref_color, min(vec3(1.0), max(vec3(0.0), material_mix(diffuse)+F)));

  beauty = min(max(beauty, vec3(0.0,0.0,0.0)),vec3(1.0,1.0,1.0));

  return vec4(beauty, 1.0);
}

vec4 render_uv_dif(vec2 uv) {
  Cam cam = get_cam(uv);
  float depth = texture2D(u_tex_depth, v_pos*0.5+0.5).r;
  if (depth == 1.0) return vec4(0.0);
  depth = denorm_depth(depth);
  vec3 p = cam.eye + cam.ray * depth;
  vec3 mp = mapP(p);
  vec2 uv_dif = ctos(mp);
  vec4 packed = vec4(pack(uv_dif.x), pack(uv_dif.y));
  // return sample_diffuse(stoc(unpacked));
  return packed;
}

vec4 render_uv_ref(vec2 uv) {
  Cam cam = get_cam(uv);
  float depth = texture2D(u_tex_depth, v_pos*0.5+0.5).r;
  if (depth == 1.0) return vec4(0.0);
  depth = denorm_depth(depth);
  vec3 p = cam.eye + cam.ray * depth;
  vec3 norm = normal(p);
  vec3 ref_ray = reflect(cam.ray, norm);
  vec2 uv_ref = ctos(ref_ray);
  vec4 packed = vec4(pack(uv_ref.x), pack(uv_ref.y));
  // return sample_diffuse(stoc(unpacked));
  return packed;
}

void main() {
  vec4 color = vec4(0.0,0.0,0.0,1.0);

  vec2 uv = v_pos;
  vec2 render_uv = v_pos;
  vec2 rbx = vec2(-1,1);
  vec2 rby = vec2(-1,1);
  uv = uv*0.5+0.5;
  uv.x = (u_viewport.z-u_viewport.x) * uv.x + u_viewport.x;
  uv.y = (u_viewport.w-u_viewport.y) * uv.y + u_viewport.y;
  uv = uv*2.0-1.0;
  render_uv = uv;

  float render_aspect = u_ren_res.x / u_ren_res.y;
  if (render_aspect > 1.0) {
    render_uv.y /= render_aspect;
    rby /= render_aspect;
  } else if (render_aspect < 1.0) {
    render_uv.x *= render_aspect;
    rbx *= render_aspect;
  }

  vec2 preview_uv = render_uv;
  float preview_aspect = u_res.x / u_res.y;
  float mixed_aspect = preview_aspect / render_aspect;
  if (mixed_aspect > 1.0) {
    preview_uv.x *= mixed_aspect;
  } else if (mixed_aspect < 1.0) {
    preview_uv.y /= mixed_aspect;
  }

  if (u_render) {
    uv = render_uv;
  } else {
    uv = preview_uv;
  }



  if (u_tex_mode == 2) {

    float depth = render_depth(uv);
    depth = norm_depth(depth);
    color.x = depth;

  } else if (u_tex_mode == 3) {

    vec3 norm = render_norm(uv);
    norm = norm_norm(norm);

    color.rgb = norm;

  } else if (u_tex_mode == 4) {

    color = render_beauty(uv);
    if (u_ren_bounds && !u_render) {
      if (uv.x < rbx.x || uv.x > rbx.y || uv.y < rby.x || uv.y > rby.y) {
        color.rgb = mix(color.rgb, vec3(0.5,0.5,0.5), 0.5);
      }
    }

  } else if (u_tex_mode == 5) {

    color = render_uv_dif(uv);

  } else if (u_tex_mode == 6) {

    color = render_uv_ref(uv);

  } else if (u_tex_mode == 7) {

    color = render_scan(vec3(uv,u_scan_pos*2.0-1.0)*u_scan_size);

  }

  gl_FragColor = color;
}
