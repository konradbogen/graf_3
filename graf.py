
import numpy as np 
from sql import SQL

input = ""
output = ""

deleted = []

file = "pad"
sql = SQL (file)
cluster = "Mond"
path_toggle = False
path_index = 0

with open(file + '.txt') as f:
    lines = f.readlines ()

def parse_line (line):
    cluster = get_cluster (line)
    harm, type, content = get_content (line)
    sylls, stress = count_sylls (content)
    sql.insert (cluster, harm, type, content, sylls, stress)

def delete_line (line):
    cont = line.replace ("!", "")
    deleted.append (cont)
    acont = cont.replace ("\n", "")
    sql.delete (acont)

def remove_brackets(content):
    content = content.replace ("[", "")
    content = content.replace ("]", "")
    return content

def count_sylls (content):
    i = content.find ("(")
    if i == -1:
        wo = content
    else:
        wo = content[0:i:1]
    sylls = wo.split (" ")
    stress = 0
    n_sylls = len (sylls)
    for syll in sylls:
        stress += 1
        if "[" in syll:
            break
    return n_sylls, stress

def get_content(line):
    harm = ""
    type = "t"
    content = line.strip ().replace ("-", "").replace ("\n", "")
    if "(" in line:
        type = "m"
        h_s, h_e = get_bracket_indices (line, "(", ")")
        harm = line[h_s+1:h_e:1]
        content = line [0:h_s:1].replace ("\n", "")
    return harm,type,content

def get_cluster(line):
    b_s, b_e = get_bracket_indices (line, "[", "]")
    cluster = line[b_s+1:b_e:1]
    return cluster
   
def get_bracket_indices (line, open, close):
    s = line.find (open)
    e = line.find (close)
    return s, e

def add_edge (a, b):
    a = a.replace ("\n", "").replace ("-", "")
    b = b.replace ("\n", "").replace ("-", "")
    a_id = sql.get_id (a)
    b_id = sql.get_id (b)
    sql.add_edge (a_id, b_id)
    print (a_id)

def change_cluster ():
    global cluster
    clus = sql.get_clusters ("t")
    i = int (np.floor (np.random.rand () * len (clus))) 
    cluster = clus[i][0]

def add_to_path (line):
    a = line.replace ("\n", "").replace ("-", "")
    global path_toggle
    if (path_toggle == True):
        id = sql.get_id (a)
        

def toggle_path ():
    global path_toggle
    if path_toggle == False:
        path_toggle = True
        sql.insert_new_path ()
    else:
        path_toggle = False

i = 0
for line in lines:
    if line.startswith ("!"):
        delete_line (line)
    elif line.startswith ("--"):
        toggle_path ()
    else:
        if line not in deleted and len(line) > 2:
            parse_line (line)
            if line.startswith ("-"):
                add_edge (lines [i - 1], line)
    add_to_path (line)
    i += 1

def trigger (last_line):
    if last_line != "":
        incidents = sql.incident_edges (last_line)
        if len (incidents) > 0:
            incident = incidents [int (np.random.rand () * len (incidents))]
            to = incident [1]
            line = sql.content_from_id (to)
            return line
    global output
    lines = sql.query (cluster, "t")
    i = int (np.floor (np.random.rand () * len (lines)))
    return lines [i][1] 


last_line = ""
for i in range (0, 10):
    line = trigger (last_line)
    if line != last_line:
        output += line + "\n"
    last_line = line
    if (np.random.rand () < 0.4):
        change_cluster ()


with open(file + '.txt', 'w') as f:
    f.write (output)





