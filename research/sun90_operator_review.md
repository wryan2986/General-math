# Independent review of the Sun $90 operator certificate

Reviewed 2026-10-09 by a separately delegated AI research agent. Scope: `scripts/verify_sun90_operator.py`, including the formal generating-function input, recurrence conversion, right division, and initial-coefficient argument. The verifier was not edited.

**Conclusion: the proof logic is valid. No cancellation, initial-index gap, or unsupported minimality/special-value claim was found.** Running `python General-math/scripts/verify_sun90_operator.py` completed successfully with SymPy 1.14.0 and reproduced the stored certificate.

## Checks of the argument

1. **The generating function supplies the actual formal solution.** Reindexing the defining binomial sum gives
   $$
   B_n=\sum_{j+k=n}\frac{(j+3k)!}{j!k!^3}(-324)^j.
   $$
   Summing first over $j$ gives
   $$
   B(z)=\frac1{1+324z}\sum_{k\ge0}\frac{(3k)!}{k!^3}
   \left(\frac{z}{(1+324z)^3}\right)^k.
   $$
   Every coefficient involves only finitely many $k$, so this is valid in $\mathbb Q[[z]]$, without an analytic convergence assumption. The factorial identity converts this to the stated ${}_2F_1(1/3,2/3;1;\cdot)$. Its coefficient recurrence directly verifies the Gauss equation used by the script.

2. **The pullback chain rule is correct.** For $y(r(z))=h(z)B(z)$, differentiating twice gives exactly the three expressions in `chain`. The divisions by $r'(z)$ are valid formally because $r'(0)=27$. The script verifies all three polynomial ODE coefficients by exact rational simplification. Multiplying the resulting ODE by $z$ and replacing derivatives by $\theta=zD$ also has the correct powers of $z$.

3. **The recurrence transformation has no missing index.** The central-binomial ratio is
   $$
   \frac{\binom{2n}{n}}{\binom{2(n-j)}{n-j}}
   =\prod_{k=0}^{j-1}\frac{2(2n-2k-1)}{n-k}.
   $$
   Here the recurrence length is $d=6$. Denominator clearing is valid for $n\ge6$; the only common factor cancelled afterward is $n-5$, which is nonzero in that range. The script separately checks **all indices $0,1,2,3,4,5$** using the defining integer sums, including the otherwise exceptional index 5. Consequently $L(F)=0$ holds coefficientwise at every index. The substitution `rec[j].subs(n,T+j)` is the correct conversion back to $z^jP_j(\theta)$.

4. **The noncommutative right division uses the correct order.** Conversion from $\theta$-powers to $D$-powers uses Stirling numbers of the second kind. The division loop applies the Leibniz rule to $(fD^s)\circ R$, establishing $L=Q\circ R$, with zero remainder. This is the direction needed for $Q(R(F))=0$.

5. **The final kernel argument closes the logical gap.** Right divisibility alone would not imply $R(F)=0$. The additional checks supply that implication: writing $Q=\sum_{j=0}^3v_j(z)D^j$, each $v_j(z)/z^j$ is regular at zero and its constant term, in increasing $j$, is
   $$
   -24,\quad18,\quad-6,\quad1.
   $$
   Thus the coefficient multiplying the leading term of any nonzero formal series of order $\nu$ is
   $$
   -24+18\nu-6\nu(\nu-1)+\nu(\nu-1)(\nu-2)
   =(\nu-2)(\nu-3)(\nu-4).
   $$
   The first five coefficients of $H=R(F)$ are checked to vanish. If $H\ne0$, its first exponent is an integer $\nu\ge5$, for which this product is nonzero. That contradicts $Q(H)=0$, proving $R(F)=0$.

## Exact scope of the result

The result is a proved fourth-order differential equation for the specified generating function, with reproducible exact symbolic arithmetic. It is not a proof that order four is minimal, not a formal proof-assistant certification, and not a proof of the conjectured value $(357zF'(z)+103F(z))|_{z=1/2160}=90/\pi$. The verifier and its output accurately preserve these limits.
