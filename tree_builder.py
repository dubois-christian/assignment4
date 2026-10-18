"""A company reporting directory built from linked binary-tree nodes."""


class EmployeeNode:
    """An employee with at most two direct reports."""

    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None


class TeamTree:
    """Manage a reporting hierarchy without a list or dictionary of employees."""

    def __init__(self):
        self.root = None

    def insert(self, manager_name, employee_name, side, current_node=None):
        """Search recursively; return whether the manager was found.

        A found manager stops the search even if their requested side is full.
        Names should be unique; otherwise the first preorder match is used.
        """
        starting_search = current_node is None
        if starting_search:
            side = side.strip().lower()
            if side not in ("left", "right"):
                print("Error: side must be 'left' or 'right'.")
                return False
            if not employee_name.strip():
                print("Error: employee name cannot be blank.")
                return False
            current_node = self.root
            if current_node is None:
                print("Error: add a team lead before adding employees.")
                return False

        if current_node.name == manager_name:
            if getattr(current_node, side) is not None:
                print(f"Error: {manager_name}'s {side} report is already occupied.")
            else:
                setattr(current_node, side, EmployeeNode(employee_name))
                print(f"{employee_name} added to the {side.upper()} of {manager_name}.")
            return True

        # Recurse only into existing children so None never restarts at root.
        if current_node.left is not None:
            if self.insert(manager_name, employee_name, side, current_node.left):
                return True
        if current_node.right is not None:
            if self.insert(manager_name, employee_name, side, current_node.right):
                return True
        if starting_search:
            print(f"Error: manager '{manager_name}' does not exist.")
        return False

    def print_tree(self, node=None, level=0):
        """Print employees in preorder, indenting each reporting level."""
        if node is None:
            if level == 0:
                node = self.root
                if node is None:
                    print("The team directory is empty.")
                    return
            else:
                return
        print("  " * level + "- " + node.name)
        self.print_tree(node.left, level + 1)
        self.print_tree(node.right, level + 1)


def company_directory():
    """Run the starter repository's interactive team-management menu."""
    tree = TeamTree()
    while True:
        print("\nTeam Management Menu")
        print("1. Add Team Lead (root)")
        print("2. Add Employee")
        print("3. Print Team Structure")
        print("4. Exit")
        choice = input("Choose an option (1-4): ").strip()
        if choice == "1":
            if tree.root is not None:
                print("Team lead already exists.")
            else:
                name = input("Enter team lead's name: ").strip()
                if not name:
                    print("Error: team lead's name cannot be blank.")
                    continue
                tree.root = EmployeeNode(name)
                print(f"{name} added as the team lead.")
        elif choice == "2":
            manager = input("Enter the manager's name: ").strip()
            employee = input("Enter the new employee's name: ").strip()
            side = input("Should this employee be on the LEFT or RIGHT of the manager? ")
            tree.insert(manager, employee, side)
        elif choice == "3":
            print("\nCurrent Team Structure:")
            tree.print_tree()
        elif choice == "4":
            print("Good Bye!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    company_directory()
