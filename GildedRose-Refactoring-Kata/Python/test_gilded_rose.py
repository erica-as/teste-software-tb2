# -*- coding: utf-8 -*-
import pytest
from gilded_rose import GildedRose, Item


# T1 - Item normal "+5 Dexterity Vest", sell_in=5, quality=10
# Cobre: C1, C5
def test_normal_item_before_sell_by_date():
    """
    Cenário: Item normal com sell_in positivo e quality > 0
    Comandos cobertos:
    C1: item.quality = item.quality - 1 (pré-decremento)
    C5: item.sell_in = item.sell_in - 1
    """
    items = [Item("+5 Dexterity Vest", sell_in=5, quality=10)]
    GildedRose(items).update_quality()
    assert items[0].sell_in == 4
    assert items[0].quality == 9


# T2 - "Aged Brie", sell_in=5, quality=30
# Cobre: C2, C5
def test_aged_brie_before_sell_by_date():
    """
    Cenário: Aged Brie com sell_in positivo e quality < 50
    Comandos cobertos:
    C2: item.quality = item.quality + 1 (incremento base)
    C5: item.sell_in = item.sell_in - 1
    """
    items = [Item("Aged Brie", sell_in=5, quality=30)]
    GildedRose(items).update_quality()
    assert items[0].sell_in == 4
    assert items[0].quality == 31


# T3 - Backstage passes, sell_in=10, quality=40
# Cobre: C2, C3, C5
def test_backstage_pass_sell_in_10():
    """
    Cenário: Backstage passes com sell_in=10 (dentro da faixa < 11)
    Comandos cobertos:
    C2: item.quality = item.quality + 1 (incremento base)
    C3: item.quality = item.quality + 1 (bônus sell_in < 11)
    C5: item.sell_in = item.sell_in - 1
    """
    items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=40)]
    GildedRose(items).update_quality()
    assert items[0].sell_in == 9
    assert items[0].quality == 42  # +1 base +1 bônus <11


# T4 - Backstage passes, sell_in=5, quality=40
# Cobre: C2, C3, C4, C5
def test_backstage_pass_sell_in_5():
    """
    Cenário: Backstage passes com sell_in=5 (dentro das faixas < 11 e < 6)
    Comandos cobertos:
    C2: item.quality = item.quality + 1 (incremento base)
    C3: item.quality = item.quality + 1 (bônus sell_in < 11)
    C4: item.quality = item.quality + 1 (bônus sell_in < 6)
    C5: item.sell_in = item.sell_in - 1
    """
    items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=40)]
    GildedRose(items).update_quality()
    assert items[0].sell_in == 4
    assert items[0].quality == 43  # +1 base +1 bônus <11 +1 bônus <6


# T5 - "Sulfuras, Hand of Ragnaros", sell_in=0, quality=80
# Verifica que C5 NÃO é executado
def test_sulfuras_never_changes():
    """
    Cenário: Sulfuras - item lendário imutável
    Nenhum comando de alteração deve ser executado.
    C5 NÃO é executado: sell_in permanece igual
    """
    items = [Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80)]
    GildedRose(items).update_quality()
    assert items[0].sell_in == 0
    assert items[0].quality == 80


# T6 - Item normal "+5 Dexterity Vest", sell_in=-1, quality=10
# Cobre: C1, C5, C6
def test_normal_item_after_sell_by_date():
    """
    Cenário: Item normal vencido (sell_in negativo)
    Comandos cobertos:
    C1: item.quality = item.quality - 1 (pré-decremento)
    C5: item.sell_in = item.sell_in - 1
    C6: item.quality = item.quality - 1 (pós sell_in < 0, quality > 0)
    """
    items = [Item("+5 Dexterity Vest", sell_in=-1, quality=10)]
    GildedRose(items).update_quality()
    assert items[0].sell_in == -2
    assert items[0].quality == 8  # -1 (C1) -1 (C6) = 8


# T7 - Backstage passes, sell_in=0, quality=20
# Cobre: C2, C3, C4, C5, C7
# ⚠️ ATENÇÃO: A IA documentou apenas C5 e C7, mas sell_in=0 ainda
# passa pelos bônus ANTES do decremento — C2, C3 e C4 também são cobertos.
# O resultado final é 0 pois C7 zera o quality.
def test_backstage_pass_after_concert():
    """
    Cenário: Backstage passes no dia do show / pós-show (sell_in=0)
    Comandos cobertos (rastreamento completo):
    C2: item.quality = item.quality + 1 (incremento base)      → 20→21
    C3: item.quality = item.quality + 1 (bônus sell_in < 11)   → 21→22
    C4: item.quality = item.quality + 1 (bônus sell_in < 6)    → 22→23
    C5: item.sell_in = item.sell_in - 1                        → 0→-1
    C7: item.quality = item.quality - item.quality             → 23→0

    NOTA: A IA (DeepSeek) documentou apenas C5 e C7 neste teste,
    ignorando que sell_in=0 ainda dispara C2, C3 e C4 antes do decremento.
    As assertions estão corretas, mas a rastreabilidade estava incompleta.
    """
    items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=0, quality=20)]
    GildedRose(items).update_quality()
    assert items[0].sell_in == -1
    assert items[0].quality == 0


# T8 - "Aged Brie", sell_in=0, quality=40
# Cobre: C2, C5, C8
def test_aged_brie_after_sell_by_date():
    """
    Cenário: Aged Brie vencido (sell_in=0, vai para -1)
    Comandos cobertos:
    C2: item.quality = item.quality + 1 (incremento base)      → 40→41
    C5: item.sell_in = item.sell_in - 1                        → 0→-1
    C8: item.quality = item.quality + 1 (Aged Brie, sell_in<0) → 41→42
    """
    items = [Item("Aged Brie", sell_in=0, quality=40)]
    GildedRose(items).update_quality()
    assert items[0].sell_in == -1
    assert items[0].quality == 42  # +1 (C2) +1 (C8) = +2


# ─────────────────────────────────────────────
# Executar com:  pytest test_gilded_rose.py -v
# ─────────────────────────────────────────────