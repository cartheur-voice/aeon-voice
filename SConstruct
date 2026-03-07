# Scons build file (Linux-only)

import sys
import os
import os.path
import platform
import re

boost_includedir=Dir("#external").Dir("libs").Dir("boost").Dir("include")


def get_version(is_release):
    next_version="1.16.4"
    return next_version


def passthru(env, cmd, unique=False):
    return cmd.rstrip()


def CheckPKGConfig(context):
    context.Message("Checking for pkg-config... ")
    result=context.TryAction("pkg-config --version")[0]
    context.Result(result)
    return result


def CheckPKG(context,name):
    context.Message("Checking for {}... ".format(name))
    result=context.TryAction("pkg-config --exists '{}'".format(name))[0]
    context.Result(result)
    return result


def get_spd_module_dir():
    env = Environment()
    try:
        return env.ParseConfig("pkg-config speech-dispatcher --variable=modulebindir", passthru)
    except:
        return False


def validate_spd_version(key,val,env):
    m=re.match(r"^\d+\.\d+",val)
    if m is None:
        raise Exception("Invalid value of spd_version: {}".format(val))


def CheckSpdVersion(ctx):
    ctx.Message("Checking Speech Dispatcher version ... ")
    ver=ctx.env.get("spd_version",None)
    if ver is not None:
        ctx.Result(ver)
        return ver
    res, ver=ctx.TryAction("pkg-config --modversion speech-dispatcher > $TARGET")
    ver=ver.strip()
    if not res:
        src='#include <stdio.h>\n#include <speech-dispatcher/libspeechd_version.h>\nint main() {\nint major=LIBSPEECHD_MAJOR_VERSION;\nint minor=LIBSPEECHD_MINOR_VERSION;\nprintf("%d.%d",major,minor);\nreturn 0;}'
        res,ver=ctx.TryRun(src,".c")
    if not res:
        ctx.Result(res)
        return res
    ctx.env["spd_version"]=ver
    ctx.Result(ver)
    return ver


def convert_flags(value):
    return value.split()


def convert_path(value):
    return value.split(":")


def setup():
    global BUILDDIR,var_cache
    system=platform.system().lower()
    BUILDDIR=os.path.join("build",system)
    var_cache=os.path.join(BUILDDIR,"user.conf")
    Execute(Mkdir(BUILDDIR))
    SConsignFile(os.path.join(BUILDDIR,"scons"))


def create_languages_user_var():
    langs_dir=Dir("#data").Dir("languages")
    names=[name for name in sorted(os.listdir(langs_dir.path)) if os.path.isdir(langs_dir.Entry(name).path)]
    langs=[name.lower() for name in names]
    name_map=dict(zip(names,langs))
    def_langs=[lang for lang in langs if lang not in["georgian"]]
    print("Extended languages skipped")
    help="Which languages to install"
    return ListVariable("languages",help,def_langs,langs,name_map)


def create_audio_libs_user_var():
    libs=["pulse","libao","portaudio"]
    help="Which audio libraries to use if they are available"
    return ListVariable("audio_libs",help,libs,libs)


def create_user_vars():
    args={"DESTDIR":""}
    args.update(ARGUMENTS)
    vars=Variables(var_cache,args)
    vars.Add(BoolVariable("dev","The build will only be used for development: no global installation, run from the source directory, compile helper utilities",False))
    vars.Add(create_languages_user_var())
    vars.Add(BoolVariable("enable_sonic","Build with Sonic",False))
    vars.Add(BoolVariable("enable_pkg","Enable package directory code",False))
    vars.Add(create_audio_libs_user_var())
    vars.Add(BoolVariable("release","Whether we are building a release",True))
    vars.Add(PathVariable("spd_module_dir", "Speech dispatcher module directory", get_spd_module_dir(),  PathVariable.PathAccept))
    vars.Add("spd_version","Speech dispatcher version",validator=validate_spd_version)
    vars.Add("prefix","Installation prefix","/usr/local")
    vars.Add("bindir","Program installation directory","$prefix/bin")
    vars.Add("libdir","Library installation directory","$prefix/lib")
    vars.Add("includedir","Header installation directory","$prefix/include")
    vars.Add("datadir","Data installation directory","$prefix/share")
    vars.Add("sysconfdir","A directory for configuration files","$prefix/etc")
    vars.Add("servicedir",".service file installation directory","$datadir/dbus-1/services")
    vars.Add("DESTDIR","Support for staged installation","")
    vars.Add(BoolVariable("enable_shared","Build a shared library",True))
    vars.Add("CPPPATH","List of directories where to search for headers",[],converter=convert_path)
    vars.Add("LIBPATH","List of directories where to search for libraries",[],converter=convert_path)
    vars.Add("CPPFLAGS","C/C++ preprocessor flags",[],converter=convert_flags)
    vars.Add("CCFLAGS","C/C++ compiler flags",["-O2"],converter=convert_flags)
    vars.Add("CFLAGS","C compiler flags",[],converter=convert_flags)
    vars.Add("CXXFLAGS","C++ compiler flags",[],converter=convert_flags)
    vars.Add("LINKFLAGS","Linker flags",[],converter=convert_flags)
    return vars


def create_base_env(user_vars):
    env_args={"variables":user_vars}
    env_args["tools"]=["default","installer","textfile","library"]
    env_args["LIBS"]=[]
    env_args["package_name"]="AeonVoice"
    env_args["CPPDEFINES"]=[]
    env=Environment(**env_args)
    if env["dev"]:
        env["prefix"]=os.path.abspath("local")
        env["RPATH"]=env.Dir("$libdir").abspath
    env["package_version"]=get_version(env["release"])
    env.Append(CPPDEFINES=("PACKAGE",env.subst(r'\"$package_name\"')))
    env["libcore"]="AeonVoice_core"
    env["libaudio"]="AeonVoice_audio"
    return env


def display_help(env,vars):
    Help("Type 'scons' to build the package.\n")
    Help("Then type 'scons install' to install it.\n")
    Help("Type 'scons --clean install' to uninstall the software.\n")
    Help("You may use the following configuration variables:\n")
    Help(vars.GenerateHelpText(env))


def clone_base_env(base_env,user_vars):
    env=base_env.Clone()
    user_vars.Update(env)
    if "gcc" in env["TOOLS"]:
        env.MergeFlags("-pthread")
        env.AppendUnique(CXXFLAGS=["-std=c++11"])
        env.AppendUnique(CFLAGS=["-std=c11"])
        if 'SOURCE_DATE_EPOCH' in os.environ:
            env['ENV']['SOURCE_DATE_EPOCH'] = os.environ['SOURCE_DATE_EPOCH']
    env["BUILDDIR"]=BUILDDIR
    third_party_dir=os.path.join("src","third-party")
    for path in Glob(os.path.join(third_party_dir,"*"),strings=True):
        if os.path.isdir(path):
            env.Prepend(CPPPATH=("#"+path))
    env.Prepend(CPPPATH=boost_includedir)
    env.Prepend(CPPPATH=(os.path.join("#"+env["BUILDDIR"],"include"),".",os.path.join("#src","include")))
    return env


def configure(env):
    tests={"CheckPKGConfig":CheckPKGConfig,"CheckPKG":CheckPKG,"CheckSpdVersion":CheckSpdVersion}
    conf=env.Configure(conf_dir=os.path.join(env["BUILDDIR"],"configure_tests"),
                       log_file=os.path.join(env["BUILDDIR"],"configure.log"),
                       config_h=os.path.join(env["BUILDDIR"],"include","configure.h"),
                       custom_tests=tests)
    if not conf.CheckCC():
        print("The C compiler is not working")
        exit(1)
    if not conf.CheckCXX():
        print("The C++ compiler is not working")
        exit(1)
    has_giomm=False
    has_pkg_config=conf.CheckPKGConfig()
    if has_pkg_config:
        if "pulse" in env["audio_libs"] and not conf.CheckPKG("libpulse-simple"):
            env["audio_libs"].remove("pulse")
        if "libao" in env["audio_libs"] and not conf.CheckPKG("ao"):
            env["audio_libs"].remove("libao")
        if "portaudio" in env["audio_libs"] and not conf.CheckPKG("portaudio-2.0"):
            env["audio_libs"].remove("portaudio")
        if env["audio_libs"]:
            conf.CheckSpdVersion()
    else:
        env["audio_libs"]=[]
    conf.Finish()

    env.Prepend(LIBPATH=os.path.join("#"+env["BUILDDIR"],"core"))
    src_subdirs=["third-party", "pkg", "hts_engine", "core", "lib"]
    if env["dev"]:
        src_subdirs.append("utils")
    src_subdirs.append("audio")
    src_subdirs.append("test")
    if env["audio_libs"]:
        src_subdirs.append("sd_module")
    env.Prepend(LIBPATH=os.path.join("#"+env["BUILDDIR"],"audio"))
    if has_giomm:
        src_subdirs.append("service")
    src_subdirs.append("include")
    return src_subdirs


def build_binaries(base_env,user_vars):
    env=clone_base_env(base_env,user_vars)
    src_subdirs=configure(env)
    for subdir in src_subdirs:
        SConscript(os.path.join("src",subdir,"SConscript"),
                   variant_dir=os.path.join(env["BUILDDIR"],subdir),
                   exports={"env":env},
                   duplicate=0)


def build_for_linux(base_env,user_vars):
    build_binaries(base_env,user_vars)
    for subdir in ["data","config"]:
        SConscript(os.path.join(subdir,"SConscript"),exports={"env":base_env},
                   variant_dir=os.path.join(BUILDDIR,subdir),
                   duplicate=0)


setup()
vars=create_user_vars()
base_env=create_base_env(vars)
display_help(base_env,vars)
vars.Save(var_cache,base_env)
SConscript(dirs=boost_includedir)
if not sys.platform.startswith("linux"):
    print("This repository now supports Linux only")
    Exit(1)
build_for_linux(base_env,vars)
