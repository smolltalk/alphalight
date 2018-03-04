import json

conf = json.load(open('test_config.json'))


class PropertyNode(object):
    def __init__(self, name, obj, parent=None):
        self.name = name
        self.parent = parent
        self.properties = {}
        if isinstance(obj, str):
            self.type = 'string'
        elif isinstance(obj, dict):
            if '__type' in obj.keys():
                self.type = obj['__type']
            else:
                self.type = 'object'
            if self.type == 'object':
                for property_name in obj.keys():
                    if not property_name.startswith('__'):
                        self.properties[property_name] = PropertyNode(
                            property_name, obj[property_name], self)
            else:
                if '__value' in obj.keys():
                    self.value = obj['__value']

    def is_root(self):
        return self.parent == None

    def has_properties(self):
        return len(self.properties) > 0

    def property(self, property_name):
        return self.properties[property_name]

    def property_first(self):
        if len(self.properties) == 0:
            return None
        return self.properties[list(self.properties.keys())[0]]

    def property_after(self, property_name, delta):
        if len(self.properties) == 0:
            return None
        key_list = list(self.properties.keys())
        i = key_list.index(property_name)
        i = (i + delta) % len(key_list)
        return self.properties[key_list[i]]

class PropertyNodeBrowser(object):
    
    def __init__(node)
        self.node = node

    def display(self):

    def move_to(self, node):
        if node is self.node:
            return
        self.node = node
        c = node.name + ': ' + node.value
    

    def input(i):
        if a == '+' or a == '-':
            if not node.is_root():
                self.move_to(node.parent.property_after(self.node.name, 1 if a == '+' else -1))
        elif a == 'in':
            if self.node.has_properties():
                self.move_to(node.property_first)
            else:
                # switch in edit mode
        elif a == 'out':
            if not node.is_root():
                self.move_to(node.parent)
                        

p = PropertyNode('CONF', conf)
print(p.property('param1'))
