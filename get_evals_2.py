import chess.pgn
import chess.engine
import sqlite3
import json

engine = chess.engine.SimpleEngine.popen_uci("/usr/bin/stockfish")
engine.configure({'Threads':8, "Hash": 1024})

con = sqlite3.connect("evaluations.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS evaluations(fen PRIMARY KEY, moves)")

pgn_filename = "games.pgn"
pgn = open(pgn_filename)

game = chess.pgn.read_game(pgn)
games_count = 0
moves_processed = 0
moves_skipped = 0
failed_to_process = 0
while game:
	for node in game.mainline():
		board = node.board()
		fen = node.board().fen()
			
		fen_search = cur.execute("SELECT * FROM evaluations WHERE fen=?", (fen,))
		is_fen_searched = fen_search.fetchone() is not None
		if not is_fen_searched:
			analysis = engine.analyse(node.board(), chess.engine.Limit(nodes=100000), multipv=3)
			try:
				moves_and_evals = [{"eval": str(a['score']), "move": str(a["pv"][0])} for a in analysis]
				data = [(fen, json.dumps(moves_and_evals))]
				cur.executemany("INSERT INTO evaluations VALUES(?, ?)", data)
				moves_processed += 1
			except Exception:
				print(analysis)
				failed_to_process += 1
		else:
			moves_skipped += 1
		con.commit()
	games_count += 1
	game = chess.pgn.read_game(pgn)
	print("games processed: ", games_count, "moves processed: ", moves_processed, "moves skipped: ", moves_skipped, "failed: ", failed_to_process)
engine.quit()
