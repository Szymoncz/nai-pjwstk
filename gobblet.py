from dataclasses import dataclass


BOARD_CELLS = 9
PLAYERS = (0, 1)
HUMAN = 0
COMPUTER = 1
WIN_LINES = (
	(0, 1, 2),
	(3, 4, 5),
	(6, 7, 8),
	(0, 3, 6),
	(1, 4, 7),
	(2, 5, 8),
	(0, 4, 8),
	(2, 4, 6),
)

Piece = tuple[int, int]
Move = tuple[int | None, int, int]


@dataclass(frozen=True)
class GameState:
	board: tuple[tuple[Piece, ...], ...]
	reserves: tuple[tuple[int, int, int], tuple[int, int, int]]


def new_game() -> GameState:
	board = tuple(() for _ in range(BOARD_CELLS))
	reserves = ((2, 2, 2), (2, 2, 2))
	return GameState(board, reserves)


def visible_piece(state: GameState, cell: int) -> Piece | None:
	stack = state.board[cell]
	return stack[-1] if stack else None


def has_line(state: GameState, player: int) -> bool:
	for line in WIN_LINES:
		if all(
			visible_piece(state, cell) is not None
			and visible_piece(state, cell)[0] == player
			for cell in line
		):
			return True
	return False


def winner(state: GameState) -> int | None:
	for player in PLAYERS:
		if has_line(state, player):
			return player
	return None


def apply_move(state: GameState, player: int, move: Move) -> GameState:
	source, target, size = move
	board = list(state.board)
	reserves = [list(player_reserve) for player_reserve in state.reserves]

	if source is None:
		reserves[player][size - 1] -= 1
	else:
		source_stack = list(board[source])
		source_stack.pop()
		board[source] = tuple(source_stack)

	target_stack = list(board[target])
	target_stack.append((player, size))
	board[target] = tuple(target_stack)
	return GameState(tuple(board), tuple(tuple(items) for items in reserves))


def legal_moves(state: GameState, player: int) -> list[Move]:
	pieces: list[tuple[int | None, int]] = []
	for size, amount in enumerate(state.reserves[player], start=1):
		if amount > 0:
			pieces.append((None, size))

	for source, stack in enumerate(state.board):
		if stack and stack[-1][0] == player:
			pieces.append((source, stack[-1][1]))

	moves: list[Move] = []
	for source, size in pieces:
		for target in range(BOARD_CELLS):
			if target == source:
				continue

			top_piece = visible_piece(state, target)
			if top_piece is not None and top_piece[1] >= size:
				continue

			move = (source, target, size)
			next_state = apply_move(state, player, move)
			if has_line(next_state, 1 - player) and not has_line(next_state, player):
				continue
			moves.append(move)
	return moves


def evaluate(state: GameState, player: int) -> int:
	winning_player = winner(state)
	if winning_player == player:
		return 10_000
	if winning_player is not None:
		return -10_000

	scores = [0, 0]
	for line in WIN_LINES:
		tops = [visible_piece(state, cell) for cell in line]
		for line_player in PLAYERS:
			own_pieces = [piece for piece in tops if piece is not None and piece[0] == line_player]
			other_pieces = [piece for piece in tops if piece is not None and piece[0] != line_player]
			if other_pieces or not own_pieces:
				continue

			line_value = 3 if len(own_pieces) == 1 else 24
			scores[line_player] += line_value + sum(piece[1] for piece in own_pieces)

	return scores[player] - scores[1 - player]