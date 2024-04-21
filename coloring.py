#
#   Implementation of distance-2 coloring algorithm
#   based on the article "An efficient self-stabilizing distance-2 coloring
#   algorithm" written by Jean R.S. Blair, and Fredrik Manne.
#
#   Source: https://www.sciencedirect.com/science/article/pii/S0304397512000813
#
import matplotlib.pyplot as plt
import networkx as nx

# ------------------------------ Graph definition ------------------------------
N = 12 # size of the graph
MAX_ITER = 40 # maximum number of iterations

G = [[1, 11],
 [0, 2],
 [1, 3, 4],
 [2, 10],
 [2, 5],
 [4, 6],
 [5, 7, 8],
 [6, 9],
 [6, 9],
 [7, 8, 10],
 [3, 9, 11],
 [0, 10]]

if len(G) != N:
    print("Error: Graph size is not equal to N")


# ------------------------------ Global memory ---------------------------------
dist1deg = [0 for i in range(N)]
dist2deg = [0 for i in range(N)]
c = [1 for i in range(N)]
flag = [False for i in range(N)]
p = [0 for i in range(N)]
s = [0 for i in range(N)]
t = [0 for i in range(N)]
coloring = [False for i in range(N)]


# ---------------------------- Layer 1 functions -------------------------------
def Distance1(i):
    if dist1deg[i] != len(G[i]) + 1: # N[i] = len(G[i]) + 1
        dist1deg[i] = len(G[i]) + 1


def Distance2(i):
    dist2 = 0
    for j in G[i]:
        dist2 += dist1deg[j]
    dist2 = dist2 - dist1deg[i] + 2

    if dist2deg[i] != dist2:
        dist2deg[i] = dist2


def Reset(i):
    # We check if all of the neighbours allow the coloring
    p_neighbour = True
    for j in G[i]:
        if coloring[j] == True:
            p_neighbour = False
            break

    if coloring[i] == True and p_neighbour == False:
        # We reset the coloring because not all
        # of the neighbours allow the coloring
        coloring[i] = False
    elif flag[i] == False:
        # We didn't ask for coloring before starting
        coloring[i] = False


# ---------------------------- Layer 2 functions -------------------------------
def NextColor(i, j):
    for w in range(max(1, c[j]), dist2deg[i] + 1):
        # We check if the color is already used by neighbour other than j
        color_used = False

        for k in G[i]:
            if k != j and c[k] == w:
                color_used = True
                break

        if i != j and w == c[i]:
            color_used = True

        if color_used == False:
            return (c[j], w)
        
    return (False, False)


def CorrectPointer(i):
    # We look for the node that wants to colored or has conflict
    for j in G[i]:
        # Node wants to color itself
        if flag[j] == True:
            c_j, w_j = NextColor(i, j)
            return (j, c_j, w_j)
        
        # Node has conflict with one of our neighbours
        for k in G[j]:
            if k != j and c[k] == c[j]:
                c_j, w_j = NextColor(i, j)
                return (j, c_j, w_j)
        
        if j != i and c[j] == c[i]:
            c_j, w_j = NextColor(i, j)
            return (j, c_j, w_j)

    # No node wants to color itself or has conflict        
    return (False, False, False)


def NotifyNeighbour(i):
    # If we don't actively help other neighbour in this time, we can look for node
    # to help
    if p[i] == False or coloring[p[i]] == False:
        p[i], s[i], t[i] = CorrectPointer(i)


def RespondToColor(i):
    # If we actively help other neighbour, we respond to his proposed color
    if p[i] != False and coloring[p[i]] == True:
        s[i], t[i] = NextColor(i, p[i])


# ---------------------------- Layer 3 functions -------------------------------
def NeedNewColor(i):
    # We check if we are not the problem and need to recolor ourselves
    if flag[i] == False:
        # Check if any neighbour has a problem with us (and our current color)
        for j in G[i]:
            if p[j] == i and s[j] == c[i] and t[j] > c[i]:
                flag[i] = True

    # We check if we don't use too much colors
    if (c[i] >= 1 and c[i] > dist2deg[i]) or c[i] <= 0:
        flag[i] = True

def StartRecoloring(i):
    # We want to color but didn't start yet
    if flag[i] == True and coloring[i] == False:
        # We check if all of the neighbours allow the coloring
        allow = True
        for j in G[i]:
            # Some neighbour is not helping us at the moment
            # or he is thinking of our old color
            if p[j] != i or s[j] != c[i]:
                allow = False
                break

        if allow == True:
            coloring[i] = True
            c[i] = -1 # Dummy color to start the process
            s[i], t[i] = NextColor(i, i)


def ChangeColor(i):
    # If we are in the process of recoloring, then we change the color
    # and wait for the response from the neighbours
    if coloring[i] == True:
        # Every neighbour acknowledges the new color
        acknowledges = True
        for j in G[i]:
            if p[j] == i and s[j] != c[i]:
                acknowledges = False
                break

        if acknowledges == True:
            # We check if anyone has a problem with our new color
            agree = True
            for j in G[i]:
                if p[j] == i and s[j] == c[i] and t[j] > c[i]:
                    agree = False
                    break

            if agree == False:
                # We need to change the color
                if c[i] == -1:
                    c[i] = 0 # We move to another dummy color
                else:
                    # We choose the largest color proposed by neighbours
                    c[i] = max([t[j] for j in G[i]])
                # We check if we are aware of any conflicts with our neighbours
                s[i], t[i] = NextColor(i, i)


def DoneColoring(i):
    # Check if we are done with coloring - so every neighbour agrees with our color
    if coloring[i] == True:
        done = True
        for j in G[i]:
            if p[j] == i and (s[j] != c[i] or t[j] != c[i]):
                done = False
                break

        if done == True:
            coloring[i] = False
            flag[i] = False


# -------------------------- Distance-2 coloring -------------------------------
def Distance2Coloring(i):
    # Layer 1 functions
    Distance1(i)
    Distance2(i)
    Reset(i)

    # Layer 2 functions
    NotifyNeighbour(i)
    RespondToColor(i)

    # Layer 3 functions
    NeedNewColor(i)
    StartRecoloring(i)
    ChangeColor(i)
    DoneColoring(i)


# --------------------------- Utility functions --------------------------------
def PrintState():
    print("dist1deg = ", dist1deg)
    print("dist2deg = ", dist2deg)
    print("c = ", c)
    print("flag = ", flag)
    print("p = ", p)
    print("s = ", s)
    print("t = ", t)
    print("coloring = ", coloring)
    print("\n")


color_map = {-1: '#D496A7', 0: '#B24C63', 1: '#5438DC', 
              2: '#357DED', 3: '#56EEF4', 4: '#32E875',
              5: '#F3E749', 6: '#F3A649', 7: '#F36849',
              8: '#F34949', 9: '#F3498D', 10: '#B349F3'}


def DisplayGraph(iter, positions):
    node_colors = [color_map[color] for color in c]

    plt.text(0.5, 1.5, s=f"Iteration {iter}", fontsize=22, horizontalalignment='right', verticalalignment='top')
    nx.draw(graph_image, pos=positions, node_size=800, with_labels=True, cmap=plt.get_cmap('jet'),
            node_color=node_colors)
    plt.savefig(f'images/iter_{str(iter).zfill(3)}.png')
    plt.clf()          


def CheckColoring():
    # Check that every node in distance 1 has different color
    for i in range(N):
        for j in G[i]:
            if c[i] == c[j]:
                return False
            
    # Check that every node in distance 2 has different color
    for i in range(N):
        for j in G[i]:
            for k in G[j]:
                if i != k and c[i] == c[k]:
                    return False
                
    return True

# -------------------------- Algorithm execution -------------------------------
# Prepare graph for visualization
graph_image = nx.Graph()
for v in range(N):
    graph_image.add_node(v)

for v in range(N):
    for u in G[v]:
        if v < u:
            graph_image.add_edge(v, u)

random_pos = nx.random_layout(graph_image, seed=1410)
pos = nx.spring_layout(graph_image, pos=random_pos)

# Start the algorithm
iter = 0

while True:
    iter += 1
    print("iter = ", iter)

    for node in range(N):
        Distance2Coloring(node)

    # Display state information
    PrintState()
    DisplayGraph(iter, pos)
    if iter == MAX_ITER:
        break

# Check the final coloring
print(f"[Result] Iterations: {iter}")
valid = CheckColoring()
if valid:
    print("[Result] Coloring is valid! :-)")
else:
    print("[Result] Coloring is invalid! :'(")
