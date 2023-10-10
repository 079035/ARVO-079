#This file is created to transform the url to some moved repo.

from utils import *

TRANS_TABLE = {
'/src/freetype2': 'https://github.com/freetype/freetype.git',
'/src/skia/third_party/externals/libjpeg-turbo': 'https://github.com/libjpeg-turbo/libjpeg-turbo.git',
'/src/radare2-regressions': 'https://github.com/rlaemmert/radare2-regressions.git',
'/src/x264': 'https://code.videolan.org/videolan/x264.git',
'/src/vorbis': 'https://gitlab.xiph.org/xiph/vorbis.git',
'/src/theora': 'https://github.com/xiph/theora.git',
'/src/opus': 'https://github.com/xiph/opus.git',
'/src/ogg': 'https://github.com/xiph/ogg.git',
'/src/libxml2': 'https://github.com/GNOME/libxml2.git',
'/src/libmicrohttpd': 'https://github.com/Karlson2k/libmicrohttpd.git',
'/src/wireshark': 'https://github.com/wireshark/wireshark.git',
'/src/kimageformats': 'https://github.com/KDE/kimageformats.git',
'/src/extra-cmake-modules': 'https://github.com/KDE/extra-cmake-modules.git',
'/src/kcodecs': 'https://github.com/KDE/kcodecs.git',
'/src/karchive': 'https://github.com/KDE/karchive.git',
'/src/libtheora': 'https://github.com/xiph/theora.git',
'/src/libva': "https://github.com/intel/libva.git",
'/src/libssh2': "https://github.com/libssh2/libssh2.git",
'/src/quickjs': "https://github.com/bellard/quickjs",
'/src/lwan': "https://github.com/lpereira/lwan.git",
}

def trans_table(item_name,item_url,item_type):
    if item_name in TRANS_TABLE:
        return TRANS_TABLE[item_name],"git"
    else:
        return item_url,item_type


# git svn init https://github.com/llvm/llvm-project.git
# git svn fetch -r309364
tabal_svn = {
'/src/llvm/projects/compiler-rt': "https://github.com/llvm/llvm-project.git",
'/src/llvm/tools/clang/tools/extra': "https://github.com/llvm/llvm-project.git",
'/src/llvm/tools/clang': "https://github.com/llvm/llvm-project.git",
'/src/llvm': "https://github.com/llvm/llvm-project.git",
'/src/libcxx': "https://github.com/llvm/llvm-project.git",
'/src/libcxxabi': "https://github.com/llvm/llvm-project.git",
'/src/llvm_libcxxabi': "https://github.com/llvm/llvm-project.git",
'/src/libfuzzer': 'https://github.com/llvm/llvm-project.git',# use the existed one 


}
table2 = {
 '/src/skia/third_party/externals/angle2': 'https://chromium.googlesource.com/angle/angle.git',
 '/src/libva': 'https://github.com/01org/libva',
 '/src/x265': 'https://github.com/videolan/x265.git',# only 
 '/src/trunk': 'http://svn.xvid.org/trunk',
 '/src/quickjs': 'https://github.com/horhof/quickjs',#repo is removed, 10 isues are related 

}

def find_srcmap_include_key(key_name):
    workdir = Path(DATADIR) / "Issues" 
    srcmap = list(workdir.glob('*/*.srcmap.json'))
    for _ in srcmap:
        with open(_) as f:
            try:
                data = json.loads(f.read())
            except:
                continue
        if key_name in data.keys():
            print(data[key_name])
            return 
def find_all_srcmap_include_key(key_name):
    workdir = Path(DATADIR) / "Issues" 
    srcmap = list(workdir.glob('*/*.srcmap.json'))
    for _ in srcmap:
        with open(_) as f:
            data = json.loads(f.read())
        if key_name in data.keys():
            print(data[key_name],_)        
if __name__ == "__main__":
    find_all_srcmap_include_key('/src/libfuzzer')