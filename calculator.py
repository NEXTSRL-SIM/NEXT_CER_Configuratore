def compute_benefits(
    consumo,
    base_kwp,
    bonus_kwp,
    prezzo_energia,
    rid,
    cer,
    quota,
    costo_impianto,
    resa,
    autoc_base_perc,
    autoc_bonus_perc
):
    """
    Replica perfetta del modello Excel configuratore NEXT.
    """

    # -----------------------------
    # 1) PRODUZIONE BONUS (kWh)
    # -----------------------------
    produzione_bonus = bonus_kwp * resa

    # -----------------------------
    # 2) AUTOCONSUMO (kWh)
    # -----------------------------
    autoconsumo_base = autoc_base_perc * consumo
    autoconsumo_bonus = autoc_bonus_perc * consumo

    # -----------------------------
    # 3) ENERGIA IMMESSA (kWh)
    # -----------------------------
    energia_immessa = max(produzione_bonus - autoconsumo_bonus, 0)

    # -----------------------------
    # 4) DELTA AUTOCONSUMO vs BASE
    # -----------------------------
    delta_autoconsumo = autoconsumo_bonus - autoconsumo_base

    # -----------------------------
    # 5) VANTAGGIO EXTRA AUTOCONSUMO (€)
    # -----------------------------
    vantaggio_extra_autoconsumo = delta_autoconsumo * prezzo_energia

    # -----------------------------
    # 6) RID (€)
    # -----------------------------
    rid_annuo = energia_immessa * rid

    # -----------------------------
    # 7) CER PRUDENTE (€)
    # CER * quota energia condivisa
    # -----------------------------
    cer_prudente = energia_immessa * cer * quota

    # -----------------------------
    # 8) TOTALE BENEFICI ANNUI (Upgrade+CER)
    # -----------------------------
    totale_benefici_annui = (
        vantaggio_extra_autoconsumo +
        rid_annuo +
        cer_prudente
    )

    # -----------------------------
    # 9) DETRAZIONE FISCALE
    # -----------------------------
    detrazione_totale = costo_impianto * 0.50
    detrazione_annua = detrazione_totale / 10

    # -----------------------------
    # 10) BENEFICIO ANNUALE TOTALE (con detrazione)
    # -----------------------------
    beneficio_annuale_totale = totale_benefici_annui + detrazione_annua

    # -----------------------------
    # 11) RISPARMIO IN BOLLETTA ANNUO
    # -----------------------------
    risparmio_bolletta = autoconsumo_bonus * prezzo_energia

    # -----------------------------
    # 12) RISPARMIO COMPLESSIVO ANNUALE
    # -----------------------------
    risparmio_complessivo_annuo = beneficio_annuale_totale + risparmio_bolletta

    # -----------------------------
    # 13) TOTALI 10 E 20 ANNI
    # -----------------------------
    beneficio_10_anni = beneficio_annuale_totale * 10
    beneficio_20_anni = beneficio_annuale_totale * 20

    risparmio_complessivo_10 = risparmio_complessivo_annuo * 10

    # -----------------------------
    # OUTPUT COMPLETO (Excel-like)
    # -----------------------------
    return {
        # Produzione
        "produzione_bonus": produzione_bonus,

        # Autoconsumo
        "autoconsumo_bonus": autoconsumo_bonus,
        "energia_immessa": energia_immessa,

        # Delta
        "delta_autoconsumo": delta_autoconsumo,
        "vantaggio_extra_autoconsumo": vantaggio_extra_autoconsumo,

        # Incentivi
        "rid_annuo": rid_annuo,
        "cer_prudente": cer_prudente,

        # Totali annui
        "totale_benefici_annui": totale_benefici_annui,
        "detrazione_annua": detrazione_annua,
        "beneficio_annuale_totale": beneficio_annuale_totale,

        # Risparmio bolletta
        "risparmio_bolletta": risparmio_bolletta,
        "risparmio_complessivo_annuo": risparmio_complessivo_annuo,

        # Totali lungo periodo
        "beneficio_10_anni": beneficio_10_anni,
        "beneficio_20_anni": beneficio_20_anni,
        "risparmio_complessivo_10": risparmio_complessivo_10
    }
