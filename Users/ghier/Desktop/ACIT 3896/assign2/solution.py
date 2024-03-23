class FileNode:
    def __init__(self, name, parent=None, data=""):
        self.name = name
        self.parent = parent
        self.children = []
        self.data = data
        if parent:
            parent.children.append(self)

    def __str__(self):
        return f"{self.name} ({len(self.children)})"

    def fullpath(self):
        path = []
        current = self
        while current:
            path.insert(0, current.name)
            current = current.parent
        return path

    def count_normal_files(self):
        count = 0
        if not self.children:
            count += 1
        for child in self.children:
            count += child.count_normal_files()
        return count

    def find_by_localpart(self, target_name):
        matches = []
        if self.name == target_name:
            matches.append(self)
        for child in self.children:
            matches.extend(child.find_by_localpart(target_name))
        return matches

    def format_tree_string(self, sort=False, depth=0):
        lines = []
        indent = '    ' * depth
        lines.append(indent + self.name)
        if sort:
            sorted_children = sorted(self.children, key=lambda x: x.name)
            for child in sorted_children:
                lines.extend(child.format_tree_string(sort, depth + 1))
        else:
            for child in self.children:
                lines.extend(child.format_tree_string(sort, depth + 1))
        return lines

    def closest_common_ancestor(self, other_node):
        def get_ancestors(node):
            ancestors = set()
            while node:
                ancestors.add(node)
                node = node.parent
            return ancestors

        self_ancestors = get_ancestors(self)
        other_ancestors = get_ancestors(other_node)

        common_ancestors = self_ancestors.intersection(other_ancestors)

        if common_ancestors:
            return max(common_ancestors, key=lambda x: x.depth)
        else:
            return None
