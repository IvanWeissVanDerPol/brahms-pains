#!/usr/bin/env python3
"""Rename remaining 7-9 msg untiered_personal chats."""

from __future__ import annotations

import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH" / "wa_messages/untiered_personal"


def main():
    MANUAL_MAP = {
        # 60+ msgs
        "Lid_264647361974519": "Lid_264647361974519",  # Empty first msg - leave as-is
        # 23 msgs
        "Lid_116647134245016": "Lid_116647134245016",  # Empty first msg - leave as-is
        # 16 msgs
        "Lid_2083797373166": "Lid_2083797373166",  # Empty first msg - leave as-is
        # 7-9 msgs with identity
        "Chat_13135550002": "Messages_Query",
        "Chat_2347045635469": "Sarah_Sin_Fines_Lucro",  # "Sarah, Organización Sin Fines de Lucro"
        "Chat_31625105226": "Richard_Alicia_Kannekens_Referral",  # "Alicia Kannekens passed me your contact"
        "Chat_33617854901": "Doing_Something_Query",
        "Chat_5491173660945": "El_Alquimista_Colegiales_AR",  # "El Alquimista Colegiales, Paraguay"
        "Chat_56942458964": "United_Airlines_Number_Query",
        "Chat_595972808418": "Es_Ale_Number",
        "Chat_595972862043": "Hola_Que_Tal_595",
        "Chat_595972908916": "Arirang_QR_Chat",
        "Chat_595976161000": "Irritacion_Piel_Huevos_Query",
        "Chat_595976933610": "Pedido_Arribo_Query",
        "Chat_595981825140": "Ivan_Self_Intro_Chat",
        "Chat_595981945931": "Doctor_Visit_Query",
        "Chat_595981973355": "Hugo_Calcumath",  # "Soy Hugoo, alias Calcumath🧮"
        "Chat_595983595027": "Que_Tal_Weiss",
        "Chat_595984607510": "Delivery_San_Lorenzo",
        "Chat_595984872609": "Vos_Con_Lau_Query",
        "Chat_595984962826": "Poke_Sushi_Ubicacion",
        "Chat_595985552000": "Gustavo_QA_Practica",  # "Hola Gustavo, de la práctica de QA"
        "Chat_595986652329": "Cunada_De_Laura",  # "Soy la cuñada de Laura"
        "Chat_595987122940": "Holiiis_Chat",
        "Chat_595991851222": "Chat_595991851222",  # empty
        "Chat_595992228058": "Confirmacion_Final_Query",
        "Chat_595992297541": "Recepcion_Imagenes",
        "Lid_258617261465627": "De_Donde_Sos_Query",
        "Lid_89220043534564": "CI_Number_Request_2",
        "Chat_15617591585": "Jeweler_Grindr",  # "Jeweler from Grindr"
        "Chat_595976909490": "Casa_Cuanto_Pasan",
        "Chat_595981516108": "Estoy_Para_La_No",
        "Chat_595981556506": "Piercing_Titaneo_Disenos",
        "Chat_595981586063": "Monchis_Driver",
        "Chat_595982429294": "Sole_Laptop_Tech_Support",  # "Hola Sole, problemas con mi laptop"
        "Chat_595987111437": "Te_Veo_Chat",
        "Chat_595991182268": "Zonaroja_Anuncio_Query",
        "Lid_137624291393721": "Laviejaholanda_Muebles_Vintage",
        "Lid_37371181568043": "Estufa_Ubi_Query",
        "Lid_92968996368548": "Buenas_Lid_929",
        "Chat_595972913916": "Pasaron_Tu_Numero",
        "Chat_595973512556": "Reforestacion_Drones_Video",
        "Chat_595981210320": "Buenos_Dias_595",
        "Chat_595981541913": "Buenas_Tardes_595",
        "Chat_595981781796": "Nissei_Salesperson",
        "Chat_595982501582": "Maria_Riveros_Bristol",  # "María Riveros asesora de Bristol"
        "Chat_595986139619": "Alejandro_Chat",
        "Chat_595986831760": "Hola_Por_Donde",
        "Chat_595992026352": "More_Info_English_Query",
        "Chat_59899000784": "Itau_UY_Bot",
        "Lid_1159674785945": "Lara_Number_Referral",  # "Me pasó tu número Lara"
        "Lid_57205206347846": "Sin_Reserva_Tienda",
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
