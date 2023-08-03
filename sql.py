from sqlite3 import OperationalError
import sqlite3

class SQL:
    def __init__ (self):
        self.conn = sqlite3.connect('graf.db')
        self.cur = self.conn.cursor()

    def get_clusters(self, type):
        query = "SELECT MAX(cluster) FROM Node WHERE type = \"{ttype}\" GROUP BY cluster;".format (ttype = type)
        self.cur.execute (query)
        fetched = self.cur.fetchall() 
        return fetched
    
    def get_id (self, a):
        query = "SELECT id FROM Node WHERE cont = \"" + a + "\";"
        self.cur.execute (query)
        a = self.cur.fetchall()
        return a[0][0]

    def delete (self, con):
        query = "DELETE FROM Node WHERE Node.cont = \'" + con + "\';"
        self.run_sql (query)

    def insert (self, cluster, harm, type, content, sylls, stress):
        command = "INSERT INTO Node (cont, cluster, type, harm, syll, stress) VALUES ({c}, {cl}, {t}, {h}, {sy}, {st});".format (
            c = q(content), cl = q(cluster), t = q(type), h = q(harm), sy = q(sylls), st = q(stress)
        )
        already = self.query_content (content)
        if len (already) == 0:
            self.run_sql (command)
    
    def incident_edges (self, cont):
        id = self.get_id (cont)
        query = "SELECT * FROM EDGE WHERE a = " + str (id) + ";"
        self.cur.execute (query)
        q = self.cur.fetchall()
        return q 

    def add_edge (self, a, b):
        already = self.query_edge (a, b)
        if len (already) == 0:
            command = "INSERT INTO Edge (a, b) VALUES (" + str (a) + "," + str (b) + ");"
            self.run_sql (command)

    def query_edge(self, a, b):
        query = "SELECT * FROM Edge WHERE (a = " + str (a) + " AND b = " + str (b) + ")"
        self.cur.execute (query)
        fetched = self.cur.fetchall() 
        return fetched

    def query_content(self, con):
        query = "SELECT * FROM Node WHERE (cont = \"" + con + "\")"
        self.cur.execute (query)
        fetched = self.cur.fetchall() 
        return fetched
    
    def content_from_id (self, id):
        query = "SELECT cont FROM Node WHERE (id  = " + str (id) + ");"
        self.cur.execute (query)
        fetched = self.cur.fetchall() 
        return fetched[0][0]
    

    def query(self, clu, type):
        query = "SELECT * FROM Node WHERE (cluster=\"{clus}\" AND type=\"{type}\");".format (clus=clu, type=type)
        self.cur.execute (query)
        fetched = self.cur.fetchall()
        if (fetched == []):
            print ("Warning! Zero with " + query)
        return fetched

    def query_sylls (self, clu, type, sy, st):
        query = "SELECT * FROM Node WHERE (cluster=\"{clus}\" AND syll=\"{syll}\" AND stress=\"{stress}\");".format (clus=clu, type=type, syll=sy, stress=st)
        self.cur.execute (query)
        fetched = self.cur.fetchall()
        if (fetched == []):
            print ("Warning! Zero with " + query)
        return fetched

    def exec_from_file(self, filename):
        fd = open(filename, 'r')
        sqlFile = fd.read()
        fd.close()
        sqlCommands = sqlFile.split(';')
        for command in sqlCommands:
            try:
                c.execute(command)
            except OperationalError as msg:
                print("Command skipped: ", msg)
    
    def run_sql(self, command):
        try:
            self.cur.execute(command)
            self.conn.commit ()
        except OperationalError as msg:
            print("Command skipped: ", msg)
        print (command)


def q (s):
    return "\"" + str (s) + "\""