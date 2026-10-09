// Independent exact finite-field check for the Shallit-9 pair-block certificate.
// No project implementation is imported. Build with g++ -O3 -std=c++17.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using U = std::uint64_t;
constexpr U P = 2147483647ULL;  // Primality checked below by trial division.

U mul(U a, U b) {
    U c = a * b; // a,b<P: product is strictly below 2^62.
    c = (c & P) + (c >> 31);
    c = (c & P) + (c >> 31);
    return c >= P ? c - P : c;
}

U power(U x, U n) {
    U r = 1;
    while (n) {
        if (n & 1) r = mul(r, x);
        x = mul(x, x);
        n >>= 1;
    }
    return r;
}

bool prime_by_trial_division(U n) {
    if (n < 2) return false;
    for (U d = 2; d * d <= n; ++d) if (n % d == 0) return false;
    return true;
}

std::vector<U> expand(std::string pair, int depth) {
    for (int i = 0; i < depth; ++i) {
        std::string next;
        next.reserve(pair.size() * 2);
        for (char c : pair) {
            switch (c) {
            case '1': next += "12"; break;
            case '2': next += "23"; break;
            case '3': next += "14"; break;
            case '4': next += "32"; break;
            default: throw std::runtime_error("bad alphabet");
            }
        }
        pair.swap(next);
    }
    std::vector<U> result;
    for (char c : pair) result.push_back(c - '0');
    return result;
}

struct Sample { std::string pair; int order; int offset; U residue; };

int main(int argc, char** argv) {
    int depth = argc > 1 ? std::atoi(argv[1]) : 12;
    if (depth < 1 || depth > 16) return 3;
    if (!prime_by_trial_division(P)) return 4;
    const int bound = (1 << (depth - 1)) + 1;
    const std::vector<std::string> pairs = {"12", "14", "21", "22", "23", "31", "32", "41", "42"};
    std::vector<Sample> samples;
    U checks = 0, fingerprint = 0;
    std::cout << "{\n  \"modulus\": " << P << ",\n  \"primality\": \"trial division all d through floor(sqrt(p))\",\n"
              << "  \"substitution_depth\": " << depth << ",\n  \"max_order\": " << bound << ",\n  \"blocks\": [\n";
    bool firstblock = true;
    for (const std::string& pair : pairs) {
        std::vector<U> prev = expand(pair, depth);
        const int N = prev.size();
        std::vector<U> older(N + 2, 1);
        U blockchecks = 0;
        for (int order = 1; order <= bound; ++order) {
            if (order > 1) {
                const int L = N - 2 * order + 2;
                std::vector<U> prefix(L + 1, 1), now(L);
                for (int i = 0; i < L; ++i) {
                    if (older[i + 2] == 0) throw std::runtime_error("zero condensation denominator");
                    prefix[i + 1] = mul(prefix[i], older[i + 2]);
                }
                U inverse_product = power(prefix[L], P - 2);
                for (int i = L - 1; i >= 0; --i) {
                    const U denominator_inverse = mul(inverse_product, prefix[i]);
                    inverse_product = mul(inverse_product, older[i + 2]);
                    U numerator = mul(prev[i], prev[i + 2]) + P - mul(prev[i + 1], prev[i + 1]);
                    if (numerator >= P) numerator -= P;
                    now[i] = mul(numerator, denominator_inverse);
                }
                older.swap(prev);
                prev.swap(now);
            }
            for (int offset = 0; offset < (int)prev.size(); ++offset) {
                U residue = prev[offset];
                ++checks;
                ++blockchecks;
                if (residue == 0) {
                    std::cerr << "MODULAR ZERO (not integer singularity): pair=" << pair
                              << " order=" << order << " offset=" << offset << "\n";
                    return 2;
                }
                fingerprint = (mul(fingerprint, 1000003) + residue) % P;
                if (order <= 8 && (offset == 0 || offset == 1 || offset == 17 || offset == N / 2))
                    samples.push_back({pair, order, offset, residue});
            }
        }
        if (!firstblock) std::cout << ",\n";
        firstblock = false;
        std::cout << "    {\"pair\": \"" << pair << "\", \"length\": " << N
                  << ", \"determinants_checked\": " << blockchecks << ", \"all_nonzero\": true}";
    }
    std::cout << "\n  ],\n  \"total_checked_including_duplicates\": " << checks
              << ",\n  \"all_nonzero\": true,\n  \"recurrence\": \"Desnanot-Jacobi with nonzero denominators and batch inverses\",\n"
              << "  \"fingerprint_mod_p\": " << fingerprint << ",\n  \"direct_check_samples\": [\n";
    bool firstsample = true;
    for (const auto& s : samples) {
        if (!firstsample) std::cout << ",\n";
        firstsample = false;
        std::cout << "    {\"pair\": \"" << s.pair << "\", \"order\": " << s.order
                  << ", \"offset\": " << s.offset << ", \"residue\": " << s.residue << "}";
    }
    std::cout << "\n  ]\n}\n";
}
