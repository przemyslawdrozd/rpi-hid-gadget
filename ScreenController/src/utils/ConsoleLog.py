from rich.console import Console
from rich.table import Table

class ConsoleLog:
    def __init__(self):
        self.__console = Console()

    def log(self, screen_data, instructions):
        """Logs the data in a table format, using dictionary keys as column headers."""
        if not isinstance(screen_data, dict):
            raise ValueError("screen_data must be a dictionary")
        
        if not isinstance(instructions, list):
            raise ValueError("instructions must be a list of strings")
        
        # Create a table with dynamic columns based on the keys in the screen_data
        table = Table(title="Aggregated Screen Data")

        # Collect row data excluding the instructions initially
        row_data = []

        # Add the keys from the screen_data as columns
        for key in screen_data.keys():
            if isinstance(screen_data[key], dict):
                # Add sub-keys for nested dictionaries like target_dots
                for sub_key in screen_data[key].keys():
                    table.add_column(f"{sub_key}", justify="center")
                    row_data.append(str(screen_data[key][sub_key]))
            else:
                table.add_column(key, justify="center")
                row_data.append(str(screen_data[key]))

        # Add the instructions as a separate column at the end
        instructions_str = ", ".join(instructions)
        table.add_column("Key Instructions", justify="center")
        row_data.append(instructions_str)

        # Add a single row with all the values
        table.add_row(*row_data)

        # Print the table to the console
        self.__console.print(table)
