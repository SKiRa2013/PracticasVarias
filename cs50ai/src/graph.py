from collections import deque
from typing import Any

from action import Action
from constant_types import NodeType, SearchType

class GraphNode:
    """A node in a graph structure.
    
Attributes:
    name(str): The name of the node.
    data(Any): Data kept in the node.
    type(int): The type of the node (start, end, normal). Relate to NodeType class constants for node types.
    points_to(dict[Action, GraphNode]): A dictionary mapping, with a specific made Action, other GraphNode instances that this node points to.
    """
    
    def __init__(self, name: str, data: Any | None = None, node_type: int = NodeType.UNDEFINED_NODETYPE):        
        self.name: str = name
        self.node_type: int = node_type
        
        self.data: Any | None = data
        self.points_to: dict[Action, GraphNode] = {}
        
    def __str__(self):
        node_string = f"{'>' if self.node_type == NodeType.START_NODE else ''}Node(name={self.name}, data={self.data}){'<' if self.node_type == NodeType.END_NODE else ''}"

        for action, neighbor in self.points_to.items():
            node_string += f"\n  --[{action.tag}, cost={action.cost}]--> Node(name={neighbor.name})"
            
        return f"{node_string}\n"

    __repr__ = __str__

class Graph:
    """A graph structure consisting of GraphNode instances.

Attributes:
    start(GraphNode): The starting node of the graph.
    """
      
    def __init__(self):
        self.start: GraphNode = None
        
    def __str__(self) -> str:
        graph_string = "Graph Structure:\n\n"
        
        to_visit = deque()
        to_visit.append(self.start)
        
        visited = set()
        
        while to_visit:
            current = to_visit.popleft()
            
            if current in visited:
                continue
            
            visited.add(current)
            
            graph_string += f"{current}\n"
            
            for neighbor in current.points_to.values():
                if neighbor not in visited:
                    to_visit.append(neighbor)
                    
        return f"{graph_string}\n"
    
    __repr__ = __str__
    
    def insert_node(self, new_node: GraphNode):
        """Inserts a new node with the preset attribute values 
        """
        
    def add_node(self, new_node: GraphNode, parent: GraphNode = None, action: Action = None):
        """Adds a node to the graph.
        """
        
        if parent is None and action is None:
            if self.start is not None:
                raise ValueError("Graph already has a start node.")
            
            new_node.node_type = NodeType.START_NODE
            self.start = new_node
            return
        
        if parent is None or action is None:
            raise ValueError("Both parent and action must be provided to add a non-start node.")
            
        parent.points_to[action] = new_node
        
    def get_node_by_name(self, target_name: str) -> GraphNode | None:
        """Returns the node with the given target_name, or None if not found.
        """
        
        to_visit = [self.start]
        visited = set()
        
        while to_visit:
            current = to_visit.pop()
            
            if current.name == target_name:
                return current
            
            visited.add(current)
            
            for neighbor in current.points_to.values():
                if neighbor not in visited:
                    to_visit.append(neighbor)
                    
        return None
        
    def transition_function(self, node: GraphNode, action: Action) -> GraphNode | None:
        """Given a current node and an action, returns the resulting node after taking that action.
        
        If the action is not valid from the current node, returns None.
        """
        
        return node.points_to.get(action, None)

    def cost_sum(self, action_list: list[Action]) -> float:
        """Returns the total cost of a list of actions.
        """
        
        return sum(action.cost for action in action_list)
    
    def reach_goal(self, goal: GraphNode, search_type: int) -> list[Action]:
        """Sets the goal node and returns the path of actions to reach it using different search types.
        
        Use SearchType enumeration for search_type parameter.
        
Breadth-First Search:
        - UNIFORMED SEARCH ALGORITHM
        - Explores nodes at the present depth prior to moving on to nodes at the next depth level.
        - Utilizes a queue (FIFO) to explore the graph.
        
Depth-First Search:
        - UNIFORMED SEARCH ALGORITHM
        - Explores as far as possible along each branch before backtracking.
        - Utilizes a stack (LIFO) to explore the graph.
        
Uniform-Cost Search:
        - UNIFORMED SEARCH ALGORITHM
        - Expands the least costly node first, ensuring the optimal path is found.
        - This is an optimized version of Dijkstra's algorithm, because it only checks the nodes that the original points to instead of all nodes in the graph.
        """
        
        # Uninformed Search: Breadth-First Search and Depth-First Search
        if search_type in (SearchType.BREADTH_FIRST_SEARCH, SearchType.DEPTH_FIRST_SEARCH):
            frontier = deque()
            frontier.append({Action(cost=0, tag="Start from A"): self.start})
            
            explored_set = set()
            
            path = []
            
            while frontier:
                if search_type == SearchType.DEPTH_FIRST_SEARCH:
                    current: dict = frontier.pop() 
                    
                elif search_type == SearchType.BREADTH_FIRST_SEARCH: 
                    current: dict = frontier.popleft()
                
                path.append(list(current.keys())[0])
                
                current_node: GraphNode = current.get(list(current.keys())[0])
                
                if current_node == goal:
                    path.append(Action(cost=0, tag=f"Reached goal node {goal.name}"))
                    return path
                
                explored_set.add(current_node)
                print(f"Explored set, new element: Node {current_node.name}")
                
                for action, neighbor in current_node.points_to.items():              
                    if neighbor not in explored_set and neighbor not in frontier:
                        frontier.append({action: neighbor})
                    else:
                        print("Already explored or in frontier:", neighbor.name)
                        
            raise Exception(f"Goal node {goal.name} not reachable from start node {self.start.name}.")
        
        # Informed Search: Placeholder for future implementation
        if search_type in (SearchType.GREEDY_BEST_FIRST_SEARCH, SearchType.A_STAR_SEARCH):
            raise NotImplementedError("Informed search algorithms are not yet implemented.")
             
        raise NotImplementedError(f"Search ID #{search_type} is not recognized or is not yet implemented.")       