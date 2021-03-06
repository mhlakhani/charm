""" 
Digital Signature Algorithm (DSA)

| From: "NIST proposed in Aug 1991 for use in DSS."
| Published in: FIPS 186
| Available from: 
| Notes: 

* type:           signature (ring-based)
* setting:        integer and elliptic curve groups

:Authors:    J. Ayo Akinyele
:Date:       5/2011
"""
from toolbox.ecgroup import *
from toolbox.PKSig import PKSig
from toolbox.eccurve import prime192v2

debug = False
class ECDSA(PKSig):
    def __init__(self, groupObj):
        PKSig.__init__(self)
        global group
        group = groupObj
        
    def keygen(self, bits):
        group.paramgen(bits)
        x, g = group.random(), group.random(G)
        y = (g ** x)
        return ({'g':g, 'y':y}, x)
    
    def sign(self, pk, x, M):
        while True:
            k = group.random()
            r = group.zr(pk['g'] ** k)
            e = group.hash(M)
            s = (~k) * (e + x * r)
            if (r == 0 or s == 0):
                print ("unlikely error r = %s, s = %s" % (r,s))
                continue
            else:
                break
        return { 'r':r, 's':s }
        
    def verify(self, pk, sig, M):
        w = ~sig['s']
        u1 = group.hash(M) * w
        u2 = sig['r'] * w
        v = (pk['g'] ** u1) * (pk['y'] ** u2)
    
        if group.zr(v) == sig['r']:
            return True
        else:
            return False
def main():
    groupObj = ECGroup(prime192v2)
    ecdsa = ECDSA(groupObj)
    
    (pk, sk) = ecdsa.keygen(0)
    m = "hello world! this is a test message."

    sig = ecdsa.sign(pk, sk, m)
    assert ecdsa.verify(pk, sig, m), "Failed verification!"
    if debug: print("Signature Verified!!!")
    
if __name__ == "__main__":
    debug = True
    main()

