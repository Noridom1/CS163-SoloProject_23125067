MyEdges = {}
CheckEdges = {}
with open("Testing/Edges.txt", 'r') as f:
    for line in f:
        data = line.split()
        MyEdges[(int(data[0]), int(data[1]))] = int(data[2])
with open("Testing/CheckEdges.txt", 'r') as f:
    for line in f:
        data = line.split()
        CheckEdges[(int(data[0]), int(data[1]))] = int(data[2])
with open("Testing/CheckEdgesResult.txt", 'w') as f:
    NotExist = []
    Wrong = []
    for edge, weight in MyEdges.items():
        if edge not in CheckEdges:
            NotExist.append((edge[0], edge[1], weight))
            continue
        if weight != CheckEdges[edge]:
            Wrong.append((edge[0], edge[1], weight, CheckEdges[edge]))
    f.write("Do not exist:\n")
    for notexist in NotExist:
        f.write(f"{notexist}\n")
    f.write("Wrong:\n")
    for wrong in Wrong:
        f.write(f"{wrong}\n")
        


