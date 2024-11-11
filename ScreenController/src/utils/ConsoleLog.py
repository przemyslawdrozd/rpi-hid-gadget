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

        # Add a single row with all the values
        row_data = []

        # Add instructions at the end as a joined string
        instructions_str = ", ".join(instructions)
        row_data.append(instructions_str)

        # Add an extra column for instructions
        table.add_column("instructions", justify="center")
        for value in screen_data.values():
            if isinstance(value, dict):
                # Add the values from the nested dictionary
                row_data.extend([str(sub_value) for sub_value in value.values()])
            else:
                row_data.append(str(value))
                
        # Add the keys from the screen_data as columns
        for key in screen_data.keys():
            if isinstance(screen_data[key], dict):
                # Add sub-keys for nested dictionaries like target_dots
                for sub_key in screen_data[key].keys():
                    table.add_column(f"{sub_key}", justify="center")
            else:
                table.add_column(key, justify="center")
        


        table.add_row(*row_data)

        # Print the table to the console
        self.__console.print(table)
