from typing import Dict, Any, List, Optional, Tuple
import re
from dataclasses import dataclass
from ttsim.utils.matrix import BoardMatrix
from ttsim.utils.parser import FunctionParser

@dataclass
class ParsedFunction:
    """Represents a parsed function call."""
    name: str
    parameters: Dict[str, Any]
    line_number: int
    raw_text: str

class FunctionParser:
    """Parses natural language instructions into structured function calls."""
    
    def __init__(self):
        """Initialize the function parser with supported functions."""
        self.supported_functions = {
            "place_part": {
                "parameters": {
                    "component": {"type": "string", "required": True},
                    "x": {"type": "integer", "required": True},
                    "y": {"type": "integer", "required": True}
                },
                "description": "Place a component on the board"
            },
            "simulate": {
                "parameters": {
                    "steps": {"type": "integer", "required": True}
                },
                "description": "Run the simulation"
            },
            "get_board_state": {
                "parameters": {},
                "description": "Get the current board state"
            }
        }
        
        # Regular expressions for parsing
        self.function_pattern = re.compile(r'(\w+)\s*\((.*?)\)')
        self.parameter_pattern = re.compile(r'(\w+)\s*=\s*([^,]+)')
    
    def parse_instruction(self, instruction: str, line_number: int = 1) -> Optional[ParsedFunction]:
        """Parse a single instruction into a function call.
        
        Args:
            instruction: The instruction text to parse
            line_number: Line number in the source (for error reporting)
            
        Returns:
            Optional[ParsedFunction]: Parsed function if successful
        """
        # Clean the instruction
        instruction = instruction.strip()
        
        # Try to match function pattern
        match = self.function_pattern.match(instruction)
        if not match:
            return None
            
        function_name = match.group(1)
        if function_name not in self.supported_functions:
            return None
            
        # Parse parameters
        params_text = match.group(2)
        parameters = self._parse_parameters(params_text, function_name)
        if parameters is None:
            return None
            
        return ParsedFunction(
            name=function_name,
            parameters=parameters,
            line_number=line_number,
            raw_text=instruction
        )
    
    def parse_instructions(self, text: str) -> List[ParsedFunction]:
        """Parse multiple instructions from text.
        
        Args:
            text: Text containing multiple instructions
            
        Returns:
            List[ParsedFunction]: List of parsed functions
        """
        functions = []
        for i, line in enumerate(text.split('\n'), 1):
            if line.strip():
                func = self.parse_instruction(line, i)
                if func:
                    functions.append(func)
        return functions
    
    def _parse_parameters(self, params_text: str, function_name: str) -> Optional[Dict[str, Any]]:
        """Parse function parameters from text.
        
        Args:
            params_text: Text containing parameters
            function_name: Name of the function
            
        Returns:
            Optional[Dict[str, Any]]: Parsed parameters if successful
        """
        parameters = {}
        expected_params = self.supported_functions[function_name]["parameters"]
        
        # Handle empty parameters
        if not params_text.strip():
            if not expected_params:
                return {}
            return None
            
        # Parse each parameter
        for param_match in self.parameter_pattern.finditer(params_text):
            name = param_match.group(1)
            value = param_match.group(2).strip()
            
            if name not in expected_params:
                return None
                
            # Convert value to appropriate type
            param_type = expected_params[name]["type"]
            try:
                if param_type == "integer":
                    parameters[name] = int(value)
                elif param_type == "string":
                    parameters[name] = value.strip('"\'')
                else:
                    parameters[name] = value
            except ValueError:
                return None
        
        # Check required parameters
        for name, spec in expected_params.items():
            if spec["required"] and name not in parameters:
                return None
                
        return parameters
    
    def validate_function(self, func: ParsedFunction) -> List[str]:
        """Validate a parsed function.
        
        Args:
            func: The parsed function to validate
            
        Returns:
            List[str]: List of validation errors
        """
        errors = []
        
        # Check if function is supported
        if func.name not in self.supported_functions:
            errors.append(f"Unsupported function: {func.name}")
            return errors
            
        # Get expected parameters
        expected_params = self.supported_functions[func.name]["parameters"]
        
        # Check required parameters
        for name, spec in expected_params.items():
            if spec["required"] and name not in func.parameters:
                errors.append(f"Missing required parameter: {name}")
                
        # Check parameter types
        for name, value in func.parameters.items():
            if name in expected_params:
                expected_type = expected_params[name]["type"]
                if expected_type == "integer" and not isinstance(value, int):
                    errors.append(f"Parameter {name} must be an integer")
                elif expected_type == "string" and not isinstance(value, str):
                    errors.append(f"Parameter {name} must be a string")
                    
        return errors 

# Create a board
board = BoardMatrix()

# Create a parser
parser = FunctionParser()

# Parse instructions
instructions = """
place_part(component="bit", x=0, y=0)
simulate(steps=100)
get_board_state()
"""
functions = parser.parse_instructions(instructions)

# Execute functions
for func in functions:
    if func.name == "place_part":
        board.place_component(**func.parameters)
    elif func.name == "simulate":
        # Handle simulation
        pass
    elif func.name == "get_board_state":
        state = board.get_board_state() 