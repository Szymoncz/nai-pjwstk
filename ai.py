from easyAI import Negamax, TwoPlayerGame

from gobblet import COMPUTER, GameState, Move, apply_move, evaluate, legal_moves, winner


SEARCH_DEPTH = 3


class EasyGobbletGame(TwoPlayerGame):
	def __init__(self, state: GameState, current_player: int) -> None:
		self.state = state
		self.current_player = current_player
		self.players = [None, None]
		self.history: list[GameState] = []

	def possible_moves(self) -> list[Move]:
		return legal_moves(self.state, self.current_player - 1)

	def make_move(self, move: Move) -> None:
		self.history.append(self.state)
		self.state = apply_move(self.state, self.current_player - 1, move)

	def unmake_move(self, move: Move) -> None:
		self.state = self.history.pop()

	def is_over(self) -> bool:
		return winner(self.state) is not None or not self.possible_moves()

	def scoring(self) -> int:
		winning_player = winner(self.state)
		if winning_player is not None:
			return 10_000 if winning_player == self.current_player - 1 else -10_000
		return evaluate(self.state, self.current_player - 1)

	def ttentry(self) -> tuple[GameState, int]:
		return self.state, self.current_player


def choose_computer_move(state: GameState) -> Move | None:
	game = EasyGobbletGame(state, COMPUTER + 1)
	return Negamax(SEARCH_DEPTH)(game)