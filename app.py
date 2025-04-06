from flask import Flask, request, jsonify # type: ignore
from flask_cors import CORS # type: ignore

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Function to check if a number can be placed in a given position
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

# Backtracking function to solve the Sudoku puzzle
def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:  # Empty cell
                for num in range(1, 10):  # Try numbers 1-9
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0  # Backtrack
                return False
    return True

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    board = data.get('board')

    if board and solve_sudoku(board):
        return jsonify({'solved_board': board})
    else:
        return jsonify({'error': 'No solution found'}), 400

if __name__ == '__main__':
    app.run(debug=True)
