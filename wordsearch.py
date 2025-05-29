import random
import string
import tkinter as tk
import pyautogui
from dfs import WordSearch

x0 = 0
y0 = 0
d = 82

def generate_random_board(size=12):
    return [''.join(random.choices(string.ascii_uppercase, k=size)) for _ in range(size)]

def place_words_on_board(words, size=12):
    board = [[None for _ in range(size)] for _ in range(size)]
    directions = [(dr, dc) for dr in [-1,0,1] for dc in [-1,0,1] if not (dr==0 and dc==0)]
    for word in words:
        placed = False
        attempts = 0
        while not placed and attempts < 100:
            dr, dc = random.choice(directions)
            if dr == 0 and dc == 0:
                continue
            max_r = size-1 if dr <= 0 else size-len(word)
            max_c = size-1 if dc <= 0 else size-len(word)
            min_r = len(word)-1 if dr < 0 else 0
            min_c = len(word)-1 if dc < 0 else 0
            r0 = random.randint(min_r, max_r)
            c0 = random.randint(min_c, max_c)
            r, c = r0, c0
            can_place = True
            for ch in word:
                if board[r][c] not in (None, ch):
                    can_place = False
                    break
                r += dr
                c += dc
            if can_place:
                r, c = r0, c0
                for ch in word:
                    board[r][c] = ch
                    r += dr
                    c += dc
                placed = True
            attempts += 1
    # Fill the rest with random letters
    for r in range(size):
        for c in range(size):
            if board[r][c] is None:
                board[r][c] = random.choice(string.ascii_uppercase)
    return [''.join(row) for row in board]

def load_words_from_file(filename, n=10):
    with open(filename, 'r') as f:
        lines = [line.strip().upper() for line in f if line.strip() and not line.startswith('//')]
    return set(random.sample(lines, n))

words = load_words_from_file('words.txt', 14)
board = place_words_on_board(words, 12)

def solve(board, words):
    ws = WordSearch()
    for word in words:
        path = ws.isExist([list(row) for row in board], word)
        if path:
            r0, c0, r1, c1 = path
            print(word)
            click(r0, c0, r1, c1)
            
def get_word(board, r0, c0, dr, dc, r1, c1):
    r = r0
    c = c0
    letters = ''

    while r != r1 or c != c1:
        letters += board[r][c]
        r += dr
        c += dc
    
    letters += board[r1][c1]
    return letters

def print_board(board):
    for row in board:
        print(*row)

def click(r0, c0, r1, c1):
    pyautogui.moveTo(x0 + (c0 * d), y0 + (r0 * d), 0.5)
    pyautogui.dragTo(x0 + (c1 * d), y0 + (r1 * d), 0.5)

class WordSearchGUI:
    def __init__(self, master, board, words):
        self.master = master
        self.board = board
        self.words = list(words)
        self.found_words = set()
        self.labels = []
        self.word_labels = []
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.master)
        frame.pack(side=tk.LEFT, padx=10, pady=10)
        for r in range(12):
            row = []
            for c in range(12):
                lbl = tk.Label(frame, text=self.board[r][c], width=2, height=1, font=("Consolas", 18), borderwidth=1, relief="solid")
                lbl.grid(row=r, column=c, padx=1, pady=1)
                row.append(lbl)
            self.labels.append(row)
        # Word list
        word_frame = tk.Frame(self.master)
        word_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        tk.Label(word_frame, text="Words to find:", font=("Arial", 12, "bold")).pack()
        for w in self.words:
            lbl = tk.Label(word_frame, text=w, font=("Arial", 12))
            lbl.pack(anchor='w')
            self.word_labels.append(lbl)
        # Solve button
        btn = tk.Button(self.master, text="Solve", command=self.solve_and_highlight, font=("Arial", 12, "bold"))
        btn.pack(pady=10)
        # Reset button
        reset_btn = tk.Button(self.master, text="Reset", command=self.reset_board, font=("Arial", 12, "bold"), bg='#e0e0e0')
        reset_btn.pack(pady=5)

    def reset_board(self):
        global board, words
        words = load_words_from_file('words.txt', 15)
        board = place_words_on_board(words, 12)
        self.board = board
        self.words = list(words)
        for r in range(12):
            for c in range(12):
                self.labels[r][c].config(text=self.board[r][c], bg='lightgray')
        for i, lbl in enumerate(self.word_labels):
            if i < len(self.words):
                lbl.config(text=self.words[i], bg='lightgray')
            else:
                lbl.config(text='', bg='lightgray')

    def solve_and_highlight(self):
        # Daftar warna pastel untuk highlight
        highlight_colors = [
            '#ffe066', '#b5ead7', '#ffb7b2', '#b2cefe', '#e2f0cb',
            '#f6dfeb', '#f7cac9', '#c7ceea', '#f9f9c5', '#d4a5a5',
            '#b5ead7', '#f3eac2', '#c2f0fc', '#f7d6e0', '#d0e6a5', '#f6c6ea'
        ]
        # Clear previous highlights
        for r in range(12):
            for c in range(12):
                self.labels[r][c].config(bg='lightgray')
        for lbl in self.word_labels:
            lbl.config(bg='lightgray')
        # Patch click to highlight with color per word
        highlight_map = {}  # (r0,c0,r1,c1): color
        def highlight(r0, c0, r1, c1, color):
            dr = 1 if r1 > r0 else (-1 if r1 < r0 else 0)
            dc = 1 if c1 > c0 else (-1 if c1 < c0 else 0)
            r, c = r0, c0
            while r != r1 or c != c1:
                self.labels[r][c].config(bg=color)
                r += dr
                c += dc
            self.labels[r1][c1].config(bg=color)
        # Patch click globally
        global click
        old_click = click
        found_positions = {}
        def patched_click(r0, c0, r1, c1):
            # Simpan posisi untuk pewarnaan setelah solve
            found_positions[(r0, c0, r1, c1)] = True
        click = patched_click
        # Run solver untuk dapatkan posisi kata
        solve(self.board, set(self.words))
        # Highlight tiap kata dengan warna berbeda
        for idx, word in enumerate(self.words):
            color = highlight_colors[idx % len(highlight_colors)]
            # Cari posisi kata di grid
            found = False
            for r0 in range(12):
                for c0 in range(12):
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            if dr == 0 and dc == 0:
                                continue
                            r1 = r0 + (dr * (len(word) - 1))
                            c1 = c0 + (dc * (len(word) - 1))
                            if 0 <= r1 < 12 and 0 <= c1 < 12:
                                w = get_word(self.board, r0, c0, dr, dc, r1, c1)
                                if w == word:
                                    highlight(r0, c0, r1, c1, color)
                                    self.word_labels[idx].config(bg=color)
                                    found = True
                                    break
                        if found:
                            break
                    if found:
                        break
                if found:
                    break
        click = old_click

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Word Search Solver")
    gui = WordSearchGUI(root, board, words)
    root.mainloop()