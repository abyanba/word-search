from typing import List


class WordSearch:
    def isExist(self, board: List[List[str]], word: str) -> bool:
        # banyaknya baris di board
        for row in range(len(board)):
            # banyaknya kolom di satu row
            for col in range(len(board[0])):
                # cocok sama karakter pertama, maka dfs
                if board[row][col] == word[0]:
                    if self.dfs(board, row, col, word):
                        return True
        return False

    def dfs(self, board, row, col, word):
        if not word:
            # udah sampe di karakter akhir
            return True

        if (
            (0 <= row < len(board))
            and (0 <= col < len(board[0]))
            and board[row][col] != "#"
            and board[row][col] == word[0]
        ):
            temp = board[row][col]
            # udah dikunjungi
            board[row][col] = "#"

            # cek kanan, kiri, bawah, atas
            for _rowInc, _colInc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if self.dfs(board, row + _rowInc, col + _colInc, word[1:]):
                    return True

            board[row][col] = temp
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
