import sys
import os.path
import os
from SCons.Script import *

def exists(env):
    if env["PLATFORM"]=="win32":
        return False
    else:
        return True

def Install(env,src,instpath,instname=None,sysdir=True,mode=0o644,shlib=False):
    destpath=env.subst("$DESTDIR"+instpath)
    env.Alias("install",destpath)
    if instname:
        inst=env.InstallAs(os.path.join(destpath,instname),src)
    else:
        if shlib:
            inst=env.InstallVersionedLib(destpath,src)
        else:
            inst=env.Install(destpath,src)
    env.AddPostAction(inst,Chmod("$TARGET",mode))
    return inst

def InstallProgram(env,src):
    return Install(env,src,"$bindir",mode=0o755)

def InstallSpdModule(env,src):
    return Install(env,src,"$spd_module_dir",mode=0o755)

def InstallData(env,src,dest=None):
    if dest:
        inst=Install(env,src,os.path.join("$datadir","$package_name",dest))
    else:
        inst=Install(env,src,os.path.join("$datadir","$package_name"))
    env.Clean("install",env.subst("$DESTDIR$datadir/$package_name"))
    return inst

def InstallConfig(env,src,dest=None):
    if dest:
        inst=Install(env,src,os.path.join("$sysconfdir","$package_name",dest))
    else:
        inst=Install(env,src,os.path.join("$sysconfdir","$package_name"))
    env.Clean("install",env.subst("$DESTDIR$sysconfdir/$package_name"))
    return inst

def InstallStaticLibrary(env,src):
    return Install(env,src,"$libdir")

def InstallSharedLibrary(env,src):
    return Install(env,src,"$libdir",shlib=True,mode=0o755)

def InstallLibrary(env,src):
    if env.IsLibraryShared():
        return InstallSharedLibrary(env,src)
    else:
        return InstallStaticLibrary(env,src)

def InstallHeader(env,src):
    return Install(env,src,"$includedir")

def InstallServiceFile(env,src):
    service_file=env.Substfile(src,SUBST_DICT={"@bindir@":"$bindir"})
    return Install(env,service_file,"$servicedir")

def generate(env):
    env.AddMethod(InstallProgram)
    env.AddMethod(InstallData)
    env.AddMethod(InstallConfig)
    env.AddMethod(InstallLibrary)
    env.AddMethod(InstallHeader)
    env.AddMethod(InstallServiceFile)
    env.AddMethod(InstallSpdModule)
