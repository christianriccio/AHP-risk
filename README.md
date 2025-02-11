# AHP-based risk assessment
This repository present a python implementation of the **simplified Analytic Hierarchy Process (AHP)** method named AHP Express, proposed by [^1], which reduces the cognitive bias due to decision-makers by comparing each criteria (or alternative) in a group against only **one reference item** instead of conducting a full pairwise comparison of each item against the others. 

This particular code implementation is oriented toward a **risk assessment context** and concern the comparison of Bloackchain vs. Cloud technologies to manage smart city data; neverthless the code is fully adaptable to any context such that, in example: 

- There are many factors or subfactors to compare, and 
- We aim to compare alternatives under each factor or subfactor,
- A simpler approach is preferred rather than building an $` n \times n `$ comparison matrix at each level.

## 1. Theoretical Background
### 1.1 "Traditional" AHP
The AHP method was prposed by [^2] in 1980, it requires pairwise comparisons of every element in a set. This brings to:
- For *n* items, a full pairwise comparison requires $` \frac{n(n-1)}{2} `$ judjements,
- For larger *n* this become so much time-consuming and can introduce biases leading to inconsistencies. 
### 1.2 AHP Express
The AHP Express method helps in avoiding to construct a full $` (n \times n) `$ matrix and computing the following eigenvectors. Instead, a **reference item** is chosed and any other item is compared against it. Here is the core idea: 
1. **Pick a reference item R** in each grouop (criteria, sub-criteria, or alternatives).
2. For each other item *i* is asked "*How many times more important (or more risky) is i compared to R?*"
  Let this ratio be $` r_{i} `$:
  - if the user says "*i* is 3x more important than R", then  $` r_{i} = 3 `$
  - if the user says "R is 2x more important than *i*", then this implies $` r_{i} = 1/2 `$
3. The reference has unnormalized wight of $` w_{R} = 1 `$
4. The unnormalized weight of each item *i* is $` w_{i} = r_{i} `$
5. The we normalize all the weights so they sum to 1
6. This normalized weight are used instead of the principal eigenvector typically computed in the standard AHP

This process lead to a number of comparisons of $` n-1 `$ judjements. In suach a case there is no need for consistency ratio checks, in fact inconsistency occurs mainly if evaluations are made between alternatives of seemingly minor importance to the decsionmaker. 


### 1.3 Reference element vs. Reference alternative 
The concept of **reference element** is applied at multiple levels: 
- Top-level factors: one factor is chosed as reference factor and all the other factors are compared to it 
- Subfactors: for each factor, one subfactor is picked as reference and all the other subfactors are compared to it
- Alternatives: for each subfactor (or factor, if no subfactor exsist), one alternative is picked as reference and the other alternative(s) is compared to it.


## 2. Code overview 
The code is an interactive web-based application implemented in [Streamlit](https://streamlit.io).
### 2.1 Structure of the code
+ Functions:
  
+ Main App:
  

## 3. Results Interpretation
Each alternative gets a final score, representing a *risk score*; in a risk assessment context a a higher score might mean hogher risk, so one pick the alternative with a lower risk.  
## 4. How to use this app 

You have to ways to use the app: 
-  At the following [link] (), or
-   Following this steps:
   1. Install dependencies:
     * Python 3.8+
     * Streamlit
     * matplotlib
     * Numpy
     * graphviz
  ```console
      pip install streamlit graphviz matplotlib numpy
  ```
  2. save the script as you wish (in example app.py)
  3. run the script:
  ```console
      streamlit run app.py
  ```
  4. Intertact with the app in the browser:
     * Enter the decision objective
     * Provide the ALternatives
     * Provide the Top-level factors
     * if any, provide subfactors under each factor
     * Generate the Hieararchy Diagram to quicly inspect the structure of the decsion problem
     * AHP express will compute the weights at each level (by choosing the corresponding refrence element)
     * Calculate the Final Scores by clicking the button and get a bar chart

### Acknowledgments
> [!NOTE]
> Feel free to use (or modify) the code as long as you mention the repository and who implemented it, for further details contact at the following email christian.riccio@unicampania.it

## References 

[^1]: LEAL, José Eugenio. AHP-express: A simplified version of the analytical hierarchy process method. MethodsX, 2020, 7: 100748.
[^2]: SAATY, Roseanna W. The analytic hierarchy process—what it is and how it is used. Mathematical modelling, 1987, 9.3-5: 161-176.



