varying vec2 v_pos;
uniform sampler2D u_tex;
uniform vec2 u_res;
uniform int u_mode;
uniform int u_size;


vec4 pt(sampler2D tex, vec2 uv) {
  vec2 uvi = fract(uv/2.0)*2.0;
  if (uvi.x >= 1.0) uv.x = floor(uv.x) + (1.0-fract(uv.x));
  if (uvi.y >= 1.0) uv.y = floor(uv.y) + (1.0-fract(uv.y));
  return texture2D(tex, uv);
}


vec4 blur5(sampler2D image, vec2 uv, vec2 resolution, vec2 direction) {
  vec4 color = vec4(0.0);
  vec2 off1 = vec2(1.3333333333333333) * direction;
  color += pt(image, uv) * 0.29411764705882354;
  color += pt(image, uv + (off1 / resolution)) * 0.35294117647058826;
  color += pt(image, uv - (off1 / resolution)) * 0.35294117647058826;
  return color;
}

vec4 blur9(sampler2D image, vec2 uv, vec2 resolution, vec2 direction) {
  vec4 color = vec4(0.0);
  vec2 off1 = vec2(1.3846153846) * direction;
  vec2 off2 = vec2(3.2307692308) * direction;
  color += pt(image, uv) * 0.2270270270;
  color += pt(image, uv + (off1 / resolution)) * 0.3162162162;
  color += pt(image, uv - (off1 / resolution)) * 0.3162162162;
  color += pt(image, uv + (off2 / resolution)) * 0.0702702703;
  color += pt(image, uv - (off2 / resolution)) * 0.0702702703;
  return color;
}

vec4 blur13(sampler2D image, vec2 uv, vec2 resolution, vec2 direction) {
  vec4 color = vec4(0.0);
  vec2 off1 = vec2(1.411764705882353) * direction;
  vec2 off2 = vec2(3.2941176470588234) * direction;
  vec2 off3 = vec2(5.176470588235294) * direction;
  color += pt(image, uv) * 0.1964825501511404;
  color += pt(image, uv + (off1 / resolution)) * 0.2969069646728344;
  color += pt(image, uv - (off1 / resolution)) * 0.2969069646728344;
  color += pt(image, uv + (off2 / resolution)) * 0.09447039785044732;
  color += pt(image, uv - (off2 / resolution)) * 0.09447039785044732;
  color += pt(image, uv + (off3 / resolution)) * 0.010381362401148057;
  color += pt(image, uv - (off3 / resolution)) * 0.010381362401148057;
  return color;
}

void main() {
  vec4 color;
  vec2 uv = (v_pos/2.0+0.5);

  if (u_mode == 0) {
    color = texture2D(u_tex, uv);
  } else if (u_mode == 1) {
    if (u_size == 0) {
      color = blur5(u_tex, uv, u_res, vec2(1.0, 0.0));
    } else if (u_size == 1) {
      color = blur9(u_tex, uv, u_res, vec2(1.0, 0.0));
    } else if (u_size == 2) {
      color = blur13(u_tex, uv, u_res, vec2(1.0, 0.0));
    }

  } else if (u_mode == 2) {
    if (u_size == 0) {
      color = blur5(u_tex, uv, u_res, vec2(0.0, 1.0));
    } else if (u_size == 1) {
      color = blur9(u_tex, uv, u_res, vec2(0.0, 1.0));
    } else if (u_size == 2) {
      color = blur13(u_tex, uv, u_res, vec2(0.0, 1.0));
    }
  }

  gl_FragColor = color;
}
