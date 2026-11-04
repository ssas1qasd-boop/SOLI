import sys, os, json, struct
sys.path.insert(0,'/tmp/claude-0/rdsrc/renderdoc/build/lib')
os.environ['DISPLAY']=':84'
import renderdoc as rd
rd.InitialiseReplay(rd.GlobalEnvironment(), [])
cap = rd.OpenCaptureFile(); cap.OpenFile(sys.argv[1], '', None)
r, ctrl = cap.OpenCapture(rd.ReplayOptions(), None)
sf = ctrl.GetStructuredFile(); tag = sys.argv[2]
res = {str(x.resourceId): x.name for x in ctrl.GetResources()}
acts=[]
def walk(a):
    for x in a: acts.append(x); walk(x.children)
walk(ctrl.GetRootActions())
B=rd.SDBasic
def sv(c):
    t=c.type.basetype
    if c.NumChildren()>0 and t in (B.Array,B.Struct): return '['+', '.join(sv(c.GetChild(i)) for i in range(c.NumChildren()))+']'
    if t==B.Resource: return res.get(str(c.AsResourceId()),'0')
    if t==B.Float: return ('%g'%c.AsFloat())
    if t in (B.UnsignedInteger,B.SignedInteger): 
        s=c.AsString(); return s if s else str(c.AsInt())
    if t==B.Boolean: return str(c.AsBool())
    return c.AsString()
# all API calls in frame
evs=[]
for a in acts:
    for e in a.events:
        ch = sf.chunks[e.chunkIndex]
        ps=[]
        for i in range(ch.NumChildren()):
            c=ch.GetChild(i); v=sv(c)
            if c.name=='DebugMessages' or c.name=='Program' : continue
            ps.append('%s = %s'%(c.name, v))
        evs.append((e.eventId, ch.name, ', '.join(ps)))
out={'events':evs,'draws':[]}
for a in acts:
    if not (a.flags & rd.ActionFlags.Drawcall): continue
    ctrl.SetFrameEvent(a.eventId, True)
    gl = ctrl.GetGLPipelineState(); ps = ctrl.GetPipelineState()
    d={'eid':a.eventId,'name':a.GetName(sf),'n':a.numIndices}
    d['vao']=res.get(str(gl.vertexInput.vertexArrayObject), str(gl.vertexInput.vertexArrayObject))
    d['ibuf']=res.get(str(gl.vertexInput.indexBuffer), str(gl.vertexInput.indexBuffer))
    at=gl.vertexInput.attributes[0]
    vb=gl.vertexInput.vertexBuffers[at.vertexBufferSlot]
    d['attr0']={'enabled':at.enabled,'fmt':at.format.Name(),'comp':at.format.compCount,'slot':at.vertexBufferSlot,'offset':at.byteOffset,
               'buf':res.get(str(vb.resourceId),str(vb.resourceId)),'stride':vb.byteStride}
    # raw vertex buffer contents
    raw=ctrl.GetBufferData(vb.resourceId,0,0); nf=len(raw)//4
    d['vbuf']=[round(x,3) for x in struct.unpack('%df'%nf, raw[:nf*4])]
    if gl.vertexInput.indexBuffer!=rd.ResourceId.Null():
        ib=ctrl.GetBufferData(gl.vertexInput.indexBuffer,0,0); d['idx']=list(struct.unpack('%dI'%(len(ib)//4),ib))
    # uniforms
    refl=ps.GetShaderReflection(rd.ShaderStage.Vertex); u={}
    for st in (rd.ShaderStage.Vertex, rd.ShaderStage.Pixel):
        refl=ps.GetShaderReflection(st); 
        for i,cb in enumerate(refl.constantBlocks):
            vars=ctrl.GetCBufferVariableContents(ps.GetGraphicsPipelineObject(), refl.resourceId, st, ps.GetShaderEntryPoint(st), i, rd.ResourceId.Null(),0,0)
            for v in vars: u[v.name]=[round(x,3) for x in v.value.f32v[:v.columns]]
    d['uni']=u
    d['prog']=res.get(str(gl.vertexShader.programResourceId),'')
    d['vs']=gl.vertexShader.reflection.rawBytes.decode(errors='ignore') if False else ''
    # post VS positions
    m=ctrl.GetPostVSData(0,0,rd.MeshDataStage.VSOut)
    pv=ctrl.GetBufferData(m.vertexResourceId, m.vertexByteOffset, 0)
    d['post']=[ [round(x,3) for x in struct.unpack_from('4f',pv,i*m.vertexByteStride)] for i in range(len(pv)//m.vertexByteStride)]
    # output image
    tgt=ps.GetOutputTargets()[0].resource
    s=rd.TextureSave(); s.resourceId=tgt; s.destType=rd.FileType.PNG
    fn='%s_eid%d.png'%(tag,a.eventId); ctrl.SaveTexture(s, os.path.abspath(fn)); d['png']=fn
    d['target']=res.get(str(tgt),str(tgt))
    out['draws'].append(d)
json.dump(out,open(tag+'.json','w'),indent=1)
for d in out['draws']: print(json.dumps({k:v for k,v in d.items() if k not in('vbuf',)}))
ctrl.Shutdown(); cap.Shutdown(); rd.ShutdownReplay()
