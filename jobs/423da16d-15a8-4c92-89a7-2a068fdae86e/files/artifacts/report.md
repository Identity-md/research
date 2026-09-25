# Euler’s polynomial: correction to the proposed claim

The claim that \(n^2+n+41\) is prime for every natural number \(n\) is **false**, so no valid proof of that claim can be supplied. The following argument can be used directly in the seminar note.

**Proposition.** The polynomial \(f(n)=n^2+n+41\) does not take prime values for every natural number.

**Proof.**

1. Take \(n=40\), which is a natural number whether the convention includes zero or starts at one.
2. Substitution gives
   \[
   f(40)=40^2+40+41=1600+40+41=1681=41\cdot41.
   \]
3. A prime integer greater than one has no positive divisors other than one and itself. Here \(41\) divides \(1681\), and \(1<41<1681\). Thus \(f(40)\) is composite.
4. A statement asserted for every natural number is false if it fails at even one natural number. Hence the proposed claim is false. \(\square\)

The correct finite statement is that \(f(n)\) is prime for every integer \(0\le n\le39\). This is explicitly stated in the published extract of Robert Heffernan, Nick Lord, and Des MacHale, [“Euler’s prime-producing polynomial revisited,” *The Mathematical Gazette* 108 (571), 69–77 (2024)](https://www.cambridge.org/core/journals/mathematical-gazette/article/eulers-primeproducing-polynomial-revisited/1F76183BF30CECE688E31E8F10F37AC8), DOI: 10.1017/mag.2024.11 (accessed 25 September 2026). The finite statement was also checked locally by exact trial division using the accompanying [verification script](verify.py). Together with the displayed factorization, it establishes that 40 is the first nonnegative input giving a composite value.

For completeness, failures occur infinitely often. For every integer \(k\ge1\), direct algebra gives
\[
f(41k)=41(41k^2+k+1).
\]
Both factors exceed one, so each such value is composite. This is an additional deduction, not a computational extrapolation.

**Evidence and limits.** The counterexample and infinite family above are exact mathematical deductions reproduced in full here; neither depends on the external citation. The finite prime range is supported by the cited research article’s extract and the local exhaustive check. Trial division is conclusive because a composite positive integer has a divisor between 2 and its square root: if both factors exceeded the square root, their product would exceed the integer. The script uses integer arithmetic and tests every candidate divisor in that range.

The reported hand checks and supervisor’s acceptance are user-provided context, not independently verified evidence. Checking the first twenty values is consistent with the finite statement, but does not establish a universal assertion. There is no remaining uncertainty about the falsity of the proposed claim. No claim is made here about a classification of all later prime-producing inputs; that question is outside this note. The local check is the authoring agent’s own verification, not an independent review.
