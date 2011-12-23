
#!/usr/bin/env python
# rsacryptstr.py - Saurav R Tuladhar, sauravtuladhar@gmail.com

# This is a demo program takes a string ( Roman letters only for now ) as a plain
# text input and encrypts using a simple form or RSA algorithm. The program provi
# des. Functions for public and private key generation, encrypting the plain text
# and decrypting the crypttext.

# This implementation is a part of project work for MTH441 ( Abstract Algebra )

from pylab import *

def get_prime(N):
    """ Returns Nth prime number"""    
    counter = 1   # Counts number of primes
    idx = 0
    primeList = [2]
    
    while counter < N:
        isPrime = True 
        idx = idx + 1
        testNum = 2*idx + 1
        
        for x in primeList:
            if testNum % x == 0:   # Only check for prime numbers < testNum. Based on Fundamental Theorem of Arithmetic. 
                isPrime = False 
                break

        if isPrime == True:
            primeList = primeList + [testNum]
            counter  = counter + 1

    return primeList[-1]
#-----------------------------------------------------------------------------------
def xgcd(a, b):
    """ Returns extended gcd results

        Function arguments: xgcd(a, b)
        a and b are two integers who gcd is computed.
        If g = gcd(a, b), ax + by = g.
        Returns (g, x, y)"""
    
    x = 0
    y = 1
    lastx = 1
    lasty = 0

    while b != 0:
        q = a / b
        (a, b) = (b, a % b)
        (x, lastx) = (lastx - q*x, x)
        (y, lasty) = (lasty - q*y, y)

    return (a, lastx, lasty)

#--------------------------------------------------------------------------
def genkey():
    """ Generates RSA public and private key pair

        Return arguments return(e, d, n):
        e -- Public exponent
        d -- Private exponent
        n -- Modulo number
    """
    print 'Generating RSA key pair...'
    a = 500
    b = 2500   # Consider a_th to b_th prime numbers
    rndp = int( a  + (b - a)*rand())
    rndq = int( a  + (b - a)*rand())
    p = get_prime(rndp)    
    q = get_prime(rndq)
    n = p*q   # Modulo number
    m = (p - 1)*(q - 1)   # Toitent function
    e = 65537   # Encryption exponent ( fixed prime number choosen )
    (g, x, y) = xgcd(e, m)
    d = x + m   # Ensure d is always positive

    return (e, d, n)


#------------------------------------------------------------------------
def ptext2pcode( ptext ):
    """ This function encodes the input plaintext string such that each letter
    is represented by a two digit number related to its ASCII value. The resulting
    'pcode' is a numeric string with 2*len(ptext) digits.

    e.g 'abc' = 'xxxxxx'  x - a digit
    
    Argument: ptext2pcode( ptext )
    ptext: plaintext string """

    ptextlo = ptext.lower()   # Consider only lower case characters
    pcode = []
    prange = range(len(ptext))
    for idx in prange:
        pch = str(ord(ptextlo[idx]) - ord('a') + 10)
        pcode.append(pch)

    return ''.join(pcode)

#--------------------------------------------------------------------------
def split_pcode(pcode):
    """ Splits the 'pcode' numeric string to blocks of 3 digits returns as list.
    The last digit might not be 3 digits long.
    e.g. 'xxyyzz' => ['xxy', 'yzz']"""
    idx = 0
    pblock = []
    while (idx + 3) < len(pcode):
        pblock.append(pcode[idx:idx + 3])
        idx = idx + 3

    pblock.append(pcode[idx:len(pcode)])
    return pblock
        
#-------------------------------------------------------------------------
def encrypt(pblock,e,n):
    """ Encrypts each 3 digit numbers of  pcode  """
    ctext = []
    for blk in pblock:
        cblock = str(pow( int(blk), e, n))
        ctext.append(cblock)

    return ' '.join(ctext)   # Return cipher text as string with block values separated by space

#-------------------------------------------------------------------------
def decrypt(ctext, d, n):
    """ Decrypt each block of cipher text to return 3 digit number. Since the
    last block is not necessarily 3 digit, extra decision making sequence is needed
    to correctly extract last block"""
    clist = ctext.split(' ')
    ccode = []
    for blk in clist[0:-1]:   # Last block is decoded later
        cblock = str(pow(int(blk), d, n))
        ccode.append(cblock.zfill(3))   # Ensure that each block is 3 digit
    # Determining the last block
    cblock = str(pow(int(clist[-1]), d, n))
    if (len(clist[0:-1]) % 2 == 0):   # Even
        if len(cblock) == 1:
            ccode.append(cblock.zfill(2))
        else:
            ccode.append(cblock)
    else:  # Odd
        if len(cblock) == 1:
            ccode.append(cblock)
        else:
            ccode.append(cblock.zfill(3))
        
    return ''.join(ccode)
#--------------------------------------------------------------------------
def ccode2rtext(ccode):
    """ Convert the decrypted codes to corresponding Roman letters """
    idx = 0
    rtext = []
    while idx < len(ccode):
        rblk = ccode[idx:idx + 2]
        rtext.append(chr(int(rblk) + ord('a') - 10))
        idx = idx + 2

    return ''.join(rtext)



#-------------------------------------------------------------------------
def rsa_encrypt(ptext, e, n):
    """ Encrypt plaintext x using public key (e, n) """
    pcode = ptext2pcode(ptext)
    pblock = split_pcode(pcode)
    ciphertext = encrypt(pblock, e, n)
    return ciphertext

#-------------------------------------------------------------------------
def rsa_decrypt(ctext, d, n):
    """ Decrypt RSA cipher text using private key (d, n) """
    ccode = decrypt(ctext, d, n)
    decodedtext = ccode2rtext(ccode)
    return decodedtext
       
#--------------------------------------------------------------------------

def main():
    """ Main function """
    ptext = 'abstractalgebra'

    (e, d, n) = genkey()
    print ' Key pair (',e, n,') and (',d, n,')'    
    print ' Encrypting plaintext = ', ptext
    ctext = rsa_encrypt(ptext, e, n)
    print ' Cipher text  = ', ctext
    dtext = rsa_decrypt(ctext, d, n)
    print ' Deciphered text is ', dtext
    
if __name__ == '__main__':
   main()
    
    

    
    
    
    
