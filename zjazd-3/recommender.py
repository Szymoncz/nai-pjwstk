"""
Silnik rekomendacji filmów/seriali.

OPIS PROBLEMU
    Ankieta: kilkanaście osób oceniło filmy/seriale w skali 1-10 (ratings.json).
    Dla wybranego użytkownika program wskazuje 5 filmów, których nie oglądał,
    a które powinny mu się spodobać (rekomendacje), oraz 5, które raczej mu się
    nie spodobają (antyrekomendacje).

AUTOR
    Szymon Czudowski, Radosław Krawiec

METODA
    1. Dla każdej innej osoby liczymy odległość ocen na wspólnie ocenionych
       filmach (im mniejsza, tym podobniejszy gust). Dwie metryki: euclidean
       i manhattan.
    2. Wybieramy najbliższą osobę ("bliźniaka gustu").
    3. Z filmów, które ona widziała, a wybrany użytkownik nie:
       5 najwyżej ocenionych = rekomendacje, 5 najniżej = antyrekomendacje.

INSTRUKCJA UŻYCIA
    python recommender.py                  # pokaże listę osób i zapyta, dla kogo
    python recommender.py szymon           # wystarczy fragment imienia/nazwiska
    python recommender.py "Oskar Niedźwiedzki"
    Dane: ratings.json w tym samym folderze.
"""

import json
import math
import sys

MIN_COMMON = 3  # tyle wspólnych filmów trzeba mieć, by liczyć odległość


def distance(ratings, user1, user2, metric):
    """Średnia odległość ocen dwóch użytkowników na wspólnych filmach.

    Args:
        ratings: słownik {użytkownik: {film: ocena}}.
        user1, user2: nazwy użytkowników.
        metric: "euclidean" (pierwiastek ze średniej kwadratów różnic)
                lub "manhattan" (średnia różnic bezwzględnych).

    Returns:
        Odległość (float) lub math.inf, gdy wspólnych filmów jest za mało.
    """
    common = [m for m in ratings[user1] if m in ratings[user2]]
    if len(common) < MIN_COMMON:
        return math.inf
    diffs = [abs(ratings[user1][m] - ratings[user2][m]) for m in common]
    if metric == "euclidean":
        return math.sqrt(sum(d ** 2 for d in diffs) / len(diffs))
    return sum(diffs) / len(diffs)


def recommend(ratings, user, metric, n=5):
    """Zwraca (najbliższy użytkownik, jego odległość, rekomendacje, antyrekomendacje).

    Rekomendacje i antyrekomendacje to listy (film, ocena bliźniaka).
    """
    others = [u for u in ratings if u != user]
    twin = min(others, key=lambda u: distance(ratings, user, u, metric))
    unseen = [(m, r) for m, r in ratings[twin].items() if m not in ratings[user]]
    unseen.sort(key=lambda x: x[1], reverse=True)
    return twin, distance(ratings, user, twin, metric), unseen[:n], unseen[::-1][:n]


def choose_user(ratings, query=None):
    """Wybiera użytkownika: po fragmencie nazwy (bez wielkości liter) albo z listy.

    Bez `query` wypisuje ponumerowaną listę osób i pyta o numer lub nazwę.
    """
    names = list(ratings)
    if query is None:
        print("Dostępni użytkownicy:")
        for i, name in enumerate(names, 1):
            print(f"  {i:>2}. {name} ({len(ratings[name])} ocen)")
        query = input("Podaj numer lub nazwę: ").strip()
    if query.isdigit() and 1 <= int(query) <= len(names):
        return names[int(query) - 1]
    matches = [n for n in names if query.lower() in n.lower()]
    if len(matches) != 1:
        raise SystemExit(f"Nie znaleziono jednoznacznie '{query}'. Dostępni: {', '.join(names)}")
    return matches[0]


if __name__ == "__main__":
    with open("ratings.json", encoding="utf-8") as f:
        ratings = json.load(f)
    user = choose_user(ratings, sys.argv[1] if len(sys.argv) > 1 else None)

    for metric in ("euclidean", "manhattan"):
        twin, dist, good, bad = recommend(ratings, user, metric)
        print(f"\n=== {user} | {metric} | najbliższy: {twin} (odległość {dist:.2f}) ===")
        print("Polecane:")
        for movie, r in good:
            print(f"  {r:>2}  {movie}")
        print("Antyrekomendacje:")
        for movie, r in bad:
            print(f"  {r:>2}  {movie}")
