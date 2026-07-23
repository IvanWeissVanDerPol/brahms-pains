# WhatsApp corpus triage — psychology-analysis relevance (v2)

Total chats analyzed: **769**

Groups analyzed (with extracted participants): **171**


## v2 changes (July 2026)

- Added **group co-membership** scoring: contacts in ≥2 of Ivan's groups are
  treated as `hidden_friend` even if their 1-on-1 chat has few messages.
- New score component: `groups_shared_with_ivan * 800`.
- New category: `hidden_friend` (with score floor of 200 so they don't drop).
- Circle assignment output in `_triage_circles.json` and downstream symlinks in `circles/`.

## Category breakdown

| Category | # chats | total msgs | my text chars |
|---|---:|---:|---:|
| personal_1on1 | 324 | 254,578 | 6,176,517 |
| notification | 89 | 41,459 | 859,121 |
| low_signal | 335 | 1,311 | 35,398 |
| hidden_friend | 21 | 141 | 6,624 |

**Recommended KEEP** (personal / active-group / hidden-friend, score ≥ 500): 270 chats
**Recommended DROP** (notification / low-signal): 424 chats
**🚨 Hidden friends RESCUED** (high group overlap, low 1-on-1 volume): 21 chats

### Hidden friends (rescued from `low_signal`)

| JID | Groups | Msgs | Score | Circle | Suggested tier |
|---|---:|---:|---:|---|---|
| `595984708142` | 13 | 6 | 10440.0 | `fpuna_cs_classmates` | tier2_core |
| `595972124230` | 6 | 3 | 4831.7 | `fpuna_cs_classmates` | tier3_extended |
| `595991469087` | 6 | 5 | 4809.8 | `pytesting_community` | tier3_extended |
| `595961525896` | 4 | 5 | 3270.2 | `fpuna_cs_classmates` | tier3_extended |
| `595984264979` | 4 | 3 | 3252.5 | `fpuna_cs_classmates` | tier3_extended |
| `595972808418` | 4 | 7 | 3240.9 | `fpuna_cs_classmates` | tier3_extended |
| `595972386499` | 4 | 3 | 3200.0 | `fpuna_cs_classmates` | tier3_extended |
| `595986743708` | 3 | 6 | 3296.2 | `fpuna_cs_classmates` | tier3_extended |
| `595983858997` | 3 | 12 | 2698.3 | `fpuna_cs_classmates` | tier3_extended |
| `595971545477` | 3 | 6 | 2402.7 | `fpuna_cs_classmates` | tier3_extended |
| `595992222691` | 2 | 3 | 7883.3 | `pytesting_community` | tier3_extended |
| `595993598454` | 2 | 8 | 2511.9 | `fpuna_cs_classmates` | tier3_extended |
| `13135550002` | 2 | 7 | 2031.7 | `inner_circle_casa_weiss` | tier3_extended |
| `595992282576` | 2 | 39 | 1999.5 | `fpuna_cs_classmates` | tier3_extended |
| `595994609417` | 2 | 7 | 1800.0 | `fpuna_cs_classmates` | tier3_extended |
| `595973908532` | 2 | 5 | 1792.0 | `pytesting_community` | tier3_extended |
| `595971792390` | 2 | 1 | 1669.0 | `fpuna_cs_classmates` | tier3_extended |
| `595994723736` | 2 | 4 | 1668.8 | `fpuna_cs_classmates` | tier3_extended |
| `595981685815` | 2 | 9 | 1612.5 | `fpuna_cs_classmates` | tier3_extended |
| `595982138376` | 2 | 1 | 1601.5 | `other_contacts` | tier3_extended |
| `595971722516` | 2 | 1 | 1600.0 | `fpuna_cs_classmates` | tier3_extended |

## Top 50 chats by psychology signal

| # | slug | category | msgs | mine% | groups | audio | starred | long | my_chars | span_d | score |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `ami_school___wa_chat_595981225272_62` | personal_1on1 | 28,457 | 52% | 1 | 3175 | 4 | 172 | 473,856 | 2114.9 | 896,122.1 |
| 2 | `_wa_chat_595983008816_9253` | personal_1on1 | 325 | 97% | 0 | 0 | 0 | 305 | 391,776 | 0.0 | 730,526.3 |
| 3 | `02__p8816___wa_chat_595983008816_9253` | personal_1on1 | 325 | 97% | 0 | 0 | 0 | 305 | 391,776 | 0.0 | 730,526.3 |
| 4 | `laura_x___wa_chat_595976538689_3231` | personal_1on1 | 23,105 | 51% | 6 | 2921 | 2 | 87 | 322,316 | 967.4 | 668,531.8 |
| 5 | `jonathan_verdun___wa_chat_595971922708_3654` | personal_1on1 | 34,526 | 32% | 1 | 1674 | 1 | 204 | 473,883 | 842.9 | 662,281.1 |
| 6 | `05__lourdes_youko_kurama___wa_chat_595981791823_1683` | personal_1on1 | 16,905 | 50% | 0 | 2261 | 4 | 99 | 304,558 | 1502.7 | 584,755.3 |
| 7 | `06__p4569___wa_chat_595981324569_1092` | personal_1on1 | 663 | 100% | 0 | 1 | 0 | 278 | 241,499 | 559.2 | 502,466.9 |
| 8 | `_wa_chat_595971167729_9255` | personal_1on1 | 364 | 99% | 0 | 0 | 0 | 356 | 188,801 | 0.0 | 460,691.7 |
| 9 | `07__p7729___wa_chat_595971167729_9255` | personal_1on1 | 364 | 99% | 0 | 0 | 0 | 356 | 188,801 | 0.0 | 460,691.7 |
| 10 | `gabriel_g_curuguaty___wa_chat_595982515138_64` | personal_1on1 | 11,305 | 50% | 1 | 1727 | 3 | 118 | 218,225 | 2119.1 | 456,239.7 |
| 11 | `07__kiki_hermana___wa_chat_595985724135_111` | personal_1on1 | 7,838 | 49% | 4 | 552 | 0 | 105 | 282,308 | 2108.9 | 395,026.2 |
| 12 | `10__alejandro_cabral___wa_chat_595972130867_49` | personal_1on1 | 23,000 | 46% | 26 | 991 | 1 | 59 | 222,535 | 2121.3 | 369,123.0 |
| 13 | `11__p3549___wa_chat_595976333549_9257` | personal_1on1 | 238 | 99% | 0 | 0 | 0 | 233 | 120,166 | 0.0 | 296,244.3 |
| 14 | `09__p3549___wa_chat_595976333549_9257` | personal_1on1 | 238 | 99% | 0 | 0 | 0 | 233 | 120,166 | 0.0 | 296,244.3 |
| 15 | `12__p3082___wa_chat_595971353082_9263` | personal_1on1 | 202 | 99% | 0 | 0 | 0 | 201 | 104,044 | 0.0 | 256,045.8 |
| 16 | `10__p3082___wa_chat_595971353082_9263` | personal_1on1 | 202 | 99% | 0 | 0 | 0 | 201 | 104,044 | 0.0 | 256,045.8 |
| 17 | `fpuna_alvaro_alt___wa_chat_595986805654_1271` | personal_1on1 | 7,392 | 46% | 23 | 718 | 0 | 42 | 109,330 | 1718.3 | 220,533.6 |
| 18 | `14__friend_brasilia___wa_chat_595983822921_11297` | personal_1on1 | 3,898 | 54% | 0 | 136 | 0 | 62 | 140,774 | 350.4 | 192,930.5 |
| 19 | `skype_friend___wa_chat_595981925772_1253` | personal_1on1 | 4,230 | 54% | 21 | 185 | 0 | 33 | 130,686 | 1701.3 | 191,599.6 |
| 20 | `helpp_friend___wa_chat_595981868718_92` | personal_1on1 | 3,985 | 56% | 17 | 230 | 0 | 30 | 67,874 | 2018.3 | 127,881.7 |
| 21 | `16__friend_alvaro___wa_chat_595962291837_9625` | personal_1on1 | 4,269 | 51% | 1 | 637 | 0 | 11 | 51,715 | 437.2 | 123,566.8 |
| 22 | `18__friend_ann_group___wa_chat_595985725366_99` | personal_1on1 | 2,788 | 59% | 4 | 424 | 0 | 18 | 46,069 | 2102.2 | 109,402.0 |
| 23 | `ann_kink___wa_chat_595991549029_1956` | personal_1on1 | 5,155 | 41% | 5 | 240 | 0 | 27 | 70,771 | 1269.8 | 108,986.1 |
| 24 | `guitar_friend___wa_chat_595985725871_86` | personal_1on1 | 4,121 | 48% | 3 | 316 | 0 | 13 | 50,551 | 1796.1 | 94,122.5 |
| 25 | `21__friend_casual___wa_chat_595994341668_1955` | personal_1on1 | 1,667 | 48% | 1 | 60 | 0 | 15 | 68,447 | 1212.7 | 84,412.6 |
| 26 | `22__cesar_poli___wa_chat_595991470829_106` | personal_1on1 | 3,157 | 53% | 18 | 126 | 0 | 16 | 36,356 | 1995.7 | 76,688.9 |
| 27 | `becas_kansas_friend___wa_chat_595984933862_1330` | personal_1on1 | 2,877 | 50% | 20 | 105 | 0 | 9 | 41,266 | 1362.1 | 75,155.3 |
| 28 | `22__friend_tiktok_share___wa_chat_595985249907_9628` | personal_1on1 | 2,399 | 53% | 1 | 152 | 0 | 26 | 43,757 | 426.1 | 75,131.9 |
| 29 | `compiladores_friend___wa_chat_595982510082_1723` | personal_1on1 | 1,432 | 49% | 16 | 81 | 0 | 11 | 40,984 | 1429.3 | 70,213.9 |
| 30 | `23__friend_uwu___wa_chat_595985340001_2439` | personal_1on1 | 4,098 | 40% | 0 | 278 | 0 | 11 | 36,195 | 1292.8 | 68,548.0 |
| 31 | `28__lilian_riveros___wa_chat_595983111686_3524` | personal_1on1 | 604 | 51% | 5 | 19 | 1 | 30 | 38,336 | 1061.2 | 62,064.4 |
| 32 | `25__sexshop_companion___wa_chat_595976569739_2083` | personal_1on1 | 1,128 | 53% | 1 | 47 | 0 | 18 | 42,567 | 1303.4 | 61,372.2 |
| 33 | `27__job_auto_response___wa_chat_595986418879_1688` | personal_1on1 | 896 | 66% | 0 | 61 | 0 | 29 | 30,863 | 1192.6 | 58,946.8 |
| 34 | `alvaro_drip___wa_chat_595984160109_1257` | personal_1on1 | 2,697 | 51% | 17 | 90 | 0 | 7 | 27,892 | 1683.4 | 57,911.1 |
| 35 | `30__kansas_springbreak___wa_chat_595972209763_2943` | personal_1on1 | 1,171 | 43% | 0 | 35 | 0 | 33 | 38,780 | 167.6 | 56,613.9 |
| 36 | `31__household_financial___wa_chat_15055778339_2872` | personal_1on1 | 598 | 52% | 0 | 36 | 0 | 21 | 34,677 | 1160.5 | 51,968.4 |
| 37 | `32__friend_youtube___wa_chat_595986138387_1265` | personal_1on1 | 1,864 | 37% | 1 | 38 | 0 | 24 | 35,886 | 1716.6 | 51,433.4 |
| 38 | `34__friend_simple___wa_chat_595973572212_1994` | personal_1on1 | 2,236 | 55% | 5 | 46 | 0 | 15 | 31,050 | 960.7 | 50,682.9 |
| 39 | `33__kiki_adjacent___wa_chat_595993553949_12779` | personal_1on1 | 2,525 | 50% | 0 | 121 | 0 | 7 | 32,991 | 228.1 | 49,053.8 |
| 40 | `qa_impostor_friend___wa_chat_595981258488_3525` | personal_1on1 | 1,327 | 46% | 4 | 98 | 0 | 10 | 29,847 | 388.0 | 47,441.1 |
| 41 | `35__friend_photos___wa_chat_595986868241_10607` | personal_1on1 | 726 | 44% | 1 | 63 | 0 | 10 | 35,815 | 179.8 | 46,200.9 |
| 42 | `alejandro_alt_2___wa_chat_595981459382_4380` | personal_1on1 | 327 | 54% | 5 | 9 | 0 | 20 | 18,185 | 731.2 | 35,409.4 |
| 43 | `044__p5289___wa_chat_595971505289_110` | personal_1on1 | 1,420 | 52% | 11 | 74 | 0 | 4 | 11,894 | 1431.7 | 33,208.4 |
| 44 | `38__friend_arrival___wa_chat_595986464184_1811` | personal_1on1 | 1,392 | 47% | 0 | 60 | 0 | 7 | 23,078 | 321.6 | 32,757.3 |
| 45 | `041__p9386___wa_chat_595986129386_1781` | personal_1on1 | 753 | 54% | 5 | 18 | 0 | 7 | 18,046 | 1336.8 | 30,918.3 |
| 46 | `045__p5424___wa_chat_595991705424_1202` | personal_1on1 | 703 | 49% | 7 | 29 | 0 | 14 | 13,001 | 744.8 | 29,925.6 |
| 47 | `043__p3357___wa_chat_595961943357_4695` | personal_1on1 | 612 | 53% | 5 | 16 | 0 | 10 | 15,864 | 944.4 | 28,871.6 |
| 48 | `061__p8035___wa_chat_595971378035_1724` | personal_1on1 | 642 | 51% | 17 | 17 | 0 | 3 | 9,836 | 746.0 | 28,281.4 |
| 49 | `40__victor_urgent___wa_chat_595981473912_1762` | personal_1on1 | 19 | 68% | 0 | 1 | 0 | 3 | 20,577 | 999.6 | 27,966.5 |
| 50 | `fpuna_uncertain___wa_chat_595991357332_1958` | personal_1on1 | 1,468 | 53% | 4 | 28 | 0 | 7 | 16,779 | 206.2 | 27,308.9 |

## Bottom 30 (candidates for drop)

| slug | category | msgs | mine% | groups | reason |
|---|---|---:|---:|---:|---|
| `097__lid_854912___wa_lid_118262125854912_15538` | notification | 5,060 | 48% | 2 | no participation |
| `lid_425545___wa_lid_113090817425545_13053` | notification | 15,598 | 40% | 5 | no participation |
| `lid_532196___wa_lid_206588111532196_14798` | notification | 3,825 | 42% | 0 | no participation |
| `lid_967999___wa_lid_96606732967999_13130` | notification | 2,151 | 53% | 0 | no participation |
| `lid_946676___wa_lid_154288881946676_13498` | notification | 3,539 | 14% | 39 | no participation |
| `lid_547891___wa_lid_158089659547891_14700` | notification | 2,588 | 49% | 2 | no participation |
| `lid_042926___wa_lid_170287115042926_13746` | notification | 83 | 43% | 1 | no participation |
| `lid_936873___wa_lid_42490228936873_15160` | notification | 336 | 38% | 0 | no participation |
| `lid_566845___wa_lid_137533459566845_13164` | notification | 1,210 | 44% | 1 | no participation |
| `lid_013386___wa_lid_214709794013386_13829` | notification | 814 | 50% | 0 | no participation |
| `lid_782842___wa_lid_245255651782842_15190` | notification | 578 | 50% | 0 | no participation |
| `_wa_lid_276639095242788_17033` | notification | 514 | 44% | 1 | no participation |
| `_wa_lid_171416456540224_13129` | notification | 208 | 59% | 3 | no participation |
| `_wa_lid_101722055782411_12984` | notification | 262 | 53% | 0 | no participation |
| `_wa_lid_174058297675951_15024` | notification | 332 | 46% | 1 | no participation |
| `_wa_lid_47094433870013_13326` | notification | 158 | 58% | 1 | no participation |
| `_wa_chat_31625105226_2952` | low_signal | 7 | 42% | 0 | too few msgs |
| `_wa_lid_137624291393721_16788` | low_signal | 8 | 62% | 0 | too few msgs |
| `_wa_lid_159223061151983_16955` | notification | 283 | 55% | 0 | no participation |
| `_wa_lid_58390113992826_13561` | notification | 89 | 58% | 1 | no participation |
| `_wa_lid_57797458792574_15073` | notification | 281 | 57% | 3 | no participation |
| `_wa_lid_227972770435229_13533` | notification | 257 | 57% | 0 | no participation |
| `_wa_lid_171790185791507_13193` | low_signal | 2 | 100% | 0 | too few msgs |
| `_wa_lid_31452213305549_13192` | low_signal | 2 | 100% | 0 | too few msgs |
| `_wa_lid_196542485012495_14659` | notification | 20 | 60% | 0 | no participation |
| `_wa_lid_189486155702510_15527` | notification | 125 | 45% | 5 | no participation |
| `_wa_chat_595971227824_5316` | low_signal | 7 | 28% | 1 | too few msgs |
| `_wa_chat_595992280435_9318` | low_signal | 8 | 50% | 0 | too few msgs |
| `_wa_lid_217278167707806_14595` | notification | 194 | 47% | 1 | no participation |
| `_wa_chat_595981472444_1308` | low_signal | 7 | 28% | 1 | too few msgs |
