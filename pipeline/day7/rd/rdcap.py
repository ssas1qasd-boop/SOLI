import sys, time, os
sys.path.insert(0,'/tmp/claude-0/rdsrc/renderdoc/build/lib')
os.environ['DISPLAY']=':84'
import renderdoc as rd
exe = sys.argv[1]; args=' '.join(sys.argv[2:])
opts = rd.CaptureOptions()
opts.refAllResources = True
res = rd.ExecuteAndInject(exe, os.getcwd(), args, [], os.path.abspath('cap'), opts, False)
print('inject', res.result, res.ident)
time.sleep(2)
tc = rd.CreateTargetControl('', res.ident, 'rdcap', True)
print('target', tc.GetTarget(), tc.GetAPI())
tc.TriggerCapture(1)
t0=time.time(); path=None
while time.time()-t0<20:
    m = tc.ReceiveMessage(None)
    if m.type == rd.TargetControlMessageType.NewCapture:
        path = m.newCapture.path; print('capture', path, m.newCapture.frameNumber); break
    if m.type == rd.TargetControlMessageType.Disconnected: print('disc'); break
tc.Shutdown()
os.system('pkill -x %s' % os.path.basename(exe)[:15])
