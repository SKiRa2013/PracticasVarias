class Action:
    """An action that is taken so an agent can move from one graph node to another.

Attributes:
    tag(str, optional): The tag/name of the action.
    cost(float): The cost associated with taking this action. Defaults to 1.0.
    """    
    
    def __init__(self, tag: str, cost: float = 1.0):
        self.tag: str = tag
        self.cost: float = cost
    
    def __str__(self) -> str:
        return f"Action(tag='{self.tag}', cost={self.cost})"
    
    __repr__ = __str__