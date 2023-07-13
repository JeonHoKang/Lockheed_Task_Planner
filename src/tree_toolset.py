import yaml

class TreeToolSet:
    def __init__(self) -> None:
        pass
    def search_tree(self, dictionary, node_id):
        if dictionary['id'] == node_id:
            contingency_node = dictionary
            return contingency_node
        else:
            res = []
            if 'children' in dictionary:
                for child in dictionary['children']:
                    parent = dictionary
                    res.append(self.search_tree(child, node_id))
            else:
                return Nones

            for element in res:
                if element:
                    return element
                    
    def create_pairs_with_dfs(self, start):
        visited = []  # Set to track visited vertices
        edges = []
        stack = [start]  # Stack to keep track of vertices to visit
        type_list = []
        full_id = []
        while stack:
            vertex = stack.pop()  # Pop a vertex from the stack

            if vertex["id"] not in visited:
                print(vertex["id"])  # Process the vertex (in this case, print it)
                visited.append(vertex["id"])  # Mark the vertex as visited
                # Add adjacent vertices to the stack
                if "children" in vertex:
                    for child in reversed(vertex["children"]):
                        stack.append(child)
                        edges.append((vertex["id"], child["id"]))
                        full_id.append((vertex, child))
        return edges, full_id


    def insert_element(self, dictionary, target_id, type, new_element, input_order_number):
        input_order_number = int(input_order_number)
        node_type = type
        if dictionary['id'] == target_id:
            if 'children' not in dictionary:
                dictionary['children'] = []
                del dictionary['agent']
                dictionary['type'] = node_type
                dictionary['children'].append(new_element)
            else:
                if len(dictionary['children'])+1 < input_order_number:
                    print("exceeds the number of children - Defaulting to first child")
                    input_order_number = 0
                else:
                    dictionary['children'].insert(input_order_number, new_element)

        else:
            if 'children' in dictionary:
                for child in dictionary['children']:
                    self.insert_element(child, target_id, node_type,
                                new_element, input_order_number)


    def delete_element(self, dictionary, target_id, parent=None):
        if dictionary['id'] == target_id:
            delete_index = parent['children'].index(dictionary)
            parent['children'].pop(delete_index)
            if len(parent['children']) == 0:
                print("no longer parent")
                del parent['children']
                parent['agent'] = []
        else:
            if 'children' in dictionary:
                parent = None
                for child in dictionary['children']:
                    parent = dictionary
                    self.delete_element(child, target_id, parent=parent)


    def create_dict_from_list(self, pairs):
        local_dict = {}
        name_id_dict = {}
        latest_id = -1
        index_list = []
        for pair in pairs:
            parent = pair[0]
            child = pair[1]
            child_id = 0
            parent_id = 0
            if parent not in name_id_dict:
                latest_id += 1
                local_dict[latest_id] = parent
                parent_id = latest_id
                name_id_dict[parent] = parent_id

            else:
                parent_id = name_id_dict[parent]

            if child not in name_id_dict:
                latest_id += 1
                local_dict[latest_id] = child
                child_id = latest_id
                name_id_dict[child] = child_id
            else:
                child_id = name_id_dict[child]

            index_list.append((parent_id, child_id))

        return local_dict, index_list


    def create_dict_list_from_pairs(self, pairs):
        local_dict = {}
        name_id_dict = {}
        latest_id = -1
        index_list = []
        for pair in pairs:
            parent = pair[0]
            child = pair[1]
            child_id = 0
            parent_id = 0
            if parent['id'] not in name_id_dict:
                latest_id += 1
                local_dict[latest_id] = parent
                parent_id = latest_id
                name_id_dict[parent['id']] = parent_id
            else:
                parent_id = name_id_dict[parent['id']]

            if child['id'] not in name_id_dict:
                latest_id += 1
                local_dict[latest_id] = child
                child_id = latest_id
                name_id_dict[child['id']] = child_id
            else:
                child_id = name_id_dict[child['id']]

            index_list.append((parent_id, child_id))

        return local_dict
    
    def dict_yaml_export(self, export_dictionary, problem_dir, file_name):
        file_dir = problem_dir + file_name
        print('-----created------')
        print(file_dir)
        with open(file_dir, 'w') as file:
            yaml.dump(export_dictionary, file, sort_keys=False, Dumper=NoTagNoQuotesDumper)

    def safe_dict_yaml_export(self, export_dictionary, problem_dir, file_name):
        file_dir = problem_dir + file_name
        print('-----created------')
        print(file_dir)
        with open(file_dir, 'w') as file:
            yaml.safe_dump(export_dictionary, file, sort_keys=False)

    def safe_dict_yaml_export(self, export_dictionary, problem_dir, file_name):
        file_dir = problem_dir + file_name
        print('-----created------')
        print(file_dir)
        with open(file_dir, 'w') as file:
            yaml.safe_dump(export_dictionary, file, sort_keys=False)

class NoTagNoQuotesDumper(yaml.Dumper):
    """
    Export yaml file in the desired format - without string tag etc
    """
    def represent_data(self, data):
        if isinstance(data, tuple):
            return self.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)
        return super().represent_data(data)

    def represent_scalar(self, tag, value, style=None):
        if style is None:
            style = self.default_style
        if tag == 'tag:yaml.org,2002:str' and '\n' in value:
            style = '|'
        return super().represent_scalar(tag, value, style)
