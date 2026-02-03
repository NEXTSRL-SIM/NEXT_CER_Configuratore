def genera_report(kwp_base, kwp_bonus, risultati):

    return f"""### Report Cliente NEXT

Impianto standard: **{kwp_base:.2f} kWp**  
Impianto potenziato NEXT: **{kwp_bonus:.2f} kWp**

---

## Beneficio annuo complessivo

➡ **{risultati['Beneficio totale annuo']:.0f} € / anno**

---

## Beneficio totale

- 10 anni: **{risultati['Beneficio totale 10 anni']:.0f} €**
- 20 anni: **{risultati['Beneficio totale 20 anni']:.0f} €**

NEXT – Comunità Energetica
"""
