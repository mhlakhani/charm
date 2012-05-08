from setuptools import setup, Extension
import os,platform

def patch_distutils():
    import os
    from distutils import sysconfig
    from distutils.sysconfig import get_python_inc as du_get_python_inc

    def get_python_inc(plat_specific=0, *args, **kwargs):
        if plat_specific == 0:
            out = os.environ["PY4A_INC"]
        else:
            out = du_get_python_inc(plat_specific=plat_specific, *args, **kwargs)
        return out
    setattr(sysconfig, 'get_python_inc', get_python_inc)
    
    # Just so that it creates the global so we can set it later
    sysconfig.get_config_var('Py_ENABLE_SHARED')
    getattr(sysconfig, '_config_vars')['Py_ENABLE_SHARED'] = False

    def customize_compiler(compiler):
        cflags = "-I%s" % os.environ["PY4A_INC"]
        cflags+= " -I%s" % os.environ["PY4A"]
        cflags+= " -I%s" % os.environ["GMP_INC"]
        cflags+= " -I%s" % os.environ["PBC_INC"]
        cflags+= " -I%s" % os.environ["OSSL_INC"]
        cflags+= " -I."
        cflags+=" -MMD -MP -MF -fpic -ffunction-sections -funwind-tables -fstack-protector"
        cflags+=" -D__ARM_ARCH_5__ -D__ARM_ARCH_5T__ -D__ARM_ARCH_5E__ -D__ARM_ARCH_5TE__"
        cflags+=" -Wno-psabi -march=armv5te -mtune=xscale -msoft-float -mthumb -Os"
        cflags+=" -fomit-frame-pointer -fno-strict-aliasing -finline-limit=64"
        cflags+=" -DANDROID  -Wa,--noexecstack -O2 -DNDEBUG -g"
        cc = "arm-linux-androideabi-gcc"
        cxx = "arm-linux-androideabi-g++"
        cpp = "arm-linux-androideabi-cpp"
        ldshared= "%s -shared" % cxx
        ldshared+=" -L%s" % os.environ["PY4A_LIB"]
        ldshared+=" -L%s/Lib" % os.environ["PY4A_LIB"]
        ldshared+=" -L%s" % os.environ["GMP_LIB"]
        ldshared+=" -L%s " % os.environ["OSSL_LIB"]
        ldshared+=" -L."
        ldshared+=" -lc -lstdc++ -lm -Wl,--no-undefined -Wl,-z,noexecstack -lpython3 -lpython3.2m"
        ccshared = sysconfig.get_config_vars("CCSHARED")
        so_ext = "so"

        if 'LDFLAGS' in os.environ:
                ldshared += os.environ['LDFLAGS']
        if 'CFLAGS' in os.environ:
            cflags += os.environ['CFLAGS']
            ldshared += os.environ['CFLAGS']
        if 'CPPFLAGS' in os.environ:
                cpp += os.environ['CPPFLAGS']
                cflags += os.environ['CPPFLAGS']
                ldshared += os.environ['CPPFLAGS']
     
        cc_cmd = cc + ' ' + cflags
        compiler.set_executables(
            preprocessor=cpp,
            compiler=cc_cmd,
            compiler_so=cc_cmd + ' ' + ' '.join(ccshared),
            compiler_cxx=cxx,
            linker_so=ldshared,
            linker_exe=cc)

        compiler.shared_lib_extension = so_ext
    setattr(sysconfig, 'customize_compiler', customize_compiler)

    def get_config_h_filename():
        inc_dir = os.path.join(os.environ["PY4A_INC"], "..")
        config_h = 'pyconfig.h'
        return os.path.join(inc_dir, config_h)
    setattr(sysconfig, 'get_config_h_filename', get_config_h_filename)

_ext_modules = []

def read_config(file):
    f = open(file, 'r')
    lines = f.read().split('\n')   
    config_key = {}
    for e in lines:
        if e.find('=') != -1:
           param = e.split('=')
           config_key[ param[0] ] = param[1] 
    f.close()
    return config_key

print("Platform:", platform.system())
config = os.environ.get('CONFIG_FILE')
opt = {'PAIR_MOD':'yes', 'USE_PBC':'yes', 'INT_MOD':'yes','ECC_MOD':'yes'}
if config != None:
   print("Config file:", config)
   opt = read_config(config)

path = 'charm-src/'
_macros = []
_charm_version = opt.get('VERSION')

if opt.get('PAIR_MOD') == 'yes':
    if opt.get('USE_PBC') == 'yes':
        pairing_module = Extension('pairing', include_dirs = [path+'utils/'], 
                           sources = [path+'pairingmath/pairingmodule.c', path+'utils/sha1.c', path+'utils/base64.c'],
                           libraries=['pbc', 'gmp'])
    else:
        # build MIRACL based pairing module - note that this is for experimental use only
        pairing_module = Extension('pairing', include_dirs = [path+'utils/', path+'pairingmath/miracl/'], 
                           sources = [path+'pairingmath/pairingmodule2.c', path+'utils/sha1.c', path+'pairingmath/miracl/miraclwrapper.cc'],
                           libraries=['gmp','stdc++'], extra_objects=[path+'pairingmath/miracl/miracl.a'], extra_compile_args=None)
    _ext_modules.append(pairing_module)
   
if opt.get('INT_MOD') == 'yes':
   integer_module = Extension('integer', include_dirs = [path+'utils/'],
                           sources = [path+'integermath/integermodule.c', path+'utils/sha1.c', path+'utils/base64.c'], 
                           libraries=['gmp', 'crypto'])
   _ext_modules.append(integer_module)
   
if opt.get('ECC_MOD') == 'yes':
   ecc_module = Extension('ecc', include_dirs = [path+'utils/'], 
                sources = [path+'ecmath/ecmodule.c', path+'utils/sha1.c', path+'utils/base64.c'], 
                libraries=['gmp', 'crypto'])
   _ext_modules.append(ecc_module)

benchmark_module = Extension('benchmark', sources = [path+'utils/benchmarkmodule.c'])
cryptobase = Extension('cryptobase', sources = [path+'cryptobase/cryptobasemodule.c'])

aes = Extension('AES', sources = [path+'cryptobase/AES.c'])
des  = Extension('DES', include_dirs = [path+'cryptobase/libtom/'], sources = [path+'cryptobase/DES.c'])
des3  = Extension('DES3', include_dirs = [path+'cryptobase/libtom/'], sources = [path+'cryptobase/DES3.c'])
_ext_modules.extend([benchmark_module, cryptobase, aes, des, des3])

if platform.system() in ['Linux', 'Windows']:
   # add benchmark module to pairing, integer and ecc 
   if opt.get('PAIR_MOD') == 'yes': pairing_module.sources.append(path+'utils/benchmarkmodule.c')
   if opt.get('INT_MOD') == 'yes': integer_module.sources.append(path+'utils/benchmarkmodule.c')
   if opt.get('ECC_MOD') == 'yes': ecc_module.sources.append(path+'utils/benchmarkmodule.c')

if os.environ.get('CHARM_ANDROID', 'no') == 'yes':
    
    #export PY4A="../python-for-android/python3-alpha/python3-src"
    #export PY4A_INC="${PY4A}/Include"
    #export PY4A_LIB="${PY4A}"
    #export PYTHONPATH="${PYTHONPATH}:${PY4A}/Python"
    #export GMP_INC="${PY4A}/../gmp-5.0.2"
    #export PBC_INC="${PY4A}/../pbc-0.5.12/include"
    #export OSSL_INC="${PY4A}/../openssl/include"
    #export GMP_LIB="${PY4A}/../thirdparty/lib"
    #export PBC_LIB=""
    #export OSSL_LIB="${PY4A}/../openssl/lib"
    #export CHARM_ANDROID="yes"

    patch_distutils()

setup(name = 'Charm-Crypto',
    ext_package = 'charm',
    version =  _charm_version,
    description = 'Charm is a framework for rapid prototyping of cryptosystems',
    ext_modules = _ext_modules,
    author = "J Ayo Akinyele",
    author_email = "ayo.akinyele@charm-crypto.com",
    url = "http://charm-crypto.com/",
    packages = ['charm', 'toolbox', 'compiler', 'schemes'],
    package_dir = {'charm': 'charm-src/charm'},
    package_data = {'charm':['__init__.py', 'engine/*.py'], 'toolbox':['*.py'], 'compiler':['*.py'], 'schemes':['*.py'], 'param':['*.param']},
        license = 'GPL'
     )


