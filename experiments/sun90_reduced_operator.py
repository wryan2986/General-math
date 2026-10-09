#!/usr/bin/env python3
"""Exact recovery and algebraic proof of a fourth-order Sun-series operator.

This is research toward the $90 identity, not a proof of its special value.
"""
import math
import sympy as s
from sympy.polys.matrices import DomainMatrix

n,z,T=s.symbols('n z T')
t=-324
def B(k):
    return sum(math.factorial(k+2*j)//(math.factorial(j)**3*math.factorial(k-j))*t**(k-j)
               for j in range(k+1))
a=[math.comb(2*k,k)*B(k) for k in range(100)]
order,degree=4,4
matrix=s.Matrix([[0 if k<j else (k-j)**r*a[k-j]
                  for j in range(degree+1) for r in range(order+1)]
                 for k in range(45)])
ns=DomainMatrix.from_Matrix(matrix).nullspace().to_Matrix()
assert ns.rows==1
v=list(ns.row(0));div=s.gcd_list(v);v=[s.cancel(x/div) for x in v]
if v[4]<0:v=[-x for x in v]
p=[s.factor(sum(v[j*(order+1)+r]*T**r for r in range(order+1))) for j in range(degree+1)]
print('EXACT RECOVERED theta coefficients:',[str(x) for x in p],flush=True)
for k in range(45,len(a)):
    assert sum(int(p[j].subs(T,k-j))*a[k-j] for j in range(min(k,degree)+1))==0
print('Verified on 55 coefficients not used for recovery; still needs algebraic proof.',flush=True)
lead=s.factor(sum(s.Poly(p[j],T).coeff_monomial(T**4)*z**j for j in range(5)))
print('Leading coefficient:',lead,flush=True)

# Build independently derived order-seven theta operator L for A.
h=1-t*z;g=1+2*t*z;Q=h**3-27*z
anum=s.expand(g**2*(h**3-54*z)-6*t*z*(1+t*z)*Q)
c2=s.expand(z*h**2*g*Q);c1=s.expand(h*anum-2*t*z*h*g*Q);c0=s.expand(-6*g**3-t*anum)
ob=s.Poly(s.expand(c2/z*T*(T-1)+c1*T+z*c0),z)
pj=[ob.nth(j) for j in range(ob.degree()+1)]
d=len(pj)-1
fall=s.prod(n-r for r in range(d));rec=[]
for j in range(d+1):
    ratio=s.prod(2*(2*n-2*r-1)/(n-r) for r in range(j))
    rec.append(s.factor(s.cancel(fall*ratio*pj[j].subs(T,n-j))))
common=s.gcd_list(rec);rec=[s.factor(x/common) for x in rec]
Ltheta=s.expand(sum(z**j*rec[j].subs(n,T+j) for j in range(len(rec))))
Rtheta=s.expand(sum(z**j*p[j] for j in range(len(p))))

# Convert sum_j z^j P_j(theta) to rational-coefficient D=d/dz operators.
def theta_to_D(expr):
    poly=s.Poly(expr,T);out={}
    # theta^r = sum_i S(r,i) z^i D^i, second-kind Stirling numbers.
    from sympy.functions.combinatorial.numbers import stirling
    for (r,),coef in poly.terms():
        for i in range(r+1):
            if r==0 and i==0:st=1
            elif i==0:st=0
            else:st=stirling(r,i,kind=2)
            out[i]=out.get(i,0)+coef*st*z**i
    return {i:s.factor(v) for i,v in out.items() if v!=0}

L=theta_to_D(Ltheta);R=theta_to_D(Rtheta)
def left_multiple(f,shift,A):
    out={}
    for j,v in A.items():
        for k in range(shift+1):
            degree=j+shift-k
            out[degree]=out.get(degree,0)+f*s.binomial(shift,k)*s.diff(v,z,k)
    return out

rem=L.copy();quot={}
while rem and max(rem)>=max(R):
    shift=max(rem)-max(R)
    f=s.cancel(rem[max(rem)]/R[max(R)])
    quot[shift]=f
    subtract=left_multiple(f,shift,R)
    for j,v in subtract.items():
        value=s.cancel(rem.get(j,0)-v)
        if value==0:rem.pop(j,None)
        else:rem[j]=value
print('Right-division remainder of proved L by candidate R:',{j:str(s.factor(v)) for j,v in rem.items()},flush=True)
print('Left quotient:',{j:str(s.factor(v)) for j,v in quot.items()},flush=True)
assert rem == {}
for k in range(d):
    assert sum(int(rec[j].subs(n,k))*a[k-j] for j in range(min(k,d)+1))==0
# The higher-order equation is proved from the hypergeometric equation for
# n>=d; the previous finite checks settle its exceptional initial indices.
# A right factor alone is insufficient. If h=R(F), the quotient gives Q(h)=0.
# q_j(z)/z^j is regular at zero, and its indicial polynomial has roots 2,3,4.
indicial=s.factor(sum(s.limit(quot[j]/z**j,z,0)*s.prod(T-r for r in range(j))
                       for j in quot))
assert s.expand(indicial-(T-2)*(T-3)*(T-4))==0
initial_h=[sum(p[j].subs(T,k-j)*a[k-j] for j in range(min(k,degree)+1)) for k in range(5)]
assert all(x==0 for x in initial_h)
print('Quotient indicial polynomial:',str(indicial),flush=True)
print('First five coefficients of R(F):',[int(x) for x in initial_h],flush=True)
print('PROVED: R(F)=0. A nonzero residual with order>=5 would contradict Q(h)=0 because the indicial polynomial is nonzero there.',flush=True)
print('No minimality or special-value identity is claimed.',flush=True)

