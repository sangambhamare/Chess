# Install necessary packages
# pip install django gunicorn python-chess

# views.py
import os
from django.shortcuts import render
from django.http import JsonResponse
import chess

def index(request):
    return render(request, "index.html")

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
