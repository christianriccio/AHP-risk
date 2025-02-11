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
  - **`normalize_weights()`**: this function divides each weight by the total sum so they sum up to 1
  - **`plot_bar_chart()`** and **`plot_final_scores_bar_chart()`**: functions for bar chart plot
  - **`compare_item_against_reference()`**: encapsulate the streamlit buttons and sliders and perform the comparison of one item with the chosen reference
  - **`compute_comparison_weights()`**: use the comparison function to generate unnormalized weights for an entire list of items, relative to a single reference element
  
+ Main App: main application is dived in steps.
  1. **Step 1**: Define the Overall Objective
  2. **Step 2**: define the alternatives
  3. **Step 3**: define the top-level factors
  4. **Step 4**: for each factor, define zero or more subfactors
  5. **Step 5**: generate a hearchy diagram using **Graphviz** module
  6. **Step 6**: Compare top-level factors using AHP express
     + a reference factor is picked, set the weight to 1, and compare each other factor to it
     + normalize and store the results in `st.session_state["factor_weights"]` in order to not lose ttrack of the weights every time a button is clicked
  7. **Step 7**: compare this time the subfactor, in the same manner (if there is any)
     + store the results in `st.session_state[""subfactor_weight_dict]`
  8. **Step 8**: for each subfactor, compare the alternatives with AHP express
     + store results in `st.session_state["alt_weights_by_subfactor"]`
  9. **Step 9**: compute the final scores for each alternative by multiplying the factor weights x subfactor weights x alternatie weights 

## 2.2 Navigating in the code 
### 2.2.1 Imports and Session State
```python
import streamlit as st
import graphviz
import matplotlib.pyplot as plt
import io

if "alt_weights_by_subfactor" not in st.session_state:
    st.session_state["alt_weights_by_subfactor"] = {}
if "subfactor_weight_dict" not in st.session_state:
    st.session_state["subfactor_weight_dict"] = {}
```
+ I make ssure that `alt_weights_by_subfactor` and `subfactr_weight_dict` are in the `session_state` so the user's entries are stored across different button clicks
  
### 2.2.2 Functions 
```python
def normalize_weights(weight_dict):
    """function to normalize a dictionary og weights to sum them to 1"""
    total = sum(weight_dict.values())
    return {k: v / total for k, v in weight_dict.items()} if total != 0 else {k: 0 for k in weight_dict}

def plot_bar_chart(title, data, y_label):
    fig, ax = plt.subplots()
    ax.bar(list(data.keys()), list(data.values()), color="skyblue")
    ax.set_ylabel(y_label)
    ax.set_title(title)
    plt.xticks(rotation=45)
    st.pyplot(fig)

def plot_final_scores_bar_chart(title, data):
    fig, ax = plt.subplots()
    ax.bar(list(data.keys()), list(data.values()), color=["orange", "green"])
    ax.set_ylabel("Overall Score")
    ax.set_title(title)
    plt.xticks(rotation=0)
    st.pyplot(fig)
```
- `normalize_weights()` sum all unnormalized weights and divides each weight by that sum, so the tolal is 1 
- functions to plot bar charts

```python
def compare_item_against_reference(item,reference,slider_label="Magnitude (1=equal, up to 9)",radio_question="Which is bigger?",radio_options=None,slider_default=1,radio_key="",slider_key=""):
    """
    this function implement the comparison of one item against a reference using a radio and slider input.
    Returns a weight based on the comparison.
    """
    if radio_options is None:
        radio_options = [f"{item} is bigger", "Equal", f"{reference} is bigger"]
    side = st.radio(radio_question, options=radio_options, index=1, key=radio_key)
    slider_value = st.slider(slider_label, 1, 9, slider_default, 1, key=slider_key)
    if side == "Equal" or slider_value == 1:
        return 1.0
    elif side.startswith(item):
        return float(slider_value)
    else:
        return 1.0 / float(slider_value)
```
- this function implemente the streamlit components (radio, slider) to get a single ratio for item vs. reference

```python
def compute_comparison_weights(items, reference, key_prefix, radio_question="Which is bigger?"):
    """
    compute the unnormalized weights based on user comparisons
    """
    weights = {reference: 1.0}
    for item in items:
        if item == reference:
            continue
        radio_key = f"{key_prefix}_radio_{item}"
        slider_key = f"{key_prefix}_slider_{item}"
        weight = compare_item_against_reference(
            item,
            reference,
            radio_question=radio_question,
            radio_key=radio_key,
            slider_key=slider_key
        )
        weights[item] = weight
    return weights
```
- this function, for each group, the reference is picked and unnormalized weights for the rest
### 2.2.3 Main app flow 
```python
def main():
    st.title("AHP-based risk assessment using the Express impelementation")
...
```
-------
#### Step 1&2: Objective and Alternatives
```python
# --- Step 1
    st.header("Step 1: Define Objective")
    default_objective = "Select the architecture (Blockchain vs. Cloud) with the lowest overall risk."
    objective = st.text_input("Overall Objective:", value=default_objective)

# --- Step 2
    st.header("Step 2: Alternatives")
    st.markdown("We'll compare two main alternatives by default: **Blockchain** and **Cloud**.")
    alt_text = st.text_area("List alternatives (one per line):", value="Blockchain\nCloud")
    alternatives_list = [a.strip() for a in alt_text.splitlines() if a.strip()]
    st.write("**Your alternatives are:**", alternatives_list)
```
By default two alternatives are assumed, that are for the purpose of the paper, comparing the risk of "Cloud" vs. "Blockchain" technologies. 

#### Step 3: Top-level factors
```python
 default_factors = "Human Factor\nLocal Infrastructure Factor\nPublic Infrastructure Factor"
    factor_text = st.text_area("Enter top-level factors (one per line):", value=default_factors)
    factors_list = [f.strip() for f in factor_text.splitlines() if f.strip()]
```
- by default 3 main factors are presented, but they caan be changed as well.

#### Step 4: Subfactors
```python
 subfactor_dict = {}
    for factor in factors_list:
        default_subs = ""
        if factor.lower().startswith("human"):
            default_subs = "Data Protection Violation\nData Modification Violation\nHuman Error"
        ....
        subs = st.text_area(
            f"Subfactors for '{factor}': (one per line) - optional",
            value=default_subs,
            key=f"subfactors_{factor}"
        )
        subfactors = [s.strip() for s in subs.splitlines() if s.strip()]
        subfactor_dict[factor] = subfactors
```
- for each factor, subfactor can be defined, if there is any otherwise None.

#### Step 5: Hierarchy Diagram 
```python
    if st.button("Generate Hierarchy Diagram"):
        dot = graphviz.Digraph()
        dot.node("Objective", objective)
        for factor in factors_list:
            dot.node(factor, factor)
            dot.edge("Objective", factor)
            sf_list = subfactor_dict.get(factor, [])
            if not sf_list:
                # If no subfactors => direct link factor -> alt
               
            else:
                # factor -> subfactor -> alt
        st.graphviz_chart(dot)
```
- here the hierarchy diagram is drawn

#### Step 6: AHP Express top-level factors 

```python
if len(factors_list) > 1:
    ref_factor = st.selectbox("Choose reference factor:", factors_list)
    factor_weights_raw = compute_comparison_weights(
        factors_list,
        ref_factor,
        key_prefix="factor",
        radio_question="Which factor is more important/riskier?"
    )
    if st.button("Compute Factor Weights"):
        norm_factor_weights = normalize_weights(factor_weights_raw)
        st.session_state["factor_weights"] = norm_factor_weights
        ...
```
- one reference factor is picked and gets unnormalized weight = 1.0
- each other factor is compared to it
- results are ten normalized and stored

#### Step 7: AHP Express for subfactors 

```python
for factor in factors_list:
    sf_list = subfactor_dict.get(factor, [])
    if len(sf_list) <= 1:
        # if there is 0 or 1 subfactor, default weights is set
        subfactor_weight_dict[factor] = ...
        continue

    # for more than 1 subfactor:
    ref_sf = st.selectbox(f"Reference subfactor under '{factor}'", sf_list)
    sf_weights_raw = compute_comparison_weights(...)
    if st.button(...):
        norm_sf_weights = normalize_weights(sf_weights_raw)
        st.session_state["subfactor_weight_dict"][factor] = norm_sf_weights
        ...

```
#### Step 8: Compare ALternative for each subfactor

```python
for factor in factors_list:
    sf_list = subfactor_dict.get(factor, [])
    if not sf_list:
        sf_list = [factor]  # If no subfactors, the factor itself is the "subfactor"
    for sf in sf_list:
        #  user pick a reference alternative:
        ref_alt = st.selectbox(f"Reference alternative for '{sf}'", alternatives_list)
        alt_weights_raw = compute_comparison_weights(alternatives_list, ref_alt, key_prefix=f"alt_{sf}")
        if st.button(f"Compute Alt Weights for '{sf}'"):
            norm_alt_weights = normalize_weights(alt_weights_raw)
            st.session_state["alt_weights_by_subfactor"][sf] = norm_alt_weights
            ...
```
- reference alternative is picked and the other is compared to it
- ratio is stored
- normalization across alternatives is done

#### Step 9: Final scores calculation 
```python
if st.button("Calculate Final Scores (AHP Express)"):
    factor_weights = st.session_state["factor_weights"]
    subfactor_weight_dict = st.session_state.get("subfactor_weight_dict", {})
    alt_weights_by_subfactor = st.session_state.get("alt_weights_by_subfactor", {})

    final_scores = {alt: 0.0 for alt in alternatives_list}
    for factor in factors_list:
        f_weight = factor_weights.get(factor, 0.0)
        sf_list = subfactor_dict.get(factor, [])
        if not sf_list:
            sub_weights = {factor: 1.0}
        else:
            sub_weights = subfactor_weight_dict.get(factor, {})
            ...

        for sf, sf_weight in sub_weights.items():
            alt_w = alt_weights_by_subfactor.get(sf, ...)
            for alt in alternatives_list:
                final_scores[alt] += f_weight * sf_weight * alt_w[alt]

    
    st.write("Final Scores for Each Alternative (Lower = Better)")
    for alt, score in final_scores.items():
        st.write(f"- {alt}: {score:.4f}")
    plot_final_scores_bar_chart("Final AHP-Express Scores", final_scores)

```
- final result is displayed in a bar chart and made available for CSV download


## 3. Results Interpretation
Each alternative gets a final score, representing a *risk score*; in a risk assessment context a a higher score might mean hogher risk, so one pick the alternative with a lower risk.  
## 4. How to use this app 

You have to ways to use the app: 
-  At the following [link](https://ahp-risk.streamlit.app/), or
-   Following this steps:
   1. Install dependencies:
    + Python 3.8+
    + Streamlit
    + matplotlib
    + graphviz
  ```console
  pip install streamlit graphviz matplotlib
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



