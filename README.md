Gilded Rose — Iteração 2: Auditoria (Resumo)

Objetivo
--------
Auditar o método `update_quality` em `GildedRose-Refactoring-Kata/Python/gilded_rose.py` para verificar se a suíte de testes gerada pelo Deep Seek cobre os caminhos relevantes e identificar casos de teste faltantes por meio de análise caixa-branca (CFG e complexidade ciclomática).

Descrição do código
-------------------
- Arquivo principal: `GildedRose-Refactoring-Kata/Python/gilded_rose.py`.
- Estrutura: classe `Item` (atributos `name`, `sell_in`, `quality`) e classe `GildedRose` com o método `update_quality()`.
- Regras principais resumidas:
  - Itens normais: `sell_in` decrementa; `quality` decrementa (perda dobra após o vencimento).
  - `Aged Brie`: `quality` aumenta até o máximo de 50.
  - `Backstage passes`: `quality` aumenta conforme `sell_in` diminui e zera após o evento.
  - `Sulfuras`: não sofre alterações.
  - `Conjured` (quando implementado): depreciação acelerada.

Objetivo da atividade
---------------------
Comparar a suíte gerada pelo Deep Seek com a análise estrutural do método (`CFG` + complexidade ciclomática) e mapear os inputs mínimos (`name`, `sell_in`, `quality`) necessários para cobrir os ramos identificados.

Comandos para executar os testes gerados
-------------------------------------
1. Criar e ativar um ambiente virtual (opcional):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instalar dependências e `pytest` (se necessário):

```bash
pip install -r GildedRose-Refactoring-Kata/Python/requirements.txt  # se existir
pip install pytest
```

3. Executar os testes gerados pelo Deep Seek:

```bash
cd GildedRose-Refactoring-Kata/Python
pytest -v
```