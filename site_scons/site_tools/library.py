import sys
from SCons.Script import *

def IsLibraryShared(env):
    if sys.platform=="win32":
        return (env["liblevel"]>1)
    else:
        return (env["enable_shared"] and (env["liblevel"]>0))

def BuildLibrary(env,target,sources):
    if env.IsLibraryShared():
        if sys.platform=="win32":
            return env.SharedLibrary(target,sources,MS_LINKER_SUBSYSTEM="WINDOWS")
        else:
            return env.SharedLibrary(target,sources,SHLIBVERSION=env["libversion"])
    elif env["liblevel"]==0:
        if env.get("enable_shared",False):
            return env.SharedObject(sources)
        else:
            return env.StaticObject(sources)
    else:
        return env.StaticLibrary(target,sources)

def exists(env):
    return True

def generate(env):
    env.AddMethod(BuildLibrary)
    env.AddMethod(IsLibraryShared)
