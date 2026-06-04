# Nomenclature_Min
Exercices de nomenclature
const cations = {
  1: { formula: "Na⁺", name: "Sodium" },
  2: { formula: "K⁺", name: "Potassium" },
  3: { formula: "H⁺", name: "Hydrogène" },
  4: { formula: "Li⁺", name: "Lithium" },
  5: { formula: "Al³⁺", name: "Aluminium" },
  6: { formula: "Ca²⁺", name: "Calcium" },
  7: { formula: "Cr³⁺", name: "Chrome" },
  8: { formula: "Mg²⁺", name: "Magnésium" },
  9: { formula: "Fe³⁺", name: "Fer (III)" },
  10: { formula: "Fe²⁺", name: "Fer (II)" },
  11: { formula: "Cu²⁺", name: "Cuivre (II)" },
  12: { formula: "Cu⁺", name: "Cuivre (I)" },
  13: { formula: "Ni²⁺", name: "Nickel" },
  14: { formula: "Ag⁺", name: "Argent" },
  15: { formula: "Zn²⁺", name: "Zinc" },
  16: { formula: "Co²⁺", name: "Cobalt" },
  17: { formula: "Cs⁺", name: "Césium" },
  18: { formula: "Rb⁺", name: "Rubidium" },
  19: { formula: "NH₄⁺", name: "Ammonium" },
  20: { formula: "Ba²⁺", name: "Baryum" }
};

const anions = {
  1: { formula: "H₂PO₄⁻", name: "Dihydrogénophosphate" },
  2: { formula: "Cr₂O₇²⁻", name: "Dichromate" },
  3: { formula: "HCO₃⁻", name: "Hydrogénocarbonate" },
  4: { formula: "Br⁻", name: "Bromure" },
  5: { formula: "CrO₄²⁻", name: "Chromate" },
  6: { formula: "CO₃²⁻", name: "Carbonate" },
  7: { formula: "Cl⁻", name: "Chlorure" },
  8: { formula: "SO₃²⁻", name: "Sulfite" },
  9: { formula: "N³⁻", name: "Nitrure" },
  10: { formula: "F⁻", name: "Fluorure" },
  11: { formula: "NO₂⁻", name: "Nitrite" },
  12: { formula: "HPO₄²⁻", name: "Hydrogénophosphate" },
  13: { formula: "NO₃⁻", name: "Nitrate" },
  14: { formula: "HSO₄⁻", name: "Hydrogénosulfate" },
  15: { formula: "I⁻", name: "Iodure" },
  16: { formula: "OH⁻", name: "Hydroxyde" },
  17: { formula: "O²⁻", name: "Oxyde" },
  18: { formula: "PO₄³⁻", name: "Phosphate" },
  19: { formula: "MnO₄⁻", name: "Permanganate" },
  20: { formula: "S²⁻", name: "Sulfure" }
};

let currentRoll = null;

const die1 = document.querySelector("#die1");
const die2 = document.querySelector("#die2");
const cationName = document.querySelector("#cationName");
const anionName = document.querySelector("#anionName");
const historyBody = document.querySelector("#historyBody");

function rollD20() {
  return Math.floor(Math.random() * 20) + 1;
}

function rollDice() {
  const d1 = rollD20();
  const d2 = rollD20();

  currentRoll = {
    d1,
    d2,
    cation: cations[d1],
    anion: anions[d2]
  };

  die1.textContent = d1;
  die2.textContent = d2;
  cationName.textContent = `${currentRoll.cation.formula} — ${currentRoll.cation.name}`;
  anionName.textContent = `${currentRoll.anion.formula} — ${currentRoll.anion.name}`;

  document.querySelector("#formulaInput").value = "";
  document.querySelector("#nameInput").value = "";
  document.querySelector("#typeInput").value = "";
}

function saveRound() {
  if (!currentRoll) {
    alert("Lance d’abord les dés, jeune alchimiste.");
    return;
  }

  const formula = document.querySelector("#formulaInput").value.trim();
  const name = document.querySelector("#nameInput").value.trim();
  const type = document.querySelector("#typeInput").value.trim();

  const row = document.createElement("tr");
  row.innerHTML = `
    <td>${currentRoll.d1} + ${currentRoll.d2}</td>
    <td>${currentRoll.cation.formula} ${currentRoll.cation.name}</td>
    <td>${currentRoll.anion.formula} ${currentRoll.anion.name}</td>
    <td>${formula || "—"}</td>
    <td>${name || "—"}</td>
    <td>${type || "—"}</td>
  `;
  historyBody.prepend(row);
}

function resetGame() {
  currentRoll = null;
  die1.textContent = "?";
  die2.textContent = "?";
  cationName.textContent = "—";
  anionName.textContent = "—";
  historyBody.innerHTML = "";
}

document.querySelector("#rollBtn").addEventListener("click", rollDice);
document.querySelector("#saveBtn").addEventListener("click", saveRound);
document.querySelector("#resetBtn").addEventListener("click", resetGame);

<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Jeu de nomenclature chimique</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <main class="app">
    <section class="card hero">
      <h1>🎲 Jeu de nomenclature chimique</h1>
      <p>
        Lance deux dés : le premier donne le cation, le deuxième donne l’anion.
        À toi d’écrire la formule, le nom et le type de corps chimique.
      </p>

      <div class="controls">
        <button id="rollBtn">Lancer les dés</button>
        <button id="resetBtn" class="secondary">Réinitialiser</button>
      </div>
    </section>

    <section class="dice-zone">
      <div class="die-card">
        <h2>Dé n°1 — Cation</h2>
        <div id="die1" class="die">?</div>
        <p id="cationName" class="ion">—</p>
      </div>

      <div class="die-card">
        <h2>Dé n°2 — Anion</h2>
        <div id="die2" class="die">?</div>
        <p id="anionName" class="ion">—</p>
      </div>
    </section>

    <section class="card answer">
      <h2>Réponse de l’équipe</h2>
      <label>
        Formule moléculaire
        <input id="formulaInput" placeholder="Ex. NaCl" />
      </label>

      <label>
        Nom
        <input id="nameInput" placeholder="Ex. chlorure de sodium" />
      </label>

      <label>
        Type de corps chimique
        <input id="typeInput" placeholder="Ex. sel, acide, hydroxyde..." />
      </label>

      <button id="saveBtn">Valider la manche</button>
    </section>

    <section class="card">
      <h2>Historique</h2>
      <table>
        <thead>
          <tr>
            <th>Dé 1 + Dé 2</th>
            <th>Cation</th>
            <th>Anion</th>
            <th>Formule</th>
            <th>Nom</th>
            <th>Type</th>
          </tr>
        </thead>
        <tbody id="historyBody"></tbody>
      </table>
    </section>
  </main>

  <script src="script.js"></script>
</body>
</html>

