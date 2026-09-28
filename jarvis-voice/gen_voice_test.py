"""
Gera audio da Francisca e cria HTML com reator sincronizado via Web Audio API.
"""
import asyncio, edge_tts, base64, os

TEXT = (
    "Olá. Sou Francisca, a voz do sistema Jarvis. "
    "Estou conectada ao núcleo de inteligência artificial e pronta para operar. "
    "Todos os sistemas estão funcionando normalmente. "
    "O reator de arco está ativo e respondendo à minha voz em tempo real. "
    "Pode me dar um comando a qualquer momento."
)

async def gen():
    c = edge_tts.Communicate(TEXT, "pt-BR-FranciscaNeural", rate="+5%")
    data = b""
    async for chunk in c.stream():
        if chunk["type"] == "audio":
            data += chunk["data"]
    return data

audio = asyncio.run(gen())
b64   = base64.b64encode(audio).decode()
print(f"[ok] Audio gerado: {len(audio)} bytes")

# ── HTML com reator + Web Audio API ──────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Jarvis — Voz Sincronizada</title>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{
    background:radial-gradient(ellipse at 50% 55%,#001428 0%,#000509 60%,#000 100%);
    min-height:100vh;display:flex;flex-direction:column;
    align-items:center;justify-content:center;
    font-family:'Segoe UI',sans-serif;overflow:hidden;
  }}
  .ambient{{
    position:fixed;inset:0;pointer-events:none;
    background:radial-gradient(ellipse 500px 400px at 50% 50%,#00aaff08 0%,transparent 70%);
    animation:ap 3s ease-in-out infinite;
  }}
  @keyframes ap{{0%,100%{{opacity:.6}}50%{{opacity:1}}}}
  canvas{{display:block}}
  .ui{{display:flex;flex-direction:column;align-items:center;gap:28px}}
  .status{{color:#00d4ff;font-size:11px;letter-spacing:5px;text-transform:uppercase;opacity:.8;display:flex;align-items:center;gap:10px}}
  .dot{{width:6px;height:6px;border-radius:50%;background:#00ff88;box-shadow:0 0 6px #00ff88;animation:blink 2s infinite}}
  @keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:.3}}}}
  .play-btn{{
    margin-top:4px;padding:12px 36px;border-radius:30px;
    border:1.5px solid #00d4ff66;background:transparent;
    color:#00d4ff;font-size:13px;letter-spacing:3px;text-transform:uppercase;
    cursor:pointer;transition:all .2s;
  }}
  .play-btn:hover{{background:#00d4ff15;border-color:#00d4ff;box-shadow:0 0 18px #00d4ff44}}
  .play-btn:disabled{{opacity:.4;cursor:default}}
  .vol-bar{{
    width:240px;height:4px;background:#00d4ff15;border-radius:2px;overflow:hidden;
  }}
  .vol-fill{{height:100%;background:#00d4ff;border-radius:2px;width:0%;transition:width .05s}}
</style>
</head>
<body>
<div class="ambient"></div>
<audio id="tts" src="data:audio/mp3;base64,{b64}" crossorigin="anonymous"></audio>

<div class="ui">
  <canvas id="arc" width="420" height="420"></canvas>
  <div class="status"><div class="dot"></div><span id="stxt">Reator em Espera</span></div>
  <div class="vol-bar"><div class="vol-fill" id="volFill"></div></div>
  <button class="play-btn" id="playBtn" onclick="startVoice()">▶ OUVIR FRANCISCA</button>
</div>

<script>
const canvas=document.getElementById('arc');
const ctx=canvas.getContext('2d');
const CX=210,CY=210;
let t=0,amp=0,smoothAmp=0,sparks=[],arcs=[];
let analyser=null,dataArray=null,audioCtx=null;

// ── Web Audio API ────────────────────────────────────────────
function startVoice(){{
  const audio=document.getElementById('tts');
  document.getElementById('playBtn').disabled=true;
  document.getElementById('stxt').textContent='Francisca está falando...';

  if(!audioCtx){{
    audioCtx=new (window.AudioContext||window.webkitAudioContext)();
    const src=audioCtx.createMediaElementSource(audio);
    analyser=audioCtx.createAnalyser();
    analyser.fftSize=512;
    analyser.smoothingTimeConstant=0.75;
    dataArray=new Uint8Array(analyser.frequencyBinCount);
    src.connect(analyser);
    analyser.connect(audioCtx.destination);
  }}

  audio.currentTime=0;
  audio.play();
  audio.onended=()=>{{
    document.getElementById('stxt').textContent='Transmissão concluída';
    document.getElementById('playBtn').disabled=false;
    document.getElementById('playBtn').textContent='↺ REPETIR';
    amp=0;
  }};
}}

function getAmp(){{
  if(!analyser) return 0;
  analyser.getByteFrequencyData(dataArray);
  // Foco na faixa de voz humana (250Hz–4kHz)
  const start=Math.floor(dataArray.length*0.05);
  const end  =Math.floor(dataArray.length*0.35);
  let sum=0;
  for(let i=start;i<end;i++) sum+=dataArray[i];
  return sum/(end-start)/255;
}}

// ── Sparks & Arcs ────────────────────────────────────────────
function spawnSpark(intensity){{
  const a=Math.random()*Math.PI*2, r=55+Math.random()*30;
  sparks.push({{
    x:CX+r*Math.cos(a),y:CY+r*Math.sin(a),
    vx:(Math.random()-.5)*3*intensity,vy:(Math.random()-.5)*3*intensity,
    life:1,decay:.04+Math.random()*.06
  }});
}}
function spawnArc(){{
  const a1=Math.random()*Math.PI*2,r1=55+Math.random()*25;
  const a2=a1+(Math.random()-.5)*1.4,r2=55+Math.random()*25;
  arcs.push({{
    x1:CX+r1*Math.cos(a1),y1:CY+r1*Math.sin(a1),
    x2:CX+r2*Math.cos(a2),y2:CY+r2*Math.sin(a2),
    mx:CX+(r1+r2)/2*Math.cos((a1+a2)/2)+(Math.random()-.5)*35,
    my:CY+(r1+r2)/2*Math.sin((a1+a2)/2)+(Math.random()-.5)*35,
    life:1,decay:.18
  }});
}}

// ── Draw ─────────────────────────────────────────────────────
function draw(){{
  amp=getAmp();
  smoothAmp=smoothAmp*.7+amp*.3;
  const A=smoothAmp;
  const beat=0.5+0.5*Math.sin(t*2);
  const eGlow=0.4+A*1.8;
  const speed=0.8+A*4;

  document.getElementById('volFill').style.width=(A*100*2.5)+'%';

  ctx.clearRect(0,0,420,420);

  // Anel externo metálico
  const gM=ctx.createRadialGradient(CX-10,CY-10,150,CX,CY,200);
  gM.addColorStop(0,'#2a3a4a');gM.addColorStop(.4,'#1a2535');gM.addColorStop(1,'#0a1520');
  ctx.beginPath();ctx.arc(CX,CY,195,0,Math.PI*2);ctx.fillStyle=gM;ctx.fill();
  ctx.beginPath();ctx.arc(CX,CY,195,0,Math.PI*2);
  ctx.strokeStyle='#2a4060';ctx.lineWidth=3;
  ctx.shadowColor='#004488';ctx.shadowBlur=8+A*20;ctx.stroke();ctx.shadowBlur=0;

  // Parafusos
  for(let i=0;i<3;i++){{
    const a=(i/3)*Math.PI*2-Math.PI/2;
    const bx=CX+182*Math.cos(a),by=CY+182*Math.sin(a);
    ctx.beginPath();ctx.arc(bx,by,7,0,Math.PI*2);
    const g=ctx.createRadialGradient(bx-2,by-2,1,bx,by,7);
    g.addColorStop(0,'#3a5070');g.addColorStop(1,'#0d1e2e');
    ctx.fillStyle=g;ctx.fill();
    ctx.strokeStyle=`rgba(0,170,255,${{0.1+A*.4}})`;ctx.lineWidth=1;ctx.stroke();
    ctx.strokeStyle='#1a3050';ctx.lineWidth=1.5;
    ctx.beginPath();ctx.moveTo(bx-3,by);ctx.lineTo(bx+3,by);ctx.stroke();
    ctx.beginPath();ctx.moveTo(bx,by-3);ctx.lineTo(bx,by+3);ctx.stroke();
  }}

  // Canal energético externo
  ctx.beginPath();ctx.arc(CX,CY,170,0,Math.PI*2);
  ctx.strokeStyle=`rgba(0,100,180,${{0.2+A*.6}})`;ctx.lineWidth=8;
  ctx.shadowColor='#0066cc';ctx.shadowBlur=10+A*25;ctx.stroke();ctx.shadowBlur=0;

  // Anel 1 (horário)
  ctx.save();ctx.translate(CX,CY);ctx.rotate(t*speed*.4);
  ctx.beginPath();ctx.arc(0,0,148,0,Math.PI*2);
  ctx.setLineDash([25,8,8,8,40,8,12,8]);
  ctx.strokeStyle=`rgba(0,170,255,${{0.5+A*1}})`;ctx.lineWidth=3+A*2;
  ctx.shadowColor='#00aaff';ctx.shadowBlur=12+A*30;ctx.stroke();
  ctx.setLineDash([]);ctx.restore();ctx.shadowBlur=0;

  // Anel 2 (anti-horário)
  ctx.save();ctx.translate(CX,CY);ctx.rotate(-t*speed*.65);
  ctx.beginPath();ctx.arc(0,0,128,0,Math.PI*2);
  ctx.setLineDash([15,10,35,10]);
  ctx.strokeStyle=`rgba(0,200,255,${{0.6+A*1}})`;ctx.lineWidth=2.5+A*2;
  ctx.shadowColor='#00ccff';ctx.shadowBlur=15+A*35;ctx.stroke();
  ctx.setLineDash([]);ctx.restore();ctx.shadowBlur=0;

  // Anel intermediário + marcações
  ctx.beginPath();ctx.arc(CX,CY,110,0,Math.PI*2);
  ctx.strokeStyle=`rgba(0,100,160,${{0.3+A*.5}})`;ctx.lineWidth=10+A*6;
  ctx.shadowColor='#0088cc';ctx.shadowBlur=8+A*20;ctx.stroke();ctx.shadowBlur=0;
  for(let i=0;i<12;i++){{
    const a=(i/12)*Math.PI*2+t*speed*.1;
    ctx.beginPath();
    ctx.moveTo(CX+100*Math.cos(a),CY+100*Math.sin(a));
    ctx.lineTo(CX+120*Math.cos(a),CY+120*Math.sin(a));
    ctx.strokeStyle=`rgba(0,180,255,${{0.3+A*.8}})`;
    ctx.lineWidth=i%3===0?2+A*2:1+A;
    ctx.shadowColor='#00aaff';ctx.shadowBlur=i%3===0?8+A*15:4+A*8;
    ctx.stroke();ctx.shadowBlur=0;
  }}

  // Anel interno (rápido)
  ctx.save();ctx.translate(CX,CY);ctx.rotate(t*speed*1.3);
  ctx.beginPath();ctx.arc(0,0,88,0,Math.PI*2);
  ctx.setLineDash([10,5,20,5,10,5,30,5]);
  ctx.strokeStyle=`rgba(100,220,255,${{0.7+A*1}})`;ctx.lineWidth=2+A*2;
  ctx.shadowColor='#00eeff';ctx.shadowBlur=18+A*40;ctx.stroke();
  ctx.setLineDash([]);ctx.restore();ctx.shadowBlur=0;

  // Triângulo duplo
  const triAng=-Math.PI/2+t*speed*.28;
  const triR=68, triAlpha=0.5+A*1.2;
  ctx.save();ctx.translate(CX,CY);ctx.rotate(triAng);
  ctx.beginPath();
  for(let i=0;i<3;i++){{
    const a=(i/3)*Math.PI*2-Math.PI/2;
    i===0?ctx.moveTo(triR*Math.cos(a),triR*Math.sin(a)):ctx.lineTo(triR*Math.cos(a),triR*Math.sin(a));
  }}
  ctx.closePath();
  ctx.strokeStyle=`rgba(0,220,255,${{triAlpha}})`;ctx.lineWidth=2+A*3;
  ctx.shadowColor='#00eeff';ctx.shadowBlur=22+A*45;ctx.stroke();
  ctx.rotate(Math.PI);
  ctx.beginPath();
  for(let i=0;i<3;i++){{
    const a=(i/3)*Math.PI*2-Math.PI/2;
    i===0?ctx.moveTo(triR*.6*Math.cos(a),triR*.6*Math.sin(a)):ctx.lineTo(triR*.6*Math.cos(a),triR*.6*Math.sin(a));
  }}
  ctx.closePath();
  ctx.strokeStyle=`rgba(150,240,255,${{triAlpha*.7}})`;ctx.lineWidth=1.5+A*2;
  ctx.shadowColor='#aaeeff';ctx.shadowBlur=12+A*25;ctx.stroke();
  ctx.restore();ctx.shadowBlur=0;

  // Vértices do triângulo
  for(let i=0;i<3;i++){{
    const a=triAng+(i/3)*Math.PI*2-Math.PI/2;
    const vx=CX+triR*Math.cos(a),vy=CY+triR*Math.sin(a);
    ctx.beginPath();ctx.arc(vx,vy,3+A*4,0,Math.PI*2);
    const gv=ctx.createRadialGradient(vx,vy,0,vx,vy,3+A*4);
    gv.addColorStop(0,'#ffffff');gv.addColorStop(1,'#00aaff');
    ctx.fillStyle=gv;ctx.shadowColor='#00ffff';ctx.shadowBlur=15+A*40;ctx.fill();ctx.shadowBlur=0;
  }}

  // Core — pulsa com a voz
  const coreSize=40+A*28;
  const gC0=ctx.createRadialGradient(CX,CY,0,CX,CY,coreSize+30);
  gC0.addColorStop(0,`rgba(180,240,255,${{0.1+A*.3}})`);gC0.addColorStop(1,'rgba(0,0,0,0)');
  ctx.beginPath();ctx.arc(CX,CY,coreSize+30,0,Math.PI*2);ctx.fillStyle=gC0;ctx.fill();

  const gC=ctx.createRadialGradient(CX-5,CY-5,0,CX,CY,coreSize);
  gC.addColorStop(0,'#ffffff');
  gC.addColorStop(.15,'#e8f8ff');
  gC.addColorStop(.45,`rgba(0,200,255,${{0.8+A*.2}})`);
  gC.addColorStop(.8,`rgba(0,80,180,${{0.7+A*.3}})`);
  gC.addColorStop(1,`rgba(0,20,60,0.4)`);
  ctx.beginPath();ctx.arc(CX,CY,coreSize,0,Math.PI*2);
  ctx.fillStyle=gC;ctx.shadowColor='#00eeff';ctx.shadowBlur=35+A*70;ctx.fill();ctx.shadowBlur=0;

  // Reflexo
  const gR=ctx.createRadialGradient(CX-12,CY-12,0,CX-12,CY-12,12+A*6);
  gR.addColorStop(0,`rgba(255,255,255,${{0.3+A*.4}})`);gR.addColorStop(1,'rgba(255,255,255,0)');
  ctx.beginPath();ctx.arc(CX-12,CY-12,12+A*6,0,Math.PI*2);ctx.fillStyle=gR;ctx.fill();

  // Raios radiais durante fala alta
  if(A>0.3){{
    for(let i=0;i<8;i++){{
      const a=(i/8)*Math.PI*2+t*1.5;
      const r0=coreSize, r1=r0+15+A*25;
      ctx.beginPath();
      ctx.moveTo(CX+r0*Math.cos(a),CY+r0*Math.sin(a));
      ctx.lineTo(CX+r1*Math.cos(a),CY+r1*Math.sin(a));
      ctx.strokeStyle=`rgba(0,240,255,${{A*.8}})`;ctx.lineWidth=1+A*2;
      ctx.shadowColor='#00ffff';ctx.shadowBlur=10+A*20;ctx.stroke();ctx.shadowBlur=0;
    }}
  }}

  // Sparks
  if(A>.15&&Math.random()<A*.25) spawnSpark(1+A*2);
  if(A>.4&&Math.random()<A*.1) spawnArc();
  sparks=sparks.filter(s=>s.life>0);
  sparks.forEach(s=>{{
    ctx.beginPath();ctx.arc(s.x,s.y,1.5,0,Math.PI*2);
    ctx.fillStyle=`rgba(100,220,255,${{s.life}})`;
    ctx.shadowColor='#00ffff';ctx.shadowBlur=8*s.life;ctx.fill();ctx.shadowBlur=0;
    s.x+=s.vx;s.y+=s.vy;s.vy+=.04;s.life-=s.decay;
  }});
  arcs=arcs.filter(a=>a.life>0);
  arcs.forEach(a=>{{
    ctx.beginPath();ctx.moveTo(a.x1,a.y1);ctx.quadraticCurveTo(a.mx,a.my,a.x2,a.y2);
    ctx.strokeStyle=`rgba(200,240,255,${{a.life*.9}})`;ctx.lineWidth=1+a.life;
    ctx.shadowColor='#ffffff';ctx.shadowBlur=12*a.life;ctx.stroke();ctx.shadowBlur=0;
    a.life-=a.decay;
  }});

  t+=0.016;
  requestAnimationFrame(draw);
}}
draw();
</script>
</body>
</html>"""

out = r"C:\Users\mau\Projetos\jarvis-voice\voice-sync-test.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print(f"[ok] HTML gerado: {out}")
