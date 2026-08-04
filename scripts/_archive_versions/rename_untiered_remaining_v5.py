#!/usr/bin/env python3
"""Final rename pass for remaining 4+ msg untiered_personal."""

from __future__ import annotations

import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH" / "wa_messages/untiered_personal"


def main():
    MANUAL_MAP = {
        # 60 msgs
        "Lid_264647361974519": "Lid_264647361974519",  # empty first msg
        # 23 msgs
        "Lid_116647134245016": "Lid_116647134245016",  # simple "Hola"
        # 16 msgs
        "Lid_2083797373166": "Lid_2083797373166",  # empty first msg
        # 7 msgs
        "Chat_595991851222": "Chat_595991851222",  # empty
        # 6 msgs - more identities
        "Lid_40570311434494": "Compra_Minima_Query",
        "Lid_159961812320427": "Kinda_Random_IA_Stuff",  # "kinda random, recorde que estabas kinda into IA stuff"
        "Lid_119769609064508": "Suno_Music_Share",
        "Lid_119259044835572": "Metxmorfosis_Chat",  # "Hola Metxmorfosis" (Ivan's nickname)
        "Chat_595994538574": "Podcast_Query",
        "Chat_595992468570": "Haupeiii_Chat",
        "Chat_595986743708": "Brosco_Empresas_Query",
        "Chat_595985475708": "Hola_Ivan_595",
        "Chat_595983771093": "Hola_583",
        "Chat_595983249641": "CV_Github_Recruitment",  # "Te paso mi cv"
        "Chat_595982945349": "Hola_Buen_Dia_Chat",
        "Chat_595972902266": "Monchis_Driver_2",
        "Chat_595972273973": "App_Experience_Consulta",
        "Chat_595971636509": "Multijuegos_VB_Jenga",  # "Multijuegos VB alquiler jenga gigante"
        "Chat_595971545477": "Esta_El_Profe",
        "Chat_595962133580": "Gift_Delivery_Ubi",  # "entregarte el regalo"
        "Chat_5491161048979": "Dr_Demian_Glujovsky",  # "soy el Dr. Demián Glujovsky"
        "Chat_50257029309": "Lorena_Meet_Offer",  # "Hola Lorena, Estoy libre"
        # 5 msgs
        "Lid_89485660393604": "Buenas_Lid_894",
        "Lid_49074850025489": "Monchis_Driver_3",
        "Lid_32178616434715": "Medical_Reports_Bot",
        "Lid_266751929544901": "Hoka_Lid_266",
        "Lid_239105191460998": "Vasectomia_Viernes_13",  # "vasectomia queda para viernes 13"
        "Lid_195133299544069": "Eliana_Assertia_Solutions",  # "mi nombre es Eliana de Assertia"
        "Lid_154310071607477": "Correo_Campus_TEMU",  # "Agencia de CORREO CAMPUS UNA, recibiste un paquete TEMU"
        "Lid_139088824914000": "More_Info_Query_2",
        "Chat_595992725319": "Jessi_69dotcom_Photos",  # "Jessi vi tus fotos en 69.com.py"
        "Chat_595992679747": "Es_Mio_Solo_Que_No_Fui",
        "Chat_595986780732": "Pausanti_Delivery",
        "Chat_595985555225": "Cafeteria_1M_Query",
        "Chat_595985526379": "Happy_Birthday_Uwuwu",
        "Chat_595984312615": "Hot_Photos_Vi",  # "vi tus fotos en Hot"
        "Chat_595984175112": "Chatbot_Interior_Webinar",
        "Chat_595983444251": "Manuel_Cruz_Alexander_Coworker",  # "Manuel cruz compañero de Alexander"
        "Chat_595983153932": "Qtal_Amigo_Chat",
        "Chat_595981945426": "Te_Llame_Recien",
        "Chat_595976900782": "Entrevista_Medio_Query",
        "Chat_595973908532": "Hola_Chat_597",
        "Chat_595961103376": "Hola_Chat_596",
        "Chat_359876591429": "Kate_Money_Question",  # "Hey it's Kate!"
        "Chat_34650513549": "Vacantes_Share",  # "compartiré todas las vacantes"
        "Chat_18492797199": "No_Broncas_Agencia",  # "no ando buscando broncas"
        # 4 msgs
        "Lid_130219130274040": "Hola_Lid_130",
        "Chat_62882162936422": "Esperando_Gran_Dia",
        "Chat_595992720978": "Ubicacion_Buenas_Noches",
        "Chat_595991921600": "Numero_Equivocado_Frank",
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
