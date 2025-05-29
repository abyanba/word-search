from typing import List, Tuple

class WordSearch:
    def isExist(self, board: List[List[str]], word: str) -> Tuple[int, int, int, int] | None:
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == word[0]:
                    path = []
                    if self.dfs(board, row, col, word, path):
                        return path[0][0], path[0][1], path[-1][0], path[-1][1]
        return None

    def dfs(self, board, row, col, word, path):
        if not word:
            return True

        if (
            0 <= row < len(board)
            and 0 <= col < len(board[0])
            and board[row][col] != "#"
            and board[row][col] == word[0]
        ):
            temp = board[row][col]
            board[row][col] = "#"
            path.append((row, col))

            for _rowInc, _colInc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                if self.dfs(board, row + _rowInc, col + _colInc, word[1:], path):
                    return True

            board[row][col] = temp
            path.pop()

        return False

if __name__ == "__main__":
    # testing
    instance = WordSearch()
    board = [
	["T", "E", "S"], 
	["A", "B", "C"], 
	["1", "2", "3"]
    ]
    print(instance.isExist(board, "TESCB21"))
    print(instance.isExist(board, "TESB"))
