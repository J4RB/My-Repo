import sqlite3

class Highscore():
    def __init__(self, dato, score):
        self.dato = dato
        self.score = score

    def set_id(self, id):
        self.id = id

class Highscore_data():
    def __init__(self):
        self.db = sqlite3.connect('Highscores.db')

    def get_highscore_list(self):
        c = self.db.cursor()
        c.execute('SELECT h.dato, h.score, h.id FROM highscores h;')
        h_list = []
        for h in c:
            highscores = Highscore(h[0], h[1])
            highscores.set_id(h[2])
            h_list.append(highscores)
        return h_list

    # function returns N largest elements
    def N_max_elements(self, list1, N):
        # get a list of lists with the date and score in it
        pre_sorted = []
        for i in range(0, len(list1)):
            pre_sorted.append([list1[i].dato, list1[i].score])

        # sort the list of lists with dates and scores according to scores and return the 10 best
        pre_sorted.sort(key = lambda i: i[1], reverse=True)     # lambda the way the sort function sorts
        best_N = []
        for score in range(0, N):
            best_N.append(pre_sorted[score])
        return best_N

    def create_tables(self):
        try:
            self.db.execute("""CREATE TABLE IF NOT EXISTS highscores (
                id INTEGER PRIMARY KEY,
                dato DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                score INTEGER);""")

            #print('Tabel oprettet')
        except Exception as e:
            print(f'Tabellen findes allerede: {e}')