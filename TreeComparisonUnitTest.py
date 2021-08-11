import TreeComparison

# test the counting of elements
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


# test the 1D transformation
tree = {'B-2':'D-1'}
if TreeComparison.Tree1Dtransformation(tree) != ['B-2','D-1']:
    print("error in tree 1D transformation")

tree = {'B-2':['D-1']}
if TreeComparison.Tree1Dtransformation(tree) != ['B-2','D-1']:
    print("error in tree 1D transformation")


tree = {'B-2': ['C-1', {'B-1': ['V-1']}, 'D-1']}
if TreeComparison.Tree1Dtransformation(tree) != ['C-1','B-2','B-1', 'V-1','D-1']:
    print("error in tree 1D transformation")


tree = {'A-1': [{'B-2': ['D-1', 'C-1', {'B-1': ['X-1']}]}]}
if TreeComparison.Tree1Dtransformation(tree) != ['A-1','D-1','B-2','C-1','B-1','X-1']:
    print("error in tree 1D transformation")

tree = {'A-1': [{'B-2': ['D-1', 'C-1', {'B-1': [{'X-1':'y'}]}]}]}
if TreeComparison.Tree1Dtransformation(tree) != ['A-1','D-1','B-2','C-1','B-1','X-1','y']:
    print("error in tree 1D transformation")

tree = {'A' : [{'B': [{'G':['H']}]}, 'C', {'D': ['E', 'F']}]}
if TreeComparison.Tree1Dtransformation(tree) != ['B','G','H','A','C','E','D','F']:
    print("error in tree 1D transformation")

# marche pas
#tree = {'A' : [{'B': {'G':'H'}}, 'C', {'D': ['E', 'F']}]}
#if TreeComparison.Tree1Dtransformation(tree) != ['B','G','H','A','C','E','D','F']:
#    print("error in tree 1D transformation")
#    print(TreeComparison.Tree1Dtransformation(tree))

# test the tree comparison functions
Tree1 = ['B','G','H','A','C','E','D','F']
Tree2 = ['B','G','H','A', 'A', 'C','E','D','M']
Matrix = TreeComparison.ComparisonMatrix(Tree1, Tree2)
print(Matrix)
TreeComparison.PlotMatchingMatrix(Matrix)

#TreeComparison.ComparisonReport(Tree1,Tree2)