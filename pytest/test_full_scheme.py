import kem

def test_encaps_decaps_roundtrip():
    ek, dk = kem.keygen()
    K, c = kem.encaps(ek)
    K_prime = kem.decaps(dk, c)
    assert K == K_prime

def test_roundtrip_multiple():
    for _ in range(10):
        ek, dk = kem.keygen()
        K, c = kem.encaps(ek)
        K_prime = kem.decaps(dk, c)
        assert K == K_prime

def test_different_keys_produce_different_K():
    ek1, dk1 = kem.keygen()
    ek2, dk2 = kem.keygen()
    K1, c1 = kem.encaps(ek1)
    K2, c2 = kem.encaps(ek2)
    assert K1 != K2

def test_wrong_dk_returns_different_K():
    ek1, dk1 = kem.keygen()
    ek2, dk2 = kem.keygen()
    K, c = kem.encaps(ek1)
    K_wrong = kem.decaps(dk2, c)  # wrong dk -> implicit rejection
    assert K != K_wrong