# tree matching algorighm


import DatabaseInterface

# there could be two ways of matching a tree, 
# 1) matching the tree by trying to get an other tree according to right option selection
#   the option selection would be predefined according to the question asked
# 2) matching by sight navigation : asking what's next and go there one by one
#   this way of doing should be used when the initial tree is not built yet, the model tree and
#   the matching tree could be built simultaneously
#   the go-along building process could change the model tree dynamically, according to what is found
#   the go-along process could ask alternatively for similarities or dissimilarities
#   process not automatizeable since it is not known in advanced what is searched

 
# handling of match command
# match(Tree = {'A':'B'}, score = (1, 0, 0, 0), max = 10 )

# "max" for maximum number of returned distinct subtrees (best score first), 
#   this occurs if top element has several instances or different subtrees are possible
#   by default only one tree is returned, the one with the best score result
# "score" describes the reward of similarity, or dissimilarity, tuple like (5, 1, 2, 3) :
#    (element right, element moved or duplicated, new element inserted, element deleted ) 
#   this parameter is mandatory
# "scoreratio", tuple like (0.5, 0, 0, 0), number between 0 an 1 is for mimimum percentage score to achieve
#   here sum of scores for similar elements must be at least 50%  
#   the sum of all score ratios must be below 1, otherwise it will be difficult to find a match
#   by default no score ratio is required
# "scorefromlimit", tuple like (0, 0, 0, 0  ) specifies from what starting level the score applies
#   0 is the level of 'A'
#   by default it is the first element
# "scoretolimit", tuples like (10, 10, 10, 10 ) specifies to what level the score goes
#   scoretolimit must be higher that score from limit
#   scoretolimit cannot be deeper than the input tree to match, ie level of B = 1
#   by default it is the size of the tree
#
# Ex: for a desired exact match, the score parameter will be selected so that only similarity is rewarded

# subtree search tactic 1 , horizontal layered building : 
# 1) identify all instances of 'A'
# 2) add a found linked element to the subtree of A, compute the score, reiterate
# 3) when all linked elements of instances of A have been found, 
#   keep the (max * tree depth) subtrees with the best score
# 4) reiterate 2 and 3 at next lower level 
#   at each iteration, reduce the kept subtrees to (max * (input tree depth - current depth))

def match (Tree, **option):
    if Tree == {} : 
        return {}



# iterator for sight navigation??
# gives what is below, what is at the side, and what is above
# provides unique identifier of these items, for further step