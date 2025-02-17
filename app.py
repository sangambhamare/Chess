# Install necessary packages
# pip install django gunicorn python-chess

# views.py
import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import chess

def index(request):
    return HttpResponse('''<!DOCTYPE html>
<html>
<head>
    <title>Online Chess Game</title>
</head>
<body>
    <h1>Play Chess</h1>
    <button onclick="startGame()">New Game</button>
    <input type="text" id="move" placeholder="Enter move e.g., e2e4">
    <button onclick="makeMove()">Make Move</button>
    <p id="game-status"></p>
    <script>
        function startGame() {
            fetch("/new-game/")
                .then(response => response.json())
                .then(data => document.getElementById("game-status").innerText = "New Game Started: " + data.fen);
        }

        function makeMove() {
            let move = document.getElementById("move").value;
            fetch("/make-move/", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: "move=" + move
            })
            .then(response => response.json())
            .then(data => document.getElementById("game-status").innerText = data.status ? data.fen : data.error);
        }
    </script>
</body>
</html>")

def new_game(request):
    board = chess.Board()
    request.session["board_fen"] = board.fen()
    return JsonResponse({"fen": board.fen()})

def make_move(request):
    if request.method == "POST":
        move = request.POST.get("move")
        board = chess.Board(request.session.get("board_fen", chess.STARTING_FEN))
        
        if chess.Move.from_uci(move) in board.legal_moves:
            board.push(chess.Move.from_uci(move))
            request.session["board_fen"] = board.fen()
            return JsonResponse({"fen": board.fen(), "status": "valid move"})
        else:
            return JsonResponse({"error": "Invalid move"})
    
    return JsonResponse({"error": "Invalid request"})
