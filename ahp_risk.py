import streamlit as st
import graphviz
import matplotlib.pyplot as plt
import io


if "alt_weights_by_subfactor" not in st.session_state:
    st.session_state["alt_weights_by_subfactor"] = {}
if "subfactor_weight_dict" not in st.session_state:
    st.session_state["subfactor_weight_dict"] = {}

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

# App

def main():
    st.title("AHP-based risk assessment using the Express impelementation")
    st.markdown(
        """
        This tool implements a simplified version of AHP (AHP Express) where each set of elements is compared
        only to a **reference element**, reducing the number of pairwise comparisons.
        """
    )

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

    # --- Step 3
    st.header("Step 3: Define Top-level Risk/Decision Factors")
    default_factors = "Human Factor\nLocal Infrastructure Factor\nPublic Infrastructure Factor"
    factor_text = st.text_area("Enter top-level factors (one per line):", value=default_factors)
    factors_list = [f.strip() for f in factor_text.splitlines() if f.strip()]
    st.write("**Top-level factors:**", factors_list)

    # --- Step 4
    st.header("Step 4: Define Subfactors Under Each Factor (If Any)")
    st.markdown(
        "For each factor, specify zero or more subfactors. "
        "If a factor has no subfactors, the factor itself is used directly when scoring alternatives."
    )
    subfactor_dict = {}
    for factor in factors_list:
        default_subs = ""
        if factor.lower().startswith("human"):
            default_subs = "Data Protection Violation\nData Modification Violation\nHuman Error"
        elif factor.lower().startswith("local"):
            default_subs = "Equipment Failure\nSecurity Breach"
        elif factor.lower().startswith("public"):
            default_subs = "Power Failure\nNetwork Malfunctioning\nBase Software & Middleware Vulnerability"

        subs = st.text_area(
            f"Subfactors for '{factor}': (one per line) - optional",
            value=default_subs,
            key=f"subfactors_{factor}"
        )
        subfactors = [s.strip() for s in subs.splitlines() if s.strip()]
        subfactor_dict[factor] = subfactors

    # --- Step 5
    st.header("Step 5: Hierarchy Diagram")
    if st.button("Generate Hierarchy Diagram"):
        dot = graphviz.Digraph()
        dot.node("Objective", objective)
        for factor in factors_list:
            dot.node(factor, factor)
            dot.edge("Objective", factor)
            sf_list = subfactor_dict.get(factor, [])
            if not sf_list:
                # If no subfactors, attach alternatives directly
                for alt in alternatives_list:
                    alt_node = f"{factor}_{alt}"
                    dot.node(alt_node, alt)
                    dot.edge(factor, alt_node)
            else:
                for sf in sf_list:
                    # Create a unique node id for subfactors
                    sf_node = f"{factor}_{sf}"
                    dot.node(sf_node, sf)
                    dot.edge(factor, sf_node)
                    for alt in alternatives_list:
                        alt_node = f"{sf_node}_{alt}"
                        dot.node(alt_node, alt)
                        dot.edge(sf_node, alt_node)
        st.graphviz_chart(dot)

    # --- Step 6
    st.header("Step 6: AHP Express for Top-level Factors")
    if len(factors_list) > 1:
        ref_factor = st.selectbox("Choose reference factor:", factors_list, key="ref_factor")
        st.info(f"Reference factor '{ref_factor}' is automatically assigned a weight of 1.0 (before normalization).")
        factor_weights_raw = compute_comparison_weights(
            factors_list,
            ref_factor,
            key_prefix="factor",
            radio_question="Which factor is more important/riskier?"
        )
        if st.button("Compute Factor Weights"):
            norm_factor_weights = normalize_weights(factor_weights_raw)
            st.write("**Unnormalized factor weights:**", factor_weights_raw)
            st.write("**Normalized factor weights:**", norm_factor_weights)
            plot_bar_chart("Top-level Factor Weights (AHP Express)", norm_factor_weights, "Weight")
            buf = io.StringIO()
            buf.write("Factor,Weight\n")
            for fct, w in norm_factor_weights.items():
                buf.write(f"{fct},{w:.4f}\n")
            st.download_button("Download Top-level Factor Weights (CSV)", data=buf.getvalue(), file_name="factor_weights.csv", mime="text/csv")
            st.session_state["factor_weights"] = norm_factor_weights
    else:
        st.info("Only one factor provided. Assigning weight 1.0 by default.")
        if factors_list:
            st.session_state["factor_weights"] = {factors_list[0]: 1.0}

    # --- Step 7
    st.header("Step 7: AHP Express for Subfactors")
    subfactor_weight_dict = {}  # dictionary to hold subfactor weights for each factor
    for factor in factors_list:
        sf_list = subfactor_dict.get(factor, [])
        if len(sf_list) <= 1:
            # for no subfactors or a single subfactor, assign default weight
            subfactor_weight_dict[factor] = {sf_list[0]: 1.0} if sf_list else {}
            continue
        st.subheader(f"Subfactor Weights for '{factor}'")
        ref_sf = st.selectbox(f"Reference subfactor under '{factor}'", sf_list, key=f"ref_sf_{factor}")
        sf_weights_raw = compute_comparison_weights(
            sf_list,
            ref_sf,
            key_prefix=f"sf_{factor}",
            radio_question="Which subfactor is more important/riskier?"
        )
        if st.button(f"Compute Subfactor Weights for '{factor}'", key=f"compute_sf_{factor}"):
            norm_sf_weights = normalize_weights(sf_weights_raw)
            st.session_state["subfactor_weight_dict"][factor] = norm_sf_weights
            st.write("**Unnormalized Subfactor Weights:**", sf_weights_raw)
            st.write("**Normalized Subfactor Weights:**", norm_sf_weights)
            plot_bar_chart(f"Subfactor Weights under '{factor}'", norm_sf_weights, "Weight")
            buf_sf = io.StringIO()
            buf_sf.write("Subfactor,Weight\n")
            for subf, w in norm_sf_weights.items():
                buf_sf.write(f"{subf},{w:.4f}\n")
            st.download_button(
                f"Download Subfactor Weights for {factor}",
                data=buf_sf.getvalue(),
                file_name=f"subfactor_weights_{factor}.csv",
                mime="text/csv"
            )

    # --- Step 8
    st.header("Step 8: Compare Alternatives for Each Subfactor (or Factor if no subfactors)")
    alt_weights_by_subfactor = {}
    if len(alternatives_list) < 2:
        st.warning("At least 2 alternatives are required for pairwise comparisons.")
    else:
        # Iterate over each factor and its subfactors 
        for factor in factors_list:
            sf_list = subfactor_dict.get(factor, [])
            if not sf_list:
                sf_list = [factor]
            for sf in sf_list:
                st.subheader(f"Alternative Weights for '{sf}'")
                ref_alt = st.selectbox(f"Reference alternative for '{sf}'", alternatives_list, key=f"ref_alt_{factor}_{sf}")
                alt_weights_raw = compute_comparison_weights(
                    alternatives_list,
                    ref_alt,
                    key_prefix=f"alt_{sf}",
                    radio_question="Which alternative is more risky/critical?"
                )
                if st.button(f"Compute Alt Weights for '{sf}'", key=f"compute_alt_{sf}"):
                    norm_alt_weights = normalize_weights(alt_weights_raw)
                    st.session_state["alt_weights_by_subfactor"][sf] = norm_alt_weights
                    st.write("**Unnormalized Alternative Weights:**", alt_weights_raw)
                    st.write("**Normalized Alternative Weights:**", norm_alt_weights)
                    plot_bar_chart(f"Alternative Weights under '{sf}'", norm_alt_weights, "Weight")

    # --- Step 9
    st.header("Step 9: Compute Final Overall Scores")
    if st.button("Calculate Final Scores (AHP Express)"):
        if "factor_weights" not in st.session_state:
            st.error("You must compute top-level factor weights first (Step 6).")
        else:
            final_scores = {alt: 0.0 for alt in alternatives_list}
            factor_weights = st.session_state["factor_weights"]
            subfactor_weight_dict = st.session_state.get("subfactor_weight_dict", {})
            alt_weights_by_subfactor = st.session_state.get("alt_weights_by_subfactor", {})

            # For each factor, determine subfactor weights and use alternative weights from each subfactor.
            for factor in factors_list:
                f_weight = factor_weights.get(factor, 0.0)
                sf_list = subfactor_dict.get(factor, [])
                if not sf_list:
                    sub_weights = {factor: 1.0}
                else:
                    sub_weights = subfactor_weight_dict.get(factor, {})
                    if not sub_weights:
                        sub_weights = {sf: 1.0 / len(sf_list) for sf in sf_list}
                for sf, sub_w in sub_weights.items():
                    alt_w = alt_weights_by_subfactor.get(sf, {})
                    if not alt_w:
                        eq = 1.0 / len(alternatives_list)
                        alt_w = {alt: eq for alt in alternatives_list}
                    for alt in alternatives_list:
                        final_scores[alt] += f_weight * sub_w * alt_w.get(alt, 0.0)
            st.subheader("Final Scores for Each Alternative")
            for alt, score in final_scores.items():
                st.write(f"- {alt}: {score:.4f}")
            plot_final_scores_bar_chart("Final Scores", final_scores)
            buf_final = io.StringIO()
            buf_final.write("Alternative,Final Score\n")
            for alt, score in final_scores.items():
                buf_final.write(f"{alt},{score:.4f}\n")
            st.download_button("Download Final Scores (CSV)", data=buf_final.getvalue(), file_name="final_scores_ahp_express.csv", mime="text/csv")

if __name__ == "__main__":

    main()

