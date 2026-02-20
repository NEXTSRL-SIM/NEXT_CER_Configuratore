# calculator.py

# ---------------------------------------------------------
# QUOTA COPERTURA CONSUMI (ex autoconsumo bonus)
# ---------------------------------------------------------

def quota_copertura_from_kwp(kwp_bonus: float) -> float:
    """
    Calcola la quota di copertura dei consumi (NON autoconsumo tecnico).
    Progressione lineare all'interno della fascia.

    Fascia 1: 3.28 → 5.74
    Fascia 2: 6.56 → 9.84

    Base fascia = 80%
    Max fascia  = 85%
    """

    COPERTURA_BASE = 0.80
    COPERTURA_MAX = 0.85

    if kwp_bonus <= 5.74:
        base_fascia = 3.28
        max_fascia = 5.74
    else:
        base_fascia = 6.56
        max_fascia = 9.84

    if kwp_bonus <= base_fascia:
        return COPERTURA_BASE

    if kwp_bonus >= max_fascia:
        return COPERTURA_MAX

    posizione = (kwp_bonus - base_fascia) / (max_fascia - base_fascia)

    copertura = COPERTURA_BASE + posizione * (COPERTURA_MAX - COPERTURA_BASE)

    return copertura


# ---------------------------------------------------------
# CLIPPING INVERTER 6 kW
# ---------------------------------------------------------

def apply_clipping(bonus_kwp, resa_kwh_kwp, consumo_kwh):

    produzione_teorica = bonus_kwp * resa_kwh_kwp
    riduzione = 0.0

    if consumo_kwh <= 9000:

        kwp = round(bonus_kwp, 2)

        # Identificazione zona tramite resa
        if resa_kwh_kwp <= 1250:
            zona = "nord"
        elif resa_kwh_kwp <= 1400:
            zona = "centro"
        else:
            zona = "sud"

        clipping_table = {
            8.2:  {"nord": 0.015, "centro": 0.019, "sud": 0.023},
            9.02: {"nord": 0.029, "centro": 0.034, "sud": 0.041},
            9.84: {"nord": 0.045, "centro": 0.052, "sud": 0.059},
        }

        if kwp in clipping_table:
            riduzione = clipping_table[kwp][zona]

    produzione_effettiva = produzione_teorica * (1 - riduzione)

    return produzione_teorica, riduzione, produzione_effettiva


# ---------------------------------------------------------
# MOTORE PRINCIPALE
# ---------------------------------------------------------

def calcola_orizzonte(
    anni,
    prezzo_iniziale,
    incremento,
    autoconsumo_base,
    delta_autoconsumo,
    energia_immessa,
    rid_eur_kwh,
    cer_eur_kwh,
    quota_condivisa,
    detrazione_annua=0
):
    totale = 0

    prezzo = prezzo_iniziale

    for anno in range(1, anni + 1):

        # Benefici variabili legati al prezzo energia
        vantaggio_autoc = delta_autoconsumo * prezzo
        

        rid = energia_immessa * rid_eur_kwh
        cer = energia_immessa * quota_condivisa * cer_eur_kwh

        beneficio_annuo = (
            vantaggio_autoc
            + rid
            + cer
            + detrazione_annua
        )

        totale += beneficio_annuo

        # aggiorna prezzo anno successivo
        prezzo *= (1 + incremento)

    return totale


def calcola_risparmio_bolletta_orizzonte(
    anni,
    prezzo_iniziale,
    incremento,
    autoconsumo_base
):
    totale = 0
    prezzo = prezzo_iniziale

    for _ in range(anni):
        totale += autoconsumo_base * prezzo
        prezzo *= (1 + incremento)

    return totale

def calcola_irr(flussi, guess=0.1, toll=1e-6, max_iter=1000):
    """
    Calcolo IRR tramite metodo di Newton-Raphson
    """
    r = guess
    for _ in range(max_iter):
        npv = 0
        derivata = 0

        for t, cf in enumerate(flussi):
            npv += cf / (1 + r) ** t
            if t > 0:
                derivata -= t * cf / (1 + r) ** (t + 1)

        nuovo_r = r - npv / derivata

        if abs(nuovo_r - r) < toll:
            return nuovo_r

        r = nuovo_r

    return r


def compute_benefits(
    consumo_kwh,
    base_kwp,
    bonus_kwp,
    prezzo_energia,
    rid_eur_kwh,
    cer_eur_kwh,
    quota_condivisa,
    costo_impianto,
    resa_kwh_kwp,
    autoc_base_perc,
    autoc_bonus_perc=None,
    incremento_prezzo_annuo=0.0,
):

    # -------------------------------
    # Produzione BASE
    # -------------------------------
    produzione_base = base_kwp * resa_kwh_kwp

    # -------------------------------
    # Produzione BONUS con clipping
    # -------------------------------
    produzione_bonus_teorica, percentuale_clipping, produzione_bonus = apply_clipping(
        bonus_kwp,
        resa_kwh_kwp,
        consumo_kwh
    )

    # -------------------------------
    # Quota copertura BONUS automatica
    # -------------------------------
    if autoc_bonus_perc is None:
        autoc_bonus_perc = quota_copertura_from_kwp(bonus_kwp)

    # -------------------------------
    # Copertura consumi
    # -------------------------------
    autoconsumo_base = min(consumo_kwh * autoc_base_perc, produzione_base)
    autoconsumo_bonus = min(consumo_kwh * autoc_bonus_perc, produzione_bonus)

    delta_autoconsumo = max(autoconsumo_bonus - autoconsumo_base, 0)

    # -------------------------------
    # Energia immessa
    # -------------------------------
    energia_immessa = max(produzione_bonus - autoconsumo_bonus, 0)

    # -------------------------------
    # Benefici economici
    # -------------------------------
    vantaggio_extra_autoconsumo = delta_autoconsumo * prezzo_energia

    rid_annuo = energia_immessa * rid_eur_kwh
    cer_prudente = energia_immessa * quota_condivisa * cer_eur_kwh

    totale_benefici_annui = (
        vantaggio_extra_autoconsumo
        + rid_annuo
        + cer_prudente
    )

    # -------------------------------
    # Detrazione fiscale
    # -------------------------------
    detrazione_totale = costo_impianto * 0.50
    detrazione_annua = detrazione_totale / 10

    beneficio_annuale_totale = totale_benefici_annui + detrazione_annua

    # -------------------------------
    # Risparmio bolletta diretto
    # -------------------------------
    risparmio_bolletta = autoconsumo_base * prezzo_energia

    # -------------------------------
    # 10 ANNI
    # -------------------------------
    
    # Rendita pura (senza bolletta)
    beneficio_10_anni = calcola_orizzonte(
        10,
        prezzo_energia,
        incremento_prezzo_annuo,
        autoconsumo_base,
        delta_autoconsumo,
        energia_immessa,
        rid_eur_kwh,
        cer_eur_kwh,
        quota_condivisa,
        detrazione_annua
    )

    # Risparmio bolletta dinamico
    risparmio_bolletta_10 = calcola_risparmio_bolletta_orizzonte(
        10,
        prezzo_energia,
        incremento_prezzo_annuo,
        autoconsumo_base
    )
    risparmio_complessivo_10 = beneficio_10_anni + risparmio_bolletta_10

    # -------------------------------
    # 20 ANNI (detrazione solo primi 10)
    # -------------------------------

    # Primi 10 anni con detrazione
    beneficio_primi_10 = calcola_orizzonte(
        10,
        prezzo_energia,
        incremento_prezzo_annuo,
        autoconsumo_base,
        delta_autoconsumo,
        energia_immessa,
        rid_eur_kwh,
        cer_eur_kwh,
        quota_condivisa,
        detrazione_annua
    )

    # Secondi 10 anni SENZA detrazione
    beneficio_secondi_10 = calcola_orizzonte(
        10,
        prezzo_energia * ((1 + incremento_prezzo_annuo) ** 10),
        incremento_prezzo_annuo,
        autoconsumo_base,
        delta_autoconsumo,
        energia_immessa,
        rid_eur_kwh,
        cer_eur_kwh,
        quota_condivisa,
        0
    )

    beneficio_20_anni = beneficio_primi_10 + beneficio_secondi_10

    risparmio_bolletta_20 = calcola_risparmio_bolletta_orizzonte(
        20,
        prezzo_energia,
        incremento_prezzo_annuo,
        autoconsumo_base
    )
    risparmio_complessivo_20 = beneficio_20_anni + risparmio_bolletta_20

    # -------------------------------
    # IRR 10 ANNI
    # -------------------------------

    flussi_10 = [-costo_impianto]

    prezzo = prezzo_energia

    for anno in range(1, 11):

        vantaggio_autoc = delta_autoconsumo * prezzo
        rid = energia_immessa * rid_eur_kwh
        cer = energia_immessa * quota_condivisa * cer_eur_kwh
        detrazione = detrazione_annua if anno <= 10 else 0
        bolletta = autoconsumo_base * prezzo

        flusso = vantaggio_autoc + rid + cer + detrazione + bolletta
        flussi_10.append(flusso)

        prezzo *= (1 + incremento_prezzo_annuo)

    irr_10 = calcola_irr(flussi_10) * 100

    # -------------------------------
    # RETURN
    # -------------------------------
    return {

        # Produzione
        "produzione_base": produzione_base,
        "produzione_bonus_teorica": produzione_bonus_teorica,
        "percentuale_clipping": percentuale_clipping,
        "produzione_bonus": produzione_bonus,

        # Copertura
        "autoconsumo_base": autoconsumo_base,
        "autoconsumo_bonus": autoconsumo_bonus,
        "delta_autoconsumo": delta_autoconsumo,

        # Energia immessa
        "energia_immessa": energia_immessa,

        # Benefici annui
        "vantaggio_extra_autoconsumo": vantaggio_extra_autoconsumo,
        "rid_annuo": rid_annuo,
        "cer_prudente": cer_prudente,
        "totale_benefici_annui": totale_benefici_annui,

        # Detrazione
        "detrazione_annua": detrazione_annua,
        "beneficio_annuale_totale": beneficio_annuale_totale,

        # Risparmio bolletta
        "risparmio_bolletta": risparmio_bolletta,

        # Orizzonte temporale
        "beneficio_10_anni": beneficio_10_anni,
        "beneficio_20_anni": beneficio_20_anni,
        "risparmio_complessivo_10": risparmio_complessivo_10,
        "risparmio_complessivo_20": risparmio_complessivo_20,

        "risparmio_complessivo_annuo":
            calcola_orizzonte(
                1,
                prezzo_energia,
                incremento_prezzo_annuo,
                autoconsumo_base,
                delta_autoconsumo,
                energia_immessa,
                rid_eur_kwh,
                cer_eur_kwh,
                quota_condivisa,
                detrazione_annua
            )
            +
            calcola_risparmio_bolletta_orizzonte(
                1,
                prezzo_energia,
                incremento_prezzo_annuo,
                autoconsumo_base
            ),

        "irr_10": irr_10,
    
    }