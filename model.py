class XMLFile():

    def __init__(self):
        self.namespace = '{http://www.autocare.org}'
        self.valid = False

    def set_file(self, file):
        self.file = file
        return self

    def set_schema(self, schema):
        self.schema = schema
        return self

    def set_version(self, version):
        self.version = version
        return self

    def set_error_log(self, errors):
        self.error_log = errors
        return self

    def set_state(self, state):
        self.valid = state
        return self