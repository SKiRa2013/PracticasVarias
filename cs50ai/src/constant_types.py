class NodeType:
    """
Constants for node types:
    
    UNDEFINED_NODETYPE(int): Constant representing an undefined NodeType. Value: -1.    
    START_NODE(int): Constant representing a start NodeType. Value: 0.    
    END_NODE(int): Constant representing an end NodeType. Value: 1.    
    NORMAL_NODE(int): Constant representing a normal NodeType. Value: 2.
    """
    
    UNDEFINED_NODETYPE = -1
    START_NODE = 0
    END_NODE = 1
    NORMAL_NODE = 2
    
class SearchType:
    """
Enumeration representing different types of search strategies:

    BREADTH_FIRST_SEARCH(int): Constant representing breadth-first search. Value: 0.    
    DEPTH_FIRST_SEARCH(int): Constant representing depth-first search. Value: 1.
    UNIFORM_COST_SEARCH(int): Constant representing uniform-cost search. Value: 2.
    GREEDY_BEST_FIRST_SEARCH(int): Constant representing greedy best-first search. Value: 3.       
    A_STAR_SEARCH(int): Constant representing A* search. Value: 4.
    """
    BREADTH_FIRST_SEARCH = 0
    DEPTH_FIRST_SEARCH = 1
    UNIFORM_COST_SEARCH = 2     # Optimized Dijkstra, checks the nodes that the "original" points to, instead of all nodes
    GREEDY_BEST_FIRST_SEARCH = 3
    A_STAR_SEARCH = 4
    