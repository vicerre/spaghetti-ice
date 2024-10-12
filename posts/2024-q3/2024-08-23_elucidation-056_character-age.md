---
tags:
  - alis
  - constraint programming
  - mathematics
  - operations research
  - solana
  - vicerre
---

# Elucidation 056 – Character Age

Since the onset of their existence, I've left my characters' ages vague. The goal is not to keep their ages a mystery, but instead, out of [The Law of Conservation of Detail](https://tvtropes.org/pmwiki/pmwiki.php/Main/TheLawOfConservationOfDetail).

As my characters developed and I gained better insight into how they functioned, however, the more their ages had to fall within a certain range of constraints. Eventually, these constraints would become rigid enough that, by reasoning alone, these characters must be a certain age.

---

Define the following integer variables representing number of years:

- _A_, _S_, and _V_ as Alis's, Solana's, and Vic's ages, respectively.
- _G_ as the age difference between Alis and Vic.
- _T_ as the time in years since the three met each other.

The constraints are as follows:

| Logic                                                                                                                                                                       | Constraint(s)                        |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| Solana must be mature enough to operate a desk job.                                                                                                                         | 24 ≤ _S_                             |
| Solana must be young enough to retain her youthful spirit.                                                                                                                  | _S_ ≤ 25                             |
| Vic and Alis come from universes years apart in age. By this logic, Vic's and Alis's ages are a fixed number of years apart.                                                | _A_ + _G_ = _V_                      |
| The formative traumas that begat Alis's characterization took place when Alis studied in an esteemed research lab. I can't imagine him in this role before he was eighteen. | 18 + _T_ ≤ _A_                       |
| Vic presents himself as professorial and classical. This would be pretentious if Vic were younger than his mid-20s.                                                         | 25 ≤ _V_                             |
| From their onset, Vic and Alis push the frontiers of science. I can't see them make such advancements earlier than their late teens.                                        | 18 + _T_ ≤ _A_, 18 + _G_ + _T_ ≤ _V_ |
| To ensure romantic compatibility, Solana's and Vic's ages should be within a few years of each other. At most, I think a five-year age gap is appropriate.                  | _V_ − _S_ ≤ 5                        |

Now define the following variable values:

- _G_ as the number 9.
- _T_ as the number 2.

These constraints then simplify to the following:

- 20 ≤ _A_
- 24 ≤ _S_ ≤ 25
- 27 ≤ _V_
- _A_ + 9 = _V_
- _V_ ≤ _S_ + 5

Placing these values into a constraint solver gives us the following integer solutions:

- _A_ = 20, _S_ = 24, _V_ = 29
- _A_ = 20, _S_ = 25, _V_ = 29

From here, we can define Alis's age as 20, Solana's age as 24 or 25, and Vic's age as 29.
