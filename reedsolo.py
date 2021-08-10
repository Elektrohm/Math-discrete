from sympy.polys.galoistools import gf_gcdex, gf_strip
from sympy.polys.domains import ZZ

def gf_inv(a, irr_poly):  # irriducible polynomial 

    return gf_gcdex(gf_strip(a), irr_poly, 2 , ZZ)[0]


def p_mul(a, b):
    result = 0
    while a and b:
        if a & 1: result ^= b
        a >>= 1; b <<= 1
    return result

def p_divmod(a, b):
    """ Binary polynomial division.
        Divides a by b and returns resulting (quotient, remainder) polynomials.
        Precondition: b != 0 """
    q = 0; bl = b.bit_length()
    while True:
        shift = a.bit_length() - bl
        if shift < 0: return (q, a)
        q ^= 1 << shift; a ^= b << shift

def p_mod_mul(a, b, modulus):
    result = 0; deg = p_degree(modulus)
    assert p_degree(b) < deg
    while a and b:
        if a & 1: result ^= b
        a >>= 1; b <<= 1
        if (b >> deg) & 1: b ^= modulus
    return result

def p_egcd(a, b):
    """ Binary polynomial Extended Euclidean algorithm (iterative).
        Returns (d, x, y) where d is the Greatest Common Divisor of polynomials a and b.
        x, y are polynomials that satisfy: p_mul(a,x) ^ p_mul(b,y) = d
        Precondition: b != 0
        Postcondition: x <= p_div(b,d) and y <= p_div(a,d) """
    a = (a, 1, 0)
    b = (b, 0, 1)
    while True:
        q, r = p_divmod(a[0], b[0])
        if not r: return b
        a, b = b, (r, a[1] ^ p_mul(q, b[1]), a[2] ^ p_mul(q, b[2]))

def p_mult_inv(a, modulus):
    """ Binary polynomial modular multiplicative inverse.
        Returns b so that: p_mod(p_mul(a, b), modulus) == 1
        Precondition: modulus != 0 and p_coprime(a, modulus)
        Postcondition: b < modulus """
    d, x, y = p_egcd(a, modulus)
    assert d == 1 # inverse exists
    return x
