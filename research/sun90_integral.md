# An exact integral reduction for Sun's $90 identity

Research checkpoint: 2026-10-09 UTC. Developed with AI assistance. This note proves an integral representation and an equivalent formulation of the prize problem. **It does not evaluate the required special value, prove Sun's conjecture, or establish novelty of the reduction.** No sponsor has been contacted and no reward has been claimed.

## 1. Target and notation

Let

$$
B_n=\sum_{k=0}^n\binom nk\binom{n+2k}{2k}\binom{2k}k(-324)^{n-k},
\qquad A_n=\binom{2n}n B_n,
\qquad F(z)=\sum_{n\geq0}A_nz^n.
$$

With $\theta=z\,d/dz$, the target is

$$
(357\theta+103)F(1/2160)=\frac{90}{\pi}.
\tag{1}
$$

The original sponsor states this identity as equation (3) of [his MathOverflow question](https://mathoverflow.net/questions/369569/two-curious-series-for-1-pi). The $90 offer is also explicit on slide 14 of [his May 8, 2026 Graz lecture](https://imsc.uni-graz.at/AlgNTh/slides/Slides_080526.pdf). The audit of prize conditions is separate from this mathematical note.

Write

$$
f(q)={}_2F_1\!\left(\frac13,\frac23;1;q\right)
=\sum_{k\geq0}\frac{(1/3)_k(2/3)_k}{(k!)^2}q^k.
$$

## 2. Integral representation

**Proposition.** For real $0\leq z\leq1/2160$, put $a=1296z$. Then

$$
\boxed{
F(z)=\frac{1}{\pi\sqrt{1+a}}
\int_0^1
f\!\left(\frac{108z(1-t)(1+at)^2}{(1+a)^3}\right)
\frac{dt}{\sqrt{t(1-t)}}.
}
\tag{2}
$$

The same identity holds for complex $z$ sufficiently near zero, with the branches obtained by continuation from $z=0$.

### Proof: sum the other index first

Reindexing $n=j+k$ gives the exact factorial identity

$$
F(z)=\sum_{j,k\geq0}
\binom{2j+2k}{j+k}
\frac{(j+3k)!}{j!(k!)^3}
(-324)^jz^{j+k}.
\tag{3}
$$

For a fixed $k$, the ratios

$$
\frac{\binom{2j+2k}{j+k}}{\binom{2k}{k}}
=4^j\frac{(k+1/2)_j}{(k+1)_j},
\qquad
\frac{(j+3k)!}{(3k)!}=(3k+1)_j
$$

therefore yield

$$
F(z)=\sum_{k\geq0}\binom{2k}{k}\frac{(3k)!}{(k!)^3}z^k
{}_2F_1\!\left(k+\frac12,3k+1;k+1;-a\right).
\tag{4}
$$

Apply Euler's transformation

$$
{}_2F_1(A,B;C;x)
=(1-x)^{C-A-B}{}_2F_1(C-A,C-B;C;x),
$$

which is [DLMF 15.8.1](https://dlmf.nist.gov/15.8.E1). Here it becomes

$$
{}_2F_1\!\left(k+\frac12,3k+1;k+1;-a\right)
=(1+a)^{-3k-1/2}
{}_2F_1\!\left(\frac12,-2k;k+1;-a\right).
\tag{5}
$$

The last hypergeometric function is a polynomial. Euler's beta integral, [DLMF 15.6.1](https://dlmf.nist.gov/15.6.E1), gives

$$
{}_2F_1\!\left(\frac12,-2k;k+1;-a\right)
=\frac{\Gamma(k+1)}{\sqrt\pi\,\Gamma(k+1/2)}
\int_0^1 t^{-1/2}(1-t)^{k-1/2}(1+at)^{2k}\,dt.
\tag{6}
$$

In this polynomial case, (6) can alternatively be proved without analytic continuation: expand $(1+at)^{2k}$, integrate its finitely many terms with the beta integral, and compare the terminating series.

Now the gamma factors cancel the central binomial coefficient:

$$
\binom{2k}{k}
\frac{\Gamma(k+1)}{\sqrt\pi\,\Gamma(k+1/2)}
=\frac{4^k}{\pi}.
$$

Substitute (5) and (6) in (4), take $(1+a)^{-1/2}$ outside, and sum under the integral. The remaining series is precisely $f$, since

$$
\frac{(3k)!}{(k!)^3}
=27^k\frac{(1/3)_k(2/3)_k}{(k!)^2}.
$$

This proves (2), with the interchange justified below.

## 3. Absolute convergence and differentiation

The cancellation in $B_n$ should not be used to justify an exchange of its two summations. A direct majorant works instead. Let $r=|z|$, and suppose

$$
1296r<1,
\qquad \frac{108r}{(1-1296r)^3}<1.
\tag{7}
$$

Using $\binom{2n}{n}\leq4^n$, the sum of the absolute values of all terms in (3) is at most

$$
\begin{aligned}
&\sum_{j,k\geq0}
\frac{(j+3k)!}{j!(k!)^3}(1296r)^j(4r)^k\\
&\qquad=
\frac{1}{1-1296r}
f\!\left(\frac{108r}{(1-1296r)^3}\right)<\infty.
\end{aligned}
\tag{8}
$$

At the target $r=1/2160$, the two quantities in (7) are respectively $3/5$ and $25/32$. Both inequalities are strict, so (8) also holds for some slightly larger $r$. Consequently the original series and its $z$-derivative converge uniformly on a neighborhood of the target, and the reindexing and summation in (3)–(4) are valid there.

For real nonnegative $z$, the terms produced by (6) are nonnegative. Hence their sum and integral may be interchanged by monotone convergence; their sum is finite because (4) equals the absolutely convergent original double sum. At the target, section 4 provides the stronger uniform bound $0\leq q(t)\leq1/81$. Continuity on the compact integration interval extends this bound to $|q|<\rho<1$ in a sufficiently small complex neighborhood of the target. The defining series for $f$ and its derivative are then uniformly bounded. The only remaining endpoint weight is $1/\sqrt{t(1-t)}$, which is integrable. Differentiation under the integral in section 5 follows.

## 4. The exact cubic at the target

At $z_0=1/2160$, one has $a=3/5$, and (2) simplifies to

$$
F(z_0)=\frac{\sqrt{5/8}}{\pi}
\int_0^1 f(q(t))\frac{dt}{\sqrt{t(1-t)}},
\qquad
q(t)=\frac{(1-t)(3t+5)^2}{2048}.
\tag{9}
$$

The following identities are exact:

$$
q'(t)=-\frac{(3t+5)(9t-1)}{2048},
\quad q(0)=\frac{25}{2048},
\quad q(1/9)=\frac1{81},
\quad q(1)=0.
$$

It follows that

$$
\boxed{0\leq q(t)\leq1/81\quad(0\leq t\leq1),}
$$

with a unique maximum at $t=1/9$. The cubic is **not one-to-one on the integration interval**: a substitution using its inverse must split the interval at $1/9$ and track both inverse branches.

There is also a useful factorization of its complementary argument:

$$
1-q(t)=\frac{(t+7)(9t^2-42t+289)}{2048}.
\tag{10}
$$

The quadratic discriminant is $-8640=-576\cdot15$, and its roots are $(7\pm4i\sqrt{15})/3$. The occurrence of 7 and 15 may help identify an elliptic transformation. That possible use is a research lead, **not a proof of complex multiplication or of the special value**.

## 5. An equivalent algebraic-valued integral

The weighted derivative in the prize identity can also be carried through exactly. Define

$$
q_z(t)=\frac{108z(1-t)(1+at)^2}{(1+a)^3},\qquad a=1296z.
$$

Direct logarithmic differentiation gives

$$
\theta\log q_z(t)
=\frac{1-2a+3at}{(1+a)(1+at)},
$$

and

$$
\frac{d}{dt}\log q_z(t)
=-\frac{1-2a+3at}{(1-t)(1+at)}.
$$

Therefore

$$
\theta f(q_z(t))
=-\frac{1-t}{1+a}\frac{d}{dt}f(q_z(t)).
\tag{11}
$$

Although the displayed logarithms are undefined when $q_z(t)=0$, (11) holds there by continuity, or directly by differentiating the polynomial $q_z$.

Put $Y(t)=f(q(t))$ for the target cubic in (9). Differentiating the prefactor in (2), then using (11), gives

$$
(357\theta+103)F(z_0)
=\frac{\sqrt{5/8}}{\pi}
\int_0^1
\left[\frac{577}{16}Y(t)
-\frac{1785}{8}(1-t)Y'(t)\right]
\frac{dt}{\sqrt{t(1-t)}}.
\tag{12}
$$

Thus the original prize identity is exactly equivalent to

$$
\boxed{
\int_0^1
\left[\frac{577}{16}Y(t)
-\frac{1785}{8}(1-t)Y'(t)\right]
\frac{dt}{\sqrt{t(1-t)}}
=36\sqrt{10}.
}
\tag{13}
$$

Equation (13) remains unproved. Its derivation does not replace the missing special-value argument. In particular, a naive integration by parts of the second term creates a divergent boundary term at $t=0$, since $(1-t)/\sqrt{t(1-t)}$ diverges and $Y(0)\neq0$. Any such manipulation must introduce and justify a cancellation or boundary regularization first.

## 6. Verification and remaining work

As an independent algebra check, the expansion of the right side of (2) was evaluated with exact rational arithmetic through degree 18 using beta moments

$$
\frac1\pi\int_0^1 t^{j-1/2}(1-t)^{k-1/2}\,dt
=\frac{(1/2)_j(1/2)_k}{(j+k)!}.
$$

It matched the direct finite sums for $A_n$, beginning

$$
1,\ -636,\ 583740,\ -558322080,\ 503833726620,\ -378971038088496.
$$

This finite check supports the algebra; the transformation and convergence argument above establish the identity for all coefficients and at the target. No precision-only evaluation of (1) was treated as proof.

The focused transformation attempted here is the index reversal followed by Euler's hypergeometric transformation and beta integration. It removes the original alternating double sum and exposes one explicit cubic pullback under the arcsine measure. A further transformation identifying (9) with a product of elliptic periods, together with a rigorously evaluated derivative relation at the relevant algebraic parameters, would be a concrete next route to (13). No such transformation or complete WZ certificate was obtained in this subtask.

### Sources consulted

- Zhi-Wei Sun, [Two curious series for $1/\pi$](https://mathoverflow.net/questions/369569/two-curious-series-for-1-pi), original problem statement; retrieved 2026-10-09.
- Zhi-Wei Sun, [Combinatorial Congruences and Infinite Series involving Binomial Coefficients](https://imsc.uni-graz.at/AlgNTh/slides/Slides_080526.pdf), May 8, 2026, slide 14; sponsor offer audited in this project.
- NIST DLMF, [15.8.1, Euler's transformation](https://dlmf.nist.gov/15.8.E1); retrieved 2026-10-09.
- NIST DLMF, [15.6.1, Euler's integral representation](https://dlmf.nist.gov/15.6.E1); retrieved 2026-10-09. The DLMF uses a regularized hypergeometric notation in this formula; equation (6) above includes the gamma factor appropriate to ordinary ${}_2F_1$.
