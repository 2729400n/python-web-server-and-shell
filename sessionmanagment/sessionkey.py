import os
if(os.name!='nt'):
    from crypt import *
    import cryptography

    MAXDEPTH = 0x64


    def make_new_key(hint: str, dictionary: dict, depth=1, maxdepth=MAXDEPTH):
        algs = [METHOD_CRYPT, METHOD_MD5, METHOD_SHA256, METHOD_SHA512]
        salts = []
        depth = depth
        for i in algs:
            salts += [mksalt(i)]
        for i in salts:
            key = crypt(hint, i)
            if(key not in dictionary):
                return key
            if(depth != maxdepth):
                make_new_key(key, dictionary, depth+1)
            else:
                return -1
del os