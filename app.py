import streamlit as st
import random
import pandas as pd
import re
from math import gcd

st.set_page_config(
    page_title="Jeu de nomenclature chimique",
    page_icon="🎲",
    layout="wide"
)

CATIONS = {
    1: {"formula": "Na⁺", "name": "Sodium", "symbol": "Na", "charge": 1},
    2: {"formula": "K⁺", "name": "Potassium", "symbol": "K", "charge": 1},
    3: {"formula": "H⁺", "name": "Hydrogène", "symbol": "H", "charge": 1},
    4: {"formula": "Li⁺", "name": "Lithium", "symbol": "Li", "charge": 1},
    5: {"formula": "Al³⁺", "name": "Aluminium", "symbol": "Al", "charge": 3},
    6: {"formula": "Ca²⁺", "name": "Calcium", "symbol": "Ca", "charge": 2},
    7: {"formula": "Cr³⁺", "name": "Chrome (III)", "symbol": "Cr", "charge": 3},
    8: {"formula": "Mg²⁺", "name": "Magnésium", "symbol": "Mg", "charge": 2},
    9: {"formula": "Fe³⁺", "name": "Fer (III)", "symbol": "Fe", "charge": 3},
    10: {"formula": "Fe²⁺", "name": "Fer (II)", "symbol": "Fe", "charge": 2},
    11: {"formula": "Cu²⁺", "name": "Cuivre (II)", "symbol": "Cu", "charge": 2},
    12: {"formula": "Cu⁺", "name": "Cuivre (I)", "symbol": "Cu", "charge": 1},
    13: {"formula": "Ni²⁺", "name": "Nickel (II)", "symbol": "Ni", "charge": 2},
    14: {"formula": "Ag⁺", "name": "Argent", "symbol": "Ag", "charge": 1},
    15: {"formula": "Zn²⁺", "name": "Zinc", "symbol": "Zn", "charge": 2},
    16: {"formula": "Co²⁺", "name": "Cobalt (II)", "symbol": "Co", "charge": 2},
    17: {"formula": "Cs⁺", "name": "Césium", "symbol": "Cs", "charge": 1},
    18: {"formula": "Rb⁺", "name": "Rubidium", "symbol": "Rb", "charge": 1},
    19: {"formula": "NH₄⁺", "name": "Ammonium", "symbol": "NH4", "charge": 1},
    20: {"formula": "Ba²⁺", "name": "Baryum", "symbol": "Ba", "charge": 2},
}

ANIONS = {
    1: {"formula": "H₂PO₄⁻", "name": "Dihydrogénophosphate", "symbol": "H2PO4", "charge": -1},
    2: {"formula": "Cr₂O₇²⁻", "name": "Dichromate", "symbol": "Cr2O7", "charge": -2},
    3: {"formula": "HCO₃⁻", "name": "Hydrogénocarbonate", "symbol": "HCO3", "charge": -1},
    4: {"formula": "Br⁻", "name": "Bromure", "symbol": "Br", "charge": -1},
    5: {"formula": "CrO₄²⁻", "name": "Chromate", "symbol": "CrO4", "charge": -2},
    6: {"formula": "CO₃²⁻", "name": "Carbonate", "symbol": "CO3", "charge": -2},
    7: {"formula": "Cl⁻", "name": "Chlorure", "symbol": "Cl", "charge": -1},
    8: {"formula": "SO₃²⁻", "name": "Sulfite", "symbol": "SO3", "charge": -2},
    9: {"formula": "N³⁻", "name": "Nitrure", "symbol": "N", "charge": -3},
    10: {"formula": "F⁻", "name": "Fluorure", "symbol": "F", "charge": -1},
    11: {"formula": "NO₂⁻", "name": "Nitrite", "symbol": "NO2", "charge": -1},
    12: {"formula": "HPO₄²⁻", "name": "Hydrogénophosphate", "symbol": "HPO4", "charge": -2},
    13: {"formula": "NO₃⁻", "name": "Nitrate", "symbol": "NO3", "charge": -1},
    14: {"formula": "HSO₄⁻", "name": "Hydrogénosulfate", "symbol": "HSO4", "charge": -1},
    15: {"formula": "I⁻", "name": "Iodure", "symbol": "I", "charge": -1},
    16: {"formula": "OH⁻", "name": "Hydroxyde", "symbol": "OH", "charge": -1},
    17: {"formula": "O²⁻", "name": "Oxyde", "symbol": "O", "charge": -2},
    18: {"formula": "PO₄³⁻", "name": "Phosphate", "symbol": "PO4", "charge": -3},
    19: {"formula": "MnO₄⁻", "name": "Permanganate", "symbol": "MnO4", "charge": -1},
    20: {"formula": "S²⁻", "name": "Sulfure", "symbol": "S", "charge": -2},
}

TYPE_BY_ANION = {
    "Hydroxyde": "Hydroxyde / base",
    "Oxyde": "Oxyde",
    "Sulfure": "Sel binaire",
    "Chlorure": "Sel binaire",
    "Bromure": "Sel binaire",
    "Fluorure": "Sel binaire",
    "Iodure": "Sel binaire",
}


def format_index(n: int) -> str:
    subs = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    return "" if n == 1 else str(n).translate(subs)


def needs_parentheses(symbol: str) -> bool:
    return bool(re.search(r"\d", symbol)) or symbol in {"NH4", "OH"}


def pretty_formula(cation: dict, anion: dict) -> str:
    c_charge = abs(cation["charge"])
    a_charge = abs(anion["charge"])
    divisor = gcd(c_charge, a_charge)
    c_index = a_charge // divisor
    a_index = c_charge // divisor

    c_symbol = cation["symbol"]
    a_symbol = anion["symbol"]

    if c_index > 1 and needs_parentheses(c_symbol):
        c_symbol = f"({c_symbol})"
    if a_index > 1 and needs_parentheses(a_symbol):
        a_symbol = f"({a_symbol})"

    return f"{c_symbol}{format_index(c_index)}{a_symbol}{format_index(a_index)}"


def compound_name(cation: dict, anion: dict) -> str:
    return f"{anion['name'].lower()} de {cation['name'].lower()}"


def compound_type(cation: dict, anion: dict) -> str:
    if cation["symbol"] == "H":
        return "Acide"
    return TYPE_BY_ANION.get(anion["name"], "Sel ternaire / composé ionique")


if "roll" not in st.session_state:
    st.session_state.roll = None
if "history" not in st.session_state:
    st.session_state.history = []


def roll_dice():
    d1 = random.randint(1, 20)
    d2 = random.randint(1, 20)
    cation = CATIONS[d1]
    anion = ANIONS[d2]
    st.session_state.roll = {
        "d1": d1,
        "d2": d2,
        "cation": cation,
        "anion": anion,
        "solution_formula": pretty_formula(cation, anion),
        "solution_name": compound_name(cation, anion),
        "solution_type": compound_type(cation, anion),
    }


def reset_game():
    st.session_state.roll = None
    st.session_state.history = []


st.markdown("""
<style>
.big-title {
    font-size: 3rem;
    font-weight: 900;
    text-align: center;
    margin-bottom: 0.2rem;
}
.subtitle {
    text-align: center;
    color: #555;
    font-size: 1.15rem;
    margin-bottom: 2rem;
}
.die-box {
    border-radius: 24px;
    padding: 24px;
    background: white;
    box-shadow: 0 10px 28px rgba(0,0,0,0.08);
    text-align: center;
    min-height: 220px;
}
.die-number {
    font-size: 4rem;
    font-weight: 900;
    background: #f6c66f;
    border-radius: 22px;
    display: inline-block;
    padding: 10px 34px;
    margin: 12px;
}
.ion {
    font-size: 1.6rem;
    font-weight: 800;
    color: #416655;
}
.solution {
    border-radius: 20px;
    padding: 18px;
    background: #fff7db;
    border: 1px solid #f2d27c;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🎲 Jeu de nomenclature chimique</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Deux dés, deux ions, une formule neutre à retrouver. La chimie, mais avec un petit parfum de casino pédagogique.</div>',
    unsafe_allow_html=True
)

col_btn1, col_btn2, col_btn3 = st.columns(3)
with col_btn1:
    if st.button("🎲 Lancer les dés", use_container_width=True, type="primary"):
        roll_dice()
with col_btn2:
    if st.button("🧹 Réinitialiser", use_container_width=True):
        reset_game()
with col_btn3:
    show_solution = st.toggle("Afficher la correction", value=False)

roll = st.session_state.roll
left, right = st.columns(2)

with left:
    if roll:
        st.markdown(f"""
        <div class="die-box">
            <h2>Dé n°1 — Cation</h2>
            <div class="die-number">{roll["d1"]}</div>
            <div class="ion">{roll["cation"]["formula"]} — {roll["cation"]["name"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Clique sur **Lancer les dés** pour obtenir le cation.")

with right:
    if roll:
        st.markdown(f"""
        <div class="die-box">
            <h2>Dé n°2 — Anion</h2>
            <div class="die-number">{roll["d2"]}</div>
            <div class="ion">{roll["anion"]["formula"]} — {roll["anion"]["name"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Clique sur **Lancer les dés** pour obtenir l’anion.")

st.divider()
st.subheader("✍️ Réponse de l’équipe")

with st.form("answer_form", clear_on_submit=False):
    c1, c2, c3 = st.columns(3)
    with c1:
        user_formula = st.text_input("Formule moléculaire", placeholder="Ex. NaCl")
    with c2:
        user_name = st.text_input("Nom", placeholder="Ex. chlorure de sodium")
    with c3:
        user_type = st.text_input("Type de corps chimique", placeholder="Ex. sel, acide, hydroxyde...")

    submitted = st.form_submit_button("✅ Valider la manche", use_container_width=True)

if submitted:
    if not roll:
        st.warning("Lance d’abord les dés, jeune alchimiste.")
    else:
        st.session_state.history.insert(0, {
            "Dé 1 + Dé 2": f'{roll["d1"]} + {roll["d2"]}',
            "Cation": f'{roll["cation"]["formula"]} {roll["cation"]["name"]}',
            "Anion": f'{roll["anion"]["formula"]} {roll["anion"]["name"]}',
            "Réponse formule": user_formula,
            "Réponse nom": user_name,
            "Réponse type": user_type,
            "Correction formule": roll["solution_formula"],
            "Correction nom": roll["solution_name"],
            "Correction type": roll["solution_type"],
        })
        st.success("Manche enregistrée.")

if roll and show_solution:
    st.markdown(f"""
    <div class="solution">
        <h3>✅ Correction proposée</h3>
        <p><strong>Formule :</strong> {roll["solution_formula"]}</p>
        <p><strong>Nom :</strong> {roll["solution_name"]}</p>
        <p><strong>Type :</strong> {roll["solution_type"]}</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.subheader("📋 Historique des manches")

if st.session_state.history:
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True, hide_index=True)
else:
    st.caption("Aucune manche enregistrée pour l’instant.")

with st.expander("📚 Voir les listes cations/anions"):
    cations_df = pd.DataFrame(
        [{"Dé": k, "Ion": v["formula"], "Nom": v["name"], "Charge": v["charge"]} for k, v in CATIONS.items()]
    )
    anions_df = pd.DataFrame(
        [{"Dé": k, "Ion": v["formula"], "Nom": v["name"], "Charge": v["charge"]} for k, v in ANIONS.items()]
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Cations**")
        st.dataframe(cations_df, use_container_width=True, hide_index=True)
    with col_b:
        st.write("**Anions**")
        st.dataframe(anions_df, use_container_width=True, hide_index=True)
