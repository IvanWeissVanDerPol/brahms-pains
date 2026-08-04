#!/usr/bin/env python3
"""Comprehensive identity-based rename for untiered_personal."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH" / "wa_messages/untiered_personal"


def safe_name(name: str) -> str:
    s = re.sub(r"[^\w\s-]", "", name).strip()
    s = re.sub(r"\s+", "_", s)
    return s


def main():
    # Manual mapping based on first-message context analysis
    MANUAL_MAP = {
        # 91-100 msgs
        "Lid_170823767859295": "Kiki_Referral_Wes",  # "hi wes im ivan kiki passed me your whatsapp"
        "108__p9093___wa_chat_5215547629093_4393": "Cerri",  # "Soy Cerri"
        "Lid_58390113992826": "Raul_Hermano_Roger",  # "Habla Raul, El Hermano de Roger"
        # 80-89 msgs
        "cesar____wa_chat_595972104371_9036": "Cesar",  # already has prefix
        "Lid_55955521822873": "Photo_Sender",  # "Te envío las fotos donde salís"
        # 70-79 msgs
        "164__p0045___wa_chat_595981700045_3657": "Consult_Query",
        # 60-69 msgs
        "Lid_223446109839496": "Sara",  # "Hola! Sara soy"
        "226__p5034___wa_chat_595991715034_11083": "OT_19507_Tech",  # service order
        "Lid_180002230378511": "Sarah_Bum_Referral",  # "Me pasó tu bum Sarah"
        "140__p9007___wa_chat_595974419007_11192": "Canada_Flight_Ref",  # "Me pasaron este Numero para agendar mi vuelo a Canada"
        "Lid_264647361974519": "Lid_264647361974519",  # empty first msg, skip
        # 50-59 msgs
        "angel____wa_chat_595971102999_2992": "Angel_Gamarra_CS",  # "secretario del comité de cursos"
        "190__p9200___wa_chat_595984409200_4630": "Delivery_Query",
        "Lid_275015379464272": "Adri_Referral_Quote",  # "Me pasó su número Adri"
        "Lid_111231230845043": "Don_Juan_Web",  # "Escribo desde la Web de Don Juan"
        "Lid_83477168951296": "Reimar_Cintos",  # "de Reimar comercial"
        "150__p3900___wa_chat_595981063900_11176": "Chat_150p3900",
        "Lid_242455349821600": "Masterdom_Jose_Angelo",  # "Soy Masterdom, Jose o Angelo"
        # 40-49 msgs
        "244__p3154___wa_chat_595992853154_2985": "Profe_Curso_Query",  # "puedo aun unirme como profe"
        "227__p7977___wa_chat_595991717977_12799": "Chat_227p7977",
        "242__p1418___wa_chat_595992721418_11762": "Skokka_Melik_Ad",  # "vi tu anuncio en Skokka"
        "Chat_595974443443": "Ferrex_Pinedo",  # business bot
        "250__p3857___wa_chat_595994883857_11673": "De_Donde_Sos_Amigo",
        "166__p1463___wa_chat_595981801463_9599": "Buenas_Tardes_Ivan",
        "165__p4759___wa_chat_595981724759_9299": "Vasectomia_Query",
        "Lid_104741417795691": "Piercing_Aftercare_Buyer",
        "Chat_595984682720": "Me_Dejaste_Tu_Numero",
        "Chat_595985219034": "Regalo_Coordinacion",
        # 30-39 msgs
        "Lid_76824231051438": "Hola_Ivan_Que_Tal",
        "Lid_105909749575890": "Jose_Balcarse",  # "Le saluda Jose Balcarse"
        "Lid_95150772617227": "Consulta_Agenda",
        "Lid_63741810978885": "Lid_63741810978885",
        "johana_candidate___wa_chat_595971179825_36": "Johana_Candidate",
        "Chat_595992282576": "Saffi_Farra",
        "143__p1488___wa_chat_595974621488_7274": "San_Lorenzo_25",
        "Lid_61478682030117": "Uber_Crashea_Casa",  # "Si estás dead en la calle avisa y pongo Uber"
        "Lid_163857968414803": "Spray_Pimienta_Query",
        "188__p7377___wa_chat_595984247377_10541": "IA_Startup_Query",
        "154__p4734___wa_chat_595981204734_10154": "CI_Number_Request",
        "Lid_108796538007729": "Saul_Goodman_Page",  # "Hola te paso pag de Saúl goodman"
        "Lid_264020246429711": "Pedido_Query",
        "178__p6474___wa_chat_595983206474_9890": "INSIGNIA_07_Query",
        "Lid_56466706821352": "Lid_56466706821352",
        "156__p1606___wa_chat_595981321606_10229": "Vine_Con_Mama",
        "Lid_69123354693709": "Weissvanderpol_Chat",
        "142__p2313___wa_chat_595974612313_9192": "Tamara_Tienda_Movil",
        "230__p0194___wa_chat_595991810194_7797": "FPUNA_Estudiante",
        "193__p1669___wa_chat_595984751669_667": "Nro_Ale_Request",
        "171__p8373___wa_chat_595982418373_4145": "Podes_Reenviar",
        "Lid_233264069500985": "Pedido_Numero_Bot",
    }

    renamed = 0
    skipped = 0
    for old, new in MANUAL_MAP.items():
        if old == new:
            skipped += 1
            continue
        src = WA / old
        dst = WA / new
        if not src.exists():
            skipped += 1
            continue
        if dst.exists() and dst != src:
            shutil.rmtree(src)
            print(f"  DELETED (dup): {old}")
            continue
        shutil.move(str(src), str(dst))
        print(f"  RENAMED: {old} -> {new}")
        renamed += 1

    print("\n=== Summary ===")
    print(f"  Renamed: {renamed}")
    print(f"  Skipped: {skipped}")


if __name__ == "__main__":
    main()
