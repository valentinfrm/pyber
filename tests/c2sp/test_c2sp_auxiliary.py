import pytest

from c2sp_vectors import ALL_KEM_DATA, KEM_IDS
from pyber.auxiliary import (
    compress_poly, decompress_poly,
    byte_encode, byte_decode,
    transpose_matrix
)
from pyber import params

@pytest.mark.parametrize("kem_data", ALL_KEM_DATA, ids=KEM_IDS, indirect=True)
def test_compress_poly_u(kem_data):
    u0 = kem_data["u0"]
    expected_compressed_u0 = kem_data["compressed_u0"]
    
    compressed_u0 = compress_poly(u0, params.du)
    assert compressed_u0 == expected_compressed_u0

@pytest.mark.parametrize("kem_data", ALL_KEM_DATA, ids=KEM_IDS, indirect=True)
def test_compress_poly_v(kem_data):
    v = kem_data["v"]
    expected_compressed_v = kem_data["compressed_v"]

    compressed_v = compress_poly(v, params.dv)
    assert compressed_v == expected_compressed_v

@pytest.mark.parametrize("kem_data", ALL_KEM_DATA, ids=KEM_IDS, indirect=True)
def test_roundtrip_compression(kem_data):
    v = kem_data["v"]

    compressed = compress_poly(v, 4)
    decompressed = decompress_poly(compressed, 4)
    recompressed = compress_poly(decompressed, 4)

    assert recompressed == compressed

@pytest.mark.parametrize("kem_data", ALL_KEM_DATA, ids=KEM_IDS, indirect=True)
def test_byte_encode(kem_data):
    s0 = kem_data["s0"]
    expected_s0_bytes = kem_data["s0_bytes"]
    
    s0_bytes = byte_encode(s0, 12)

    assert s0_bytes == expected_s0_bytes

@pytest.mark.parametrize("kem_data", ALL_KEM_DATA, ids=KEM_IDS, indirect=True)
def test_byte_decode(kem_data):
    s0_bytes = kem_data["s0_bytes"]
    expected_s0 = kem_data["s0"]

    s0 = byte_decode(s0_bytes, 12)
    assert s0 == expected_s0

def test_transpose_matrix_simple():
    A = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]
    
    expected = [[1, 4, 7],
                [2, 5, 8],
                [3, 6, 9]]
    
    result = transpose_matrix(A)
    assert result == expected
    
    A2 = [[1, 2], 
          [3, 4]]
    expected2 = [[1, 3], 
                 [2, 4]]
    
    assert transpose_matrix(A2) == expected2

@pytest.mark.parametrize("kem_data", ALL_KEM_DATA, ids=KEM_IDS, indirect=True)
def test_transpose_matrix_full_size(kem_data):
    A_bytes = kem_data["A"]
    A_T_expected_bytes = kem_data["A_T"]
    
    k = params.k
    poly_len = 384
    
    A = []
    for i in range(k):
        row = []
        for j in range(k):
            start = (i * k + j) * poly_len
            poly_coeffs = byte_decode(A_bytes[start:start+poly_len], 12)
            row.append(poly_coeffs)
        A.append(row)
    
    A_T = transpose_matrix(A)
    
    A_T_bytes = b""
    for i in range(k):
        for j in range(k):
            A_T_bytes += byte_encode(A_T[i][j], 12)
    
    assert A_T_bytes == A_T_expected_bytes

def test_encode_decode_roundtrip():
    data = [1] * 256
    encoded = byte_encode(data, 12)
    decoded = byte_decode(encoded, 12)

    assert len(decoded) == 256
    assert decoded == data