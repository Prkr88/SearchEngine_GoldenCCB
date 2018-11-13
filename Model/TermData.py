class TermData:

    def __init__(self):
        self.tf = 1
        self.list_positions = []

    def update_tf(self):
        self.tf += 1

    def add_pos_to_list(self, line, offset):
        self.list_positions.append('(' + str(line) + ',' + str(offset) + ')')

    def get_term_tf(self):
        return self.tf
