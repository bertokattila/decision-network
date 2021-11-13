import sys

class Node:
    def __init__(self, id, num_of_values, parents, CPT):
        self.num_of_values = num_of_values
        self.parents = parents
        self.id = id
        self.CPT = CPT

class CPTRow:
    def __init__(self, parent_values, probabilities):
        self.parent_values = parent_values
        self.probabilities = probabilities


nodes = []
#read input
input = open("sample-inputs/input0.txt")
#f = sys.stdin

number_of_nodes = int(input.readline())
while number_of_nodes > 0:
    line = input.readline().split("\t")
    number_of_values = int(line[0])
    number_of_parents = int(line[1])
    number_of_parents_iterator = number_of_parents;

    i = 2
    parents = []
    while number_of_parents_iterator > 0:
        parent_index = int(line[i])
        parents.append(nodes[parent_index])
        number_of_parents_iterator = number_of_parents_iterator - 1
        i = i + 1
    cpt = []
    while i < len(line):
        parent_values_int = []
        probabilities_int = []
        if(number_of_parents > 0):
            parent_values = line[i].split(":")[0]
            probabilities = line[i].split(":")[1]
            parent_values = parent_values.split(",")
            probabilities = probabilities.split(",")
           
            for item in parent_values:
                parent_values_int.append(int(item))
            for item in probabilities:
                probabilities_int.append(float(item))
        else:
            probabilities = line[i]
            probabilities = probabilities.split(",")
            for item in probabilities:
                probabilities_int.append(float(item))

        cpt_row = CPTRow(parent_values_int, probabilities_int)
        cpt.append(cpt_row)
        i = i + 1
    nodes.append(Node(len(nodes), number_of_values, parents, cpt))
    number_of_nodes = number_of_nodes - 1


print("kesz")
