# AHP-based risk assessment
This repository present a python implementation of the **simplified Analytic Hierarchy Process (AHP)** method named AHP Express, proposed by [^1], which reduces the cognitive bias due to decision-makers by comparing each criteria (or alternative) in a group against only **one reference item** instead of conducting a full pairwise comparison of each item against the others. 

This particular code implementation is oriented toward a **risk assessment context** and concern the comparison of Bloackchain vs. Cloud technologies to manage smart city data; neverthless the code is fully adaptable to any context such that, in example: 

- There are many factors or subfactors to compare, and 
- We aim to compare alternatives under each factor or subfactor,
- A simpler approach is preferred rather than building an $ n \times n $ comparison matrix at each level. 







# References

[^1]: LEAL, José Eugenio. AHP-express: A simplified version of the analytical hierarchy process method. MethodsX, 2020, 7: 100748.
