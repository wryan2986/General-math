"""Exact definitions and independent finite checks for Shallit's Problem 9.

Only Python's standard library is required. Indices are zero based.
"""
from __future__ import annotations

MORPHISM = {1: (1, 2), 2: (2, 3), 3: (1, 4), 4: (3, 2)}


def morph(word: bytes) -> bytes:
    return bytes(y for x in word for y in MORPHISM[x])


def prefix(length: int) -> bytes:
    if length < 0:
        raise ValueError("negative length")
    word = bytes([1])
    while len(word) < length:
        word = morph(word)
    return word[:length]


def term(index: int) -> int:
    """A separate DFA evaluation, reading the binary expansion MSB first."""
    if index < 0:
        raise ValueError("negative index")
    state = 1
    for bit in bin(index)[2:]:
        state = MORPHISM[state][int(bit)]
    return state


def hankel(word: bytes, order: int, offset: int = 0) -> list[list[int]]:
    if order < 1 or offset < 0 or offset + 2 * order - 1 > len(word):
        raise ValueError("matrix not contained in supplied word")
    return [[word[offset + i + j] for j in range(order)] for i in range(order)]


def det_bareiss(matrix: list[list[int]]) -> int:
    """Fraction-free integer elimination, with row pivots and checked divisions."""
    a = [row[:] for row in matrix]
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError("not square")
    if n == 0:
        return 1
    sign = 1
    divisor = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            r = next((r for r in range(k + 1, n) if a[r][k]), None)
            if r is None:
                return 0
            a[k], a[r] = a[r], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                value, remainder = divmod(numerator, divisor)
                if remainder:
                    raise ArithmeticError("Bareiss division was not exact")
                a[i][j] = value
            a[i][k] = 0
        divisor = pivot
    return sign * a[-1][-1]


def det_mod(matrix: list[list[int]], prime: int) -> int:
    """Direct finite-field Gaussian elimination (independent of condensation)."""
    a = [[x % prime for x in row] for row in matrix]
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError("not square")
    result = 1
    for k in range(n):
        r = next((r for r in range(k, n) if a[r][k]), None)
        if r is None:
            return 0
        if r != k:
            a[k], a[r] = a[r], a[k]
            result = -result
        pivot = a[k][k]
        result = result * pivot % prime
        inv = pow(pivot, -1, prime)
        for i in range(k + 1, n):
            q = a[i][k] * inv % prime
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] - q * a[k][j]) % prime
    return result % prime


class SuffixAutomaton:
    """Exact substring recognizer. No hashing or probabilistic comparison."""
    def __init__(self, word: bytes):
        self.next: list[dict[int, int]] = [{}]
        self.link = [-1]
        self.length = [0]
        last = 0
        for letter in word:
            cur = len(self.next)
            self.next.append({})
            self.length.append(self.length[last] + 1)
            self.link.append(0)
            p = last
            while p >= 0 and letter not in self.next[p]:
                self.next[p][letter] = cur
                p = self.link[p]
            if p == -1:
                self.link[cur] = 0
            else:
                q = self.next[p][letter]
                if self.length[p] + 1 == self.length[q]:
                    self.link[cur] = q
                else:
                    clone = len(self.next)
                    self.next.append(self.next[q].copy())
                    self.length.append(self.length[p] + 1)
                    self.link.append(self.link[q])
                    while p >= 0 and self.next[p].get(letter) == q:
                        self.next[p][letter] = clone
                        p = self.link[p]
                    self.link[q] = self.link[cur] = clone
            last = cur

    def shortest_absent_factor(self, other: bytes) -> dict | None:
        state, matched = 0, 0
        best = None
        for end, letter in enumerate(other):
            while state and letter not in self.next[state]:
                state = self.link[state]
                matched = self.length[state]
            if letter in self.next[state]:
                state = self.next[state][letter]
                matched += 1
            else:
                state, matched = 0, 0
            # Suffixes through length 'matched' occur; the next longer does not.
            if matched < end + 1:
                size = matched + 1
                if best is None or size < best["length"]:
                    best = {"length": size, "offset": end + 1 - size}
        return best


def factor_closure(iterations: int) -> dict:
    """Find largest m such that F_m(phi^t(1))=F_m(phi^(t+1)(1)).

    See research/shallit9.md for the all-shifts implication.
    This function checks factor coverage, not determinants.
    """
    if iterations < 1:
        raise ValueError("use at least one iteration")
    w = prefix(1 << iterations)
    v = morph(w)
    absent = SuffixAutomaton(w).shortest_absent_factor(v)
    largest = len(w) if absent is None else absent["length"] - 1
    return {
        "iterations": iterations,
        "prefix_length": len(w),
        "extension_length": len(v),
        "all_factor_lengths_through": largest,
        "all_shifts_hankel_order_through_if_prefix_passes": (largest + 1) // 2,
        "first_absent_factor": absent,
        "comparison": "exact suffix automaton, no hashes",
    }

