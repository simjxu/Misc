import math
import numpy
import scipy
import matplotlib

f0 = 4000
q = 0.331
f = 45

num = pow(
    pow(pow(f0, 2) - pow(f, 2), 2) +
    pow(f0 * f / q, 2),
    2
)
den1 = pow(
    pow(f0, 4) -
    pow(f0, 2) * pow(f, 2),
    2
)
den2 = pow(pow(f0, 3) * f / q, 2)
den = den1 + den2
r = math.sqrt(num / den)

print("at 45 hz, multiply by" , r)