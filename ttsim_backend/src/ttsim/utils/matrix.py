from typing import List, Dict, Any, Optional
import numpy as np

class BoardMatrix:
    """Represents the Turing Tumble board as a matrix."""
    
    def __init__(self, size: int = 8):
        """Initialize an empty board matrix.
        
        Args:
            size: Size of the board (default: 8x8)
        """
        self.size = size
        self.grid = np.full((size, size), "empty", dtype=object)
        self.components: Dict[str, List[Dict[str, Any]]] = {
            "bits": [],
            "gears": [],
            "ramps": []
        }
    
    def place_component(self, component_type: str, x: int, y: int, state: Optional[Dict[str, Any]] = None) -> bool:
        """Place a component on the board.
        
        Args:
            component_type: Type of component (bit, gear, ramp)
            x: X coordinate
            y: Y coordinate
            state: Component state (optional)
            
        Returns:
            bool: True if placement was successful
        """
        if not self._is_valid_position(x, y):
            return False
            
        if self.grid[y][x] != "empty":
            return False
            
        self.grid[y][x] = component_type
        component = {
            "type": component_type,
            "position": {"x": x, "y": y},
            "state": state or {}
        }
        self.components[component_type + "s"].append(component)
        return True
    
    def remove_component(self, x: int, y: int) -> bool:
        """Remove a component from the board.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            bool: True if removal was successful
        """
        if not self._is_valid_position(x, y):
            return False
            
        component_type = self.grid[y][x]
        if component_type == "empty":
            return False
            
        self.grid[y][x] = "empty"
        components = self.components[component_type + "s"]
        for i, comp in enumerate(components):
            if comp["position"]["x"] == x and comp["position"]["y"] == y:
                components.pop(i)
                break
        return True
    
    def get_component(self, x: int, y: int) -> Optional[Dict[str, Any]]:
        """Get component at specified position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Optional[Dict[str, Any]]: Component data if found
        """
        if not self._is_valid_position(x, y):
            return None
            
        component_type = self.grid[y][x]
        if component_type == "empty":
            return None
            
        for comp in self.components[component_type + "s"]:
            if comp["position"]["x"] == x and comp["position"]["y"] == y:
                return comp
        return None
    
    def update_component_state(self, x: int, y: int, new_state: Dict[str, Any]) -> bool:
        """Update the state of a component.
        
        Args:
            x: X coordinate
            y: Y coordinate
            new_state: New state data
            
        Returns:
            bool: True if update was successful
        """
        component = self.get_component(x, y)
        if not component:
            return False
            
        component["state"].update(new_state)
        return True
    
    def get_board_state(self) -> Dict[str, Any]:
        """Get the current state of the board.
        
        Returns:
            Dict[str, Any]: Board state including grid and components
        """
        return {
            "size": self.size,
            "grid": self.grid.tolist(),
            "components": self.components
        }
    
    def _is_valid_position(self, x: int, y: int) -> bool:
        """Check if a position is valid on the board.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            bool: True if position is valid
        """
        return 0 <= x < self.size and 0 <= y < self.size
    
    def validate_board(self) -> List[str]:
        """Validate the current board state.
        
        Returns:
            List[str]: List of validation errors
        """
        errors = []
        
        # Check for overlapping components
        for y in range(self.size):
            for x in range(self.size):
                if self.grid[y][x] != "empty":
                    component = self.get_component(x, y)
                    if not component:
                        errors.append(f"Component at ({x}, {y}) is in grid but not in components list")
        
        # Validate component-specific rules
        for component_type, components in self.components.items():
            for comp in components:
                x, y = comp["position"]["x"], comp["position"]["y"]
                if self.grid[y][x] != component_type[:-1]:  # Remove 's' from type
                    errors.append(f"Component {component_type} at ({x}, {y}) doesn't match grid")
        
        return errors 