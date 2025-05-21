from parts.constants import ItemType
from game_logic import GameBoard

def parse_and_apply_commands(board: GameBoard, commands: list[str]):
    for command in commands:
        if "add_component" in command:
            try:
                # جدا کردن type و مختصات
                type_str = command.split("type=ItemType.")[1].split(",")[0].strip()
                x = int(command.split("x=")[1].split(",")[0].strip())
                y = int(command.split("y=")[1].split(")")[0].strip())

                component_type = ItemType[type_str.upper()]
                board.add_component(component_type, x, y)

                print(f"✅ Added {component_type} at ({x}, {y})")
            except Exception as e:
                print(f"❌ Error parsing command '{command}': {e}")
