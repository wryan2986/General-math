# Shallit Problem 9: exact search and a bounded-order theorem

Date: 2026-10-09. Generated and reviewed by AI agents. **The prize problem is unresolved in this project.** The results below are computer-assisted mathematics, not a Lean formalization or an independently refereed publication. Novelty relative to every earlier private computation is not established.

## Mathematical contract

Use the literal integer alphabet {1,2,3,4} and substitution

$$
\phi(1)=12,\quad\phi(2)=23,\quad\phi(3)=14,\quad\phi(4)=32.
$$

Let $a=\phi^\infty(1)=1223231423141232\cdots$, indexed from zero. Define

$$
H_n(k)=\det(a_{k+i+j})_{0\le i,j<n},\qquad n\ge1,\ k\ge0.
$$

The question is whether **every** $H_n(k)$ is nonzero. A negative answer needs just one exact singular matrix; a nonzero integer null vector would be a short certificate. A zero modulo a prime is not such a certificate. The alphabet cannot be replaced by arbitrary real values or a different four-letter substitution.

Original sponsor: [2014 slides](https://cs.uwaterloo.ca/~shallit/Talks/bc4.pdf), pp. 32–35; [current updates](https://cs.uwaterloo.ca/~shallit/talks.html), checked 2026-10-09. The offer is £50. The precise morphism already occurs as Problem 44 in the [2010 Oberwolfach report](https://ems.press/content/serial-article-files/46296), pp. 38–39. AI eligibility and present award priority remain unconfirmed. The sponsor's recent real-valued Problem 8 resolution does not answer this problem.

## Result 1: a complete finite search

All the following checks used exact arithmetic modulo the prime $p=2^{61}-1$.

| Prefix length $L$ | Largest order $K$ | Determinants checked | Modular zeros |
|---:|---:|---:|---:|
| 8,192 | 4,096 | 16,781,312 | 0 |
| 32,768 | 16,384 | 268,451,840 | 0 |
| **131,072** | **65,536** | **4,295,032,832** | **0** |

The domain is exactly $1\le n\le K$, $0\le k\le L-2n+1$, so the count is

$$
\sum_{n=1}^K(L-2n+2)=K(L+1-K).
$$

The large run took 515.723 seconds as measured by its executable. It used a CPU and modest linear working memory. These are nested search domains; do not add their counts as though every determinant were distinct across runs.

Desnanot–Jacobi gives

$$
H_n(k)H_{n-2}(k+2)=H_{n-1}(k)H_{n-1}(k+2)-H_{n-1}(k+1)^2.
$$

Starting with $H_0=1,H_1=a_k$, this computes each residue while all denominators remain nonzero. The central minor has shift **$k+2$**. Batch inversion accelerates field division. The program stops at a zero before attempting later division through it. Therefore, by induction, the recorded residues are actual determinant residues, not a heuristic recurrence.

All residues were nonzero, which proves nonvanishing of these integer determinants. This implication is exact; it is not a probabilistic primality or floating-point claim. A separate Lucas–Lehmer check verifies the modulus. Independently generated terms and exact integer Bareiss elimination match all **1,056** contained matrices in a length-64 prefix, orders through 32.

## Result 2: every shift, through order 2,049

Combining a finite language lemma with a second computation gives

$$
\boxed{H_n(k)\ne0\quad\text{for all }k\ge0\text{ and }1\le n\le2049.}
$$

The infinite quantifier over shifts is justified as follows.

### Lemma: exact adjacent pairs

The length-two factors of $a$ are exactly

$$
P=\{12,14,21,22,23,31,32,41,42\}.
$$

Every pair appears in $\phi^5(1)$. Internal pairs of letter images are in $P$, and the boundary pairs close on $P$:

| Pair $uv$ | First position in $\phi^5(1)$ | Boundary pair in $\phi(u)\phi(v)$ |
|---|---:|---|
| 12 | 0 | 22 |
| 14 | 6 | 23 |
| 21 | 23 | 31 |
| 22 | 1 | 32 |
| 23 | 2 | 31 |
| 31 | 5 | 41 |
| 32 | 3 | 42 |
| 41 | 11 | 21 |
| 42 | 7 | 22 |

This establishes both inclusion directions by induction, using a finite table that is readily checked independently.

### Lemma: two aligned blocks cover every short factor

For any $t\ge0$, write $B=2^t$. Because $a=\phi^t(a)$, a factor starting at $qB+r$, $0\le r<B$, of length $m\le B+1$ ends at relative index $r+m-1\le2B-1$. It is contained in

$$
\phi^t(a_qa_{q+1}),
$$

one of the nine pair blocks $\phi^t(uv)$ with $uv\in P$. Conversely each such block appears in $a$. Thus these nine finite words cover every possible shift for the required lengths.

Take $t=12$. Each block has length 8,192, and all factors of length at most 4,097 are covered. An order-$n$ Hankel matrix depends on a factor of length $2n-1$. Therefore the nine blocks suffice through $n=2049$.

### Independent computation for the lemma

A separately written C++ checker generated the nine blocks and checked every contained determinant of orders 1–2,049. It used the different prime $2^{31}-1=2,147,483,647$, whose primality it verifies by integer trial division through its square root.

- **113,301,504** residue checks, including duplicates, all nonzero.
- **288** saved samples independently matched exact rational Gaussian elimination using Python `Fraction`.
- Residue fingerprint: **624442176** modulo this prime. This fingerprint aids reproducibility; it is not by itself a proof or a cryptographic attestation.

The language argument and this independent finite computation establish the stated bounded-order theorem. The sample checks alone do not establish the entire theorem; they crosscheck the exhaustive verifier.

## A second finite-language method

For a finite word $w=\phi^t(1)$, let $F_m(w)$ denote its set of length-$m$ factors. If

$$
1\le m\le|w|,\qquad F_m(w)=F_m(\phi(w)),
$$

then $F_m(w)=F_m(a)$.

Indeed, every length-$m$ factor in $\phi(v)$ is contained in the image of a factor of $v$ of length at most $\lceil(m+1)/2\rceil\le m$. When $|v|\ge m$, extend that preimage inside $v$ to length $m$. Consequently

$$
F_m(\phi(v))=\bigcup_{u\in F_m(v)}F_m(\phi(u)).
$$

Equality at $w$ is a fixed point of this finite transformation; it persists under iteration. The increasing prefixes exhaust $a$. The hypothesis $m\le|w|$ is essential: equality between two empty finite factor sets cannot describe an infinite word.

The root implementation uses an exact suffix automaton, with no hashes. An independent suffix-array/Kasai implementation agreed on a length 32,768 comparison after 100 deterministic random comparisons with a naive algorithm. Recorded coverage:

| $t$ | Length of $w$ | All factor lengths through | First absent factor length / offset in $\phi(w)$ | All-shifts order consequence |
|---:|---:|---:|---|---:|
| 15 | 32,768 | 1,025 | 1,026 / 49,151 | 513 |
| 16 | 65,536 | 2,049 | 2,050 / 98,303 | 1,025 |
| 17 | 131,072 | 4,097 | 4,098 / 196,607 | 2,049 |

The pattern was not extrapolated to arbitrary $t$. The simpler pair-block proof already supplies the strongest stated theorem.

## Structural observations and the unresolved obstruction

Direct substitution gives

| Letter | $\phi^3$ image |
|---|---|
| 1 | 12232314 |
| 2 | 23141232 |
| 3 | 12231423 |
| 4 | 12322314 |

Every block has letter counts $(2,3,2,1)$ and integer sum 18. Hence every **aligned** eight-letter block has sum 18; the mean is $9/4$, with bounded centered partial sums. This is not true at every offset: the first length-eight block has sum 18 but the next has sum 19.

The letter-incidence matrix has characteristic polynomial $x^3(x-2)$. Its low rank after taking a power tracks counts, not ordering, and does not imply finite Hankel rank. Two further exact identities are $a_{4r+2}+a_{4r+3}=5$ and $a_{8r+1}-a_{8r}=1$.

Grouping Hankel rows and columns by parity or by residue modulo eight introduces mixed minors built from letter-indicator sequences. We did **not** find a closed finite recurrence family proving their nonvanishing. Simple sign induction fails: order-three determinants at shifts 0–7 are $3,-5,5,2,-23,-27,17,13$.

The 2010 source conjectures that every fixed finite modulus eventually encounters a zero in a number wall. This is an open historical conjecture, not a theorem used here. It is another reason not to infer an all-order proof from one successful prime or launch ever larger finite sweeps without a new idea.

## Reproduction and continuation

- [Commands and saved computation outputs](../results/shallit9/REPRODUCE.md).
- [Exact definitions and factor recognizer](../src/shallit9.py).
- [Factor-closure CLI](../scripts/factor_closure.py).

If returning to this target, prioritize a finite closed system of determinant identities and prove an invariant precluding cancellation. If a modular zero is discovered, reconstruct the exact integer matrix and certify singularity with exact elimination/nullspace arithmetic before calling it a counterexample. More nonzero numerical evidence alone is not a prize solution.
