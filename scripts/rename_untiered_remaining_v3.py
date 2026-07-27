#!/usr/bin/env python3
"""Final rename pass for remaining 10-29 msg untiered_personal."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH" / "wa_messages/untiered_personal"


def main():
    MANUAL_MAP = {
        # 30+ msgs
        "Lid_276639095242788": "Chill_Spanish_Friend",
        "Lid_159223061151983": "Dealer_Galletitas_Buyer",
        "Lid_57797458792574": "Kink_Castigos_Friend",
        "Chat_595971353082": "Credit_Spam_4",
        "Lid_217278167707806": "Thijs_Dutch_Guy_Chat",
        "Lid_47094433870013": "Hola_Ivan_Chat",
        "Lid_94898074173672": "Que_Tal_Lid_94",
        "Lid_180135860912324": "Hola_Que_Tal_180",
        "Lid_224184944877725": "Holaaa_224",
        "Lid_8212749230246": "Argentina_Uwuwu",
        "Lid_264647361974519": "Lid_264647361974519",  # empty first msg
        "Lid_63741810978885": "Holaaaa_637",
        "Chat_595981701701": "Buenas_595981701701",
        "Lid_56466706821352": "Hola_Que_Tal_564",
        "Lid_193097552105524": "Oreja_Transversal_Piercing",
        "Lid_94206383145183": "Prestamo_Query",
        "Lid_6043606212799": "Solo_San_Lorenzo_25",  # "soy solo de 25 de san lorenz"
        "Lid_248085934555139": "La_Luna_Es_Mia_Tienda",
        "Lid_218051244990519": "Che_Varea_Grill",

        # 10-29 msgs
        "Lid_142344342999195": "ETA_Coordinator",
        "Lid_116647134245016": "Lid_116647134245016",
        "Chat_595986647270": "Poke_Sushi_Delivery_2",
        "Chat_595961888226": "Haciendo_Solo_Tambien",
        "Chat_595981272697": "Luis_Vargas_Woden",  # "Luis Vargas te escribo de la empresa Woden"
        "Lid_2083797373166": "Lid_2083797373166",
        "Chat_595994385693": "Estimado_Ivan_Inconveniente",
        "Lid_176768824672276": "Grindr_Contact",
        "Chat_595981319885": "Que_Tal_Bro",
        "Chat_595971758036": "Yo_Quiero_Chat",
        "Chat_595981279546": "Que_Tal_Chat",
        "Chat_595983468273": "Castracion_Perras_Vet",
        "Chat_595981907662": "Koi_Delivery_La",
        "Chat_18888317121": "Hi_Yeah_Chat",
        "Chat_595991366842": "Buenas_Tardes_591",
        "Chat_595985745553": "IA_Agentic_Friend",  # "vos tambien estas jugando con IAs?"
        "Chat_595984151099": "Como_Lo_Que_Vos_Sabes",
        "Lid_48284106268799": "Profe_Pre_Clase_Query",
        "Lid_267318881976338": "Coffeecatpy_Insta",
        "Lid_79062059982857": "How_Re_You_AI_Friend",  # "How're you doing? I'm doing ai and agentic"
        "Chat_595984244310": "Buenas_584",
        "Chat_595985434234": "Buenas_Tardes_585",
        "Lid_204333220114444": "Jesus_Cami_Maidana_Referral",  # "Hola Jesús. Me pasó Camí Maidana"
        "Lid_63226951774393": "Me_Escribiste_Query",
        "Chat_595971885483": "Buen_Dia_Chat",
        "Chat_595983858997": "Holaaa_Chat",
        "Chat_595983031680": "Hola_Buenos_Dias",
        "Chat_595981190096": "Hola_Buenas_Noches",
        "Chat_34666604366": "Alonso_Motivus",  # "Alonso de Motivus"
        "Lid_162681097076843": "Temu_AliExpress_Pedidos",
        "Lid_165768624893999": "Remera_Lila_Talla_M_G",
        "Chat_595982388158": "Repo_BD2_Interesado",  # "Me interesa tu repo XD bd2"
        "Chat_996555325969": "TAGG_Gerente_RRHH",  # "Soy Gerente de Recursos Humanos en TAGG"
        "Lid_92750439571663": "Buenas_Lid_927",
        "Chat_13055654317": "Asistencia_Viajero_Query",
        "Lid_109581929844874": "Opciones_Llevar_Compartir",
        "Chat_918617838526": "Encantado_Conocerte",
        "Chat_595982756474": "Hola_Que_Tal_595",
        "Chat_595972546898": "Buenas_Amigo_Chat",
        "Lid_239925580546072": "Hello_More_Info_Query",
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

    print(f"\n=== Summary ===")
    print(f"  Renamed: {renamed}")
    print(f"  Skipped: {skipped}")


if __name__ == "__main__":
    main()