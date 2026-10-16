"""Gobblet 3x3: uproszczona gra turowa dla dwóch graczy.

Zasady referencyjne: https://blueorangegames.eu/en/games/gobblet/
Autorzy: [wpisz imiona i nazwiska członków zespołu]
Przygotowanie i uruchomienie: zobacz README.md.

Wariant projektu: plansza 3x3, po dwa pionki każdego z trzech rozmiarów na
gracza. Większy pionek może przykryć mniejszy. Można przesunąć własny
wierzchni pionek na inne pole. Wygrywa gracz, który ustawi trzy swoje
widoczne pionki w rzędzie, kolumnie lub po przekątnej. Nie wolno wykonać
ruchu, który odsłoni gotową linię przeciwnika.
"""

from ai import choose_computer_move
from gobblet import HUMAN, GameState, Move, apply_move, legal_moves, new_game, visible_piece, winner


def display_board(state: GameState) -> None:
	print("\nPlansza (numery pól są widoczne na pustych polach):")
	for row in range(3):
		cells = []
		for column in range(3):
			cell = row * 3 + column
			piece = visible_piece(state, cell)
			if piece is None:
				cells.append(f" {cell + 1} ")
			else:
				mark = "X" if piece[0] == HUMAN else "O"
				cells.append(f"{mark}{piece[1]} ")
		print(" | ".join(cells))
		if row < 2:
			print("---+----+---")
	print()


def describe_move(move: Move) -> str:
	source, target, size = move
	if source is None:
		return f"zapas: rozmiar {size} na pole {target + 1}"
	return f"pole {source + 1} na pole {target + 1} (rozmiar {size})"


def read_human_move(state: GameState) -> Move:
	while True:
		command = input("Twój ruch (r rozmiar pole | m źródło pole): ").split()
		try:
			if len(command) != 3:
				raise ValueError

			kind, first, second = command
			first_number = int(first)
			second_number = int(second)
			if kind == "r" and 1 <= first_number <= 3 and 1 <= second_number <= 9:
				requested = (None, second_number - 1, first_number)
			elif kind == "m" and 1 <= first_number <= 9 and 1 <= second_number <= 9:
				source = first_number - 1
				top_piece = visible_piece(state, source)
				if top_piece is None or top_piece[0] != HUMAN:
					raise ValueError
				requested = (source, second_number - 1, top_piece[1])
			else:
				raise ValueError
		except ValueError:
			print("Niepoprawny zapis. Użyj np. 'r 3 5' albo 'm 2 5'.")
			continue

		if requested in legal_moves(state, HUMAN):
			return requested
		print("Tego ruchu nie można wykonać. Sprawdź rozmiar i pole.")


def main() -> None:
	print("Gobblet 3x3: Ty grasz X, komputer gra O.")
	print("Rozmiary pionków: 1 (mały), 2 (średni), 3 (duży).")
	print("Przykład: 'r 3 5' kładzie duży pionek na polu 5.")
	print("Przykład: 'm 2 5' przesuwa pionek z pola 2 na pole 5.")

	state = new_game()
	current_player = HUMAN
	seen_positions: set[tuple[GameState, int]] = set()
	while True:
		display_board(state)
		if winner(state) is not None:
			break

		position = (state, current_player)
		if position in seen_positions:
			print("Ta sama pozycja wystąpiła ponownie. Remis!")
			return
		seen_positions.add(position)

		moves = legal_moves(state, current_player)
		if not moves:
			print("Brak legalnych ruchów. Remis!")
			return

		if current_player == HUMAN:
			move = read_human_move(state)
		else:
			move = choose_computer_move(state)
			if move is None:
				print("Brak legalnych ruchów. Remis!")
				return
			print(f"Komputer gra: {describe_move(move)}")

		state = apply_move(state, current_player, move)
		current_player = 1 - current_player

	display_board(state)
	winning_player = winner(state)
	if winning_player == HUMAN:
		print("Wygrałeś!")
	else:
		print("Wygrał komputer.")


if __name__ == "__main__":
	main()
