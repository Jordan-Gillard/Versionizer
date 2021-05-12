class FunctionNode:
    def __init__(self, node):
        self.name = node.name
        self.num_params = len(node.args.args)
        self.returns = node.returns
        self.body = node.body

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, FunctionNode):
            return False
        return (self.name == other.name and
                self.num_params == other.num_params and
                self.returns == other.returns)

    def __hash__(self):
        return hash(self.name) + hash(self.num_params)

    def __repr__(self):
        return f"{self.name}, {self.num_params} params -> {self.returns}"
