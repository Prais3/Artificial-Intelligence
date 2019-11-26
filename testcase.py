import Main
import unittest


class Testvxj5053(unittest.TestCase):

    def test_num_placements_all(self):
        self.assertEqual(vxj5053.num_placements_all(4), 43680)

    def test_num_placements_one_per_row(self):
        self.assertEqual(vxj5053.num_placements_one_per_row(4), 6144)

    def test_n_queens_valid(self):
        self.assertEqual(vxj5053.n_queens_valid([0, 2]), True)

    def test_n_queens_solutions(self):
        self.assertEqual(len(list(vxj5053.n_queens_solutions(8))), 92)

    def test_get_board(self):
        b = [[True, False], [False, True]]
        p = vxj5053.LightsOutPuzzle(b)
        self.assertEqual(p.get_board(), [[True, False], [False, True]])

    def test_perform_move(self):
        p = vxj5053.create_puzzle(3, 3)
        self.assertEqual(p.perform_move(1, 1), None)
        self.assertEqual(p.get_board(), [[False, True, False], [True, True, True], [False, True, False]])

    def test_scramble(self):
        pass

    def test_is_solved(self):
        b = [[True, False], [False, True]]
        p = vxj5053.LightsOutPuzzle(b)
        self.assertEqual(p.is_solved(), False)

    def test_copy(self):
        p = vxj5053.create_puzzle(3, 3)
        p2 = p.copy()
        self.assertEqual(p.get_board() == p2.get_board(), True)

    def test_successors(self):
        p = vxj5053.create_puzzle(3, 3)
        p2 = p.copy()
        p.perform_move(1, 1)
        self.assertEqual(p.get_board() == p2.get_board(), False)

    def test_find_solution(self):
        p = vxj5053.create_puzzle(2, 3)
        for row in range(2):
            for col in range(3):
                p.perform_move(row, col)
                self.assertEqual(p.find_solution(), [(0, 0), (0, 2)])

    def test_solve_identical_disks(self):
        self.assertEqual(vxj5053.solve_identical_disks(4, 2), [(0, 2), (1, 3)])

    def test_solve_distinct_disks(self):
        self.assertEqual(vxj5053.solve_distinct_disks(4, 3), [(1, 3), (2, 1), (0, 2), (2, 4), (1, 2)])


if __name__ == '__main__':
    unittest.main()
