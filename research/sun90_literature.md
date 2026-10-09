# Sun's $90 identity: literature and analytic continuation notes

Checked 2026-10-09. This note records exact reductions and research leads. **No proof of the prize identity was found in this session.** In particular, a differential equation for the generating function does not by itself evaluate the required special value.

## Target and original-sponsor status

Put

$$
B_n(c)=\sum_{k=0}^n\binom nk\binom{n+2k}{2k}\binom{2k}k c^{n-k},
\qquad F(z)=\sum_{n\ge0}\binom{2n}nB_n(-324)z^n.
$$

The target is

$$
(357zF'(z)+103F(z))\big|_{z=1/2160}=90/\pi.
$$

The accessible original-sponsor offer was renewed in Zhi-Wei Sun's **May 8, 2026 Graz lecture**, slide 14. It offers $90 for the first proof. Its separate $105 offer covers the associated bundle of congruences, not just one congruence. The offer contains no stated journal requirement and no explicit policy on fully AI-generated proofs. Payment and AI eligibility therefore remain unconfirmed; no contact or claim has been made.

Primary sources:

- [May 8, 2026 lecture](https://imsc.uni-graz.at/AlgNTh/slides/Slides_080526.pdf), slide 14 for the identity and offers, slides 14–15 for the congruences.
- [Sun's MathOverflow question, August 2020](https://mathoverflow.net/questions/369569/two-curious-series-for-1-pi), equation (3). No answer was displayed when checked. A later comment suggests a hypergeometric transformation but supplies no proof.
- [Sun, *List of conjectural series for powers of pi*](https://arxiv.org/html/1102.5649v47), equation (5.9), with the $90/$105 offers. This is historical evidence, not a substitute for the dated 2026 renewal.
- [Sun, *Some new series for 1/pi and related congruences*](https://arxiv.org/pdf/1104.3856), version 9, December 2017; journal publication *Nanjing University Journal of Mathematics Biquarterly* 31 (2014), 150–164. The target is equation (4.34). Remark 4.4 identifies the coefficient family's connection to MacMahon's identity below.

Fresh searches for the exact constants and coefficient family did not locate a complete proof. This search result does not guarantee that the prize remains unclaimed privately.

## Exact reductions

Write $f(w)={}_2F_1(1/3,2/3;1;w)$. Reindexing with $n=j+k$ gives

$$
B_n(c)=\sum_{j+k=n}\frac{(j+3k)!}{j!k!^3}c^j,
\qquad
\sum_{n\ge0}B_n(c)z^n
=\frac1{1-cz}f\!\left(\frac{27z}{(1-cz)^3}\right).
$$

These identities follow by the binomial theorem and $(3k)!/k!^3=27^k(1/3)_k(2/3)_k/k!^2$; they are exact formal power-series identities.

The beta integral for the central binomial coefficient then gives

$$
F(z)=\frac1\pi\int_0^1
\frac{f\!\left(108zu/(1+1296zu)^3\right)}{1+1296zu}
\frac{du}{\sqrt{u(1-u)}}.
$$

With $a=1296z$ and $u=(1-t)/(1+at)$, this becomes

$$
F(z)=\frac1{\pi\sqrt{1+a}}\int_0^1
f\!\left(\frac{108z(1-t)(1+at)^2}{(1+a)^3}\right)
\frac{dt}{\sqrt{t(1-t)}}.
$$

At the target point, the argument simplifies to

$$
q(t)=\frac{(1-t)(3t+5)^2}{2048},\qquad
1-q(t)=\frac{(t+7)(9t^2-42t+289)}{2048}.
$$

Here $0\le q(t)\le1/81$ on $[0,1]$, with the maximum at $t=1/9$. These reductions provide well-behaved integral representations, but do not evaluate the target derivative combination.

MacMahon's identity, explicitly cited by Sun, is

$$
B_n(-4)=\sum_{k=0}^n\binom nk^3.
$$

Thus this is a deformation of the Franel-number coefficient family. The identity is established prior mathematics, not a new result from this session.

The coordinating computation obtained and proved a fourth-order operator for $F$; its full certificate is maintained separately. In the scaled variable $v=108z$, its leading coefficient factors as

$$
(1+8v)(1+30v)(1+27v+216v^2).
$$

At $v=1/20$, the quadratic factor is $(17/10)^2$, while the product of the linear factors is $7/2$. These exact simplifications may assist an algebraic transformation. They do not establish an elliptic-product formula. The extra operator factor $1+30v$ may be apparent; that interpretation has not been independently proved here.

## Literature examined and the remaining gap

1. **Brafman / Bailey products.** [James Wan and Wadim Zudilin, *Generating functions of Legendre polynomials: a tribute to Fred Brafman*](https://archive.mpim-bonn.mpg.de/973/1/preprint_2011_37.pdf) develops products of two Gauss hypergeometric functions and generating functions involving $P_n$, $P_{2n}$, and $P_{3n}$, including the parameters $1/3,2/3$. These are relevant templates. No exact matching transformation for the above beta integral or coefficients was obtained.

2. **A proven Sun-prize example.** [Mathew Rogers and Armin Straub, *A solution of Sun's $520 challenge concerning 520/pi*](https://arminstraub.com/downloads/pub/sun520.pdf) uses a Legendre-polynomial generating function, a hypergeometric product, and modular special-value identities. Its coefficient family is different. Its proof cannot be substituted for a proof of the $90 identity.

3. **Failed elementary coefficient ansatz.** For $S_n(s)=\sum_k\binom nk\binom{n+2k}{2k}\binom{2k}k s^k$, a direct ansatz $S_n(s)=P_n(U)P_n(V)$, with $U,V$ independent of $n$, fails. Matching $n=1,2$ forces $UV=1+6s$ and $U^2+V^2=2+4s-12s^2$. The product at $n=3$ then equals $1+66s+630s^2+1620s^3$, whereas $S_3(s)=1+60s+630s^2+1680s^3$. This excludes that simple ansatz only; algebraic generating-function transformations remain possible.

4. **Speculative next route.** Franel numbers, elliptic generating functions, and fourth-order periods suggest comparing the family with anisotropic lattice Green functions or suitable K3 / elliptic-product families. The factors involving 7 and a quadratic discriminant $-8640=-576\cdot15$ at the target are compatible with the quadratic-form discriminant in Sun's congruences. This is a heuristic, not a proved modular identification. A successful continuation needs an explicit transformation and a rigorous special-value identity, not just numerical recognition.

## A tempting but already solved alternative

The $480 identity involving $48^k/[k(2k-1)\binom{4k}{2k}\binom{2k}k]$ is excluded. Its original offer appears in [Wang–Sun, arXiv:2006.02918](https://arxiv.org/abs/2006.02918), but a WZ proof was posted in December 2022 and an alternative integral proof in 2024 on the [original MathOverflow question](https://mathoverflow.net/questions/302982/how-to-prove-the-identity-l2-frac-cdot3-frac215-sum-limits-k-1-inf). The original WZ paper is [Kam Cheong Au, *Multiple zeta values, WZ-pairs and infinite sums computations*](https://arxiv.org/abs/2212.02986). Rediscovering its integral reduction would not produce a new prize solution.
