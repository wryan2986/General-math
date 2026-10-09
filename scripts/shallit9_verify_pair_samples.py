#!/usr/bin/env python3
"""Recheck saved pair-certificate samples by independent rational elimination.

The default input is the archived result under results/shallit9/. New output
defaults to ignored build/, preserving the archived certificate unchanged.
"""
from fractions import Fraction
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def determinant(n, offset, word):
    a = [[Fraction(word[offset + i + j]) for j in range(n)] for i in range(n)]
    result = Fraction(1)
    for k in range(n):
        row = next((j for j in range(k, n) if a[j][k]), None)
        if row is None:
            return 0
        if row != k:
            a[row], a[k] = a[k], a[row]
            result = -result
        pivot = a[k][k]
        result *= pivot
        for i in range(k + 1, n):
            factor = a[i][k] / pivot
            for j in range(k + 1, n):
                a[i][j] -= factor * a[k][j]
    assert result.denominator == 1
    return result.numerator


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', nargs='?', type=Path,
                        default=ROOT / 'results' / 'shallit9' / 'shallit9_pair_certificate_result.json')
    parser.add_argument('--output', type=Path,
                        default=ROOT / 'build' / 'shallit9_pair_certificate_verified.json')
    args = parser.parse_args()
    source = args.source
    result = json.loads(source.read_text())
    rules = {'1': '12', '2': '23', '3': '14', '4': '32'}
    blocks = {}
    for block in result['blocks']:
        word = block['pair']
        for _ in range(result['substitution_depth']):
            word = ''.join(rules[c] for c in word)
        blocks[block['pair']] = [int(c) for c in word]
    for sample in result['direct_check_samples']:
        value = determinant(sample['order'], sample['offset'], blocks[sample['pair']])
        assert value % result['modulus'] == sample['residue'], (sample, value)
    output = {key: value for key, value in result.items() if key != 'direct_check_samples'}
    output['independent_exact_Fraction_elimination_sample_checks'] = len(result['direct_check_samples'])
    output['source_of_samples'] = 'separate exact rational Gaussian elimination, not project Bareiss code'
    destination = args.output
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({'all_samples_match': True, 'count': len(result['direct_check_samples']), 'output': str(destination)}))


if __name__ == '__main__':
    main()
