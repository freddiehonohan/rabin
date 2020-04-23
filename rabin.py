import hashlib, sys

nrabin = 0x1541942cc552a95c4832350ce99c2970f5b3ce9237a09c70c0e867d28039c05209b601105d3b3634cdaee4931809bc0c41d6165a0df16829a3a31202f56003239dd2c6e12297e94ef03e6aa61a147ea2b51c476dc45f5a2406b66d1ece2755c1f3d4144c0a42acc99b599d0643654a4cac392efbcf3db84d4233834afd1

def gcd(a,b):
  if b > a:
    a,b = b,a
  while b > 0:
    a,b = b,a % b
  return a

def nextPrime(p):
 while p % 4 != 3:
   p = p + 1
 return nextPrime_3(p)
  
def nextPrime_3(p):
  m_ = 3*5*7*11*13*17*19*23*29
  while gcd(p,m_) != 1:
    p = p + 4 
  if (pow(2,p-1,p) != 1):
      return nextPrime_3(p + 4)
  if (pow(3,p-1,p) != 1):
      return nextPrime_3(p + 4)
  if (pow(5,p-1,p) != 1):
      return nextPrime_3(p + 4)
  if (pow(17,p-1,p) != 1):
      return nextPrime_3(p + 4)
  return p

# x: bytes
# return: int
def h(x):
  hx = hashlib.sha256(x).digest()
  idx = len(hx)//2
  hl = hashlib.sha256(hx[:idx]).digest()
  hr = hashlib.sha256(hx[idx:]).digest()
  return int.from_bytes(hl + hr, 'little')

# m: bytes
def root(m, p, q):
  i = 0
  while True:
    x = h(m) % nrabin
    sig =   pow(p,q-2,q) * p * pow(x,(q+1)//4,q) 
    sig = ( pow(q,p-2,p) * q * pow(x,(p+1)//4,p) + sig ) % (nrabin) 
    if (sig * sig) % nrabin == x:
      break
    m = m + bytes.fromhex("00")
    i = i + 1
  print("paddingnum: " + str(i))
  return sig

def writeNumber(number, fnam):
  with open(fnam + '.txt', 'w') as f:
    f.write('%d' % number)

def readNumber(fnam):
  with open(fnam + '.txt', 'r') as f:
    return int(f.read())

def hF(m, paddingnum):
  return h(m + bytes.fromhex("00") * paddingnum) % nrabin

def sF(hexmsg):
  p = readNumber("p")
  q = readNumber("q")
  return root(bytes.fromhex(hexmsg), p, q)


def vF(hexmsg, paddingnum, s):
  return hF(bytes.fromhex(hexmsg), paddingnum) == (s * s) % nrabin
 
'''print("\n\n rabin signature - sCrypt Inc 2020 adapted from Scheerer - all rights reserved\n\n")
print("\n\n rabin signature - copyright Scheerer Software 2018 - all rights reserved\n\n")
print("First parameter is V (Verify) or S (Sign) or G (Generate)\n\n")
print("\n\n verify signature (2 parameters):")
print("   > python rabin.py V <hexmessage> <paddingnum> <digital signature> ")

print(" create signature S (2 parameter):")
print("   > python rabin.py S <hexmessage> \n\n")

print(" generate key pair G (2 parameter):")
print("   > python rabin.py G <hexseed> \n\n")

print(" number of parameters is " + str(len(sys.argv)-1))
print(" ")
print(" ")'''

if len(sys.argv) == 5 and sys.argv[1] == "V":
  print("result of verification: " + str(vF(sys.argv[2], int(sys.argv[3]), int(sys.argv[4], 16))))

if len(sys.argv) == 3 and sys.argv[1] == "S":
  print((" digital signature:\n " + hex(sF(sys.argv[2]))))
     
if len(sys.argv) == 3 and sys.argv[1] == "G":
  print(" generate primes ... ")
  p = nextPrime( h(bytes.fromhex(sys.argv[2])) % (2**501 + 1) )  
  q = nextPrime( h(bytes.fromhex(sys.argv[2] + '00')) % (2**501 + 1) )  
  writeNumber(p, 'p')                     
  writeNumber(q, 'q')     
  print("nrabin = ", hex(p * q))
