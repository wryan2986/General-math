#!/usr/bin/env python3
"""Independent Shallit-9 language check via suffix array and Kasai LCP.

Does not import any project code or use its suffix automaton.
New output defaults to ignored build/, preserving the archived result.
"""
import argparse
import json
from pathlib import Path
import time

RULES = ('12', '23', '14', '32')
ROOT = Path(__file__).resolve().parents[1]


def substitute(text):
    return ''.join(RULES[ord(c) - ord('1')] for c in text)


def suffix_array(data):
    n = len(data)
    order = sorted(range(n), key=data.__getitem__)
    rank = [0] * n
    classes = 0
    for k, index in enumerate(order):
        if k and data[index] != data[order[k - 1]]:
            classes += 1
        rank[index] = classes
    step = 1
    while classes + 1 < n:
        order.sort(key=lambda i: (rank[i], rank[i + step] if i + step < n else -1))
        newrank = [0] * n
        classes = 0
        previous = None
        for index in order:
            key = rank[index], rank[index + step] if index + step < n else -1
            if previous is not None and key != previous:
                classes += 1
            newrank[index] = classes
            previous = key
        rank = newrank
        step *= 2
    return order


def kasai(data, order):
    n = len(data)
    position = [0] * n
    for i, suffix in enumerate(order):
        position[suffix] = i
    lcp = [0] * n
    matched = 0
    for start in range(n):
        i = position[start]
        if i == 0:
            matched = 0
            continue
        other = order[i - 1]
        while start + matched < n and other + matched < n and data[start + matched] == data[other + matched]:
            matched += 1
        lcp[i] = matched
        if matched:
            matched -= 1
    return lcp


def first_missing_length(source, extension):
    # Separators are distinct and absent from the alphabet, preventing matches
    # across either finite-word end.
    data = source + '0' + extension + '5'
    order = suffix_array(data)
    lcp = kasai(data, order)
    source_len = len(source)
    extension_begin = source_len + 1
    extension_end = extension_begin + len(extension)
    longest = [0] * len(data)
    # The closest source suffix to the left/right maximizes LCP among source
    # suffixes on that side; intervening LCP minima give its exact LCP.
    running = None
    for i, start in enumerate(order):
        if start < source_len:
            running = len(data)
        elif running is not None:
            running = min(running, lcp[i])
            longest[start] = running
    running = None
    for i in range(len(order) - 1, -1, -1):
        start = order[i]
        if start < source_len:
            running = len(data)
        elif running is not None:
            running = min(running, lcp[i + 1])
            longest[start] = max(longest[start], running)
    missing = []
    for start in range(extension_begin, extension_end):
        size = longest[start] + 1
        if start + size <= extension_end:
            missing.append((size, start - extension_begin))
    if not missing:
        return None
    size, offset = min(missing)
    assert extension[offset:offset + size] not in source
    assert size == 1 or extension[offset:offset + size - 1] in source
    return {'length': size, 'offset': offset}


def small_exhaustive_checks():
    import random
    rng = random.Random(90261009)
    for _ in range(100):
        source = ''.join(rng.choice('1234') for _ in range(rng.randint(1, 50)))
        extension = ''.join(rng.choice('1234') for _ in range(rng.randint(1, 80)))
        got = first_missing_length(source, extension)
        expected = None
        for size in range(1, len(extension) + 1):
            offsets = [i for i in range(len(extension) - size + 1) if extension[i:i + size] not in source]
            if offsets:
                expected = {'length': size, 'offset': min(offsets)}
                break
        assert got == expected, (source, extension, got, expected)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--iterations', type=int, default=15)
    p.add_argument('--output', type=Path, default=ROOT / 'build' / 'shallit9_independent_factor_result.json')
    args = p.parse_args()
    started = time.time()
    small_exhaustive_checks()
    word = '1'
    history = []
    for iteration in range(args.iterations + 1):
        pairs = sorted({word[i:i+2] for i in range(len(word)-1)})
        if iteration <= 6:
            history.append({'iteration': iteration, 'length': len(word),
                            'pair_first_occurrences': {pair: word.find(pair) for pair in pairs}})
        if iteration < args.iterations:
            word = substitute(word)
    extension = substitute(word)
    first_absent = first_missing_length(word, extension)
    coverage = first_absent['length'] - 1 if first_absent else len(word)
    result = {'iterations': args.iterations, 'prefix_length': len(word),
              'extension_length': len(extension), 'first_absent_factor': first_absent,
              'all_factor_lengths_through': coverage,
              'all_shifts_orders_through_if_all_prefix_determinants_pass': (coverage + 1) // 2,
              'method': 'independent suffix array doubling; Kasai LCP; nearest source suffix passes',
              'independent_small_random_factor_checks': 100,
              'pair_history': history, 'elapsed_seconds': time.time() - started}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'pair_history'}, indent=2))


if __name__ == '__main__':
    main()
