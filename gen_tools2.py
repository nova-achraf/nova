#!/usr/bin/env python3
"""Add 4 more tools + repaint the whole PixelSqueeze suite in a cheerful palette."""
import os, re
import gen_tools as G

OUT = "/home/user/workspace/nova-achraf"

# ---------- cheerful palette ----------
SWAP = [
    ("#0B0F14", "#FFFBF6"), ("#121820", "#FFFFFF"), ("#161E28", "#FFF7EF"),
    ("#222E3C", "#F0E4D8"), ("#E9EFF6", "#2E2118"), ("#8496A9", "#8B7768"),
    ("#38BDF8", "#FF6B4A"), ("#0EA5E9", "#FF9F1C"), ("#34D399", "#10B981"),
    ("#F87171", "#EF4444"), ("#1E3A4F", "#FFE3D1"), ("#0F202E", "#FFD0B5"),
    ("#27455C", "#FFC4A3"), ("#0A0E13", "#FBF3EA"), ("#05202B", "#FFFFFF"),
    ("#AEBECF", "#6B5647"), ("#4E5E70", "#A8917F"), ("#3D4D5E", "#C9B5A3"),
    ("#12303F", "#2E2118"), ("#1E4E63", "#2E2118"), ("#BFE9F7", "#FFF8F0"),
    ("rgba(56,189,248,", "rgba(255,107,74,"),
    ("rgba(52,211,153,.25)", "rgba(16,185,129,.30)"),
    ("rgba(52,211,153,.1)", "rgba(16,185,129,.12)"),
    ("rgba(52,211,153,.14)", "rgba(16,185,129,.14)"),
    ("background:var(--bg);color:var(--txt);",
     "background:linear-gradient(180deg,#FFF3E6,#FFFBF6 520px) fixed;color:var(--txt);"),
    ("--accent:#FF6B4A; --accent2:#FF9F1C;", "--accent:#FF6B4A; --accent2:#FF9F1C;"),
]


def recolor(text):
    for a, b in SWAP:
        text = text.replace(a, b)
    return text


# recolor the shared template for every page generated in this run
G.CSS = recolor(G.CSS)

DROP_ANY = """
  <div class="drop" id="drop">
    <div class="e">__ICON__</div>
    <div class="t">__TITLE__</div>
    <div class="s">__SUB__</div>
  </div>
  <input type="file" id="file" accept="__ACCEPT__" multiple hidden>
"""


def drop_box(icon, title, sub, accept):
    return (DROP_ANY.replace("__ICON__", icon)
                    .replace("__TITLE__", title)
                    .replace("__SUB__", sub)
                    .replace("__ACCEPT__", accept))


# =============================== MERGE PDF ===============================
merge_tool = drop_box("📑", "Drop your PDF files here", "or tap to choose · 2 to 20 files", "application/pdf") + """
  <div class="res" id="res">
    <div id="items"></div>
    <div class="opts" style="margin-top:12px">
      <div class="opt" style="margin-bottom:0">
        <div class="lbl"><span>Order</span><span class="val">use ↑ ↓ to reorder</span></div>
      </div>
    </div>
    <button class="allbtn" id="make">📑 Merge PDFs</button>
  </div>
"""

merge_js = """
var S = { files: [] };
var drop = document.getElementById('drop'), fileIn = document.getElementById('file');
var resBox = document.getElementById('res'), items = document.getElementById('items');
var makeBtn = document.getElementById('make');

drop.onclick = function(){ fileIn.click(); };
fileIn.onchange = function(e){ add(e.target.files); e.target.value = ''; };
['dragover','dragenter'].forEach(function(t){ drop.addEventListener(t, function(e){ e.preventDefault(); drop.classList.add('over'); }); });
['dragleave','drop'].forEach(function(t){ drop.addEventListener(t, function(e){ e.preventDefault(); drop.classList.remove('over'); }); });
drop.addEventListener('drop', function(e){ if (e.dataTransfer) add(e.dataTransfer.files); });

function add(list){
  var a = Array.prototype.slice.call(list).filter(function(f){
    return f.type === 'application/pdf' || /\\.pdf$/i.test(f.name);
  });
  if (!a.length){ toast('Please choose PDF files'); return; }
  S.files = S.files.concat(a);
  draw();
}

function draw(){
  resBox.classList.add('show');
  items.innerHTML = '';
  S.files.forEach(function(f, i){
    var box = document.createElement('div');
    box.className = 'item';
    var inf = document.createElement('div');
    inf.className = 'inf';
    inf.innerHTML = '<div class="nm">' + (i + 1) + '. ' + esc(f.name) + '</div><div class="sz">' + fmtSize(f.size) + '</div>';
    var up = document.createElement('button'); up.className = 'dl'; up.textContent = '↑';
    up.onclick = function(){ if (i > 0){ var t = S.files[i - 1]; S.files[i - 1] = S.files[i]; S.files[i] = t; draw(); } };
    var dn = document.createElement('button'); dn.className = 'dl'; dn.textContent = '↓';
    dn.onclick = function(){ if (i < S.files.length - 1){ var t = S.files[i + 1]; S.files[i + 1] = S.files[i]; S.files[i] = t; draw(); } };
    var rm = document.createElement('button'); rm.className = 'dl'; rm.textContent = '✕';
    rm.onclick = function(){ S.files.splice(i, 1); draw(); };
    box.appendChild(inf); box.appendChild(up); box.appendChild(dn); box.appendChild(rm);
    items.appendChild(box);
  });
}

makeBtn.onclick = async function(){
  if (!S.files.length){ toast('Add PDF files first'); return; }
  if (!window.PDFLib){ toast('PDF library still loading…'); return; }
  makeBtn.disabled = true; makeBtn.textContent = 'Merging…';
  try {
    var out = await window.PDFLib.PDFDocument.create();
    for (var i = 0; i < S.files.length; i++){
      var bytes = await S.files[i].arrayBuffer();
      var src = await window.PDFLib.PDFDocument.load(bytes, { ignoreEncryption: true });
      var pages = await out.copyPages(src, src.getPageIndices());
      pages.forEach(function(p){ out.addPage(p); });
    }
    var blob = new Blob([await out.save()], { type: 'application/pdf' });
    var url = URL.createObjectURL(blob);
    dlUrl(url, 'merged.pdf');
    toast('Merged ' + S.files.length + ' files ✓');
  } catch (e) {
    toast('Could not merge — is one file password protected?');
  }
  makeBtn.disabled = false; makeBtn.textContent = '📑 Merge PDFs';
};
"""

merge_content = """
  <div class="content">
    <h2>How to merge PDF files</h2>
    <ol>
      <li>Drop two or more PDF files.</li>
      <li>Use the ↑ ↓ buttons to put them in the right order.</li>
      <li>Press “Merge PDFs” — the combined file downloads immediately.</li>
    </ol>
    <h2>What gets preserved</h2>
    <p>Pages are copied exactly as they are: text, images, vector art and page sizes. Nothing is re-rendered or recompressed, so the quality is identical to the originals.</p>
    <h2>Password-protected files</h2>
    <p>A PDF that requires a password to open cannot be merged. Remove the password with the app that created it first, then try again.</p>
    <h2>Is it private?</h2>
    <p>Yes. The merge happens inside your browser using a local PDF library — your documents are never uploaded. This is safe for contracts, invoices and official papers.</p>
  </div>
"""

# =============================== PDF TO JPG ===============================
pdf2jpg_tool = drop_box("🖼", "Drop a PDF here", "or tap to choose · pages are converted to JPG", "application/pdf") + """
  <div class="opts">
    <div class="opt">
      <div class="lbl"><span>Quality</span><span class="val" id="scVal">2× (sharp)</span></div>
      <div class="chips" id="scales">
        <button class="chip" data-s="1">1× fast</button>
        <button class="chip on" data-s="2">2× sharp</button>
        <button class="chip" data-s="3">3× print</button>
      </div>
    </div>
  </div>

  <div class="res" id="res"><div id="items"></div>
    <button class="allbtn" id="all" disabled>⬇ Download all pages</button>
  </div>
"""

pdf2jpg_js = """
var S = { file: null, out: [], scale: 2 };
var drop = document.getElementById('drop'), fileIn = document.getElementById('file');
var resBox = document.getElementById('res'), items = document.getElementById('items');
var allBtn = document.getElementById('all');

if (window.pdfjsLib){
  window.pdfjsLib.GlobalWorkerOptions.workerSrc =
    'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
}

drop.onclick = function(){ fileIn.click(); };
fileIn.onchange = function(e){ if (e.target.files[0]) run(e.target.files[0]); e.target.value = ''; };
['dragover','dragenter'].forEach(function(t){ drop.addEventListener(t, function(e){ e.preventDefault(); drop.classList.add('over'); }); });
['dragleave','drop'].forEach(function(t){ drop.addEventListener(t, function(e){ e.preventDefault(); drop.classList.remove('over'); }); });
drop.addEventListener('drop', function(e){ if (e.dataTransfer && e.dataTransfer.files[0]) run(e.dataTransfer.files[0]); });

async function run(file){
  if (!window.pdfjsLib){ toast('PDF engine still loading…'); return; }
  S.file = file; S.out = [];
  items.innerHTML = ''; resBox.classList.add('show'); allBtn.disabled = true;

  var buf = await file.arrayBuffer();
  var pdf;
  try { pdf = await window.pdfjsLib.getDocument({ data: buf }).promise; }
  catch (e) { toast('This PDF could not be opened'); return; }

  var total = Math.min(pdf.numPages, 40);
  for (var i = 1; i <= total; i++){
    var box = document.createElement('div');
    box.className = 'item';
    box.innerHTML = '<div class="inf"><div class="nm">Page ' + i + ' / ' + pdf.numPages + '</div><div class="sz">rendering…</div></div>';
    items.appendChild(box);

    var page = await pdf.getPage(i);
    var vp = page.getViewport({ scale: S.scale });
    var cv = document.createElement('canvas');
    cv.width = Math.round(vp.width);
    cv.height = Math.round(vp.height);
    var ctx = cv.getContext('2d');
    ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, cv.width, cv.height);
    await page.render({ canvasContext: ctx, viewport: vp }).promise;

    var blob = await canvasBlob(cv, 'image/jpeg', 0.92);
    var url = URL.createObjectURL(blob);
    var name = 'page-' + i + '.jpg';
    S.out.push({ url: url, name: name });

    box.innerHTML = '';
    var im = document.createElement('img'); im.src = url;
    var inf = document.createElement('div'); inf.className = 'inf';
    inf.innerHTML = '<div class="nm">Page ' + i + '</div><div class="sz">' + cv.width + ' × ' + cv.height + 'px · <b>' + fmtSize(blob.size) + '</b></div>';
    var btn = document.createElement('button'); btn.className = 'dl'; btn.textContent = '⬇ Save';
    btn.onclick = function(u, n){ return function(){ dlUrl(u, n); }; }(url, name);
    box.appendChild(im); box.appendChild(inf); box.appendChild(btn);
  }
  if (pdf.numPages > total) toast('Converted the first ' + total + ' pages');
  allBtn.disabled = false;
}

document.getElementById('scales').onclick = function(e){
  var b = e.target.closest('.chip'); if (!b) return;
  Array.prototype.forEach.call(this.children, function(c){ c.classList.remove('on'); });
  b.classList.add('on');
  S.scale = parseInt(b.getAttribute('data-s'), 10);
  document.getElementById('scVal').textContent = b.textContent;
  if (S.file) run(S.file);
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

pdf2jpg_content = """
  <div class="content">
    <h2>How to convert PDF pages to JPG</h2>
    <ol>
      <li>Drop a PDF file.</li>
      <li>Choose the resolution: 1× for quick previews, 2× for screen use, 3× for printing.</li>
      <li>Download single pages or all of them at once.</li>
    </ol>
    <h2>Why convert a PDF to images?</h2>
    <ul>
      <li>Posting a page on social media or in a chat</li>
      <li>Sending a preview to a client without giving away the editable file</li>
      <li>Adding a page as an image inside a slide deck</li>
      <li>Reading a PDF on a device whose viewer struggles with it</li>
    </ul>
    <h2>Is the text still selectable?</h2>
    <p>No. Once a page becomes a JPG it is a flat image — that is exactly why it is useful for previews, and it is also why you should keep the original PDF if you need the text.</p>
    <h2>Privacy</h2>
    <p>Rendering happens on your device with a browser PDF engine. The document is never uploaded.</p>
  </div>
"""

# =============================== PASSPORT PHOTO ===============================
passport_tool = drop_box("🪪", "Drop your photo here", "or tap to choose · a plain background works best", "image/*") + """
  <div class="opts">
    <div class="opt">
      <div class="lbl"><span>Format</span><span class="val" id="fmtVal">35 × 45 mm</span></div>
      <div class="chips" id="fmts">
        <button class="chip on" data-w="35" data-h="45">35 × 45 mm</button>
        <button class="chip" data-w="51" data-h="51">51 × 51 mm</button>
        <button class="chip" data-w="50.8" data-h="50.8">2 × 2 in</button>
        <button class="chip" data-w="33" data-h="48">33 × 48 mm</button>
      </div>
    </div>
    <div class="opt">
      <div class="lbl"><span>Vertical framing</span><span class="val" id="pzVal">Head centred</span></div>
      <input type="range" id="pos" min="0" max="100" value="45" step="1">
    </div>
  </div>

  <div class="preview" id="prev">
    <img id="prevImg">
    <div class="cap" id="prevCap"></div>
  </div>

  <div class="res" id="res">
    <div style="display:flex;gap:9px;flex-wrap:wrap">
      <button class="allbtn" id="dlOne" style="flex:1;min-width:150px">⬇ Single photo</button>
      <button class="allbtn" id="dlSheet" style="flex:1;min-width:150px;background:linear-gradient(145deg,#10B981,#059669)">⬇ Print sheet (4)</button>
    </div>
  </div>
"""

passport_js = """
var S = { img: null, w: 35, h: 45, pos: 45, one: null, sheet: null };
var drop = document.getElementById('drop'), fileIn = document.getElementById('file');
var prev = document.getElementById('prev'), prevImg = document.getElementById('prevImg'), prevCap = document.getElementById('prevCap');
var resBox = document.getElementById('res');

var DPI = 300, MM = DPI / 25.4; // px per mm

drop.onclick = function(){ fileIn.click(); };
fileIn.onchange = function(e){ if (e.target.files[0]) load(e.target.files[0]); e.target.value = ''; };
['dragover','dragenter'].forEach(function(t){ drop.addEventListener(t, function(e){ e.preventDefault(); drop.classList.add('over'); }); });
['dragleave','drop'].forEach(function(t){ drop.addEventListener(t, function(e){ e.preventDefault(); drop.classList.remove('over'); }); });
drop.addEventListener('drop', function(e){ if (e.dataTransfer && e.dataTransfer.files[0]) load(e.dataTransfer.files[0]); });

function load(f){
  loadImg(f).then(function(o){
    S.img = o.img;
    prev.classList.add('show');
    resBox.classList.add('show');
    render();
  }).catch(function(){ toast('Could not read that image'); });
}

function render(){
  if (!S.img) return;
  var W = Math.round(S.w * MM), H = Math.round(S.h * MM);
  var cv = document.createElement('canvas');
  cv.width = W; cv.height = H;
  var ctx = cv.getContext('2d');
  ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, W, H);

  var srcRatio = S.img.naturalWidth / S.img.naturalHeight;
  var dstRatio = W / H;
  var sw, sh;
  if (srcRatio > dstRatio){ sh = S.img.naturalHeight; sw = sh * dstRatio; }
  else { sw = S.img.naturalWidth; sh = sw / dstRatio; }
  var sx = (S.img.naturalWidth - sw) / 2;
  var sy = (S.img.naturalHeight - sh) * (S.pos / 100);
  ctx.drawImage(S.img, sx, sy, sw, sh, 0, 0, W, H);

  prevImg.src = cv.toDataURL('image/jpeg', 0.95);
  prevCap.textContent = W + ' × ' + H + ' px at ' + DPI + ' dpi · ' + S.w + ' × ' + S.h + ' mm';
  S.one = cv;

  // 10 × 15 cm print sheet with 4 photos
  var SW = Math.round(100 * MM), SH = Math.round(150 * MM);
  var sheet = document.createElement('canvas');
  sheet.width = SW; sheet.height = SH;
  var s2 = sheet.getContext('2d');
  s2.fillStyle = '#fff'; s2.fillRect(0, 0, SW, SH);
  var gap = Math.round(4 * MM);
  var totalW = W * 2 + gap, totalH = H * 2 + gap;
  var ox = Math.round((SW - totalW) / 2), oy = Math.round((SH - totalH) / 2);
  for (var r = 0; r < 2; r++){
    for (var c = 0; c < 2; c++){
      s2.drawImage(cv, ox + c * (W + gap), oy + r * (H + gap));
      s2.strokeStyle = '#DDDDDD';
      s2.lineWidth = 1;
      s2.strokeRect(ox + c * (W + gap), oy + r * (H + gap), W, H);
    }
  }
  S.sheet = sheet;
}

document.getElementById('fmts').onclick = function(e){
  var b = e.target.closest('.chip'); if (!b) return;
  Array.prototype.forEach.call(this.children, function(c){ c.classList.remove('on'); });
  b.classList.add('on');
  S.w = parseFloat(b.getAttribute('data-w'));
  S.h = parseFloat(b.getAttribute('data-h'));
  document.getElementById('fmtVal').textContent = b.textContent;
  render();
};

document.getElementById('pos').oninput = function(){
  S.pos = parseInt(this.value, 10);
  document.getElementById('pzVal').textContent = S.pos < 30 ? 'Top aligned' : (S.pos > 65 ? 'Bottom aligned' : 'Head centred');
  render();
};

document.getElementById('dlOne').onclick = function(){
  if (!S.one){ toast('Add a photo first'); return; }
  S.one.toBlob(function(b){ dlUrl(URL.createObjectURL(b), 'photo-' + S.w + 'x' + S.h + 'mm.jpg'); }, 'image/jpeg', 0.95);
};
document.getElementById('dlSheet').onclick = function(){
  if (!S.sheet){ toast('Add a photo first'); return; }
  S.sheet.toBlob(function(b){ dlUrl(URL.createObjectURL(b), 'photo-sheet-10x15.jpg'); }, 'image/jpeg', 0.95);
};
"""

passport_content = """
  <div class="content">
    <h2>How to make a passport photo</h2>
    <ol>
      <li>Upload a photo taken from the front, with even light and a plain background.</li>
      <li>Pick the format your document requires: 35 × 45 mm is standard for Morocco and the Schengen visa, 2 × 2 in for the United States.</li>
      <li>Slide the framing control so the head is centred and leaves a small gap above it.</li>
      <li>Download the single photo, or the 10 × 15 cm sheet with four copies for printing.</li>
    </ol>
    <h2>Taking a photo that gets accepted</h2>
    <ul>
      <li>Plain, light background — a white wall is enough</li>
      <li>No hat, no sunglasses, ears and forehead visible</li>
      <li>Neutral expression, mouth closed, eyes open</li>
      <li>Even lighting from the front, no hard shadow behind the head</li>
      <li>Phone at eye level, not looking up at your face</li>
    </ul>
    <h2>Where can I print it?</h2>
    <p>The 4-photo sheet is exactly 10 × 15 cm at 300 dpi, the size of a standard photo print. Any photo shop or self-service kiosk can print it, and you cut the four photos yourself along the light guide lines.</p>
    <h2>Private by design</h2>
    <p>Your face never leaves your device: cropping and resizing run locally in the browser.</p>
  </div>
"""

# =============================== FAVICON ===============================
fav_tool = drop_box("⭐", "Drop a square logo here", "or tap to choose · PNG, JPG or WebP", "image/*") + """
  <div class="preview" id="prev">
    <img id="prevImg" style="image-rendering:pixelated;max-height:120px">
    <div class="cap" id="prevCap"></div>
  </div>

  <div class="res" id="res">
    <div id="items"></div>
    <button class="allbtn" id="dlIco">⬇ Download favicon.ico</button>
    <button class="allbtn" id="dlPngs" style="margin-top:9px;background:linear-gradient(145deg,#10B981,#059669)">⬇ Download PNG set</button>
    <div class="opts" style="margin-top:12px">
      <div class="opt" style="margin-bottom:0">
        <div class="lbl"><span>HTML to paste in &lt;head&gt;</span></div>
        <pre id="code" style="background:#FFF7EF;border:1px solid #F0E4D8;border-radius:10px;padding:11px;font-size:10.5px;overflow:auto;color:#6B5647;margin:0"></pre>
      </div>
    </div>
  </div>
"""

fav_js = """
var S = { img: null, pngs: [], ico: null };
var drop = document.getElementById('drop'), fileIn = document.getElementById('file');
var prev = document.getElementById('prev'), prevImg = document.getElementById('prevImg'), prevCap = document.getElementById('prevCap');
var resBox = document.getElementById('res'), items = document.getElementById('items');

var SIZES = [16, 32, 48, 64, 180, 192, 512];

drop.onclick = function(){ fileIn.click(); };
fileIn.onchange = function(e){ if (e.target.files[0]) load(e.target.files[0]); e.target.value = ''; };
['dragover','dragenter'].forEach(function(t){ drop.addEventListener(t, function(e){ e.preventDefault(); drop.classList.add('over'); }); });
['dragleave','drop'].forEach(function(t){ drop.addEventListener(t, function(e){ e.preventDefault(); drop.classList.remove('over'); }); });
drop.addEventListener('drop', function(e){ if (e.dataTransfer && e.dataTransfer.files[0]) load(e.dataTransfer.files[0]); });

function squareCanvas(size){
  var cv = document.createElement('canvas');
  cv.width = size; cv.height = size;
  var ctx = cv.getContext('2d');
  ctx.fillStyle = '#fff';
  ctx.fillRect(0, 0, size, size);
  var w = S.img.naturalWidth, h = S.img.naturalHeight;
  var s = Math.min(w, h);
  ctx.drawImage(S.img, (w - s) / 2, (h - s) / 2, s, s, 0, 0, size, size);
  return cv;
}

async function load(f){
  var o = await loadImg(f);
  S.img = o.img;
  prev.classList.add('show');
  resBox.classList.add('show');
  prevImg.src = o.url;
  prevCap.textContent = S.img.naturalWidth + ' × ' + S.img.naturalHeight + ' original';

  S.pngs = [];
  items.innerHTML = '';
  for (var i = 0; i < SIZES.length; i++){
    var size = SIZES[i];
    var cv = squareCanvas(size);
    var blob = await canvasBlob(cv, 'image/png');
    var url = URL.createObjectURL(blob);
    S.pngs.push({ size: size, blob: blob, url: url });

    var box = document.createElement('div');
    box.className = 'item';
    var img = document.createElement('img');
    img.src = url; img.style.objectFit = 'contain'; img.style.imageRendering = 'pixelated';
    var inf = document.createElement('div'); inf.className = 'inf';
    inf.innerHTML = '<div class="nm">' + size + ' × ' + size + '</div><div class="sz">' + fmtSize(blob.size) +
      (size === 180 ? ' · Apple touch icon' : (size === 512 ? ' · PWA icon' : '')) + '</div>';
    var btn = document.createElement('button'); btn.className = 'dl'; btn.textContent = '⬇ Save';
    btn.onclick = (function(u, s){ return function(){ dlUrl(u, 'favicon-' + s + '.png'); }; })(url, size);
    box.appendChild(img); box.appendChild(inf); box.appendChild(btn);
    items.appendChild(box);
  }

  // build .ico from 16/32/48
  var icoSizes = [16, 32, 48];
  var bufs = [];
  for (var k = 0; k < icoSizes.length; k++){
    var found = S.pngs.filter(function(p){ return p.size === icoSizes[k]; })[0];
    var ab = await found.blob.arrayBuffer();
    bufs.push({ size: icoSizes[k], buf: new Uint8Array(ab) });
  }
  S.ico = buildIco(bufs);

  document.getElementById('code').textContent =
    '<link rel="icon" href="/favicon.ico" sizes="any">\\n' +
    '<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">\\n' +
    '<link rel="apple-touch-icon" sizes="180x180" href="/favicon-180.png">';
}

function buildIco(list){
  var n = list.length;
  var header = new Uint8Array(6);
  header[2] = 1; header[4] = n & 255; header[5] = (n >> 8) & 255;
  var dir = new Uint8Array(16 * n);
  var offset = 6 + 16 * n;
  for (var i = 0; i < n; i++){
    var o = i * 16, p = list[i];
    dir[o] = p.size >= 256 ? 0 : p.size;
    dir[o + 1] = p.size >= 256 ? 0 : p.size;
    dir[o + 4] = 1; dir[o + 6] = 32;
    var len = p.buf.length;
    dir[o + 8] = len & 255; dir[o + 9] = (len >> 8) & 255;
    dir[o + 10] = (len >> 16) & 255; dir[o + 11] = (len >> 24) & 255;
    dir[o + 12] = offset & 255; dir[o + 13] = (offset >> 8) & 255;
    dir[o + 14] = (offset >> 16) & 255; dir[o + 15] = (offset >> 24) & 255;
    offset += len;
  }
  var out = new Uint8Array(offset);
  out.set(header, 0); out.set(dir, 6);
  var pos = 6 + 16 * n;
  for (var j = 0; j < n; j++){ out.set(list[j].buf, pos); pos += list[j].buf.length; }
  return new Blob([out], { type: 'image/x-icon' });
}

document.getElementById('dlIco').onclick = function(){
  if (!S.ico){ toast('Add an image first'); return; }
  dlUrl(URL.createObjectURL(S.ico), 'favicon.ico');
};
document.getElementById('dlPngs').onclick = function(){
  if (!S.pngs.length){ toast('Add an image first'); return; }
  var i = 0;
  (function next(){
    if (i >= S.pngs.length) return;
    var p = S.pngs[i++];
    dlUrl(p.url, 'favicon-' + p.size + '.png');
    setTimeout(next, 320);
  })();
};
"""

fav_content = """
  <div class="content">
    <h2>How to create a favicon</h2>
    <ol>
      <li>Upload a square logo or image — at least 512 × 512 is ideal.</li>
      <li>Download <b>favicon.ico</b> for the browser tab, or the full PNG set.</li>
      <li>Copy the HTML snippet and paste it inside your page’s &lt;head&gt;.</li>
    </ol>
    <h2>Which sizes do I actually need?</h2>
    <ul>
      <li><b>favicon.ico</b> — the classic tab icon, contains 16, 32 and 48 px</li>
      <li><b>32 × 32 PNG</b> — crisp tab icon on modern browsers</li>
      <li><b>180 × 180 PNG</b> — Apple touch icon for iPhone home screens</li>
      <li><b>192 / 512 PNG</b> — required by Android and by a web app manifest</li>
    </ul>
    <h2>Why does my favicon look blurry?</h2>
    <p>Because the source was too small. Browsers do not scale up nicely. Start with at least 512 × 512, and keep the design simple — a single letter or shape reads better at 16 px than a detailed illustration.</p>
    <h2>Nothing is uploaded</h2>
    <p>All sizes are generated in your browser, so your logo stays on your device.</p>
  </div>
"""

NEW = [
    ("merge", "merge-pdf.html", "Merge PDF", "Merge PDF Files Online — Free &amp; Private",
     "Combine multiple PDF files into one document for free. Reorder pages, no upload, no watermark — merging happens in your browser.",
     merge_tool, merge_js, merge_content,
     '<script src="https://cdn.jsdelivr.net/npm/pdf-lib@1.17.1/dist/pdf-lib.min.js"></script>'),

    ("pdf2jpg", "pdf-to-jpg.html", "PDF to JPG", "PDF to JPG Converter — Free, High Resolution",
     "Convert PDF pages into sharp JPG images online for free. Choose 1×, 2× or 3× resolution. No upload, no watermark.",
     pdf2jpg_tool, pdf2jpg_js, pdf2jpg_content,
     '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>'),

    ("passport", "passport-photo.html", "Passport Photo", "Passport Photo Maker — 35×45 mm, 2×2 in, Free",
     "Create a passport or visa photo at 35 × 45 mm, 51 × 51 mm or 2 × 2 inches, and download a printable 10 × 15 cm sheet with four copies. Free and private.",
     passport_tool, passport_js, passport_content, ""),

    ("fav", "favicon-maker.html", "Favicon", "Favicon Generator — .ico + PNG set, Free",
     "Generate a favicon.ico and the full PNG set (16 to 512 px) from any image. Includes the HTML snippet to paste. Free and private.",
     fav_tool, fav_js, fav_content, ""),
]

for active, filename, label, title, desc, tool_html, tool_js, content, lib in NEW:
    G.page(active, filename, title, label, desc, recolor(tool_html), tool_js, recolor(content), extra_js_lib=lib)
    # the js uses no palette literals, but recolor for safety
    path = os.path.join(OUT, filename)
    html = open(path, encoding='utf-8').read()
    html = recolor(html)
    open(path, 'w', encoding='utf-8').write(html)
    print("wrote", filename, len(html))

# ---------- repaint the existing pages ----------
for f in ["compress.html", "tools.html", "resize-image.html", "webp-converter.html",
          "crop-image.html", "rotate-image.html", "image-to-pdf.html"]:
    p = os.path.join(OUT, f)
    if not os.path.exists(p):
        continue
    s = open(p, encoding='utf-8').read()
    s = recolor(s)
    open(p, 'w', encoding='utf-8').write(s)
    print("recolored", f)

print("done")
