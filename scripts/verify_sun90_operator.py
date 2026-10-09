#!/usr/bin/env python3
"""Verify the Sun $90 generating-function operator by exact algebra.

This verifies a differential equation, NOT the conjectured 90/pi value.
No coefficient fitting or numerical approximation is used in this verifier.
Requires SymPy. Run from any working directory.
"""
import json
import math
import sympy as s
from sympy.functions.combinatorial.numbers import stirling

z, n, T = s.symbols("z n T")
t = s.Integer(-324)
h, g = 1 - t*z, 1 + 2*t*z
r = 27*z/h**3
q = h**3 - 27*z
anum = g**2*(h**3-54*z) - 6*t*z*(1+t*z)*q
c2 = z*h**2*g*q
c1 = h*anum - 2*t*z*h*g*q
c0 = -6*g**3 - t*anum

# Derive directly from r(1-r)y''+(1-2r)y'-(2/9)y=0,
# y(r(z))=h(z)B(z). Primes on y mean r derivatives.
rp, rpp = s.diff(r, z), s.diff(r, z, 2)
chain = [
    r*(1-r)*h,
    r*(1-r)*(-2*t-h*rpp/rp)+(1-2*r)*rp*h,
    r*(1-r)*t*rpp/rp-(1-2*r)*t*rp-s.Rational(2,9)*h*rp**2,
]
scale = s.cancel(c2/chain[0])
assert all(s.cancel(left-scale*right) == 0
           for left, right in zip([c2,c1,c0],chain))

# B(z)=h^-1 2F1(1/3,2/3;1;27z/h^3), established by reindexing.
# Convert its exact ODE to a recurrence, then multiply B_n by C(2n,n).
ob = s.Poly(s.expand(c2/z*T*(T-1)+c1*T+z*c0), z)
pj = [ob.nth(j) for j in range(ob.degree()+1)]
d = len(pj)-1
fall = s.prod(n-k for k in range(d))
rec = []
for j in range(d+1):
    ratio = s.prod(2*(2*n-2*k-1)/(n-k) for k in range(j))
    rec.append(s.factor(s.cancel(fall*ratio*pj[j].subs(T,n-j))))
common = s.factor(s.gcd_list(rec))
rec = [s.cancel(x/common) for x in rec]
# Cancelling the common factor is valid at n>=d; check its integer roots.
for root in s.roots(common, n):
    assert not (root.is_integer and root >= d)
Ltheta = s.expand(sum(z**j*rec[j].subs(n,T+j) for j in range(d+1)))

P = [
    T**3*(T-1),
    6*T*(1170*T**3-135*T**2+743*T+106),
    3888*(2*T+1)*(2223*T**3+2268*T**2+1949*T+648),
    272097792*(2*T+1)*(2*T+3)*(17*T**2+24*T+12),
    881596846080*(T+1)*(2*T+1)*(2*T+3)*(2*T+5),
]
Rtheta = s.expand(sum(z**j*P[j] for j in range(5)))

def theta_to_D(expr):
    out = {}
    for (power,), coefficient in s.Poly(expr,T).terms():
        for i in range(power+1):
            st = (1 if i == power == 0 else
                  0 if i == 0 else stirling(power,i,kind=2))
            out[i] = out.get(i,0)+coefficient*st*z**i
    return {i:s.factor(v) for i,v in out.items() if v != 0}

L, R = theta_to_D(Ltheta), theta_to_D(Rtheta)
rem, quotient = L.copy(), {}
while rem and max(rem) >= max(R):
    shift = max(rem)-max(R)
    f = s.cancel(rem[max(rem)]/R[max(R)])
    quotient[shift] = f
    # Leibniz rule: (f D^shift) composed with each coefficient*D^j.
    for j,v in R.items():
        for k in range(shift+1):
            power = j+shift-k
            value = s.cancel(rem.get(power,0)-f*s.binomial(shift,k)*s.diff(v,z,k))
            if value == 0:
                rem.pop(power,None)
            else:
                rem[power] = value
assert not rem

def A(k):
    return math.comb(2*k,k)*sum(
        math.factorial(k+2*j)//(math.factorial(k-j)*math.factorial(j)**3)
        *(-324)**(k-j) for j in range(k+1))

aa = [A(k) for k in range(max(d,5))]
# Exceptional recurrence indices after denominator clearing/cancellation.
for k in range(d):
    assert sum(rec[j].subs(n,k)*aa[k-j] for j in range(k+1)) == 0
initial = [sum(P[j].subs(T,k-j)*aa[k-j] for j in range(min(k,4)+1))
           for k in range(5)]
assert initial == [0]*5
for j,v in quotient.items():
    assert s.denom(s.cancel(v/z**j)).subs(z,0) != 0
indicial = s.factor(sum(s.limit(v/z**j,z,0)*s.prod(T-k for k in range(j))
                        for j,v in quotient.items()))
assert s.expand(indicial-(T-2)*(T-3)*(T-4)) == 0
# If H=R(F) were nonzero, its first exponent nu is >=5. The first coefficient
# of Q(H)=0 would be (nu-2)(nu-3)(nu-4) times its nonzero leading coefficient.
# This contradiction proves H=0 as a formal power series.

print(json.dumps({
    "status":"verified exact differential equation; prize identity NOT proved",
    "sympy_version":s.__version__,
    "chain_rule_verified":True,
    "higher_order":max(L),
    "common_recurrence_factor_cancelled":str(common),
    "exceptional_initial_indices_checked":list(range(d)),
    "right_factor_order":max(R),
    "right_division_remainder_zero":True,
    "indicial_polynomial":str(indicial),
    "initial_residual_coefficients":[int(x) for x in initial],
    "theta_coefficients":[str(s.factor(v)) for v in P],
    "left_quotient_D_coefficients":{str(j):str(s.factor(v)) for j,v in quotient.items()},
    "initial_A_coefficients":aa,
    "minimality_claimed":False,
    "special_value_proved":False,
},indent=2))
