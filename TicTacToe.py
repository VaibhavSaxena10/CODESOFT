import math

HUMAN = "O"
AI = "X"
EMPTY = " "


def print_board(board):
    """Prints the Tic-Tac-Toe board."""
    for i in range(3):
        row = board[3 * i:3 * i + 3]
        print(" | ".join(cell if cell != EMPTY else " " for cell in row))
        if i < 2:
            print("--+---+--")


def check_winner(board):
    """
    Checks for a winner.
    Returns 'X' or 'O' if there is a winner, 'draw' if tie, or None otherwise.
    """
    win_lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  
        (0, 4, 8), (2, 4, 6)              
    ]

    for a, b, c in win_lines:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]

    if EMPTY not in board:
        return "draw"

    return None


def minimax(board, is_maximizing):
    """
    Minimax algorithm.
    Returns a score from the perspective of the AI player.
    """
    result = check_winner(board)
    if result == AI:
        return 1
    elif result == HUMAN:
        return -1
    elif result == "draw":
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = AI
                score = minimax(board, False)
                board[i] = EMPTY
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = HUMAN
                score = minimax(board, True)
                board[i] = EMPTY
                best_score = min(best_score, score)
        return best_score


def best_move(board):
    """
    Finds the best move for the AI using minimax.
    Returns the index (0-8) of the best move.
    """
    best_score = -math.inf
    move = None

    for i in range(9):
        if board[i] == EMPTY:
            board[i] = AI
            score = minimax(board, False)
            board[i] = EMPTY
            if score > best_score:
                best_score = score
                move = i
    return move


def play():
    """
    Main game loop: Human (O) vs AI (X) in the console.
    """
    board = [EMPTY] * 9
    current_player = HUMAN  

    print("Welcome to Tic-Tac-Toe!")
    print("You are 'O' and the AI is 'X'.")
    print("Enter positions (0-8) as shown below:")
    print("0 | 1 | 2")
    print("--+---+--")
    print("3 | 4 | 5")
    print("--+---+--")
    print("6 | 7 | 8\n")

    while True:
        print_board(board)
        result = check_winner(board)
        if result is not None:
            if result == "draw":
                print("It's a draw!")
            else:
                print(f"{result} wins!")
            break

        if current_player == HUMAN:
            try:
                pos = int(input("Your move (0-8): "))
            except ValueError:
                print("Please enter a valid number between 0 and 8.")
                continue

            if 0 <= pos <= 8 and board[pos] == EMPTY:
                board[pos] = HUMAN
                current_player = AI
            else:
                print("Invalid move. Try again.")
        else:
            print("AI is thinking...")
            pos = best_move(board)
            board[pos] = AI
            current_player = HUMAN


if __name__ == "__main__":
    play()
