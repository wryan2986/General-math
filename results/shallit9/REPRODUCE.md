# Reproducing the Shallit Problem 9 computations

These artifacts concern the fixed point `a = phi^infinity(1)` of
`1 -> 12, 2 -> 23, 3 -> 14, 4 -> 32`, indexed from zero, and

```text
D_n(s) = det(a[s + i + j]) for 0 <= i,j < n; D_0(s) = 1.
```

**The strongest supported all-shifts result is `D_n(s) != 0` for every
`s >= 0` and `1 <= n <= 2049`.** No assertion for all orders, no exact zero
counterexample, and no prize-winning solution is established. The archived
data are outputs of computer-assisted checks, not a Lean formalization.

All commands below run from the repository root. Requirements are Python 3
with its standard library, and `g++` with C++17 and unsigned 128-bit integer
support. No external Python packages are needed. Executables and regenerated
outputs go to the git-ignored `build/` directory. The saved files in this
directory remain unchanged unless explicitly selected as an output path.

## Quick checks

```sh
python3 scripts/shallit9_crosscheck.py
python3 scripts/shallit9_verify_pair_samples.py
```

The first command compiles `src/shallit9_modular.cpp` into
`build/shallit9_modular`, generates the sequence independently by a binary
DFAO, and compares **1,056 exact integer Bareiss determinants** against
the C++ residues. These are all contained determinants in a prefix of
length 64, of orders 1 through 32. It also runs a Lucas–Lehmer primality
check for `2^61 - 1` and verifies the nine adjacent pairs and their
substitution closure. A prebuilt executable may instead be supplied with
`--binary build/shallit9_modular`; `--compiler` selects another compiler.

The second command reads the archived pair-block result and checks its
**288 saved residues** by separate exact rational Gaussian elimination:
orders 1 through 8, four offsets, and nine pair blocks. This verifies the
samples, not all 113 million entries of that sweep. The complete sweep is
a separate command below. Input may be supplied as a positional argument,
and both Python commands accept `--output PATH`.

The quick-check outputs are deterministic and can be compared with the
archived JSON files:

```sh
cmp build/shallit9_crosscheck_result.json results/shallit9/shallit9_crosscheck_result.json
cmp build/shallit9_pair_certificate_verified.json results/shallit9/shallit9_pair_certificate_verified.json
```

During repository integration on 2026-10-09, both quick checks passed and
both regenerated JSON files matched the archives byte-for-byte. The long
sweeps were not rerun during that integration.

## Complete pair-block check: all shifts through order 2049

```sh
mkdir -p build
g++ -O3 -std=c++17 src/shallit9_pair_certificate.cpp -o build/shallit9_pair_certificate
build/shallit9_pair_certificate 12 > build/shallit9_pair_certificate_result.json
python3 scripts/shallit9_verify_pair_samples.py build/shallit9_pair_certificate_result.json
cmp build/shallit9_pair_certificate_result.json results/shallit9/shallit9_pair_certificate_result.json
```

The independent C++ program uses `p = 2^31 - 1`, with primality checked by
trial division. It generates `phi^12(ab)` for each of

```text
P = {12, 14, 21, 22, 23, 31, 32, 41, 42}.
```

Every block has length 8192. All contained determinants of orders 1
through 2049 are checked: **113,301,504 residues including duplicates**,
all nonzero in the archived run. The deterministic residue fingerprint
is `624442176 mod p`; it is a reproducibility aid, not a cryptographic
proof. The JSON stores block counts and the 288 exact-check samples.

Why these finite blocks cover every shift: `P` is the exact adjacent-pair
set of `a`. All its pairs occur in `phi^5(1)`; internal and boundary pairs
of substituted allowed pairs stay in `P`. Since `a = phi^12(a)`, any
factor of length at most `4096 + 1` lies in two consecutive length-4096
substitution blocks. Hence it occurs in one of the nine checked words.
An order-`n` Hankel determinant uses a factor of length `2*n - 1`, so this
coverage reaches exactly the asserted bound `n <= 2049`.

The executable accepts a substitution depth from 1 through 16. Changing
it changes the work and the conditional order bound; only the saved
depth-12 run establishes the result reported here.

## Finite-prefix modular sweeps

The quick crosscheck already compiles the prefix checker. To compile it
directly and regenerate a selected archived sweep:

```sh
mkdir -p build
g++ -O3 -std=c++17 src/shallit9_modular.cpp -o build/shallit9_modular
build/shallit9_modular 8192 4096 > build/shallit9_modular_8192.txt
build/shallit9_modular 32768 16384 > build/shallit9_modular_32768.txt
build/shallit9_modular 131072 65536 > build/shallit9_modular_131072.txt
```

The last command is optional and substantially longer: its saved run
took approximately 516 seconds. The elapsed times and progress messages
depend on the machine. Progress is printed to stderr and is not part of
the archived result. No binaries or progress logs are stored in git.

| Prefix length `L` | Orders checked | Number of contained determinants | Archived result |
|---:|---:|---:|---|
| 8,192 | 1–4,096 | 16,781,312 | All nonzero modulo `2^61 - 1` |
| 32,768 | 1–16,384 | 268,451,840 | All nonzero modulo `2^61 - 1` |
| 131,072 | 1–65,536 | 4,295,032,832 | All nonzero modulo `2^61 - 1` |

For each order `n`, the finite-prefix range is
`0 <= s <= L - (2*n - 1)`. For these even lengths the total count is
`L^2/4 + L/2`. A large maximum order in one finite prefix is **not** an
all-shifts result at that order.

Both C++ programs use the exact Desnanot–Jacobi identity

```text
D_n(s) D_(n-2)(s+2)
  = D_(n-1)(s) D_(n-1)(s+2) - D_(n-1)(s+1)^2.
```

They check that denominators are nonzero before inversion. A detected
zero residue stops the check; it is only a candidate, not a proof of
integer singularity. A successful nonzero residue establishes integer
nonvanishing exactly, without a probabilistic claim. Any failed command
or truncated output must not be reported as a successful sweep.

## Independent factor-coverage check

```sh
python3 scripts/shallit9_independent_factor_check.py --iterations 15
```

This optional Python check uses suffix-array doubling and Kasai LCP,
independent of `scripts/factor_closure.py`. It first compares the method
with naive substring search on 100 deterministic random word pairs.
For `w = phi^15(1)`, it finds that the shortest factor of `phi(w)` absent
from `w` has length **1026**, at offset **49151**. All factor lengths
through 1025 are covered, giving an all-shifts order bound of **513**
when paired with successful prefix determinant checks. The separate
pair-block computation above establishes the stronger bound of 2049.
Its JSON elapsed time varies across runs, so bytewise equality of this
optional regenerated result is not expected.

## Artifact inventory

| Path relative to the repository root | Role |
|---|---|
| `src/shallit9_modular.cpp` | Full finite-prefix sweep modulo `2^61 - 1`; optional `dump` argument emits residues. |
| `src/shallit9_pair_certificate.cpp` | Independent nine-pair-block sweep modulo `2^31 - 1`. |
| `scripts/shallit9_crosscheck.py` | Independent DFAO, exact Bareiss comparison, Lucas–Lehmer check, and pair closure. |
| `scripts/shallit9_verify_pair_samples.py` | Exact rational elimination for saved pair-block samples. |
| `scripts/shallit9_independent_factor_check.py` | Independent suffix-array check of finite-factor coverage. |
| `results/shallit9/shallit9_crosscheck_result.json` | Archived 1,056-determinant exact comparison and pair facts. |
| `results/shallit9/shallit9_pair_certificate_result.json` | Archived complete depth-12 summary and 288 samples. |
| `results/shallit9/shallit9_pair_certificate_verified.json` | Archived summary of the independent exact sample check. |
| `results/shallit9/shallit9_independent_factor_result.json` | Archived depth-15 factor-coverage result. |
| `results/shallit9/shallit9_modular_8192.txt` | Archived prefix-8192 sweep summary. |
| `results/shallit9/shallit9_modular_32768.txt` | Archived prefix-32768 sweep summary. |
| `results/shallit9/shallit9_modular_131072.txt` | Archived prefix-131072 sweep summary. |
| `results/shallit9/REPRODUCE.md` | This reproduction guide and scope statement. |

All seven archived JSON/TXT result files were copied byte-for-byte from
the original session outputs. New checks are reproductions, not additional
independent discoveries. Research and code were produced with ChatGPT
and AI research agents; novelty of the finite bound has not been established.
