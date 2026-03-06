import params

def bytes_to_bits(byte_array):
    """LSB first"""
    result = []
    for b in byte_array:
        for _ in range(8):
            result.append(b & 1) # LSB
            b = b >> 1
    return result

def bits_to_bytes(bit_array):
    """LSB first"""
    result = []
    for i in range(len(bit_array) // 8): # cuts off remaining bits if len(bit_array) % 8 != 0
        x = 0
        for j in range(8):
            x += bit_array[i * 8 + j] * 2**j
        result.append(x)
    return result

def byte_encode(d, int_input):
    """
    encodes a list of integers into a list of bytes

    Args:
        d (int): bits per coeff
        int_input (list): integers to encode
    
    Returns:
        bytes: len(int_input) * d / 8 bytes
    """
    bits = []
    for value in int_input:
        for _ in range(d):
            bits.append(value % 2) # always LSB
            value = value >> 1

    return bytes(bits_to_bytes(bits))

def byte_decode(d, byte_input):
    """
    decodes a list of bytes into a list of integers

    Args:
        d (int): bits per coeff
        byte_input (list): 32 * d bytes
    
    Returns:
        list: integers
    """
    bits = bytes_to_bits(byte_input)
    
    integers = []
    for i in range(0, len(bits), d): # 0 -> len(bits), d = step size
        int_value = sum(bits[i + j] << j for j in range(d))
        integers.append(int_value)
    
    return integers