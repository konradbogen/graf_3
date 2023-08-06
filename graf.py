
import numpy as np 
from sql import SQL

input = ""
output = ""

deleted = []

questions = []
file = "m"
clean_lines = []

sql = SQL (file)
cluster = ""
used_clusters = []
path_toggle = False
path_index = 0
follow_path = -1
cur_path_ix = 0

with open(file + '.txt') as f:
    t = f.read ()
    lines = t.split (";")
    print (lines)

def parse_line (line):
    cluster = get_cluster (line)
    harm, type, content = get_content (line)
    sylls, stress = count_sylls (content)
    sql.insert (cluster, harm, type, content, sylls, stress)

def delete_line (line):
    cont = line.replace ("!", "")
    deleted.append (cont)
    sql.delete (cont)

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
    content = line.strip ().replace ("-", "")
    if "(" in line:
        type = "m"
        h_s, h_e = get_bracket_indices (line, "(", ")")
        harm = line[h_s+1:h_e:1]
        content = line [0:h_s:1]
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
    a = a.replace ("-", "")
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
        if a != "":
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
    if line.startswith ("--"):
        toggle_path ()
    if normalized.endswith ("?"):
        questions.append (normalized.replace ("?", ""))
    if line.startswith ("!"):
        delete_line (line)
    else:
        if line not in deleted and len(line) > 2 and line.find ("•") == -1 and line.find ("?") == -1:
            line = line.replace ("-", "")
            input += line
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
    lines = sql.query (cluster)
    i = int (np.floor (np.random.rand () * len (lines)))
    check_for_path_start (lines [i][0])
    return lines [i][1] 

def check_for_path_start (id):
    global follow_path
    global cur_path_ix
    follow_path = sql.is_path_start (id)
    cur_path_ix = 0
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

of_stop = 0
def dfs (line):
    global output
    global used_clusters
    global follow_path
    global cur_path_ix
    global of_stop
    of_stop += 1
    incidents = sql.incident_edges (line)
    id = sql.get_id (line)
    check_for_path_start (id)
    while follow_path != -1:
        id = sql.get_id_at_ix (follow_path, cur_path_ix)
        p_line = sql.content_from_id (id)
        output += p_line + "\n"
        check_for_path_start (id)
        #print_cluster(p_line)
        if cur_path_ix == sql.get_last_index (follow_path):
            follow_path = -1
            cur_path_ix = 0
        else:
            cur_path_ix += 1
    if len (incidents) > 0:
        for incident in incidents:
            to = other (incident, id)
            if marked [to] == False and sql.exists (to):
                line = sql.content_from_id (to)
                cluster = sql.cluster_from_id (to)
                if cluster not in used_clusters:
                    used_clusters.append (cluster)
                marked [to] = True
                output += line + "\n"
                #print_cluster(line)
                dfs (line)
    else:
        print ("0")
        #id = sql.path_start ()
        #line = sql.content_from_id (id)
        #if of_stop < 200:
            #dfs (line)


def print_cluster(line):
    global output
    if line.startswith ("[") and line.endswith ("]"):
        cluster = line.replace ("[", "").replace ("]", "")
    else:
        id = sql.get_id (line) 
        cluster = sql.cluster_from_id (id)
    lines = sql.query (cluster)
    for c_line in lines:
        if c_line[1] != line:
            output += c_line [1] + "\n"


def other (edge, node):
    if edge [0] == node:
        return edge [1]
    else:
        return edge [0]

#if "?" in input:
""" for i in range (0, 10):
    line = trigger (last_line)
    if line == None:
        break
    if line != last_line:
        output += line + "\n"
    last_line = line """

def remaining_clusters ():
    global output
    cs = sql.get_clusters ("t")
    for cl in cs:
        output += "[{cl}]".format (cl=cl[0]) + "\n"

if last_line != "":
    dfs (last_line)
for q in questions:
    if q.find ("•") == -1:
        print_cluster(q)
    pass

if input.endswith ("\n") == False:
    input = input + "\n"
print (input + output)
with open(file + '.txt', 'w') as f:
    f.write (input + output)






