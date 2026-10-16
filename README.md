# Gobblet 3x3

Turowa gra dla dwóch graczy. Człowiek gra `X`, komputer gra `O`. Komputer
wybiera ruchy przez `Negamax` z biblioteki `easyAI`.

## Wymagania

- Python 3.10 lub nowszy
- Dostęp do internetu podczas instalowania `easyAI`

## Uruchomienie na Linux/macOS

W terminalu przejdź do katalogu repozytorium i wykonaj:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python main.py
```

Na Debianie lub Ubuntu, jeśli tworzenie środowiska zgłasza brak `ensurepip`,
zainstaluj moduł `venv` dla używanej wersji Pythona. Dla Pythona 3.14:

```bash
sudo apt update
sudo apt install python3.14-venv
```

Następnie ponów polecenia uruchomienia z katalogu repozytorium.

## Uruchomienie na Windows

W terminalu PowerShell, w katalogu repozytorium, wykonaj:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

## Testy

Linux/macOS:

```bash
./.venv/bin/python -m unittest -v
```

Windows:

```powershell
.\.venv\Scripts\python.exe -m unittest -v
```

## Zasady wariantu

Plansza ma 3x3 pola. Każdy gracz ma po dwa pionki w trzech rozmiarach.
Większy pionek może przykryć mniejszy, a gracz może przesunąć swój widoczny
pionek na inne pole. Wygrywa pierwszy gracz, który ułoży trzy swoje widoczne
pionki w rzędzie, kolumnie lub po przekątnej. Nie wolno wykonać ruchu, który
odsłoni gotową linię przeciwnika. Powtórzenie tej samej pozycji oznacza remis.