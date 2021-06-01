import TreeComparison


tree = {'B-2':'D-1'}
if TreeComparison.NumberOfElements(tree) != 2:
    print("error in tree element numbering")

tree = {'B-2':['D-1']}
if TreeComparison.NumberOfElements(tree) != 2:
    print("error in tree element numbering")   

tree = {'B-2': ['C-1', {'B-1': ['V']}, 'D-1']}
if TreeComparison.NumberOfElements(tree) != 5:
    print("error in tree element numbering")

tree = {'A-1': [{'B-2': ['D-1', 'C-1', {'B-1': ['X-1']}]}]}
if TreeComparison.NumberOfElements(tree) != 6:
    print("error in tree element numbering")

tree = {'A-1': [{'B-2': ['D-1', 'C-1', {'B-1': [{'X-1':'y'}]}]}]}
if TreeComparison.NumberOfElements(tree) != 7:
    print("error in tree element numbering")