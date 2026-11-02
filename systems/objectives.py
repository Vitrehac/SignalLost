class ObjectiveSystem:
    def __init__(self):
        self.objectives = [
            "Restore power to the facility",
            "Enter the control room ",
            "Investigate the facility"
        ]

        self.current_index = 0


    def get_current_objective(self):
        return self.objectives[self.current_index]
    
    def advance(self):
        if self.current_index < len(self.objectives) - 1:
            self.current_index += 1