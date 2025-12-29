from constant_types import NodeType, SearchType
from graph import Graph, GraphNode
from action import Action

class MazeExample:
    def __init__(self):
        self.maze = Graph()
        
        node_list: list[GraphNode] = []
        
        with open("./src/data/maze1.txt", "r") as maze_file:
            maze_text = maze_file.readlines()
            
            for j in range(len(maze_text)):
                for i in range(len(maze_text[j])):
                    char = maze_text[j][i]
                    
                    if char == "X" or char == "\n":
                        continue
                    
                    node_types = {
                        "S": {
                            "text": "start(",
                            "nt_value": NodeType.START_NODE
                        },
                        
                        "O": {
                            "text": "goal(",
                            "nt_value": NodeType.END_NODE
                        },
                        
                        " ": {
                            "text": "blank(", 
                            "nt_value": NodeType.NORMAL_NODE
                        }
                    }
                    
                    node_type = node_types[char]
                    node = GraphNode(name=f"{node_type['text']}{i}, {j})", data={"pos": (i, j)}, node_type=node_type["nt_value"])

                    if char == "S":
                        self.maze.start = node
                        self.initial_coords = (i, j)
                        
                    elif char == "O":
                        self.goal_coords = (i, j)

                    node_list.append(node)
                    
        self.assign_connections(node_list)
        
    def assign_connections(self, nodes: list[GraphNode]):
        coord_list = [node.data["pos"] for node in nodes]
        
        for node in nodes:
            x, y = node.data["pos"]
            
            possible_moves = [
                {
                    "direction": "Up",
                    "value": (x, y - 1)
                },
                {
                    "direction": "Down",
                    "value": (x, y + 1)
                },
                {
                    "direction": "Left",
                    "value": (x - 1, y)
                },
                {
                    "direction": "Right",
                    "value": (x + 1, y)
                }
            ]
            
            for move in possible_moves:
                if move["value"] in coord_list:
                    neighbor_node = next(n for n in nodes if n.data["pos"] == move["value"])
                    node.points_to.update(
                        {
                            Action(tag=f"From {node.name} move {move['direction']} to {neighbor_node.name}", cost=1): neighbor_node
                        }
                    )
                   
        
        """
        XXXXXXXXXXXXXXXX
        X XXXX   O     X
        X XXXX XXXXXX  X
        X              X
        XSXXXXXXX XXXX X
        XX             X
        XXXXXXXXXXXXXXXX
        """
        

if __name__ == "__main__":
    maze_ex = MazeExample()
    
    search_type = input("Enter search type (ninf/inf): ")
    
    if search_type not in ("ninf", "inf"):
        print("Invalid search type. Please enter 'ninf' for non-informed search or 'inf' for informed search.")
    
    else:
        search_options = {
            "dfs": SearchType.DEPTH_FIRST_SEARCH,
            "bfs": SearchType.BREADTH_FIRST_SEARCH,
            "ucs": SearchType.UNIFORM_COST_SEARCH
        } if search_type == "ninf" else {
            "greedy": SearchType.GREEDY_BEST_FIRST_SEARCH,
            "astar": SearchType.A_STAR_SEARCH
        }
        
        print("Choose a search algorithm (", end="")
        
        algoritms = ""
        
        for search_algorithm in search_options.keys():
            algoritms += search_algorithm + ", "
        
        chosen_search = input(f"{algoritms[:-2]}): ")
        
        actions = maze_ex.maze.reach_goal(
            maze_ex.maze.get_node_by_name(
                f"goal({maze_ex.goal_coords[0]}, {maze_ex.goal_coords[1]})"
            ),
            
            search_options[chosen_search]
        )
        
        print("-" * 20)
        print(actions)
    
    
      
    
                