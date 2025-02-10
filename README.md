# AHP-based risk assessment
This repository present a python implementation of the **simplified Analytic Hierarchy Process (AHP)** method named AHP Express, proposed by [^1], which reduces the cognitive bias due to decision-makers by comparing each criteria (or alternative) in a group against only **one reference item** instead of conducting a full pairwise comparison of each item against the others. 

This particular code implementation is oriented toward a **risk assessment context** and concern the comparison of Bloackchain vs. Cloud technologies to manage smart city data; neverthless the code is fully adaptable to any context such that, in example: 

- There are many factors or subfactors to compare, and 
- We aim to compare alternatives under each factor or subfactor,
- A simpler approach is preferred rather than building an $` n \times n `$ comparison matrix at each level.

## 1. Theoretical Background
### 1.1 "Traditional" AHP
The AHP method was prposed by [Saaty] in 1980, it requires pairwise comparisons of every element in a set. This brings to:
- For *n* items, a full pairwise comparison requires $` \frac{n(n-1)}{2} `$ judjements,
- For larger *n* this become so much time-consuming and can introduce biases leading to inconsistencies. 
### 1.2 AHP Express
The AHP Express method helps in avoiding to construct a full $` (n \times n) `$ matrix and computing the following eigenvectors. Instead, a **reference item** is chosed and any other item is compared against it. Here is the core idea: 
- **Pick a reference item R** in each grouop (criteria, sub-criteria, or alternatives).
- For each other item *i* is asked "*How many times more important (or more risky) is i compared to R?*"
  Let this ratio be $` r_{i} `$:
  - if the user says "*i* is 3x more important than R", then  $` r_{i} = 3 `$ 
### 1.3 Reference element vs. Reference alternative 

## 2. Code overview 





# References

[^1]: LEAL, José Eugenio. AHP-express: A simplified version of the analytical hierarchy process method. MethodsX, 2020, 7: 100748.
[Saaty]: SAATY, Roseanna W. The analytic hierarchy process—what it is and how it is used. Mathematical modelling, 1987, 9.3-5: 161-176.
