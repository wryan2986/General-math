#!/usr/bin/env python3
"""Derive a proved differential equation and seek a smaller operator.

The derived equation follows from the hypergeometric equation, not fitting.
Any smaller operator found by fitting is explicitly only a candidate until
proved independently. Requires sympy for symbolic polynomial arithmetic.
"""
import json
import math
import sympy as s

z, theta, n = s.symbols('z theta n')
t = s.Integer(-324)
h = 1-t*z
g = 1+2*t*z
Q = h**3-27*z
anum = s.expand(g**2*(h**3-54*z)-6*t*z*(1+t*z)*Q)
c2 = s.expand(z*h**2*g*Q)
c1 = s.expand(h*anum-2*t*z*h*g*Q)
c0 = s.expand(-6*g**3-t*anum)

# B_n has a second-order ordinary differential equation c2 B''+c1 B'+c0 B=0.
# The equivalent theta form is (c2/z) theta(theta-1)+c1 theta+z*c0.
operator_b = s.Poly(s.expand(c2/z*theta*(theta-1)+c1*theta+z*c0),z)
pj = [s.factor(operator_b.nth(j)) for j in range(operator_b.degree()+1)]
print('PROVED B theta-polynomial coefficients:', [str(x) for x in pj],flush=True)

def b_term(k):
    return sum(math.factorial(k+2*j)//(math.factorial(j)**3*math.factorial(k-j))*int(t)**(k-j)
               for j in range(k+1))

bs=[b_term(k) for k in range(100)]
for k in range(1,len(bs)):
    assert sum(int(pj[j].subs(theta,k-j))*bs[k-j] for j in range(min(k,len(pj)-1)+1))==0
print('B recurrence checked against 100 direct finite sums',flush=True)

# Multiplying B_n by binom(2n,n) changes each recurrence ratio by
# binom(2n,n)/binom(2(n-j),n-j). Clear denominator using falling factorial.
d=len(pj)-1
fall=s.prod(n-r for r in range(d))
rec=[]
for j in range(d+1):
    ratio=s.prod(2*(2*n-2*r-1)/(n-r) for r in range(j))
    rec.append(s.factor(s.cancel(fall*ratio*pj[j].subs(theta,n-j))))
common=s.gcd_list(rec)
rec=[s.factor(x/common) for x in rec]
print('PROVED A recurrence coefficients in n:',[str(x) for x in rec],flush=True)
aa=[math.comb(2*k,k)*bs[k] for k in range(len(bs))]
for k in range(d,len(aa)):
    assert sum(int(rec[j].subs(n,k))*aa[k-j] for j in range(d+1))==0
print('A recurrence checked against direct finite sums',flush=True)

def nullspace_mod(matrix,p):
    a=[row[:] for row in matrix]
    rows=len(a); cols=len(a[0]); piv=[];r=0
    for c in range(cols):
        row=next((i for i in range(r,rows) if a[i][c]),None)
        if row is None: continue
        a[r],a[row]=a[row],a[r]
        inv=pow(a[r][c],-1,p)
        a[r]=[(v*inv)%p for v in a[r]]
        for i in range(r+1,rows):
            if a[i][c]:
                v=a[i][c]
                for j in range(c,cols): a[i][j]=(a[i][j]-v*a[r][j])%p
        piv.append(c);r+=1
        if r==rows: break
    if len(piv)==cols: return None
    free=next(c for c in range(cols) if c not in piv)
    v=[0]*cols;v[free]=1
    for i in range(len(piv)-1,-1,-1):
        c=piv[i];v[c]=-sum(a[i][j]*v[j] for j in range(c+1,cols))%p
    return v

p=1000000007
coeff=[x%p for x in aa]
found=[]
for order in range(2,7):
    for degree in range(1,9):
        unknowns=(order+1)*(degree+1)
        if unknowns+15>len(coeff):continue
        mat=[[0 if k<j else pow(k-j,r,p)*coeff[k-j]%p
              for j in range(degree+1) for r in range(order+1)]
             for k in range(unknowns+15)]
        v=nullspace_mod(mat,p)
        if v:
            out={'order':order,'degree':degree,'prime':p,'vector':v,
                 'status':'modularly guessed, NOT yet a proof'}
            print(json.dumps(out),flush=True)
            found.append(out)
            break
print('done',flush=True)

