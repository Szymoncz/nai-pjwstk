import unittest

from ai import choose_computer_move
from gobblet import (
    COMPUTER,
    HUMAN,
    GameState,
    apply_move,
    has_line,
    legal_moves,
    new_game,
    winner,
)


class GobbletTests(unittest.TestCase):
    def test_starting_position_has_27_moves(self):
        self.assertEqual(len(legal_moves(new_game(), HUMAN)), 27)

    def test_larger_piece_covers_smaller_piece(self):
        state = apply_move(new_game(), HUMAN, (None, 0, 1))
        state = apply_move(state, COMPUTER, (None, 0, 2))
        self.assertEqual(state.board[0], ((HUMAN, 1), (COMPUTER, 2)))

    def test_three_visible_pieces_form_a_line(self):
        state = new_game()
        for cell in (0, 1, 2):
            state = apply_move(state, HUMAN, (None, cell, 1))
        self.assertTrue(has_line(state, HUMAN))
        self.assertEqual(winner(state), HUMAN)

    def test_ai_takes_an_immediate_win(self):
        state = new_game()
        state = apply_move(state, COMPUTER, (None, 0, 1))
        state = apply_move(state, HUMAN, (None, 3, 1))
        state = apply_move(state, COMPUTER, (None, 1, 1))
        state = apply_move(state, HUMAN, (None, 4, 1))

        move = choose_computer_move(state)

        self.assertIsNotNone(move)
        self.assertEqual(move[1], 2)
        self.assertEqual(winner(apply_move(state, COMPUTER, move)), COMPUTER)

    def test_ai_cannot_uncover_opponents_winning_line(self):
        board = (
            ((HUMAN, 1), (COMPUTER, 2)),
            ((HUMAN, 1),),
            ((HUMAN, 1),),
            (),
            (),
            (),
            (),
            (),
            (),
        )
        state = GameState(board, ((1, 1, 1), (1, 1, 0)))

        moves = legal_moves(state, COMPUTER)

        self.assertNotIn((0, 5, 2), moves)


if __name__ == "__main__":
    unittest.main()