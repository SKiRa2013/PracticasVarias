from graph import Graph, GraphNode
from constant_types import NodeType, SearchType
from action import Action

class GraphExample:
    """Class representing example 1 from CS50 AI course and "Search" lecture.
    """

    def __init__(self):
        self.graph = Graph()
        
        self.graph.add_node(new_node=GraphNode("A"))
        self.graph.add_node(new_node=GraphNode("B"), parent=self.graph.start, action=Action(tag="A->B"))
        
        # Adding edge case A<->B:
        self.graph.get_node_by_name("B").points_to.update({Action(tag="B->A"): self.graph.start})
        
        self.graph.add_node(new_node=GraphNode("C"), parent=self.graph.get_node_by_name("B"), 
                               action=Action(tag="B->C"))
        
        self.graph.add_node(new_node=GraphNode("D"), parent=self.graph.get_node_by_name("B"), 
                               action=Action(tag="B->D"))
        
        self.graph.add_node(new_node=GraphNode("E", node_type=NodeType.END_NODE), parent=self.graph.get_node_by_name("C"),
                               action=Action(tag="C->E"))
        
        self.graph.add_node(new_node=GraphNode("F", node_type=NodeType.END_NODE), parent=self.graph.get_node_by_name("D"),
                               action=Action(tag="D->F"))
        
        print(self.graph)
                
        
if __name__ == "__main__":
    graph_ex = GraphExample()
    actions = graph_ex.graph.reach_goal(graph_ex.graph.get_node_by_name("E"), 
                                        {"dfs": SearchType.DEPTH_FIRST_SEARCH,
                                         "bfs": SearchType.BREADTH_FIRST_SEARCH}[input("Enter search type (dfs/bfs): ")])
    
    print(f"Actions to reach goal E: {actions}\n")
    print(f"Path cost: {graph_ex.graph.cost_sum(actions)}")    
    