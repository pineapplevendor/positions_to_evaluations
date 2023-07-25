import chess.pgn
import chess.engine
import sqlite3
import json

engine = chess.engine.SimpleEngine.popen_uci("/usr/local/bin/stockfish")
engine.configure({'Threads':8, "Hash": 1024})

con = sqlite3.connect("lichess.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS evaluations(fen PRIMARY KEY, moves, previous_moves, is_tactic, is_mate)")

pgn_filename = "lichess_games.pgn"
pgn = open(pgn_filename)

game = chess.pgn.read_game(pgn)
games_count = 0
moves_processed = 0
moves_skipped = 0
failed_to_process = 0

while game:
	previous_moves = []
	previous_eval = None
	current_eval = None
	for node in game.mainline():
		previous_moves.append(node.move)
		board = node.board()
		fen = node.board().fen()
			
		fen_search = cur.execute("SELECT * FROM evaluations WHERE fen=?", (fen,))
		is_fen_searched = fen_search.fetchone() is not None
		if not is_fen_searched:
			try:
				analysis = engine.analyse(node.board(), chess.engine.Limit(nodes=100000), multipv=3)
				score = analysis[0]['score']
				current_eval = score.white().score()
				moves_and_evals = [{"eval": str(a['score']), "move": str(a["pv"][0])} for a in analysis]
				uci_moves = str([m.uci() for m in previous_moves])

				is_tactic = current_eval and previous_eval and abs(current_eval - previous_eval) > 300
				is_mate = score.is_mate()

				data = [(fen, json.dumps(moves_and_evals), uci_moves, is_tactic, is_mate)]
				cur.executemany("INSERT INTO evaluations VALUES(?, ?, ?, ?, ?)", data)
				moves_processed += 1
				previous_eval = current_eval
			except Exception as e:
				print(fen)
				print('exception', e)
				failed_to_process += 1
		else:
			previous_eval = None
			current_eval = None
			moves_skipped += 1
		con.commit()
	games_count += 1
	game = chess.pgn.read_game(pgn)
	print("games processed: ", games_count, "moves processed: ", 
		moves_processed, "moves skipped: ", moves_skipped, "failed: ", failed_to_process)

engine.quit()
