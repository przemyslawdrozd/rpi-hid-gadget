from rich.console import Console
from rich.table import Table

class ConsoleLog:
    def __init__(self):
        self.__console = Console()

    def log(self, screen_data):
        """Logs the data in a table format, using dictionary keys as column headers."""
        if not isinstance(screen_data, dict):
            raise ValueError("Instruction must be a dictionary")

        # Create a table with dynamic columns based on the keys in the instruction
        table = Table(title="Aggregated Screen Data")

        # Add the keys from the instruction as columns
        for key in screen_data.keys():
            if isinstance(screen_data[key], dict):
                # Add sub-keys for nested dictionaries like target_dots
                for sub_key in screen_data[key].keys():
                    table.add_column(f"{sub_key}", justify="center")
            else:
                table.add_column(key, justify="center")

        # Add a single row with all the values
        row_data = []
        for value in screen_data.values():
            if isinstance(value, dict):
                # Add the values from the nested dictionary
                row_data.extend([str(sub_value) for sub_value in value.values()])
            else:
                row_data.append(str(value))

        table.add_row(*row_data)

        # Print the table to the console
        self.__console.print(table)
