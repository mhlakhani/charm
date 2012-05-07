#!/bin/bash

export PY4A="../python-for-android/python3-alpha/python3-src"
export PY4A_INC="${PY4A}/Include"
export PY4A_LIB="${PY4A}"
export PYTHONPATH="${PYTHONPATH}:${PY4A}/Python"
export GMP_INC="${PY4A}/../gmp-5.0.2"
export PBC_INC="${PY4A}/../pbc-0.5.12/include"
export OSSL_INC="${PY4A}/../openssl/include"
export GMP_LIB="${PY4A}/../thirdparty/lib"
export PBC_LIB=""
export OSSL_LIB="${PY4A}/../openssl/lib"

mkdir -p build/lib.linux-x86_64-3.2/charm/
mkdir -p build/temp.linux-x86_64-3.2/charm-src/utils/
mkdir -p build/temp.linux-x86_64-3.2/charm-src/cryptobase/
mkdir -p build/temp.linux-x86_64-3.2/charm-src/pairingmath
mkdir -p build/temp.linux-x86_64-3.2/charm-src/integermath/
mkdir -p build/temp.linux-x86_64-3.2/charm-src/ecmath/

rm -f pbc
ln -s ${PBC_INC} pbc

arm-linux-androideabi-gcc -I${PY4A_INC} -I${PY4A} -I${GMP_INC} -I. -Icharm-src/utils -MMD -MP -MF -fpic -ffunction-sections -funwind-tables -fstack-protector -D__ARM_ARCH_5__ -D__ARM_ARCH_5T__ -D__ARM_ARCH_5E__ -D__ARM_ARCH_5TE__ -Wno-psabi -march=armv5te -mtune=xscale -msoft-float -mthumb -Os -fomit-frame-pointer -fno-strict-aliasing -finline-limit=64 -DANDROID -Wa,--noexecstack -O2 -DNDEBUG -g -fPIC -c charm-src/utils/sha1.c -o build/temp.linux-x86_64-3.2/charm-src/utils/sha1.o
arm-linux-androideabi-gcc -I${PY4A_INC} -I${PY4A} -I${GMP_INC} -I. -Icharm-src/utils -MMD -MP -MF -fpic -ffunction-sections -funwind-tables -fstack-protector -D__ARM_ARCH_5__ -D__ARM_ARCH_5T__ -D__ARM_ARCH_5E__ -D__ARM_ARCH_5TE__ -Wno-psabi -march=armv5te -mtune=xscale -msoft-float -mthumb -Os -fomit-frame-pointer -fno-strict-aliasing -finline-limit=64 -DANDROID -Wa,--noexecstack -O2 -DNDEBUG -g -fPIC -c charm-src/utils/base64.c -o build/temp.linux-x86_64-3.2/charm-src/utils/base64.o
arm-linux-androideabi-gcc -I${PY4A_INC} -I${PY4A} -I${GMP_INC} -I. -Icharm-src/utils -MMD -MP -MF -fpic -ffunction-sections -funwind-tables -fstack-protector -D__ARM_ARCH_5__ -D__ARM_ARCH_5T__ -D__ARM_ARCH_5E__ -D__ARM_ARCH_5TE__ -Wno-psabi -march=armv5te -mtune=xscale -msoft-float -mthumb -Os -fomit-frame-pointer -fno-strict-aliasing -finline-limit=64 -DANDROID -Wa,--noexecstack -O2 -DNDEBUG -g -fPIC -c charm-src/utils/benchmarkmodule.c -o build/temp.linux-x86_64-3.2/charm-src/utils/benchmarkmodule.o

arm-linux-androideabi-gcc -I${PY4A_INC} -I${PY4A} -I${GMP_INC} -I${OSSL_INC} -I. -Icharm-src/utils/ -MMD -MP -MF -fpic -ffunction-sections -funwind-tables -fstack-protector -D__ARM_ARCH_5__ -D__ARM_ARCH_5T__ -D__ARM_ARCH_5E__ -D__ARM_ARCH_5TE__ -Wno-psabi -march=armv5te -mtune=xscale -msoft-float -mthumb -Os -fomit-frame-pointer -fno-strict-aliasing -finline-limit=64 -DANDROID -Wa,--noexecstack -O2 -DNDEBUG -g -fPIC -c charm-src/ecmath/ecmodule.c -o build/temp.linux-x86_64-3.2/charm-src/ecmath/ecmodule.o
arm-linux-androideabi-g++ -shared -lc -lstdc++ -lm -Wl,--no-undefined -Wl,-z,noexecstack -L${OSSL_LIB} -L${GMP_LIB} -lgmp -lpbc -lssl -lcrypto -L${PY4A_LIB} -lpython3.2m build/temp.linux-x86_64-3.2/charm-src/ecmath/ecmodule.o build/temp.linux-x86_64-3.2/charm-src/utils/sha1.o build/temp.linux-x86_64-3.2/charm-src/utils/base64.o build/temp.linux-x86_64-3.2/charm-src/utils/benchmarkmodule.o -o build/lib.linux-x86_64-3.2/charm/ecc.cpython-32mu.so

arm-linux-androideabi-gcc -I${PY4A_INC} -I${PY4A} -I${GMP_INC} -I${OSSL_INC} -I. -Icharm-src/utils/ -MMD -MP -MF -fpic -ffunction-sections -funwind-tables -fstack-protector -D__ARM_ARCH_5__ -D__ARM_ARCH_5T__ -D__ARM_ARCH_5E__ -D__ARM_ARCH_5TE__ -Wno-psabi -march=armv5te -mtune=xscale -msoft-float -mthumb -Os -fomit-frame-pointer -fno-strict-aliasing -finline-limit=64 -DANDROID -Wa,--noexecstack -O2 -DNDEBUG -g -fPIC -c charm-src/integermath/integermodule.c -o build/temp.linux-x86_64-3.2/charm-src/integermath/integermodule.o
arm-linux-androideabi-g++ -shared -lc -lstdc++ -lm -Wl,--no-undefined -Wl,-z,noexecstack -L${OSSL_LIB} -L${GMP_LIB} -lgmp -lpbc -lssl -lcrypto -L${PY4A_LIB} -lpython3.2m build/temp.linux-x86_64-3.2/charm-src/integermath/integermodule.o build/temp.linux-x86_64-3.2/charm-src/utils/sha1.o build/temp.linux-x86_64-3.2/charm-src/utils/base64.o build/temp.linux-x86_64-3.2/charm-src/utils/benchmarkmodule.o -o build/lib.linux-x86_64-3.2/charm/integer.cpython-32mu.so

arm-linux-androideabi-gcc -I${PY4A_INC} -I${PY4A} -I${GMP_INC} -I. -Icharm-src/utils -MMD -MP -MF -fpic -ffunction-sections -funwind-tables -fstack-protector -D__ARM_ARCH_5__ -D__ARM_ARCH_5T__ -D__ARM_ARCH_5E__ -D__ARM_ARCH_5TE__ -Wno-psabi -march=armv5te -mtune=xscale -msoft-float -mthumb -Os -fomit-frame-pointer -fno-strict-aliasing -finline-limit=64 -DANDROID -Wa,--noexecstack -O2 -DNDEBUG -g -fPIC -c charm-src/pairingmath/pairingmodule.c -o build/temp.linux-x86_64-3.2/charm-src/pairingmath/pairingmodule.o
arm-linux-androideabi-g++ -shared -lc -lstdc++ -lm -Wl,--no-undefined -Wl,-z,noexecstack -L${GMP_LIB} -lgmp -lpbc -L${PY4A_LIB} -lpython3.2m build/temp.linux-x86_64-3.2/charm-src/pairingmath/pairingmodule.o build/temp.linux-x86_64-3.2/charm-src/utils/sha1.o build/temp.linux-x86_64-3.2/charm-src/utils/base64.o build/temp.linux-x86_64-3.2/charm-src/utils/benchmarkmodule.o -o build/lib.linux-x86_64-3.2/charm/pairing.cpython-32mu.so

arm-linux-androideabi-gcc -I${PY4A_INC} -I${PY4A} -MMD -MP -MF -fpic -ffunction-sections -funwind-tables -fstack-protector -D__ARM_ARCH_5__ -D__ARM_ARCH_5T__ -D__ARM_ARCH_5E__ -D__ARM_ARCH_5TE__ -Wno-psabi -march=armv5te -mtune=xscale -msoft-float -mthumb -Os -fomit-frame-pointer -fno-strict-aliasing -finline-limit=64 -DANDROID -Wa,--noexecstack -O2 -DNDEBUG -g -fPIC -c charm-src/utils/benchmarkmodule.c -o build/temp.linux-x86_64-3.2/charm-src/utils/benchmarkmodule.o
arm-linux-androideabi-g++ -shared -lc -lstdc++ -lm -Wl,--no-undefined -Wl,-z,noexecstack -L${PY4A_LIB} -lpython3.2m build/temp.linux-x86_64-3.2/charm-src/utils/benchmarkmodule.o  -o build/lib.linux-x86_64-3.2/charm/benchmark.cpython-32mu.so

arm-linux-androideabi-gcc -I${PY4A_INC} -I${PY4A} -MMD -MP -MF -fpic -ffunction-sections -funwind-tables -fstack-protector -D__ARM_ARCH_5__ -D__ARM_ARCH_5T__ -D__ARM_ARCH_5E__ -D__ARM_ARCH_5TE__ -Wno-psabi -march=armv5te -mtune=xscale -msoft-float -mthumb -Os -fomit-frame-pointer -fno-strict-aliasing -finline-limit=64 -DANDROID -Wa,--noexecstack -O2 -DNDEBUG -g -fPIC -c charm-src/cryptobase/cryptobasemodule.c -o build/temp.linux-x86_64-3.2/charm-src/cryptobase/cryptobasemodule.o
arm-linux-androideabi-g++  -shared -lc -lstdc++ -lm -Wl,--no-undefined -Wl,-z,noexecstack -L${PY4A_LIB} -lpython3.2m build/temp.linux-x86_64-3.2/charm-src/cryptobase/cryptobasemodule.o  -o build/lib.linux-x86_64-3.2/charm/cryptobase.cpython-32mu.so

arm-linux-androideabi-gcc -I${PY4A_INC} -I${PY4A} -MMD -MP -MF -fpic -ffunction-sections -funwind-tables -fstack-protector -D__ARM_ARCH_5__ -D__ARM_ARCH_5T__ -D__ARM_ARCH_5E__ -D__ARM_ARCH_5TE__ -Wno-psabi -march=armv5te -mtune=xscale -msoft-float -mthumb -Os -fomit-frame-pointer -fno-strict-aliasing -finline-limit=64 -DANDROID -Wa,--noexecstack -O2 -DNDEBUG -g -fPIC -c charm-src/cryptobase/AES.c -o build/temp.linux-x86_64-3.2/charm-src/cryptobase/AES.o
arm-linux-androideabi-g++ -shared -lc -lstdc++ -lm -Wl,--no-undefined -Wl,-z,noexecstack -L${PY4A_LIB} -lpython3.2m build/temp.linux-x86_64-3.2/charm-src/cryptobase/AES.o -o build/lib.linux-x86_64-3.2/charm/AES.cpython-32mu.so

arm-linux-androideabi-gcc -I${PY4A_INC} -I${PY4A} -MMD -MP -MF -fpic -ffunction-sections -funwind-tables -fstack-protector -D__ARM_ARCH_5__ -D__ARM_ARCH_5T__ -D__ARM_ARCH_5E__ -D__ARM_ARCH_5TE__ -Wno-psabi -march=armv5te -mtune=xscale -msoft-float -mthumb -Os -fomit-frame-pointer -fno-strict-aliasing -finline-limit=64 -DANDROID -Wa,--noexecstack -O2 -DNDEBUG -g -fPIC -Icharm-src/cryptobase/libtom/ -c charm-src/cryptobase/DES.c -o build/temp.linux-x86_64-3.2/charm-src/cryptobase/DES.o
arm-linux-androideabi-g++ -shared -lc -lstdc++ -lm -Wl,--no-undefined -Wl,-z,noexecstack -L${PY4A_LIB} -lpython3.2m build/temp.linux-x86_64-3.2/charm-src/cryptobase/DES.o  -o build/lib.linux-x86_64-3.2/charm/DES.cpython-32mu.so

arm-linux-androideabi-gcc -I${PY4A_INC} -I${PY4A} -MMD -MP -MF -fpic -ffunction-sections -funwind-tables -fstack-protector -D__ARM_ARCH_5__ -D__ARM_ARCH_5T__ -D__ARM_ARCH_5E__ -D__ARM_ARCH_5TE__ -Wno-psabi -march=armv5te -mtune=xscale -msoft-float -mthumb -Os -fomit-frame-pointer -fno-strict-aliasing -finline-limit=64 -DANDROID -Wa,--noexecstack -O2 -DNDEBUG -g -fPIC -Icharm-src/cryptobase/libtom/ -c charm-src/cryptobase/DES3.c -o build/temp.linux-x86_64-3.2/charm-src/cryptobase/DES3.o
arm-linux-androideabi-g++ -shared -lc -lstdc++ -lm -Wl,--no-undefined -Wl,-z,noexecstack -L${PY4A_LIB} -lpython3.2m build/temp.linux-x86_64-3.2/charm-src/cryptobase/DES3.o  -o build/lib.linux-x86_64-3.2/charm/DES3.cpython-32mu.so

rm -f pbc
