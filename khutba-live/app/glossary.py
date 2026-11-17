"""Lexique islamique : sert à la fois
1) à guider la reconnaissance vocale (phrase list Azure) ;
2) à imposer une traduction cohérente au traducteur (prompt système, mis en cache).

Ajoutez librement vos termes : (forme arabe, translittération, rendu français).
"""

# (arabe, translittération usuelle, traduction / règle en français)
TERMES = [
    # Formules
    ("بسم الله الرحمن الرحيم", "Bismillah ar-Rahman ar-Rahim", "Au nom d'Allah, le Tout Miséricordieux, le Très Miséricordieux"),
    ("الحمد لله", "al-hamdu lillah", "Louange à Allah"),
    ("سبحانه وتعالى", "subhanahu wa ta'ala", "Gloire à Lui, l'Exalté (ou : exalté soit-Il)"),
    ("صلى الله عليه وسلم", "sallallahu 'alayhi wa sallam", "ﷺ (garder le symbole après « le Prophète »)"),
    ("رضي الله عنه", "radiyallahu 'anhu", "(qu'Allah l'agrée)"),
    ("رضي الله عنها", "radiyallahu 'anha", "(qu'Allah l'agrée)"),
    ("رحمه الله", "rahimahullah", "(qu'Allah lui fasse miséricorde)"),
    ("إن شاء الله", "in cha Allah", "si Allah le veut"),
    ("ما شاء الله", "ma cha Allah", "ma cha Allah"),
    ("أستغفر الله", "astaghfirullah", "je demande pardon à Allah"),
    ("آمين", "amin", "Amin"),
    ("أما بعد", "amma ba'd", "Ceci dit, …"),
    ("عباد الله", "'ibad Allah", "Serviteurs d'Allah"),
    ("أيها المؤمنون", "ayyuha al-mu'minun", "Ô croyants"),
    ("معاشر المسلمين", "ma'ashir al-muslimin", "Ô assemblée des musulmans"),
    ("أقول قولي هذا وأستغفر الله لي ولكم", "", "Je dis ces paroles et je demande pardon à Allah pour moi et pour vous"),
    # Noms d'Allah / Prophète
    ("الله", "Allah", "Allah (ne jamais traduire par « Dieu » seul)"),
    ("الرحمن", "ar-Rahman", "le Tout Miséricordieux"),
    ("الرحيم", "ar-Rahim", "le Très Miséricordieux"),
    ("رسول الله", "Rasul Allah", "le Messager d'Allah ﷺ"),
    ("النبي", "an-Nabi", "le Prophète ﷺ"),
    ("سيدنا محمد", "sayyidina Muhammad", "notre maître Muhammad ﷺ"),
    # Sources
    ("القرآن الكريم", "al-Qur'an al-karim", "le Noble Coran"),
    ("آية", "aya", "verset"),
    ("سورة", "sourate", "sourate"),
    ("الحديث", "hadith", "hadith"),
    ("السنة", "Sunna", "la Sunna"),
    ("الصحابة", "as-sahaba", "les Compagnons"),
    ("السلف الصالح", "as-salaf as-salih", "les pieux prédécesseurs"),
    ("الفقه", "fiqh", "le fiqh (jurisprudence)"),
    ("المذهب المالكي", "al-madhhab al-maliki", "l'école malikite"),
    # Culte
    ("الصلاة", "salat", "la prière"),
    ("الجمعة", "al-jumu'a", "le vendredi / la prière du vendredi"),
    ("الخطبة", "khutba", "le sermon (khutba)"),
    ("الزكاة", "zakat", "la zakat (aumône obligatoire)"),
    ("الصدقة", "sadaqa", "l'aumône (sadaqa)"),
    ("الصيام", "siyam", "le jeûne"),
    ("رمضان", "Ramadan", "Ramadan"),
    ("الحج", "hajj", "le pèlerinage (hajj)"),
    ("العمرة", "'umra", "la 'umra"),
    ("الوضوء", "wudu'", "les ablutions"),
    ("الدعاء", "du'a", "l'invocation"),
    ("الذكر", "dhikr", "le rappel d'Allah (dhikr)"),
    ("المسجد", "masjid", "la mosquée"),
    ("القبلة", "qibla", "la qibla"),
    # Notions
    ("التقوى", "taqwa", "la piété (taqwa)"),
    ("الإيمان", "iman", "la foi"),
    ("الإحسان", "ihsan", "l'excellence (ihsan)"),
    ("التوحيد", "tawhid", "l'unicité d'Allah (tawhid)"),
    ("الشرك", "shirk", "l'association (shirk)"),
    ("التوبة", "tawba", "le repentir"),
    ("الآخرة", "al-akhira", "l'au-delà"),
    ("الدنيا", "ad-dunya", "la vie d'ici-bas"),
    ("الجنة", "al-janna", "le Paradis"),
    ("النار", "an-nar", "l'Enfer (le Feu)"),
    ("يوم القيامة", "yawm al-qiyama", "le Jour de la Résurrection"),
    ("الحلال", "halal", "le licite"),
    ("الحرام", "haram", "l'illicite"),
    ("البدعة", "bid'a", "l'innovation (bid'a)"),
    ("الأمة", "al-umma", "la communauté (Oumma)"),
    ("صلة الرحم", "silat ar-rahim", "le maintien des liens familiaux"),
    ("بر الوالدين", "birr al-walidayn", "la bienfaisance envers les parents"),
    ("الغيبة", "ghiba", "la médisance"),
    ("الصبر", "sabr", "la patience"),
    ("الشكر", "shukr", "la gratitude"),
    ("الرزق", "rizq", "la subsistance"),
    ("القدر", "qadar", "le destin"),
]

# Darija courante dans les khoutbas (aide le traducteur à ne pas se tromper)
DARIJA = [
    ("بزاف", "beaucoup"),
    ("دابا", "maintenant"),
    ("واش", "est-ce que"),
    ("شنو / آش", "quoi"),
    ("علاش", "pourquoi"),
    ("كيفاش", "comment"),
    ("فين", "où"),
    ("خاصنا", "nous devons"),
    ("ماشي", "ce n'est pas"),
    ("حيت / حيث", "parce que"),
    ("ديال", "de (possessif)"),
    ("الناس", "les gens"),
    ("الدراري", "les enfants"),
    ("الواليدين", "les parents"),
    ("كنقولو", "nous disons"),
    ("غادي", "va / allons (futur)"),
    ("مزيان", "bien"),
    ("خايب", "mauvais"),
    ("بغينا", "nous voulons"),
    ("عافاكم", "je vous en prie / s'il vous plaît"),
    ("الله يهدينا", "qu'Allah nous guide"),
    ("الله يرحم الوالدين", "qu'Allah fasse miséricorde à vos parents"),
]


def phrases_pour_stt() -> list[str]:
    """Liste de mots/expressions à favoriser par la reconnaissance vocale."""
    out = [t[0] for t in TERMES]
    out += [d[0].split(" / ")[0] for d in DARIJA]
    return out


def glossaire_texte() -> str:
    lignes = ["# Lexique imposé (arabe → français)"]
    for ar, tr, fr in TERMES:
        lignes.append(f"- {ar}" + (f" ({tr})" if tr else "") + f" → {fr}")
    lignes.append("\n# Darija marocaine fréquente")
    for ar, fr in DARIJA:
        lignes.append(f"- {ar} → {fr}")
    return "\n".join(lignes)
