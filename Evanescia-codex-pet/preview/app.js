/* MIT — the sprite artwork has separate terms in assets/LICENSE.md. */
'use strict';
const states = [
  ['待机 · Idle',6],['向右移动',8],['向左移动',8],['挥手',4],['跳跃',5],
  ['失败反馈',8],['等待',6],['执行任务',6],['检查',6]
];
const canvas = document.querySelector('#pet');
const ctx = canvas.getContext('2d');
const image = new Image();
let row = 0, frame = 0, last = 0, looking = false, theme = 'dark', videoURL;
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const feedback = document.querySelector('#feedback');
const buttons = document.querySelector('#states');
function draw() {
  ctx.clearRect(0,0,192,208);
  if(image.complete && image.naturalWidth) ctx.drawImage(image,frame*192,row*208,192,208,0,0,192,208);
}
function selectState(index) {
  row=index; frame=0; looking=false; draw();
  document.querySelector('#state-label').textContent=states[index][0];
  [...buttons.children].forEach((b,i)=>b.setAttribute('aria-pressed',String(i===index)));
}
states.forEach(([name],index)=>{
  const button=document.createElement('button'); button.textContent=name.split(' · ')[0];
  button.setAttribute('aria-pressed',String(index===0));
  button.addEventListener('click',()=>selectState(index)); buttons.append(button);
});
image.onload=draw;
image.onerror=()=>{feedback.textContent='图集加载失败，请从仓库根目录启动本地服务器。';};
image.src='../assets/pet/spritesheet.png';
function animate(time) {
  if(!looking && !reducedMotion.matches && time-last>=140) {
    frame=(frame+1)%states[row][1]; last=time; draw();
  }
  requestAnimationFrame(animate);
}
requestAnimationFrame(animate);
function look() {
  const index=Number(document.querySelector('#gaze').value);
  row=9+Math.floor(index/8); frame=index%8; looking=true; draw();
  document.querySelector('#gaze-value').textContent=`${index*22.5}°`;
  document.querySelector('#state-label').textContent=`视线 · ${index*22.5}°`;
  [...buttons.children].forEach(b=>b.setAttribute('aria-pressed','false'));
}
document.querySelector('#gaze').addEventListener('input',look);
document.querySelector('#look').addEventListener('click',look);
document.querySelector('#toggle-theme').addEventListener('click',()=>{
  theme=theme==='dark'?'light':'dark'; document.documentElement.dataset.theme=theme;
  document.querySelector('#toggle-theme span').textContent=theme==='dark'?'切换浅色':'切换深色';
  feedback.textContent=theme==='dark'?'深色 · 粉紫夜色':'浅色 · 樱花浅色';
});
document.querySelector('#copy-theme').addEventListener('click',async()=>{
  try {
    const response=await fetch(`../themes/codex-theme-${theme}.txt`);
    if(!response.ok) throw new Error('theme');
    await navigator.clipboard.writeText((await response.text()).trim());
    feedback.textContent='主题文本已复制，请在 Codex 外观设置中导入。';
  } catch { feedback.textContent=`请直接打开 themes/codex-theme-${theme}.txt 复制完整文本。`; }
});
const video=document.querySelector('#background-video');
function clearVideo() {
  video.pause(); video.removeAttribute('src'); video.load();
  if(videoURL) URL.revokeObjectURL(videoURL);
  videoURL=undefined; document.querySelector('#video-file').value='';
  document.querySelector('#clear-video').hidden=true;
}
document.querySelector('#video-file').addEventListener('change',async event=>{
  const file=event.target.files[0]; if(!file) return;
  clearVideo(); videoURL=URL.createObjectURL(file); video.src=videoURL;
  document.querySelector('#clear-video').hidden=false;
  try { await video.play(); } catch { feedback.textContent='该视频无法播放，请选择浏览器支持的格式。'; }
});
document.querySelector('#clear-video').addEventListener('click',clearVideo);
window.addEventListener('pagehide',clearVideo);
