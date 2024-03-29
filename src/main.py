import pygame as p
from tkinter import *

from config import WINDOW_SIZE
from toggle_move_set import show_move_set, hide_move_set
from get_clicked_tile import get_clicked_tile
from GameBoard import GameBoard
from initialize_board import initialize_board
from move_and_capture import move_and_capture
from PromotionWindow import PromotionWindow
from promote_pawn import promote_pawn

tile_turn = "white"

current_tile_pos = None
previous_tile_pos = None
current_move_set = None

p.init()
p.mouse.set_cursor(p.SYSTEM_CURSOR_HAND)
p.display.set_caption("Chess")

game_window = p.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

board = GameBoard()
initialize_board(game_window, board.game_board)

p.display.update()

while True:

  event = p.event.wait()
  if event.type == p.QUIT:
    p.quit()
    quit()

  elif event.type == p.MOUSEBUTTONDOWN and event.button == 1:
    
    current_tile_pos = p.mouse.get_pos()
    current_tile = get_clicked_tile(current_tile_pos)

    current_piece = board.game_board[current_tile[1]][current_tile[0]].piece

    if (current_piece != None and current_piece.colour == tile_turn and previous_tile_pos == None):
      current_move_set = show_move_set(game_window, board.game_board, current_tile_pos)
      previous_tile_pos = current_tile_pos

    elif (current_piece == None):
      if (current_move_set != None and board.game_board[current_tile[1]][current_tile[0]] in current_move_set.get("move")):
        move_and_capture(game_window, board.game_board, current_tile, previous_tile_pos)

        if (board.game_board[current_tile[1]][current_tile[0]].piece.piece_type == "pawn"):
          board.game_board[current_tile[1]][current_tile[0]].piece.change_move_set()

          if (board.game_board[current_tile[1]][current_tile[0]].piece.colour == "white" and current_tile[1] == 0):
            print("white pawn promotion")
            promotion = PromotionWindow()
            promotion.run()
            promote_pawn(game_window, board.game_board, current_tile, promotion.selected_value)

          elif(board.game_board[current_tile[1]][current_tile[0]].piece.colour == "black" and current_tile[1] == 7):
            print("black pawn promotion")
            promotion = PromotionWindow()
            promotion.run()
            promote_pawn(game_window, board.game_board, current_tile, promotion.selected_value)

        if (tile_turn == "white"):
          tile_turn = "black"
        else:
          tile_turn = "white"

        current_tile_pos = None
        previous_tile_pos = None
        current_move_set = None
      continue

    elif (current_piece.colour != tile_turn):
      if (current_move_set != None and board.game_board[current_tile[1]][current_tile[0]] in current_move_set.get("capture")):

        move_and_capture(game_window, board.game_board, current_tile, previous_tile_pos)

        if (board.game_board[current_tile[1]][current_tile[0]].piece.piece_type == "pawn"):
          board.game_board[current_tile[1]][current_tile[0]].piece.change_move_set()

          if (board.game_board[current_tile[1]][current_tile[0]].piece.colour == "white" and current_tile[1] == 0):
            print("white pawn promotion")
            promotion = PromotionWindow()
            promotion.run()
            promote_pawn(game_window, board.game_board, current_tile, promotion.selected_value)
            
          elif(board.game_board[current_tile[1]][current_tile[0]].piece.colour == "black" and current_tile[1] == 7):
            print("black pawn promotion")
            promotion = PromotionWindow()
            promotion.run()
            promote_pawn(game_window, board.game_board, current_tile, promotion.selected_value)

        if (tile_turn == "white"):
          tile_turn = "black"
        else:
          tile_turn = "white"

        current_tile_pos = None
        previous_tile_pos = None
        current_move_set = None

      continue

    elif (current_tile == get_clicked_tile(previous_tile_pos)):
      hide_move_set(game_window, board.game_board, current_tile_pos)
      current_tile_pos = None
      previous_tile_pos = None
      current_move_set = None
      continue

  else:
    continue