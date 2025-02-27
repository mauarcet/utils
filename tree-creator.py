import os

def parse_tree(tree_str):
    lines = tree_str.strip().splitlines()
    root_name = lines[0].strip()
    root = {} if root_name.endswith("/") else None
    tree = {root_name: root}
    stack = [(0, tree[root_name], root_name)]
    for line in lines[1:]:
        norm = line.replace("│", " ")
        indent = len(norm) - len(norm.lstrip(" "))
        level = indent // 4 + 1
        trimmed = norm.strip()
        if trimmed.startswith("├──") or trimmed.startswith("└──"):
            name = trimmed[3:].strip()
        else:
            name = trimmed
        node = {} if name.endswith("/") else None
        while stack and stack[-1][0] >= level:
            stack.pop()
        parent_level, parent_node, _ = stack[-1]
        parent_node[name] = node
        if node is not None:
            stack.append((level, node, name))
    return tree

def create_structure(tree, base_path="."):
    for name, content in tree.items():
        if name.endswith("/"):
            dir_path = os.path.join(base_path, name.rstrip("/"))
            os.makedirs(dir_path, exist_ok=True)
            if isinstance(content, dict):
                create_structure(content, dir_path)
        else:
            file_path = os.path.join(base_path, name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            open(file_path, 'a').close()

def main():
    print("TreeCreator: Enter your project tree structure.")
    print("Paste the tree below and finish with an empty line:")
    
    # Read multiline input until an empty line is entered.
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    tree_str = "\n".join(lines)
    
    if not tree_str:
        print("No tree structure provided.")
        return
    
    project_tree = parse_tree(tree_str)
    create_structure(project_tree)
    print("Project structure created successfully.")

if __name__ == "__main__":
    main()

