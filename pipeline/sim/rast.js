function rasterize(W,H){ // GL window coords, y up; returns Uint8Array mask in canvas rows (y down)
  const v=[[160,120],[320,360],[480,120]];
  const m=new Uint8Array(W*H); let n=0;
  const e=(a,b,px,py)=>(b[0]-a[0])*(py-a[1])-(b[1]-a[1])*(px-a[0]);
  const area=e(v[0],v[1],v[2][0],v[2][1]); const s=area<0?-1:1;
  const tl=(a,b)=>{const dy=(b[1]-a[1])*s, dx=(b[0]-a[0])*s; return (dy===0&&dx<0)||dy>0;};
  const E=[[v[0],v[1]],[v[1],v[2]],[v[2],v[0]]];
  for(let y=0;y<H;y++)for(let x=0;x<W;x++){const px=x+.5,py=y+.5;let ok=true;
    for(const [a,b] of E){const w=e(a,b,px,py)*s; if(w<0||(w===0&&!tl(a,b))){ok=false;break;}}
    if(ok){m[(H-1-y)*W+x]=1;n++;}}
  return {m,n};
}
if(typeof module!=='undefined'){const r=rasterize(640,480);let minx=1e9,maxx=0,miny=1e9,maxy=0;for(let i=0;i<r.m.length;i++)if(r.m[i]){const x=i%640,y=479-Math.floor(i/640);minx=Math.min(minx,x);maxx=Math.max(maxx,x);miny=Math.min(miny,y);maxy=Math.max(maxy,y);}console.log(r.n,minx,maxx,miny,maxy);}
