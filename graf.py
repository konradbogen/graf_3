
import numpy as np 
from sql import SQL

input = ""
output = ""

deleted = []

questions = []
file = "new"
clean_lines = []

sql = SQL (file)
cluster = ""
path_toggle = False
path_index = 0
follow_path = -1
cur_path_ix = 0

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
    while "  " in wo:
        wo = wo.replace ("  ", " ")
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
    if "1" in line or "2" in line or "3" in line or "4" in line or "5" in line or "6" in line or "7" in line:
        type = "m"
    else:
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
        sql.add_to_path (id)        

def toggle_path ():
    global path_toggle
    if path_toggle == False:
        path_toggle = True
        sql.insert_new_path ()
    else:
        path_toggle = False

i = 0
for line in lines:
    normalized = line.replace ("\n", "")
    if line.startswith ("!") == False:
        input += line.replace ("-", "")
    if line.startswith ("!"):
        delete_line (line)
    elif line.startswith ("--"):
        toggle_path ()
    elif line.endswith ("?"):
        questions.append (normalized.replace ("?", ""))
    else:
        if line not in deleted and len(line) > 2 and line.find (">") == -1:
            parse_line (line)
            clean_lines.append (line.replace ("-", "").replace ("\n", ""))
            if line.startswith ("-"):
                add_edge (lines [i - 1], line)
    add_to_path (line)
    i += 1

def trigger (last_line):
    global follow_path
    global cur_path_ix
    if follow_path != -1:
        id = sql.get_id_at_ix (follow_path, cur_path_ix)
        line = sql.content_from_id (id)
        if cur_path_ix == sql.get_last_index (follow_path):
            follow_path = -1
            cur_path_ix = 0
        else:
            cur_path_ix += 1
        return line
    if last_line != "":
        incidents = sql.incident_edges (last_line)
        if len (incidents) > 0:
            incident = incidents [int (np.random.rand () * len (incidents))]
            to = incident [1]
            line = sql.content_from_id (to)
            check_for_path_start (to)
            return line
    global output
    lines = sql.query (cluster, "t")
    i = int (np.floor (np.random.rand () * len (lines)))
    check_for_path_start (lines [i][0])
    return lines [i][1] 

def check_for_path_start (id):
    global follow_path
    follow_path = sql.is_path_start (id)
    return follow_path

last_line = ""
if len (clean_lines) > 0:
    last_line = clean_lines [len (clean_lines) - 1]
    last_id = sql.get_id (last_line)
    cluster = sql.cluster_from_id (last_id)
    check_for_path_start (last_id)


marked = []
n_nodes = sql.n_nodes ()
for i in range (0, n_nodes):
    marked.append (False)

def dfs (line):
    global output
    incidents = sql.incident_edges (line)
    id = sql.get_id (line)
    if len (incidents) > 0:
        for incident in incidents:
            to = other (incident, id)
            if marked [to] == False:
                line = sql.content_from_id (to)
                marked [to] = True
                output += line + "\n"
                dfs (line)
    else:
        pass

def answer_questions ():
    global questions
    for question in questions:
        id = sql.get_id [question]
        cluster = sql.cluster_from_id (id)
        lines = sql.query (cluster, "t")
        for line in lines:
            output += "   >" + line [1] + "\n"


def other (edge, node):
    if edge [0] == node:
        return edge [1]
    else:
        return edge [0]

#if "?" in input:
   #for i in range (0, 10):
    #    line = trigger (last_line)
    #    if line == None:
    #        break
    #    if line != last_line:
    #        output += line + "\n"
    #    last_line = line

dfs (last_line)
        

if input.endswith ("\n") == False:
    input = input + "\n"
with open(file + '.txt', 'w') as f:
    f.write (input + output)





