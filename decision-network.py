import sys
import copy

class Node:
    def __init__(self, id, num_of_values, parents, CPT):
        self.num_of_values = num_of_values
        self.parents = parents
        self.id = id
        self.CPT = CPT
        self.is_evidence = False
    def set_evidence(self, val):
        self.is_evidence = True
        self.value = val

class CPTRow:
    def __init__(self, parent_values, probabilities):
        self.parent_values = parent_values
        self.probabilities = probabilities
class DecisionTableRow:
     def __init__(self, target_val, decision, usefullness):
            self.target_val = target_val
            self.decision = decision
            self.usefullness = usefullness

def normalize(values):
    sum_v = sum(values)
    index = 0
    while index < len(values):
        values[index] = values[index] / sum_v
        index = index + 1
    return values
        
def enumeration_ask(target_var, nodes):
    value = 0
    results = []
    while value < target_var.num_of_values:
        target_var.set_evidence(value)
        val_prob = enumerate_all(copy.deepcopy(nodes))
        results.append(val_prob)
        value = value + 1
    #print(results)
    normalize(results)
    return results
    
def enumerate_all(nodes):
    if len(nodes) == 0: return 1.0
    y = nodes[0]
    values_assigned_to_parents = []
    for parent in y.parents:
        values_assigned_to_parents.append(parent.value)
    if(y.is_evidence):
        nodes.pop(0)
        nodes_cpy = copy.copy(nodes)
        return y.CPT[tuple(values_assigned_to_parents)][y.value] * enumerate_all(nodes_cpy)
        
    else:
        sum_val = 0.0;
        value = 0
        nodes.pop(0)
        while value < y.num_of_values:
            y.set_evidence(value)
            sum_val = sum_val + y.CPT[tuple(values_assigned_to_parents)][value] * enumerate_all(copy.deepcopy(nodes))
            value = value + 1
            
        return sum_val

        
        

nodes = []
#read input
input = open("sample-inputs/input1.txt")
#input = sys.stdin

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
    cpt = dict()
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

        
        cpt[tuple(parent_values_int)] = tuple(probabilities_int)
        i = i + 1
    nodes.append(Node(len(nodes), number_of_values, parents, cpt))
    number_of_nodes = number_of_nodes - 1

number_of_evidence_variables = int(input.readline())
while number_of_evidence_variables > 0:
    line = input.readline().split("\t")
    nodes[int(line[0])].set_evidence(int(line[1]))
    number_of_evidence_variables = number_of_evidence_variables - 1

target_variable = nodes[int(input.readline())]
number_of_decisions = int(input.readline())

decision_table = dict()
i = number_of_decisions * target_variable.num_of_values
while i > 0:
    line = input.readline().split("\t")
    target_var_val = int(line[0])
    decision_index = int(line[1])
    usefullness = float(line[2])
    decision_table[tuple([target_var_val, decision_index])] = usefullness
    i = i - 1

prob_results = enumeration_ask(target_variable, nodes)

decision_index = 0
usefullness_values = []
while decision_index < number_of_decisions:
    target_var_val_index = 0
    usefullness_sum = 0
    while target_var_val_index < target_variable.num_of_values:
        usefullness_sum = usefullness_sum + prob_results[target_var_val_index] * decision_table[tuple([target_var_val_index, decision_index])]
        target_var_val_index = target_var_val_index + 1
    usefullness_values.append(usefullness_sum)
    decision_index = decision_index + 1

for item in prob_results:
    print(item)
    
print(usefullness_values.index(max(usefullness_values)))

