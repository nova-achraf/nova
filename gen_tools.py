#!/usr/bin/env python3
"""Generate the PixelSqueeze tool pages (shared template, per-tool logic)."""
import os, textwrap

OUT = "/home/user/workspace/nova-achraf"

CSS = """
:root{
  --bg:#0B0F14; --card:#121820; --card2:#161E28; --line:#222E3C;
  --txt:#E9EFF6; --dim:#8496A9; --accent:#38BDF8; --accent2:#0EA5E9;
  --green:#34D399; --red:#F87171;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--bg);color:var(--txt);
  font-family:'Inter',system-ui,-apple-system,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}
.wrap{max-width:760px;margin:0 auto;padding:0 18px}
header{border-bottom:1px solid var(--line);padding:14px 0}
.brand{display:flex;align-items:center;gap:9px}
.brand .ic{width:34px;height:34px;border-radius:10px;background:linear-gradient(145deg,#1E3A4F,#0F202E);
  border:1px solid #27455C;display:flex;align-items:center;justify-content:center;font-size:16px}
.brand b{font-size:15px;letter-spacing:-.2px}
.brand span{font-size:10px;color:var(--dim);display:block;margin-top:1px;font-weight:500}
.brand a{color:inherit;display:flex;align-items:center;gap:9px}
.nav{margin-left:auto;display:flex;gap:6px;flex-wrap:wrap}
.nav a{font-size:10.5px;color:var(--dim);border:1px solid var(--line);border-radius:8px;padding:5px 9px}
.nav a.on{color:var(--accent);border-color:var(--accent);background:rgba(56,189,248,.10)}
.hero{text-align:center;padding:28px 0 20px}
.hero h1{font-size:26px;line-height:1.22;margin:0 0 10px;letter-spacing:-.6px;font-weight:800}
.hero p{margin:0 auto;color:var(--dim);font-size:13.5px;line-height:1.65;max-width:560px}
.badges{display:flex;gap:7px;justify-content:center;flex-wrap:wrap;margin-top:14px}
.badge{font-size:10.5px;color:var(--green);background:rgba(52,211,153,.1);
  border:1px solid rgba(52,211,153,.25);border-radius:20px;padding:4px 11px;font-weight:600}
.drop{margin-top:6px;border:2px dashed var(--line);border-radius:18px;background:var(--card);
  padding:34px 20px;text-align:center;cursor:pointer;transition:.2s}
.drop:hover,.drop.over{border-color:var(--accent);background:rgba(56,189,248,.05)}
.drop .e{font-size:34px;margin-bottom:8px}
.drop .t{font-size:14px;font-weight:700}
.drop .s{font-size:11.5px;color:var(--dim);margin-top:5px}
.opts{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px;margin-top:14px}
.opt{margin-bottom:16px}
.opt:last-child{margin-bottom:0}
.opt .lbl{display:flex;justify-content:space-between;font-size:11.5px;color:var(--dim);
  font-weight:600;margin-bottom:7px}
.opt .val{color:var(--accent);font-weight:700}
input[type=range]{width:100%;accent-color:var(--accent);height:5px}
input[type=number],input[type=text]{background:var(--card2);border:1px solid var(--line);
  border-radius:10px;padding:10px 12px;color:var(--txt);font-size:13px;font-family:inherit;
  outline:none;width:100%}
input:focus{border-color:var(--accent)}
.chips{display:flex;gap:6px;flex-wrap:wrap}
.chip{background:var(--card2);border:1px solid var(--line);color:var(--dim);border-radius:9px;
  padding:7px 13px;font-size:11.5px;font-weight:600;cursor:pointer;font-family:inherit}
.chip.on{background:rgba(56,189,248,.14);border-color:var(--accent);color:var(--accent)}
.chip:active{transform:scale(.96)}
.res{margin-top:14px;display:none}
.res.show{display:block}
.item{display:flex;align-items:center;gap:12px;background:var(--card);border:1px solid var(--line);
  border-radius:14px;padding:11px;margin-bottom:9px}
.item img{width:46px;height:46px;border-radius:9px;object-fit:cover;background:#0A0E13;flex-shrink:0}
.item .inf{flex:1;min-width:0}
.item .nm{font-size:12px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.item .sz{font-size:10.5px;color:var(--dim);margin-top:3px}
.item .sz b{color:var(--green);font-weight:700}
.item .dl{background:rgba(56,189,248,.14);border:1px solid var(--accent);color:var(--accent);
  border-radius:9px;padding:8px 13px;font-size:11.5px;font-weight:700;cursor:pointer;font-family:inherit;
  white-space:nowrap}
.allbtn{width:100%;background:linear-gradient(145deg,var(--accent),var(--accent2));color:#05202B;
  border:0;border-radius:13px;padding:15px;font-size:14px;font-weight:800;cursor:pointer;
  margin-top:6px;font-family:inherit}
.allbtn:disabled{opacity:.5}
.preview{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:12px;
  margin-top:14px;text-align:center;display:none}
.preview.show{display:block}
.preview img{max-width:100%;max-height:340px;border-radius:10px;display:block;margin:0 auto}
.preview .cap{font-size:10.5px;color:var(--dim);margin-top:8px}
.content{margin:32px 0 0}
.content h2{font-size:17px;margin:24px 0 9px;letter-spacing:-.3px}
.content p{font-size:13px;line-height:1.75;color:#AEBECF;margin:0 0 10px}
.content ol,.content ul{padding-left:20px;margin:0 0 10px}
.content li{font-size:13px;line-height:1.75;color:#AEBECF;margin-bottom:6px}
.adslot{border:1px dashed var(--line);border-radius:12px;padding:22px;text-align:center;
  color:#3D4D5E;font-size:10.5px;margin:26px 0}
footer{border-top:1px solid var(--line);margin-top:34px;padding:20px 0 30px;text-align:center;
  font-size:11px;color:#4E5E70}
.toast{position:fixed;bottom:22px;left:50%;transform:translate(-50%,14px);opacity:0;transition:.25s;
  background:#12303F;border:1px solid #1E4E63;color:#BFE9F7;border-radius:11px;padding:10px 16px;
  font-size:12px;z-index:50;pointer-events:none}
.toast.show{opacity:1;transform:translate(-50%,0)}
"""

TOOLS = [
    ("resize", "resize-image.html", "Resize Image", "Resize Image Online — Free &amp; Private",
     "Resize any JPG, PNG or WebP image to an exact pixel size or percentage. Free, no sign-up, and nothing is uploaded — resizing happens in your browser."),
    ("webp", "webp-converter.html", "WebP Converter", "WebP to JPG Converter — Free &amp; Private",
     "Convert WebP to JPG or PNG, and convert JPG or PNG to WebP online for free. Batch conversion, no upload, no watermarks."),
    ("crop", "crop-image.html", "Crop Image", "Crop Image Online — Instagram, Story &amp; Profile Sizes",
     "Crop images to 1:1, 4:5, 16:9, 9:16 or a custom ratio instantly. Free browser-based cropping with no upload."),
    ("rotate", "rotate-image.html", "Rotate Image", "Rotate &amp; Flip Image Online — Free",
     "Rotate images 90°, 180° or 270° and flip them horizontally or vertically. Free, instant, and completely private."),
    ("pdf", "image-to-pdf.html", "Image to PDF", "Image to PDF Converter — JPG &amp; PNG to PDF",
     "Convert JPG, PNG and WebP images into a single PDF document for free. Choose page size and margins, no upload required."),
]


def nav(active):
    order = [("compress.html", "Compress", "compress")] + [(t[1], t[2], t[0]) for t in TOOLS]
    out = []
    for href, label, key in order:
        cls = " class=\"on\"" if key == active else ""
        out.append('<a href="%s"%s>%s</a>' % (href, cls, label))
    return "".join(out)


def page(active, filename, title, h1, desc, tool_html, tool_js, content_html, extra_head="", extra_js_lib=""):
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#0B0F14">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<meta name="robots" content="index,follow">
<link rel="canonical" href="https://nova-achraf.github.io/nova/__FILE__">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
__EXTRA_HEAD__
<style>__CSS__</style>
</head>
<body>

<header>
  <div class="wrap" style="display:flex;align-items:center;gap:10px">
    <div class="brand">
      <a href="tools.html">
        <div class="ic">🗜</div>
        <div>
          <b>PixelSqueeze</b>
          <span>Free online image tools</span>
        </div>
      </a>
    </div>
    <div class="nav">__NAV__</div>
  </div>
</header>

<div class="wrap">
  <div class="hero">
    <h1>__H1__</h1>
    <p>__DESCHERO__</p>
    <div class="badges">
      <span class="badge">✓ 100% private</span>
      <span class="badge">✓ No sign-up</span>
      <span class="badge">✓ No watermarks</span>
    </div>
  </div>

__TOOL__

  <div class="adslot">Ad space</div>

__CONTENT__

  <footer>
    PixelSqueeze — free browser-based image tools. No uploads, no accounts, no tracking pixels.
  </footer>
</div>

<div class="toast" id="toast"></div>
__LIB__
<script>
var toastEl = document.getElementById('toast');
function toast(m){
  toastEl.textContent = m;
  toastEl.classList.add('show');
  clearTimeout(toast._t);
  toast._t = setTimeout(function(){ toastEl.classList.remove('show'); }, 2000);
}
function fmtSize(b){
  if (b < 1024) return b + ' B';
  if (b < 1024 * 1024) return (b / 1024).toFixed(0) + ' KB';
  return (b / 1024 / 1024).toFixed(2) + ' MB';
}
function esc(s){ return String(s).replace(/[<>&"]/g, ''); }
function dlUrl(url, name){
  var a = document.createElement('a');
  a.href = url; a.download = name;
  document.body.appendChild(a); a.click(); a.remove();
}
function loadImg(file){
  return new Promise(function(res, rej){
    var u = URL.createObjectURL(file);
    var i = new Image();
    i.onload = function(){ res({ img: i, url: u }); };
    i.onerror = function(){ URL.revokeObjectURL(u); rej(new Error('decode')); };
    i.src = u;
  });
}
function canvasBlob(cv, mime, q){
  return new Promise(function(res, rej){
    cv.toBlob(function(b){ b ? res(b) : rej(new Error('blob')); }, mime, q);
  });
}
__JS__
</script>
</body>
</html>"""
    html = (html.replace("__TITLE__", title)
                .replace("__DESC__", desc)
                .replace("__FILE__", filename)
                .replace("__EXTRA_HEAD__", extra_head)
                .replace("__CSS__", CSS)
                .replace("__NAV__", nav(active))
                .replace("__H1__", h1)
                .replace("__DESCHERO__", desc)
                .replace("__TOOL__", tool_html)
                .replace("__CONTENT__", content_html)
                .replace("__LIB__", extra_js_lib)
                .replace("__JS__", tool_js))
    path = os.path.join(OUT, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", filename, len(html))


DROP = """
  <div class="drop" id="drop">
    <div class="e">📁</div>
    <div class="t">Drop your images here</div>
    <div class="s">or tap to choose · JPG, PNG, WebP</div>
  </div>
  <input type="file" id="file" accept="image/*" multiple hidden>
"""

# ---------------------------------------------------------------- RESIZE
resize_tool = DROP + """
  <div class="opts">
    <div class="opt">
      <div class="lbl"><span>Width (px)</span><span class="val" id="wLive">—</span></div>
      <input type="number" id="rw" placeholder="e.g. 1200" min="16" max="10000">
    </div>
    <div class="opt">
      <div class="lbl"><span>Height (px)</span><span class="val" id="hLive">—</span></div>
      <input type="number" id="rh" placeholder="e.g. 800" min="16" max="10000">
    </div>
    <div class="opt">
      <div class="lbl"><span>Method</span><span class="val" id="mVal">Fit inside</span></div>
      <div class="chips" id="methods">
        <button class="chip on" data-m="fit">Fit inside</button>
        <button class="chip" data-m="exact">Stretch exact</button>
        <button class="chip" data-m="scale">Percent</button>
      </div>
    </div>
    <div class="opt" id="pctWrap" style="display:none">
      <div class="lbl"><span>Scale</span><span class="val" id="pVal">50%</span></div>
      <input type="range" id="pct" min="10" max="100" value="50" step="5">
    </div>
    <div class="opt">
      <div class="lbl"><span>Output format</span><span class="val" id="fVal">JPG</span></div>
      <div class="chips" id="formats">
        <button class="chip on" data-f="image/jpeg">JPG</button>
        <button class="chip" data-f="image/webp">WebP</button>
        <button class="chip" data-f="image/png">PNG</button>
      </div>
    </div>
  </div>

  <div class="res" id="res"><div id="items"></div>
    <button class="allbtn" id="all" disabled>⬇ Download all</button>
  </div>
"""

resize_js = """
var S = { files: [], out: [], method: 'fit', pct: 50, mime: 'image/jpeg', W: 0, H: 0 };
var drop = document.getElementById('drop'), fileIn = document.getElementById('file');
var resBox = document.getElementById('res'), items = document.getElementById('items');
var allBtn = document.getElementById('all');

drop.onclick = function(){ fileIn.click(); };
fileIn.onchange = function(e){ add(e.target.files); e.target.value = ''; };
['dragover','dragenter'].forEach(function(t){ drop.addEventListener(t, function(e){ e.preventDefault(); drop.classList.add('over'); }); });
['dragleave','drop'].forEach(function(t){ drop.addEventListener(t, function(e){ e.preventDefault(); drop.classList.remove('over'); }); });
drop.addEventListener('drop', function(e){ if (e.dataTransfer) add(e.dataTransfer.files); });

function add(list){
  var a = Array.prototype.slice.call(list).filter(function(f){ return f.type.indexOf('image/') === 0; });
  if (!a.length) { toast('Please choose image files'); return; }
  S.files = a.slice(0, 20); run();
}

function dims(w, h){
  if (S.method === 'scale') return [Math.round(w * S.pct / 100), Math.round(h * S.pct / 100)];
  var tw = S.W || w, th = S.H || h;
  if (S.method === 'exact') return [tw, th];
  var r = Math.min(tw / w, th / h);
  return [Math.round(w * r), Math.round(h * r)];
}

function run(){
  if (!S.files.length) return;
  S.out = []; items.innerHTML = ''; resBox.classList.add('show'); allBtn.disabled = true;
  var done = 0;
  S.files.forEach(function(f, i){
    var box = document.createElement('div');
    box.className = 'item';
    box.innerHTML = '<div class="inf"><div class="nm">' + esc(f.name) + '</div><div class="sz">working…</div></div>';
    items.appendChild(box);
    loadImg(f).then(function(o){
      var d = dims(o.img.naturalWidth, o.img.naturalHeight);
      if (!d[0] || !d[1] || S.method === 'fit' && !S.W && !S.H) d = [o.img.naturalWidth, o.img.naturalHeight];
      var cv = document.createElement('canvas');
      cv.width = d[0]; cv.height = d[1];
      var ctx = cv.getContext('2d');
      if (S.mime === 'image/jpeg'){ ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, d[0], d[1]); }
      ctx.drawImage(o.img, 0, 0, d[0], d[1]);
      URL.revokeObjectURL(o.url);
      return canvasBlob(cv, S.mime, 0.92).then(function(b){ return { b: b, w: d[0], h: d[1] }; });
    }).then(function(r){
      var ext = S.mime === 'image/png' ? 'png' : (S.mime === 'image/webp' ? 'webp' : 'jpg');
      var name = f.name.replace(/\\.[^.]+$/, '') + '-' + r.w + 'x' + r.h + '.' + ext;
      var url = URL.createObjectURL(r.b);
      S.out[i] = { url: url, name: name };
      box.innerHTML = '';
      var im = document.createElement('img'); im.src = url;
      var inf = document.createElement('div'); inf.className = 'inf';
      inf.innerHTML = '<div class="nm">' + esc(f.name) + '</div><div class="sz">' + r.w + ' × ' + r.h + 'px · <b>' + fmtSize(r.b.size) + '</b></div>';
      var b = document.createElement('button'); b.className = 'dl'; b.textContent = '⬇ Save';
      b.onclick = function(){ dlUrl(url, name); };
      box.appendChild(im); box.appendChild(inf); box.appendChild(b);
      if (++done === S.files.length) allBtn.disabled = false;
    }).catch(function(){
      box.innerHTML = '<div class="inf"><div class="nm">' + esc(f.name) + '</div><div class="sz" style="color:#F87171">failed</div></div>';
      if (++done === S.files.length) allBtn.disabled = false;
    });
  });
}

document.getElementById('rw').oninput = function(){ S.W = parseInt(this.value, 10) || 0; document.getElementById('wLive').textContent = S.W ? S.W + 'px' : '—'; };
document.getElementById('rh').oninput = function(){ S.H = parseInt(this.value, 10) || 0; document.getElementById('hLive').textContent = S.H ? S.H + 'px' : '—'; };
document.getElementById('rw').onchange = run;
document.getElementById('rh').onchange = run;

document.getElementById('methods').onclick = function(e){
  var b = e.target.closest('.chip'); if (!b) return;
  Array.prototype.forEach.call(this.children, function(c){ c.classList.remove('on'); });
  b.classList.add('on');
  S.method = b.getAttribute('data-m');
  document.getElementById('mVal').textContent = b.textContent;
  document.getElementById('pctWrap').style.display = S.method === 'scale' ? 'block' : 'none';
  run();
};
document.getElementById('pct').oninput = function(){
  S.pct = parseInt(this.value, 10);
  document.getElementById('pVal').textContent = S.pct + '%';
};
document.getElementById('pct').onchange = run;

document.getElementById('formats').onclick = function(e){
  var b = e.target.closest('.chip'); if (!b) return;
  Array.prototype.forEach.call(this.children, function(c){ c.classList.remove('on'); });
  b.classList.add('on');
  S.mime = b.getAttribute('data-f');
  document.getElementById('fVal').textContent = b.textContent;
  run();
};

allBtn.onclick = function(){
  var i = 0;
  (function next(){
    if (i >= S.out.length) return;
    var r = S.out[i++]; if (r) dlUrl(r.url, r.name);
    setTimeout(next, 320);
  })();
};
"""

# ---------------------------------------------------------------- WEBP
webp_tool = DROP + """
  <div class="opts">
    <div class="opt">
      <div class="lbl"><span>Convert to</span><span class="val" id="fVal">JPG</span></div>
      <div class="chips" id="formats">
        <button class="chip on" data-f="image/jpeg">JPG</button>
        <button class="chip" data-f="image/png">PNG</button>
        <button class="chip" data-f="image/webp">WebP</button>
      </div>
    </div>
    <div class="opt">
      <div class="lbl"><span>Quality</span><span class="val" id="qVal">90%</span></div>
      <input type="range" id="quality" min="50" max="100" value="90" step="5">
    </div>
  </div>

  <div class="res" id="res"><div id="items"></div>
    <button class="allbtn" id="all" disabled>⬇ Download all</button>
  </div>
"""

webp_js = """
var S = { files: [], out: [], mime: 'image/jpeg', q: 0.9 };
var drop = document.getElementById('drop'), fileIn = document.getElementById('file');
var resBox = document.getElementById('res'), items = document.getElementById('items');
var allBtn = document.getElementById('all');

drop.onclick = function(){ fileIn.click(); };
fileIn.onchange = function(e){ add(e.target.files); e.target.value = ''; };
['dragover','dragenter'].forEach(function(t){ drop.addEventListener(t, function(e){ e.preventDefault(); drop.classList.add('over'); }); });
['dragleave','drop'].forEach(function(t){ drop.addEventListener(t, function(e){ e.preventDefault(); drop.classList.remove('over'); }); });
drop.addEventListener('drop', function(e){ if (e.dataTransfer) add(e.dataTransfer.files); });

function add(list){
  var a = Array.prototype.slice.call(list).filter(function(f){ return f.type.indexOf('image/') === 0; });
  if (!a.length){ toast('Please choose image files'); return; }
  S.files = a.slice(0, 20); run();
}

function run(){
  if (!S.files.length) return;
  S.out = []; items.innerHTML = ''; resBox.classList.add('show'); allBtn.disabled = true;
  var done = 0;
  S.files.forEach(function(f, i){
    var box = document.createElement('div'); box.className = 'item';
    box.innerHTML = '<div class="inf"><div class="nm">' + esc(f.name) + '</div><div class="sz">converting…</div></div>';
    items.appendChild(box);
    loadImg(f).then(function(o){
      var cv = document.createElement('canvas');
      cv.width = o.img.naturalWidth; cv.height = o.img.naturalHeight;
      var ctx = cv.getContext('2d');
      if (S.mime === 'image/jpeg'){ ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, cv.width, cv.height); }
      ctx.drawImage(o.img, 0, 0);
      URL.revokeObjectURL(o.url);
      return canvasBlob(cv, S.mime, S.q);
    }).then(function(b){
      var ext = S.mime === 'image/png' ? 'png' : (S.mime === 'image/webp' ? 'webp' : 'jpg');
      var name = f.name.replace(/\\.[^.]+$/, '') + '.' + ext;
      var url = URL.createObjectURL(b);
      S.out[i] = { url: url, name: name };
      box.innerHTML = '';
      var im = document.createElement('img'); im.src = url;
      var inf = document.createElement('div'); inf.className = 'inf';
      inf.innerHTML = '<div class="nm">' + esc(f.name) + '</div><div class="sz">' + fmtSize(f.size) + ' → <b>' + fmtSize(b.size) + '</b> · ' + ext.toUpperCase() + '</div>';
      var btn = document.createElement('button'); btn.className = 'dl'; btn.textContent = '⬇ Save';
      btn.onclick = function(){ dlUrl(url, name); };
      box.appendChild(im); box.appendChild(inf); box.appendChild(btn);
      if (++done === S.files.length) allBtn.disabled = false;
    }).catch(function(){
      box.innerHTML = '<div class="inf"><div class="nm">' + esc(f.name) + '</div><div class="sz" style="color:#F87171">failed (unsupported format?)</div></div>';
      if (++done === S.files.length) allBtn.disabled = false;
    });
  });
}

document.getElementById('formats').onclick = function(e){
  var b = e.target.closest('.chip'); if (!b) return;
  Array.prototype.forEach.call(this.children, function(c){ c.classList.remove('on'); });
  b.classList.add('on');
  S.mime = b.getAttribute('data-f');
  document.getElementById('fVal').textContent = b.textContent;
  run();
};
document.getElementById('quality').oninput = function(){
  S.q = parseInt(this.value, 10) / 100;
  document.getElementById('qVal').textContent = this.value + '%';
};
document.getElementById('quality').onchange = run;

allBtn.onclick = function(){
  var i = 0;
  (function next(){
    if (i >= S.out.length) return;
    var r = S.out[i++]; if (r) dlUrl(r.url, r.name);
    setTimeout(next, 320);
  })();
};
"""

# ---------------------------------------------------------------- CROP
crop_tool = DROP + """
  <div class="opts">
    <div class="opt">
      <div class="lbl"><span>Aspect ratio</span><span class="val" id="rVal">1:1</span></div>
      <div class="chips" id="ratios">
        <button class="chip on" data-r="1">1:1</button>
        <button class="chip" data-r="0.8">4:5</button>
        <button class="chip" data-r="0.5625">9:16</button>
        <button class="chip" data-r="1.7778">16:9</button>
        <button class="chip" data-r="1.91">1.91:1</button>
        <button class="chip" data-r="0">Free</button>
      </div>
    </div>
    <div class="opt" id="freeWrap" style="display:none">
      <div class="lbl"><span>Custom width : height</span><span class="val" id="cVal">800 × 600</span></div>
      <div style="display:flex;gap:8px;align-items:center">
        <input type="number" id="cw" value="800" min="16">
        <span style="color:#4E5E70">:</span>
        <input type="number" id="ch" value="600" min="16">
      </div>
    </div>
    <div class="opt">
      <div class="lbl"><span>Anchor</span><span class="val" id="aVal">Center</span></div>
      <div class="chips" id="anchors">
        <button class="chip on" data-a="center">Center</button>
        <button class="chip" data-a="top">Top</button>
        <button class="chip" data-a="bottom">Bottom</button>
        <button class="chip" data-a="left">Left</button>
        <button class="chip" data-a="right">Right</button>
      </div>
    </div>
  </div>

  <div class="res" id="res"><div id="items"></div>
    <button class="allbtn" id="all" disabled>⬇ Download all</button>
  </div>
"""

crop_js = """
var S = { files: [], out: [], ratio: 1, anchor: 'center', cw: 800, ch: 600 };
var drop = document.getElementById('drop'), fileIn = document.getElementById('file');
var resBox = document.getElementById('res'), items = document.getElementById('items');
var allBtn = document.getElementById('all');

drop.onclick = function(){ fileIn.click(); };
fileIn.onchange = function(e){ add(e.target.files); e.target.value = ''; };
['dragover','dragenter'].forEach(function(t){ drop.addEventListener(t, function(e){ e.preventDefault(); drop.classList.add('over'); }); });
['dragleave','drop'].forEach(function(t){ drop.addEventListener(t, function(e){ e.preventDefault(); drop.classList.remove('over'); }); });
drop.addEventListener('drop', function(e){ if (e.dataTransfer) add(e.dataTransfer.files); });

function add(list){
  var a = Array.prototype.slice.call(list).filter(function(f){ return f.type.indexOf('image/') === 0; });
  if (!a.length){ toast('Please choose image files'); return; }
  S.files = a.slice(0, 20); run();
}

function cropBox(w, h){
  var r = S.ratio === 0 ? (S.cw / S.ch) : S.ratio;
  var tw = w, th = Math.round(w / r);
  if (th > h){ th = h; tw = Math.round(h * r); }
  var x, y;
  if (S.anchor === 'center'){ x = Math.round((w - tw) / 2); y = Math.round((h - th) / 2); }
  else if (S.anchor === 'top'){ x = Math.round((w - tw) / 2); y = 0; }
  else if (S.anchor === 'bottom'){ x = Math.round((w - tw) / 2); y = h - th; }
  else if (S.anchor === 'left'){ x = 0; y = Math.round((h - th) / 2); }
  else { x = w - tw; y = Math.round((h - th) / 2); }
  return { x: x, y: y, w: tw, h: th };
}

function run(){
  if (!S.files.length) return;
  S.out = []; items.innerHTML = ''; resBox.classList.add('show'); allBtn.disabled = true;
  var done = 0;
  S.files.forEach(function(f, i){
    var box = document.createElement('div'); box.className = 'item';
    box.innerHTML = '<div class="inf"><div class="nm">' + esc(f.name) + '</div><div class="sz">cropping…</div></div>';
    items.appendChild(box);
    loadImg(f).then(function(o){
      var b = cropBox(o.img.naturalWidth, o.img.naturalHeight);
      var cv = document.createElement('canvas');
      cv.width = b.w; cv.height = b.h;
      var ctx = cv.getContext('2d');
      ctx.drawImage(o.img, b.x, b.y, b.w, b.h, 0, 0, b.w, b.h);
      URL.revokeObjectURL(o.url);
      return canvasBlob(cv, 'image/jpeg', 0.93).then(function(bl){ return { b: bl, w: b.w, h: b.h }; });
    }).then(function(r){
      var name = f.name.replace(/\\.[^.]+$/, '') + '-crop-' + r.w + 'x' + r.h + '.jpg';
      var url = URL.createObjectURL(r.b);
      S.out[i] = { url: url, name: name };
      box.innerHTML = '';
      var im = document.createElement('img'); im.src = url;
      var inf = document.createElement('div'); inf.className = 'inf';
      inf.innerHTML = '<div class="nm">' + esc(f.name) + '</div><div class="sz">' + r.w + ' × ' + r.h + 'px · <b>' + fmtSize(r.b.size) + '</b></div>';
      var btn = document.createElement('button'); btn.className = 'dl'; btn.textContent = '⬇ Save';
      btn.onclick = function(){ dlUrl(url, name); };
      box.appendChild(im); box.appendChild(inf); box.appendChild(btn);
      if (++done === S.files.length) allBtn.disabled = false;
    }).catch(function(){
      box.innerHTML = '<div class="inf"><div class="nm">' + esc(f.name) + '</div><div class="sz" style="color:#F87171">failed</div></div>';
      if (++done === S.files.length) allBtn.disabled = false;
    });
  });
}

document.getElementById('ratios').onclick = function(e){
  var b = e.target.closest('.chip'); if (!b) return;
  Array.prototype.forEach.call(this.children, function(c){ c.classList.remove('on'); });
  b.classList.add('on');
  S.ratio = parseFloat(b.getAttribute('data-r'));
  document.getElementById('rVal').textContent = b.textContent;
  document.getElementById('freeWrap').style.display = S.ratio === 0 ? 'block' : 'none';
  run();
};
document.getElementById('anchors').onclick = function(e){
  var b = e.target.closest('.chip'); if (!b) return;
  Array.prototype.forEach.call(this.children, function(c){ c.classList.remove('on'); });
  b.classList.add('on');
  S.anchor = b.getAttribute('data-a');
  document.getElementById('aVal').textContent = b.textContent;
  run();
};
document.getElementById('cw').onchange = function(){ S.cw = parseInt(this.value, 10) || 800; document.getElementById('cVal').textContent = S.cw + ' × ' + S.ch; run(); };
document.getElementById('ch').onchange = function(){ S.ch = parseInt(this.value, 10) || 600; document.getElementById('cVal').textContent = S.cw + ' × ' + S.ch; run(); };

allBtn.onclick = function(){
  var i = 0;
  (function next(){
    if (i >= S.out.length) return;
    var r = S.out[i++]; if (r) dlUrl(r.url, r.name);
    setTimeout(next, 320);
  })();
};
"""

# ---------------------------------------------------------------- ROTATE
rotate_tool = DROP + """
  <div class="opts">
    <div class="opt">
      <div class="lbl"><span>Rotation</span><span class="val" id="rotVal">0°</span></div>
      <div class="chips" id="rots">
        <button class="chip" data-deg="90">↻ 90°</button>
        <button class="chip" data-deg="180">↻ 180°</button>
        <button class="chip" data-deg="270">↺ 90°</button>
        <button class="chip on" data-deg="0">None</button>
      </div>
    </div>
    <div class="opt">
      <div class="lbl"><span>Flip</span><span class="val" id="flipVal">None</span></div>
      <div class="chips" id="flips">
        <button class="chip on" data-f="none">None</button>
        <button class="chip" data-f="h">Horizontal</button>
        <button class="chip" data-f="v">Vertical</button>
      </div>
    </div>
  </div>

  <div class="res" id="res"><div id="items"></div>
    <button class="allbtn" id="all" disabled>⬇ Download all</button>
  </div>
"""

rotate_js = """
var S = { files: [], out: [], deg: 0, flip: 'none' };
var drop = document.getElementById('drop'), fileIn = document.getElementById('file');
var resBox = document.getElementById('res'), items = document.getElementById('items');
var allBtn = document.getElementById('all');

drop.onclick = function(){ fileIn.click(); };
fileIn.onchange = function(e){ add(e.target.files); e.target.value = ''; };
['dragover','dragenter'].forEach(function(t){ drop.addEventListener(t, function(e){ e.preventDefault(); drop.classList.add('over'); }); });
['dragleave','drop'].forEach(function(t){ drop.addEventListener(t, function(e){ e.preventDefault(); drop.classList.remove('over'); }); });
drop.addEventListener('drop', function(e){ if (e.dataTransfer) add(e.dataTransfer.files); });

function add(list){
  var a = Array.prototype.slice.call(list).filter(function(f){ return f.type.indexOf('image/') === 0; });
  if (!a.length){ toast('Please choose image files'); return; }
  S.files = a.slice(0, 20); run();
}

function run(){
  if (!S.files.length) return;
  S.out = []; items.innerHTML = ''; resBox.classList.add('show'); allBtn.disabled = true;
  var done = 0;
  S.files.forEach(function(f, i){
    var box = document.createElement('div'); box.className = 'item';
    box.innerHTML = '<div class="inf"><div class="nm">' + esc(f.name) + '</div><div class="sz">working…</div></div>';
    items.appendChild(box);
    loadImg(f).then(function(o){
      var rad = S.deg * Math.PI / 180;
      var w = o.img.naturalWidth, h = o.img.naturalHeight;
      var swap = S.deg === 90 || S.deg === 270;
      var cv = document.createElement('canvas');
      cv.width = swap ? h : w;
      cv.height = swap ? w : h;
      var ctx = cv.getContext('2d');
      ctx.translate(cv.width / 2, cv.height / 2);
      ctx.rotate(rad);
      if (S.flip === 'h') ctx.scale(-1, 1);
      if (S.flip === 'v') ctx.scale(1, -1);
      ctx.drawImage(o.img, -w / 2, -h / 2);
      URL.revokeObjectURL(o.url);
      return canvasBlob(cv, 'image/jpeg', 0.94).then(function(b){ return { b: b, w: cv.width, h: cv.height }; });
    }).then(function(r){
      var name = f.name.replace(/\\.[^.]+$/, '') + '-rot.jpg';
      var url = URL.createObjectURL(r.b);
      S.out[i] = { url: url, name: name };
      box.innerHTML = '';
      var im = document.createElement('img'); im.src = url;
      var inf = document.createElement('div'); inf.className = 'inf';
      inf.innerHTML = '<div class="nm">' + esc(f.name) + '</div><div class="sz">' + r.w + ' × ' + r.h + 'px · <b>' + fmtSize(r.b.size) + '</b></div>';
      var btn = document.createElement('button'); btn.className = 'dl'; btn.textContent = '⬇ Save';
      btn.onclick = function(){ dlUrl(url, name); };
      box.appendChild(im); box.appendChild(inf); box.appendChild(btn);
      if (++done === S.files.length) allBtn.disabled = false;
    }).catch(function(){
      box.innerHTML = '<div class="inf"><div class="nm">' + esc(f.name) + '</div><div class="sz" style="color:#F87171">failed</div></div>';
      if (++done === S.files.length) allBtn.disabled = false;
    });
  });
}

document.getElementById('rots').onclick = function(e){
  var b = e.target.closest('.chip'); if (!b) return;
  Array.prototype.forEach.call(this.children, function(c){ c.classList.remove('on'); });
  b.classList.add('on');
  S.deg = parseInt(b.getAttribute('data-deg'), 10);
  document.getElementById('rotVal').textContent = S.deg + '°';
  run();
};
document.getElementById('flips').onclick = function(e){
  var b = e.target.closest('.chip'); if (!b) return;
  Array.prototype.forEach.call(this.children, function(c){ c.classList.remove('on'); });
  b.classList.add('on');
  S.flip = b.getAttribute('data-f');
  document.getElementById('flipVal').textContent = b.textContent;
  run();
};

allBtn.onclick = function(){
  var i = 0;
  (function next(){
    if (i >= S.out.length) return;
    var r = S.out[i++]; if (r) dlUrl(r.url, r.name);
    setTimeout(next, 320);
  })();
};
"""

# ---------------------------------------------------------------- PDF
pdf_tool = DROP + """
  <div class="opts">
    <div class="opt">
      <div class="lbl"><span>Page size</span><span class="val" id="pVal">A4</span></div>
      <div class="chips" id="pagesizes">
        <button class="chip on" data-p="a4">A4</button>
        <button class="chip" data-p="letter">Letter</button>
        <button class="chip" data-p="fit">Fit to image</button>
      </div>
    </div>
    <div class="opt">
      <div class="lbl"><span>Margin</span><span class="val" id="mgVal">0 mm</span></div>
      <input type="range" id="margin" min="0" max="30" value="0" step="5">
    </div>
  </div>

  <div class="res" id="res">
    <div id="items"></div>
    <button class="allbtn" id="make">📄 Create PDF</button>
  </div>
"""

pdf_js = """
var S = { files: [], size: 'a4', margin: 0 };
var drop = document.getElementById('drop'), fileIn = document.getElementById('file');
var resBox = document.getElementById('res'), items = document.getElementById('items');
var makeBtn = document.getElementById('make');

drop.onclick = function(){ fileIn.click(); };
fileIn.onchange = function(e){ add(e.target.files); e.target.value = ''; };
['dragover','dragenter'].forEach(function(t){ drop.addEventListener(t, function(e){ e.preventDefault(); drop.classList.add('over'); }); });
['dragleave','drop'].forEach(function(t){ drop.addEventListener(t, function(e){ e.preventDefault(); drop.classList.remove('over'); }); });
drop.addEventListener('drop', function(e){ if (e.dataTransfer) add(e.dataTransfer.files); });

function add(list){
  var a = Array.prototype.slice.call(list).filter(function(f){ return f.type.indexOf('image/') === 0; });
  if (!a.length){ toast('Please choose image files'); return; }
  S.files = a.slice(0, 30);
  items.innerHTML = S.files.map(function(f, i){
    return '<div class="item"><div class="inf"><div class="nm">' + (i + 1) + '. ' + esc(f.name) + '</div>' +
      '<div class="sz">' + fmtSize(f.size) + '</div></div></div>';
  }).join('');
  resBox.classList.add('show');
}

document.getElementById('pagesizes').onclick = function(e){
  var b = e.target.closest('.chip'); if (!b) return;
  Array.prototype.forEach.call(this.children, function(c){ c.classList.remove('on'); });
  b.classList.add('on');
  S.size = b.getAttribute('data-p');
  document.getElementById('pVal').textContent = b.textContent;
};
document.getElementById('margin').oninput = function(){
  S.margin = parseInt(this.value, 10);
  document.getElementById('mgVal').textContent = S.margin + ' mm';
};

makeBtn.onclick = function(){
  if (!S.files.length){ toast('Add images first'); return; }
  if (!window.jspdf){ toast('PDF library still loading…'); return; }
  var pdf = new window.jspdf.jsPDF({ unit: 'mm', format: 'a4' });
  var first = true;
  var chain = Promise.resolve();

  S.files.forEach(function(f){
    chain = chain.then(function(){
      return loadImg(f).then(function(o){
        var cv = document.createElement('canvas');
        cv.width = o.img.naturalWidth;
        cv.height = o.img.naturalHeight;
        var ctx = cv.getContext('2d');
        ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, cv.width, cv.height);
        ctx.drawImage(o.img, 0, 0);
        URL.revokeObjectURL(o.url);
        var data = cv.toDataURL('image/jpeg', 0.92);

        var pw, ph;
        if (S.size === 'letter'){ pw = 215.9; ph = 279.4; }
        else if (S.size === 'fit'){
          var k = 0.264583;
          pw = cv.width * k; ph = cv.height * k;
        } else { pw = 210; ph = 297; }

        if (first){
          pdf.deletePage(1);
          pdf.addPage([pw, ph], pw > ph ? 'landscape' : 'portrait');
          first = false;
        } else {
          pdf.addPage([pw, ph], pw > ph ? 'landscape' : 'portrait');
        }

        var m = S.margin;
        var aw = pw - m * 2, ah = ph - m * 2;
        var r = Math.min(aw / cv.width, ah / cv.height);
        var w = cv.width * r, h = cv.height * r;
        pdf.addImage(data, 'JPEG', m + (aw - w) / 2, m + (ah - h) / 2, w, h);
      });
    });
  });

  chain.then(function(){
    pdf.save('images.pdf');
    toast('PDF ready ✓');
  }).catch(function(){ toast('Something failed — try fewer images'); });
};
"""

# ---------------------------------------------------------------- CONTENT
CONTENT = {}

CONTENT["resize"] = """
  <div class="content">
    <h2>How to resize an image</h2>
    <ol>
      <li>Drop your photos into the box above.</li>
      <li>Enter a target width, height, or pick a percentage.</li>
      <li>Choose “Fit inside” to keep the aspect ratio, or “Stretch exact” to force both values.</li>
      <li>Download each result or press “Download all”.</li>
    </ol>
    <h2>Common sizes</h2>
    <ul>
      <li><b>1920 × 1080</b> — Full HD wallpaper or YouTube thumbnail background</li>
      <li><b>1280 × 720</b> — HD video and blog headers</li>
      <li><b>1080 × 1080</b> — Instagram square post</li>
      <li><b>1080 × 1350</b> — Instagram portrait post</li>
      <li><b>1200 × 630</b> — Facebook and Twitter link preview</li>
    </ul>
    <h2>Is resizing the same as compressing?</h2>
    <p>No. Resizing changes the number of pixels (the dimensions), while compressing reduces the file weight. Reducing dimensions usually shrinks the file too, which is why resizing is the fastest way to make a photo lighter. If you only want a smaller file at the same dimensions, use the <a href="compress.html">image compressor</a>.</p>
    <h2>Will I lose quality?</h2>
    <p>Downscaling always discards pixels, but that is usually what you want for the web. Upscaling beyond the original size adds no detail — it only softens the image, so avoid it unless you have no choice.</p>
  </div>
"""

CONTENT["webp"] = """
  <div class="content">
    <h2>How to convert WebP to JPG</h2>
    <ol>
      <li>Drop one or many images.</li>
      <li>Choose JPG, PNG, or WebP as the output.</li>
      <li>Adjust the quality slider if you are producing JPG or WebP.</li>
      <li>Download single files or everything at once.</li>
    </ol>
    <h2>What is WebP?</h2>
    <p>WebP is an image format developed by Google. It typically produces files 25–35% smaller than JPG at the same visual quality, and it supports transparency like PNG. It is supported by every modern browser, but older desktop software and some upload forms still reject it — which is why converting to JPG is often necessary.</p>
    <h2>When to keep WebP</h2>
    <p>If your images are only used on a website you control, WebP is the better choice: faster pages, fewer bytes. Convert to JPG when you need to email the file, upload it to a form that only accepts JPG or PNG, or open it in an old photo editor.</p>
    <h2>Why does WebP lose its transparency?</h2>
    <p>JPG has no alpha channel. Transparent areas become white — this tool fills the background with white automatically so you never get black boxes. Choose PNG if you need to keep transparency.</p>
  </div>
"""

CONTENT["crop"] = """
  <div class="content">
    <h2>How to crop an image</h2>
    <ol>
      <li>Add your images.</li>
      <li>Pick an aspect ratio — 1:1 for a profile picture, 4:5 for an Instagram post, 9:16 for a story.</li>
      <li>Choose the anchor to decide which part of the image is kept.</li>
      <li>Download the cropped result.</li>
    </ol>
    <h2>Popular ratios</h2>
    <ul>
      <li><b>1:1</b> — profile pictures, album covers, product grids</li>
      <li><b>4:5</b> — Instagram portrait post (1080 × 1350)</li>
      <li><b>9:16</b> — Stories, Reels, TikTok</li>
      <li><b>16:9</b> — YouTube thumbnails and video frames</li>
      <li><b>1.91:1</b> — Facebook and Twitter link previews</li>
    </ul>
    <h2>The crop is centred by default</h2>
    <p>Most photos have the subject in the middle, so the default anchor is “Center”. If your subject is near the top or on one side, change the anchor instead of losing it.</p>
    <h2>Does cropping reduce file size?</h2>
    <p>Yes — fewer pixels means less data. A 4000-pixel wide photo cropped to a 1080-pixel square can lose 80% of its weight. To shrink further at the same dimensions, run the result through the <a href="compress.html">compressor</a>.</p>
  </div>
"""

CONTENT["rotate"] = """
  <div class="content">
    <h2>How to rotate or flip an image</h2>
    <ol>
      <li>Drop your photos.</li>
      <li>Pick a rotation: 90°, 180° or 270°.</li>
      <li>Optionally mirror the image horizontally or vertically.</li>
      <li>Download the result.</li>
    </ol>
    <h2>When you need this</h2>
    <p>Phone cameras store an orientation flag instead of rotating the pixels, so a photo taken sideways can appear upright on your phone and crooked everywhere else. Rotating here writes the rotation into the pixels, which fixes the problem permanently.</p>
    <h2>Rotate or flip?</h2>
    <p>Rotation turns the image around its centre and changes the dimensions when you use 90° or 270°. Flipping mirrors the image and keeps the dimensions — useful for correcting selfies shot with a front-facing camera.</p>
    <h2>Will the quality drop?</h2>
    <p>A rotation by a multiple of 90° is lossless in terms of geometry, but the file is re-encoded as JPG here. Use the highest quality settings for archival copies, and keep the original if the image is irreplaceable.</p>
  </div>
"""

CONTENT["pdf"] = """
  <div class="content">
    <h2>How to convert images to PDF</h2>
    <ol>
      <li>Drop your images — they will be added in the order shown.</li>
      <li>Choose the page size: A4, US Letter, or fit each page to its image.</li>
      <li>Add a margin if the document will be printed.</li>
      <li>Press “Create PDF” and the file downloads immediately.</li>
    </ol>
    <h2>Typical uses</h2>
    <ul>
      <li>Sending scanned documents to an administration or employer</li>
      <li>Turning phone photos of homework, receipts or contracts into one file</li>
      <li>Building a small portfolio to email to a client</li>
      <li>Preparing images for a print shop</li>
    </ul>
    <h2>Are my images uploaded?</h2>
    <p>No. The PDF is assembled inside your browser and the file is created locally. Nothing is transmitted, which is why this tool works with private documents like ID cards and bank statements.</p>
    <h2>Tips for a small PDF</h2>
    <p>Photos straight from a phone are 3–6 MB each, so a ten-page PDF can reach 50 MB. Compress or resize the images first with the <a href="compress.html">image compressor</a>, then build the PDF — most email providers cap attachments at 10–25 MB.</p>
  </div>
"""

# ---------------------------------------------------------------- WRITE
for key, filename, label, title, desc in TOOLS:
    tool_html = {"resize": resize_tool, "webp": webp_tool, "crop": crop_tool,
                 "rotate": rotate_tool, "pdf": pdf_tool}[key]
    tool_js = {"resize": resize_js, "webp": webp_js, "crop": crop_js,
               "rotate": rotate_js, "pdf": pdf_js}[key]
    lib = '<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>' if key == "pdf" else ""
    page(key, filename, title, label, desc, tool_html, tool_js, CONTENT[key], extra_js_lib=lib)

print("done")
