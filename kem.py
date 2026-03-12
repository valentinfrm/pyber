import pke
import hash
import params
import secrets
import auxiliary as ax

def _keygen_internal(d, z):
    ek_pke, dk_pke = pke.keygen(d)

    ek = ek_pke # pke encr key = encaps key
    dk = dk_pke + ek_pke + hash.H(ek_pke) + z

    return ek, dk

def _encaps_internal(ek, m):
    """
    calculates symmetric key and the ciphertext

    Args:
        ek (bytes): encapsulation key of other Person
        m (bytes): randomness (32 Byte) -> needed to calculate K

    Returns:
        K (bytes): 32 bytes symmetric key
        c (bytes): ciphertext of m
    """
    h = hash.H(ek)
    K, r = hash.G(m + h)
    c = pke.encrypt(ek, m, r)
    return K, c 

def _decaps_internal(dk, c):
    # get components from dk
    dk_pke = dk[0:384 * params.k] # (256 * 12) / 8 = 384
    ek_pke = dk[384 * params.k:768 * params.k + 32] # 384 + 32 for rho
    h = dk[768 * params.k + 32:768 * params.k + 64] # hash of ek_pke (32 bytes)
    z = dk[768 * params.k + 64:] # implicit rejection value (32 bytes)

    # decrypt to get candidates
    m_prime = pke.decrypt(dk_pke, c)
    K_prime, r_prime = hash.G(m_prime + h)

    # reencrypt to check validity of c
    c_prime = pke.encrypt(ek_pke, m_prime, r_prime)

    K_bar = hash.J(z + c) # FO transform: deterministic implicit rejection -> CCA security

    if c != c_prime:
        return K_bar
    else:
        return K_prime

def keygen():
    try :
        d = secrets.token_bytes(32)
        z = secrets.token_bytes(32)
    except OSError as e:
        raise RuntimeError("RNG failue: keygen") from e # e gets propagated
    
    ek, dk = _keygen_internal(d, z)

    key_pair_check(ek, dk)

    return ek, dk

def encaps(ek):
    encaps_check(ek)
    try:
        m = secrets.token_bytes(32)
    except OSError as e:
        raise RuntimeError("RNG failure: encaps") from e
    
    K, c = _encaps_internal(ek, m)
    
    return K, c

def decaps(dk, c):
    decaps_check(dk, c)
    K_prime = _decaps_internal(dk, c)
    return K_prime

def key_pair_check(ek, dk):
    # RNG check
    try:
        m = secrets.token_bytes(32)
    except OSError as e:
        raise RuntimeError("RNG failure during key_pair_check") from e
        
    # encaps -> decaps produces the same K
    K,c = _encaps_internal(ek, m)
    K_prime = _decaps_internal(dk, c)

    if K != K_prime:
        raise ValueError("Key pair consistency check failed")
        
def encaps_check(ek):
    # ek type check
    if type(ek) != bytes:
        raise TypeError("encaps: ek is not of type bytes")
    
    # ek length check
    if len(ek) != 384 * params.k + 32:
        raise ValueError("encaps: ek length is not matching")
    
    # modulus check: ensures coeffs are in valid range [0, q-1]
    test = ax.byte_encode(ax.byte_decode(ek[0:384 * params.k], 12), 12)
    if test != ek[0:384 * params.k]:
        raise ValueError("encaps: modulus check failed")
    
def decaps_check(dk, c):
    _dk_check(dk)
    _c_check(c)
    
def _dk_check(dk):
    # dk type check
    if type(dk) != bytes:
        raise TypeError("decaps: dk is not of type bytes")
    
    # dk length check
    if len(dk) != 768 * params.k + 96: # dkPKE + ekPKE + h + z 
        raise ValueError("decaps: dk length is not matching")
    
    # hash check
    test = hash.H(dk[384 * params.k:768 * params.k + 32])
    if test != dk[768 * params.k + 32:768 * params.k + 64]:
        raise ValueError("decaps: H is not digesting the correct hash")
    
    
def _c_check(c):
    # c type check
    if type(c) != bytes:
        raise TypeError("decaps: c is not of type bytes")
    
    # c length check
    if len(c) != 32 * (params.du * params.k + params.dv):
        raise ValueError("decaps: c length is not matching")
