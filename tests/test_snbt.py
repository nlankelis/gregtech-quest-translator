from gregtech_quest_translator.snbt import translate_snbt_text


def test_translate_snbt_text_uses_cache():
    original = '{display:{Name:"神剑"}, Lore:["这把剑非常锋利"]}'
    cache = {
        "神剑": "Divine Sword",
        "这把剑非常锋利": "This sword is very sharp",
    }

    translated, replaced = translate_snbt_text(original, cache)

    assert replaced == 2
    assert "Divine Sword" in translated
    assert "This sword is very sharp" in translated