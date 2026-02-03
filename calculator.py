# calculator.py

def autoconsumo_bonus_from_kwp(kwp_bonus: float) -> float:
    """
    Autoconsumo bonus interpolato automaticamente in base alla taglia impianto.
    Punti fascia alta (batteria 16 kWh):
      6.56 -> 0.80
      7.38 -> 0.83
      9.02 -> 0.88
      9.84 -> 0.91
    """
    points = [
        (6.56, 0.80),
        (7.38, 0.83),
        (9.02, 0.88),
        (9.84, 0.91),
    ]

    if kwp_bonus <= points[0][0]:
        return points[0][1]
    if kwp_bonus >= points[-1][0]:
        return points[-1][1]

    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        if x1 <= kwp_bonus <= x2:
            t = (kwp_bonus - x1) / (x2 - x1)
            return y1 + t * (y2 - y1)

    return points[0][1]


# ==========================================================
# FUNZIONE PRINCIPALE USATA DA app.py
# ==========================================================

def simulate(
    consumo,
    potenza_base,
    potenza_bonus,
    costo_impianto,
    prezzo_energia,
    rid,
    cer,
    quota_condivisa,
    resa,
    autoc_base
):
    """
    Simulazione completa:
    - autoconsumo bonus calcolato automaticamente
    - benefici coerenti con Excel
    """

    autoc_bonus = autoconsumo_bonus_from_kwp(potenza_bonus)

    return compute_benefits(
        consumo_kwh=consumo,
        base_kwp=potenza_base,
        bonus_kwp=potenza_bonus,
        prezzo_energia=prezzo_energia,
        rid_eur_kwh=rid,
        cer_eur_kwh=cer,
        quota_condivisa=quota_condivisa,
        costo_impianto=costo_impianto,
        resa_kwh_kwp=resa,
        autoc_base_perc=autoc_base,
        autoc_bonus_perc=autoc_bonus,
    )


# ==========================================================
# CALCOLO BENEFICI (COERENTE CON EXCEL)
# ==========================================================

def compute_benefits(
    consumo_kwh: float,
    base_kwp: float,
    bonus_kwp: float,
    prezzo_energia: float,
    rid_eur_kwh: float,
    cer_eur_kwh: float,
    quota_condivisa: float,
    costo_impianto: float,
    resa_kwh_kwp: float,
    autoc_base_perc: float,
    autoc_bonus_perc: float,
) -> dict:

    # Produzioni
    produzione_base = base_kwp * resa_kwh_kwp
    produzione_bonus = bonus_kwp * resa_kwh_kwp

    # Autoconsumi teorici
    autoc_base_teorico = consumo_kwh * autoc_base_perc
    autoc_bonus_teorico = consumo_kwh * autoc_bonus_perc

    # Clamp fisico
    autoconsumo_base = min(autoc_base_teorico, produzione_base)
    autoconsumo_bonus = min(autoc_bonus_teorico, produzione_bonus)

    # Energia immessa
    energia_immessa = max(produzione_bonus - autoconsumo_bonus, 0)

    # Delta autoconsumo reale
    delta_autoconsumo = max(autoconsumo_bonus - autoconsumo_base, 0)

    # Extra autoconsumo (€)
    vantaggio_extra_autoconsumo = delta_autoconsumo * prezzo_energia

    # RID e CER
    rid_annuo = energia_immessa * rid_eur_kwh
    cer_prudente = energia_immessa * quota_condivisa * cer_eur_kwh

    totale_benefici_annui = (
        vantaggio_extra_autoconsumo
        + rid_annuo
        + cer_prudente
    )

    # Detrazione fiscale
    detrazione_totale = costo_impianto * 0.50
    detrazione_annua = detrazione_totale / 10

    beneficio_annuale_totale = totale_benefici_annui + detrazione_annua

    # Beneficio 10 anni
    beneficio_10_anni = beneficio_annuale_totale * 10

    # Beneficio 20 anni (detrazione solo per 10 anni)
    beneficio_20_anni = (totale_benefici_annui * 20) + detrazione_totale

    # Risparmio bolletta (senza doppio conteggio extra)
    risparmio_bolletta = max(
        (autoconsumo_bonus - delta_autoconsumo),
        0
    ) * prezzo_energia

    # Risparmio complessivo
    risparmio_complessivo_annuo = beneficio_annuale_totale + risparmio_bolletta
    risparmio_complessivo_10 = beneficio_10_anni + (risparmio_bolletta * 10)

    return {
        # Energia
        "produzione_base": produzione_base,
        "produzione_bonus": produzione_bonus,
        "autoconsumo_base": autoconsumo_base,
        "autoconsumo_bonus": autoconsumo_bonus,
        "energia_immessa": energia_immessa,
        "delta_autoconsumo": delta_autoconsumo,

        # Economico annuo
        "vantaggio_extra_autoconsumo": vantaggio_extra_autoconsumo,
        "rid_annuo": rid_annuo,
        "cer_prudente": cer_prudente,
        "totale_benefici_annui": totale_benefici_annui,

        # Detrazione
        "detrazione_totale": detrazione_totale,
        "detrazione_annua": detrazione_annua,

        # Totali
        "beneficio_annuale_totale": beneficio_annuale_totale,
        "beneficio_10_anni": beneficio_10_anni,
        "beneficio_20_anni": beneficio_20_anni,

        # Bolletta
        "risparmio_bolletta": risparmio_bolletta,
        "risparmio_complessivo_annuo": risparmio_complessivo_annuo,
        "risparmio_complessivo_10": risparmio_complessivo_10,
    }
