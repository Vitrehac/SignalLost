class ObjectiveSystem:
    def get_current_objective(self, state):
        if not state.power_restored:
            return "Restore power to the facility"
        
        if not state.control_room_entered:
            return "Enter the control room"
        
        if not state.security_unlocked:
            if not state.computer_read:
                return "Find the security code (check the computer)"
            return "Unlock containment access"

        if not state.containment_entered:
            return "Find the containment chamber"
        
        return "Investigate the containment sector"