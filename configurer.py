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


p = PropertyNode('CONF', conf)
print(p.property('param1'))
