gsap.registerPlugin(ScrollTrigger);
const reduced = window.matchMedia('(prefers-reduced-motion:reduce)').matches;

/* ── Scroll progress bar ── */
window.addEventListener('scroll',()=>{
  const p = window.scrollY/(document.body.scrollHeight-window.innerHeight);
  document.getElementById('prog').style.transform=`scaleX(${p})`;
},{passive:true});

/* ── Custom cursor ── */
(()=>{
  const c=document.getElementById('cur');
  if(!c)return;
  let mx=0,my=0,cx=0,cy=0;
  window.addEventListener('mousemove',e=>{mx=e.clientX;my=e.clientY},{passive:true});
  (function loop(){
    cx+=(mx-cx)*.14;
    cy+=(my-cy)*.14;
    c.style.transform=`translate(${cx}px,${cy}px) translate(-50%,-50%)`;
    requestAnimationFrame(loop);
  })();
  document.querySelectorAll('a,button,.mc,.wc,.btn').forEach(el=>{
    el.addEventListener('mouseenter',()=>c.classList.add('big'));
    el.addEventListener('mouseleave',()=>c.classList.remove('big'));
  });
})();

/* ── Nav entrance ── */
gsap.to('.nav',{opacity:1,y:0,duration:.6,ease:'power3.out',delay:.1});

/* ── Hero: line-by-line clip reveal ── */
if(!reduced){
  gsap.fromTo('.hero-eye',{opacity:0,y:40},{opacity:1,y:0,duration:1,ease:'power3.out',delay:.35});
  document.querySelectorAll('.hero-h1 .line').forEach((line,i)=>{
    gsap.fromTo(line,{y:'112%'},{y:'0%',duration:1.1,ease:'power3.out',delay:.5+i*.14});
  });
  gsap.fromTo('.hero-rule',{opacity:0,scaleX:0},{opacity:1,scaleX:1,duration:.9,ease:'power3.out',delay:1.25,transformOrigin:'left'});
  gsap.fromTo('.hero-bottom',{opacity:0,y:32},{opacity:1,y:0,duration:.85,ease:'power3.out',delay:1.4});
}else{
  document.querySelectorAll('.hero-eye,.hero-rule,.hero-bottom')
    .forEach(el=>Object.assign(el.style,{opacity:1,transform:'none'}));
  document.querySelectorAll('.hero-h1 .line')
    .forEach(el=>Object.assign(el.style,{transform:'translateY(0)'}));
}

/* ── Lifestyle strip parallax ── */
(()=>{
  const strip=document.querySelector('.life');
  const bg=document.getElementById('lifeBg');
  if(!strip||!bg)return;
  function upd(){
    const r=strip.getBoundingClientRect();
    if(r.bottom<0||r.top>window.innerHeight)return;
    const f=(window.innerHeight/2-(r.top+r.height/2))/window.innerHeight;
    bg.style.transform=`translateY(${f*55}px)`;
  }
  window.addEventListener('scroll',upd,{passive:true});
  window.addEventListener('resize',upd);upd();
})();

/* ── 3D card tilt on menu cards ── */
if(!reduced){
  document.querySelectorAll('.mc').forEach(card=>{
    card.addEventListener('mousemove',e=>{
      const r=card.getBoundingClientRect();
      const x=(e.clientX-r.left)/r.width-.5;
      const y=(e.clientY-r.top)/r.height-.5;
      gsap.to(card,{rotateX:-y*10,rotateY:x*10,duration:.3,ease:'power2.out',overwrite:'auto'});
    });
    card.addEventListener('mouseleave',()=>{
      gsap.to(card,{rotateX:0,rotateY:0,duration:.7,ease:'elastic.out(1,.6)',overwrite:'auto'});
    });
  });
}

/* ════════════════════════════════════════════════════════
   DISH BUILDING SCENE  — unified 17-frame scroll scrub
   Phases:
     01  frames 01–06  ingredient layers fall onto the plate
     02  frames 07–09  dish assembled beautifully
     03  frames 10–12  meal sealed in its container
     04  frames 13–17  container packed & box closes → delivered
════════════════════════════════════════════════════════ */
(()=>{
  const section   = document.querySelector('.ex-section');
  if(!section) return;

  const etEye     = document.getElementById('etEye');
  const etH       = document.getElementById('etH');
  const exStep    = document.getElementById('exStep');
  const exStepNum = document.getElementById('exStepNum');
  const exStepLbl = document.getElementById('exStepLbl');
  const exInfo    = document.getElementById('exInfo');
  const phi1      = document.getElementById('phi1');
  const phi2      = document.getElementById('phi2');
  const phi3      = document.getElementById('phi3');
  const phi4      = document.getElementById('phi4');

  const fallSeqEl = document.getElementById('fallSeq');
  const fallImgs  = fallSeqEl ? Array.from(fallSeqEl.querySelectorAll('.fall-img')) : [];
  const buildLabels = Array.from(document.querySelectorAll('[data-build-label]'));
  const N         = fallImgs.length;
  if (!N) return;
  let currentProgress = 0;

  function mix(a, b, t) {
    return a + (b - a) * t;
  }

  function phaseProgress(value, start, end) {
    return gsap.utils.clamp(0, 1, (value - start) / (end - start));
  }

  function clamp01(value) {
    return gsap.utils.clamp(0, 1, value);
  }

  function smoothstep(t) {
    return t * t * (3 - 2 * t);
  }

  function getScenePose(frame) {
    if (frame < 6.2) {
      const t = smoothstep(phaseProgress(frame, 0, 6.2));
      return {
        x: mix(106, 26, t),
        y: mix(-138, 0, t),
        scale: mix(0.76, 1.015, t),
        rotate: mix(-11, 0, t),
        ampY: mix(40, 12, t),
        ampX: mix(10, 2, t),
        ampR: mix(-4.2, -0.6, t),
      };
    }

    if (frame < 9.2) {
      const t = smoothstep(phaseProgress(frame, 6.2, 9.2));
      return {
        x: mix(4, 0, t),
        y: mix(10, 0, t),
        scale: mix(1.02, 1.02, t),
        rotate: mix(1.4, 0, t),
        ampY: mix(9, 5, t),
        ampX: mix(2, 1, t),
        ampR: mix(1, 0.3, t),
      };
    }

    if (frame < 12.9) {
      const t = smoothstep(phaseProgress(frame, 9.2, 12.9));
      return {
        x: mix(7, 0, t),
        y: mix(30, 0, t),
        scale: mix(1.05, 0.99, t),
        rotate: mix(-2.5, 0, t),
        ampY: mix(8, 5, t),
        ampX: mix(3, 1, t),
        ampR: mix(0.8, 0.2, t),
      };
    }

    const t = smoothstep(phaseProgress(frame, 12.9, N - 1));
    return {
      x: mix(8, 0, t),
      y: mix(-4, 0, t),
      scale: mix(1.02, 1, t),
      rotate: mix(3, 0, t),
      ampY: mix(10, 4, t),
      ampX: mix(-4, -1, t),
      ampR: mix(-1.1, -0.2, t),
    };
  }

  function mapProgressToFrame(progress) {
    const p = clamp01(progress);
    const segments = [
      [0.00, 0.08, 0.00, 0.06],
      [0.08, 0.22, 0.06, 0.95],
      [0.22, 0.38, 0.95, 2.05],
      [0.38, 0.56, 2.05, 6.20],
      [0.56, 0.74, 6.20, 9.20],
      [0.74, 0.90, 9.20, 12.90],
      [0.90, 1.00, 12.90, N - 1],
    ];

    for (const [start, end, from, to] of segments) {
      if (p <= end) {
        const local = smoothstep(phaseProgress(p, start, end));
        return mix(from, to, local);
      }
    }
    return N - 1;
  }

  function updateBuildLabels(idx) {
    const clamped = Math.max(0, Math.min(N - 1, idx));
    const visible = clamped < 6.05 && currentProgress > 0.08;
    let activeMax = -1;

    if (visible) {
      if (clamped < 1.15) activeMax = 0;
      else if (clamped < 2.15) activeMax = 1;
      else if (clamped < 3.2) activeMax = 2;
      else activeMax = 3;
    }

    buildLabels.forEach((label) => {
      const step = Number(label.dataset.buildLabel);
      const isOn = visible && step <= activeMax;
      label.classList.toggle('is-on', isOn);

      if (isOn) {
        const row = activeMax - step;
        label.style.transform = `translateX(0) translateY(${row * 46}px)`;
      } else {
        label.style.transform = 'translateX(-18px) translateY(8px)';
      }
    });
  }

  function showFrame(idx) {
    const clamped = Math.max(0, Math.min(N - 1, idx));
    const visualFrame = clamped < 6.2 ? Math.round(clamped) : clamped;
    const lo = Math.floor(visualFrame);
    const hi = Math.min(N - 1, lo + 1);
    const t  = smoothstep(visualFrame - lo);
    const pose = getScenePose(clamped);
    const seqOpacity = smoothstep(phaseProgress(currentProgress, 0.06, 0.16));

    if (fallSeqEl) {
      fallSeqEl.style.opacity = seqOpacity.toFixed(3);
      fallSeqEl.style.transform = `translate(-50%, -50%) translate3d(${pose.x.toFixed(1)}px, ${pose.y.toFixed(1)}px, 0) scale(${pose.scale.toFixed(3)}) rotate(${pose.rotate.toFixed(2)}deg)`;
      fallSeqEl.style.filter = 'drop-shadow(0 34px 46px rgba(0,0,0,.16))';
    }

    fallImgs.forEach((img, i) => {
      const dist = i - visualFrame;
      const isBuildFrame = clamped < 6.2 && i <= 5;
      const shiftY = isBuildFrame ? 0 : dist * -pose.ampY;
      const shiftX = isBuildFrame ? 0 : dist * pose.ampX;
      const scale = isBuildFrame ? 1 : 1 - Math.min(Math.abs(dist) * 0.045, 0.12);
      const rotate = isBuildFrame ? 0 : dist * pose.ampR;

      if      (i === lo) img.style.opacity = (1 - t).toFixed(3);
      else if (i === hi) img.style.opacity = t.toFixed(3);
      else               img.style.opacity = '0';

      img.style.transform = `translate3d(${shiftX.toFixed(1)}px, ${shiftY.toFixed(1)}px, 0) scale(${scale.toFixed(3)}) rotate(${rotate.toFixed(2)}deg)`;
    });
    updateBuildLabels(clamped);
  }

  if(reduced){
    currentProgress = 1;
    if(fallSeqEl){ gsap.set(fallSeqEl,{opacity:1}); showFrame(N-1); }
    gsap.set(exStep, {opacity:1});
    return;
  }

  /* ── initial states ── */
  if(fallSeqEl) gsap.set(fallSeqEl, {opacity:0});
  showFrame(0);
  gsap.set(exInfo,               {yPercent:0, opacity:0, scale:.94, y:16});
  gsap.set([phi1,phi2,phi3,phi4],{opacity:0, y:18});
  gsap.set(exStep,               {opacity:0});
  gsap.set([etEye,etH],          {opacity:0, y:26, x:-18});

  const tl = gsap.timeline();

  /* rAF smoothing: keeps frame transitions fluid even when scroll delta spikes */
  let targetF = 0, currF = 0, lastTick = performance.now();
  (function tick(now) {
    const dt = Math.min(64, now - lastTick || 16.7);
    lastTick = now;
    const d = targetF - currF;
    const smoothingMs = Math.abs(d) > 1.8 ? 74 : 140;
    const alpha = 1 - Math.exp(-dt / smoothingMs);
    if (Math.abs(d) > 0.001) {
      currF += d * alpha;
      showFrame(currF);
    }
    requestAnimationFrame(tick);
  })(lastTick);

  /* ── 0: step pill + opening title ── */
  tl.to(exStep,{opacity:1, duration:.55, ease:'power3.out'}, 0)
    .to(etEye, {opacity:1, y:0, duration:.55, ease:'power3.out'}, .12)
    .to(etH,   {opacity:1, y:0, duration:.75, ease:'power3.out'}, .24);

  /* ── Phase 1 end: title out, phi1 in ── */
  tl.to([etEye,etH], {opacity:0, y:-22, duration:.38, ease:'power2.inOut'}, 5.35);
  tl.to(phi1,        {opacity:1, y:0,   duration:.55, ease:'power3.out'}, 5.55);

  /* ── Phase 2: assembled → show info panel after the build stack clears ── */
  tl.to(phi1,   {opacity:0, y:-16, duration:.42, ease:'power2.inOut'}, 7.18);
  tl.call(()=>{exStepNum.textContent='01'; exStepLbl.textContent='BUILT FRESH'}, null, 7.55);
  tl.to(exInfo, {yPercent:0, opacity:1, scale:1, y:0, duration:.68, ease:'power3.out'}, 7.62);

  /* ── Phase 3: container → hide info, phi2 ── */
  tl.to(exInfo, {yPercent:0, opacity:0, scale:.9, duration:.45, ease:'power2.inOut'}, 9.66);
  tl.call(()=>{exStepNum.textContent='02'; exStepLbl.textContent='SEALED FRESH'}, null, 10.0);
  tl.to(phi2,   {opacity:1, y:0, duration:.62, ease:'power3.out'}, 10.06);

  /* ── Phase 4 start: box packing → phi3 ── */
  tl.to(phi2, {opacity:0, y:-16, duration:.4, ease:'power2.inOut'}, 11.92);
  tl.call(()=>{exStepNum.textContent='03'; exStepLbl.textContent='IN THE BOX'}, null, 12.25);
  tl.to(phi3, {opacity:1, y:0, duration:.58, ease:'power3.out'}, 12.32);

  /* ── Delivered ── */
  tl.to(phi3, {opacity:0, y:-16, duration:.38, ease:'power2.inOut'}, 13.3);
  tl.call(()=>{exStepNum.textContent='04'; exStepLbl.textContent='TO YOUR DOOR'}, null, 13.55);
  tl.to(phi4, {opacity:1, y:0, duration:.6, ease:'power3.out'}, 13.63);

  /* ── scrub to scroll ── */
  ScrollTrigger.create({
    trigger: section,
    start:   'top top',
    end:     'bottom bottom',
    scrub:   1.05,
    animation: tl,
    onUpdate: (self) => {
      currentProgress = self.progress;
      targetF = mapProgressToFrame(self.progress);
    },
  });

  let rt;
  window.addEventListener('resize', ()=>{
    clearTimeout(rt);
    rt = setTimeout(()=>ScrollTrigger.refresh(), 200);
  });
})();

/* ── Menu cards + generic reveals (CSS class-based) ── */
const obs=new IntersectionObserver(entries=>{
  entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('show');obs.unobserve(e.target)}});
},{threshold:.07});
document.querySelectorAll('.mc,.reveal').forEach(el=>obs.observe(el));

/* ── Why cards: odd slides from left, even from right ── */
if(!reduced){
  document.querySelectorAll('.wc').forEach((el,i)=>{
    gsap.set(el,{opacity:0,x:i%2===0?-72:72,y:28});
    const o=new IntersectionObserver(entries=>{
      entries.forEach(e=>{
        if(!e.isIntersecting)return;
        gsap.to(e.target,{opacity:1,x:0,y:0,duration:.95,ease:'power3.out',delay:i*.1,
          onComplete:()=>{
            e.target.classList.add('show');
            gsap.set(e.target,{clearProps:'all'});
          }
        });
        o.disconnect();
      });
    },{threshold:.08});
    o.observe(el);
  });
}else{
  document.querySelectorAll('.wc').forEach(el=>el.classList.add('show'));
}

/* ── Testimonials: #1 from left, #2 from below, #3 from right ── */
if(!reduced){
  const dirs=[{x:-76,y:0},{x:0,y:64},{x:76,y:0}];
  document.querySelectorAll('.tc').forEach((el,i)=>{
    const d=dirs[i%3];
    gsap.set(el,{opacity:0,...d});
    const o=new IntersectionObserver(entries=>{
      entries.forEach(e=>{
        if(!e.isIntersecting)return;
        gsap.to(e.target,{opacity:1,x:0,y:0,duration:1,ease:'power3.out',delay:i*.16,
          onComplete:()=>{
            e.target.classList.add('show');
            gsap.set(e.target,{clearProps:'all'});
          }
        });
        o.disconnect();
      });
    },{threshold:.1});
    o.observe(el);
  });
}else{
  document.querySelectorAll('.tc').forEach(el=>el.classList.add('show'));
}

/* ── CTA heading: word-by-word spring rise ── */
(()=>{
  const ctaH2=document.getElementById('ctaH2');
  if(!ctaH2)return;
  const words=ctaH2.querySelectorAll('.cta-word-inner');
  if(!reduced) gsap.set(words,{y:'110%'});
  const o=new IntersectionObserver(entries=>{
    entries.forEach(e=>{
      if(!e.isIntersecting)return;
      if(!reduced){
        words.forEach((w,i)=>gsap.to(w,{y:'0%',duration:1.15,ease:'back.out(1.4)',delay:i*.24}));
      }else{
        words.forEach(w=>{w.style.transform='translateY(0)';});
      }
      o.disconnect();
    });
  },{threshold:.3});
  o.observe(ctaH2);
})();
