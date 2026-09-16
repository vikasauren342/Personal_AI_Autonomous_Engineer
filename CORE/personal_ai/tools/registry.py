import subprocess,sys
class ToolRegistry:
    def __init__(self,root,env):
        self.root,self.env=root,env; self.tools={'python':self.python,'shell':self.shell,'filesystem_read':self.filesystem_read}
    def python(self,code): return self._run([sys.executable,'-c',code])
    def shell(self,command): return self._run(command,shell=True)
    def filesystem_read(self,path):
        from pathlib import Path
        p=(self.root/str(path)).resolve()
        if not str(p).startswith(str(self.root.resolve())): raise PermissionError('path outside project root')
        return {'path':str(p),'content':p.read_text(encoding='utf-8')}
    def _run(self,cmd,shell=False):
        p=subprocess.run(cmd,shell=shell,capture_output=True,text=True,timeout=60); return {'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    def call(self,name,*args,**kwargs):
        if name not in self.tools: raise KeyError(name)
        return self.tools[name](*args,**kwargs)
