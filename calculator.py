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
    """
    Calcolo coerente con Excel, con 2 correzioni:
    1) Delta autoconsumo calcolato sui kWh REALI (dopo clamp su produzione).
    2) Risparmio bolletta calcolato su autoconsumo totale MA ESCLUDENDO l'extra autoconsumo
       (per evitare doppio conteggio con la voce "vantaggio extra autoconsumo").
    """

    # Produzioni
    produzione_base = base_kwp * resa_kwh_kwp
    produzione_bonus = bonus_kwp * resa_kwh_kwp

    # Autoconsumi teorici (su consumo)
    autoc_base_teorico = consumo_kwh * autoc_base_perc
    autoc_bonus_teorico = consumo_kwh * autoc_bonus_perc

    # Clamp fisico: non posso autoconsumare più della produzione di quell'impianto
    autoconsumo_base = min(autoc_base_teorico, produzione_base)
    autoconsumo_bonus = min(autoc_bonus_teorico, produzione_bonus)

    # Energia immessa
    energia_immessa = max(produzione_bonus - autoconsumo_bonus, 0)

    # ✅ Delta autoconsumo REALE (kWh) = differenza tra bonus e base dopo clamp
    delta_autoconsumo = max(autoconsumo_bonus - autoconsumo_base, 0)

    # Vantaggio extra autoconsumo (€/anno)
    vantaggio_extra_autoconsumo = delta_autoconsumo * prezzo_energia

    # RID e CER
    rid_annuo = energia_immessa * rid_eur_kwh
    cer_prudente = energia_immessa * quota_condivisa * cer_eur_kwh

    totale_benefici_annui = vantaggio_extra_autoconsumo + rid_annuo + cer_prudente

    # Detrazione 50% in 10 anni
    detrazione_totale = costo_impianto * 0.50
    detrazione_annua = detrazione_totale / 10

    beneficio_annuale_totale = totale_benefici_annui + detrazione_annua

    # ✅ 10 anni: (benefici annui + detrazione annua) * 10
    beneficio_10_anni = beneficio_annuale_totale * 10

    # ✅ 20 anni: benefici annui * 20 + detrazione annua * 10 (NO raddoppio detrazione)
    beneficio_20_anni = (totale_benefici_annui * 20) + (detrazione_annua * 10)

    # ✅ RISPARMIO IN BOLLETTA (evita doppio conteggio):
    # risparmio totale da autoconsumo bonus - valore extra già contabilizzato
    # = (autoconsumo_bonus * prezzo) - (delta_autoconsumo * prezzo)
    risparmio_bolletta = max((autoconsumo_bonus - delta_autoconsumo), 0) * prezzo_energia

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
        "detrazione_totale": detrazione_totale,
        "detrazione_annua": detrazione_annua,
        "beneficio_annuale_totale": beneficio_annuale_totale,

        # Tempo
        "beneficio_10_anni": beneficio_10_anni,
        "beneficio_20_anni": beneficio_20_anni,

        # Bolletta (senza doppio conteggio extra)
        "risparmio_bolletta": risparmio_bolletta,
        "risparmio_complessivo_annuo": risparmio_complessivo_annuo,
        "risparmio_complessivo_10": risparmio_complessivo_10,
    }
