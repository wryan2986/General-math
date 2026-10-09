#!/usr/bin/env python3
"""Independent exact Bareiss + DFA verification of C++ condensation.

Run from the repository root with ``python3 scripts/shallit9_crosscheck.py``.
Uses only the Python standard library and a C++17 compiler. By default it
compiles the verifier and writes the new result under the ignored build/.
Pass --binary to check an existing executable instead of compiling one.
"""
from pathlib import Path
import argparse
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
P = 2**61 - 1
PHI = {1: (1, 2), 2: (2, 3), 3: (1, 4), 4: (3, 2)}

def at(n):
    """DFAO evaluation uses bits, independent of C++ substitution generation."""
    state = 1
    for bit in bin(n)[2:]:
        state = PHI[state][int(bit)]
    return state

def det_bareiss(mat):
    a = [row[:] for row in mat]
    size = len(a)
    if not size:
        return 1
    sign = 1
    prev = 1
    for k in range(size - 1):
        pivotrow = next((i for i in range(k, size) if a[i][k]), None)
        if pivotrow is None:
            return 0
        if pivotrow != k:
            a[k], a[pivotrow] = a[pivotrow], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, size):
            for j in range(k + 1, size):
                numerator = pivot * a[i][j] - a[i][k] * a[k][j]
                quotient, remainder = divmod(numerator, prev)
                assert remainder == 0, (k, i, j, numerator, prev)
                a[i][j] = quotient
            a[i][k] = 0
        prev = pivot
    return sign * a[-1][-1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', type=Path, help='existing modular verifier executable')
    parser.add_argument('--compiler', default='g++', help='C++17 compiler; default: g++')
    parser.add_argument('--output', type=Path, default=ROOT / 'build' / 'shallit9_crosscheck_result.json')
    args = parser.parse_args()
    if args.binary is None:
        binary = ROOT / 'build' / 'shallit9_modular'
        binary.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([
            args.compiler, '-O3', '-std=c++17',
            str(ROOT / 'src' / 'shallit9_modular.cpp'), '-o', str(binary),
        ], check=True)
    else:
        binary = args.binary.resolve()

    # Deterministic primality certificate for the Mersenne modulus.
    # The exponent 61 is prime; Lucas-Lehmer states 2^61-1 prime iff final s=0.
    assert all(61 % d for d in range(2, 8))
    lucas_lehmer = 4
    for _ in range(59):
        lucas_lehmer = (lucas_lehmer**2 - 2) % P
    assert lucas_lehmer == 0
    length = 64
    output = subprocess.check_output(
        [str(binary), str(length), str(length // 2), "dump"],
        text=True,
    )
    checked = 0
    for line in output.splitlines():
        if not line.startswith("D "):
            continue
        _, order, shift, modular = line.split()
        n, k, residue = int(order), int(shift), int(modular)
        actual = det_bareiss([[at(k + i + j) for j in range(n)] for i in range(n)])
        assert actual != 0, (n, k)
        assert actual % P == residue, (n, k, actual, residue)
        checked += 1
    assert checked == length**2 // 4 + length // 2

    w = [1]
    for _ in range(5):
        w = [v for state in w for v in PHI[state]]
    pairs = set(zip(w, w[1:]))
    assert pairs == {(1,2),(1,4),(2,1),(2,2),(2,3),(3,1),(3,2),(4,1),(4,2)}
    # Every internal/boundary pair of the image remains among these nine.
    for state in range(1, 5):
        assert PHI[state] in pairs
    for u, v in pairs:
        assert (PHI[u][-1], PHI[v][0]) in pairs
    result = {
        "prime": P,
        "lucas_lehmer_verified": True,
        "prefix_length": length,
        "max_order": length // 2,
        "exact_determinants_crosschecked": checked,
        "generator": "DFAO from binary digits",
        "determinant_method": "exact integer Bareiss elimination",
        "comparison": "equals C++ condensation residue modulo prime",
        "adjacent_pairs": sorted("".join(map(str, pair)) for pair in pairs),
        "pair_set_present_in_phi_power": 5,
        "pair_set_closed_under_substitution": True,
    }
    path = args.output
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
