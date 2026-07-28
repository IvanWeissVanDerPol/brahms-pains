#!/usr/bin/env python3
"""Continue renaming remaining untiered_personal chats with identity."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WA = REPO / "SOURCE_OF_TRUTH" / "wa_messages/untiered_personal"


def main():
    MANUAL_MAP = {
        # 20-29 msgs
        "204__p8337___wa_chat_595985508337_5804": "Dolly_Sabanas",  # "soy Dolly tu mamá me dijo que necesitan sábanas"
        "168__p6355___wa_chat_595981816355_9271": "Buenas_168p6355",
        "214__p9915___wa_chat_595986169915_1860": "Fabricio_Mendoza_AIESEC",  # "Te saluda Fabricio Mendoza de AIESEC"
        "144__p3758___wa_chat_595976123758_9811": "Sol_Visuar_Ecommerce",  # "te Saluda Sol de visuar e-commerce"
        "155__p5412___wa_chat_595981285412_9804": "Holiiis_Chat",
        "128__p7980___wa_chat_595971727980_3616": "Google_Maps_Interest",
        "106__p5319___wa_chat_5212215805319_11532": "Tinder_Match",  # "hicimos match en Tinder"
        "Lid_264098176585956": "Vasectomia_Query_2",
        "219__p1824___wa_chat_595986551824_11679": "Soy_Solo_Chat",
        "185__p6852___wa_chat_595984106852_10933": "Hello_Uwuw",
        "Lid_127702967255270": "Hola_Bro",
        "Chat_595983864324": "Delivery_Hasta_Acá",
        "196__p8527___wa_chat_595984898527_10680": "Que_Tal_196p8527",
        "158__p7867___wa_chat_595981417867_9058": "Mail_IT_Alizanza",
        "Lid_126641942577239": "Buenas_Lid_126",
        "Chat_595981611611": "Tigo_Bot_Liza",
        "Lid_116647134245016": "Lid_116647134245016",
        "Chat_595986246274": "Bueno_Dia_Chat",
        "231__p2405___wa_chat_595991852405_9217": "Jose_Insfran_Weiss",  # "mi nombre es JOSE INSFRAN"
        "173__p3536___wa_chat_595982733536_6569": "Sole_Laptop_Help",  # "Hola Sole Soy Iván Weiss, problemas con laptop"
        "136__p1492___wa_chat_595972391492_3663": "BD2_Query",
        "Lid_97869453389924": "Mario_Asado",  # "Querés caer en lo de Mario"
        "Lid_32569055793373": "Ivan_25_Self_Intro",  # "Hola yo soy Iván de 25"
        "Lid_27660126265454": "Entradas_Query",
        "Lid_265755698413630": "Mi_Loco",
        "Chat_595981396088": "After_Talentoso",
        "Chat_595981231604": "Holis_Como_Estas",
        "221__p4914___wa_chat_595986804914_6611": "Combos_Fruit_Query",
        "Lid_6808060059709": "Mas_Info_Query",
        "Lid_270789232308448": "Hola_Te_Ayudo",
        "Chat_595982191340": "Romina_Tupi_Electro",  # "le saluda Romina Gonzalez de Tupi"
        "135__p9084___wa_chat_595972179084_4679": "Test_Automation_Experience",
        "Lid_199570671841348": "Amanda_Chat",  # already named Lid_ but kept
        "Lid_196542485012495": "Olga_Referral",  # "Me pasó tu número Olga"
        "Chat_595991447905": "Wow_Foto_Chat",
        "247__p5246___wa_chat_595994445246_6538": "Taller_Invierno_Ivan",  # "taller de invierno de Introducción al a"

        # 10-19 msgs
        "Lid_83386857160841": "Fernando_Norte_Single_Bi",
        "Chat_595993390824": "Skokka_Luana_Ad",
        "197__p0920___wa_chat_595984900920_9052": "Augusto_Chat",  # "Augusto soy"
        "162__p9125___wa_chat_595981609125_10582": "Grafimark_Francisco",  # business
        "Lid_803343483120": "Pagopar_Mariana",  # "Mariana Ibarra te saluda"
        "Lid_279907431121033": "Menu_Pass",
        "Lid_252068023513155": "OpenCode_Wall_AI",  # "agentic workflow in OpenCode"
        "Chat_595985879261": "Buenos_Dias_Chat",
        "Chat_595982340951": "Doc_Mod_Query",
        "125__p2994___wa_chat_595971652994_2127": "Ivan_Weiss_IIN_Colbes",  # "Soy Iván weiss de iin"
        "109__p5262___wa_chat_5491122505262_9620": "El_Alquimista_Grower",  # "El Alquimista - Grower Things"
        "Lid_187763085328400": "Isaac_Monchis_Pedido",
        "Chat_5491127039665": "WSP_Assist_00E9E00",  # WhatsApp support
        "Chat_15144029271": "Like_This_Chat",
        "Lid_93565963268321": "Isopropilico_precios",
        "Lid_228256204722393": "Remeras_Disenos_Query",
        "Lid_222062828380404": "En_Verdad_Te_Gustaria",
        "Chat_595992531288": "Que_Tal_Amigo",
        "Chat_595992217506": "Soy_Solo_Short",
        "Chat_595986493535": "Textura_Goma_Print",
        "Chat_595985272826": "Edificio_Brasilia",
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