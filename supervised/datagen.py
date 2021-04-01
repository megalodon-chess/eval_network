#
#  Eval Network
#  Testing neural network evaluation.
#  Copyright Megalodon Chess 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import sys
import os
import struct
import random
import multiprocessing
import chess
import chess.engine

PARENT = os.path.dirname(os.path.realpath(__file__))
if os.path.isfile(os.path.join(PARENT, "path.txt")):
    with open(os.path.join(PARENT, "path.txt"), "r") as file:
        ENG_PATH = file.read().strip()
else:
    ENG_PATH = input("Engine path: ")
OUT_PATH = os.path.join(PARENT, "out.dat")
THREADS = multiprocessing.cpu_count()
DEPTH = 20


def log(msg):
    sys.stdout.write("\r"+" "*80+"\r")
    sys.stdout.write(msg)
    sys.stdout.flush()


def randpos():
    board = chess.Board()
    num_moves = random.randint(10, 60)
    for i in range(num_moves):
        moves = list(board.generate_legal_moves())
        if len(moves) == 0:
            break
        board.push(random.choice(moves))
    return board


def piece_char(piece: chess.Piece):
    if piece is None:
        return chr(0).encode()
    return piece.symbol().encode()


def append_result(file, board, result):
    score = result["score"].pov(chess.WHITE).score(mate_score=100000)
    for i in range(64):
        file.write(piece_char(board.piece_at(i)))
    file.write(struct.pack("f", score/100))


def main():
    engine = chess.engine.SimpleEngine.popen_uci(ENG_PATH)
    if "Threads" in engine.options:
        engine.configure({"Threads": THREADS})

    with open(OUT_PATH, "wb") as file:
        positions = 0
        while True:
            try:
                board = randpos()
                result = engine.analyse(board, chess.engine.Limit(depth=DEPTH))
                append_result(file, board, result)
                file.flush()

                positions += 1
                log(f"Analyzed {positions} positions.")
            except KeyboardInterrupt:
                file.flush()
                print("Terminated")
                break

    engine.quit()


main()
