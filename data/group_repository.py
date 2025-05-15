from domain.entities import KpopGroup

class GroupRepository:
    def __init__(self):
        self.groups = {}

    def browse(self):
        return list(self.groups.values())

    def read(self, name):
        for group_name, group in self.groups.items():
            if group_name.lower() == name.lower():
                return group
        return None

    def add(self, group: KpopGroup):
        if self.read(group.name):
            return False
        self.groups[group.name] = group
        return True

    def edit(self, name, new_name=None, new_members=None):  
        group = self.read(name)
        if group:
            if new_name:
                if self.read(new_name):
                    return False
                del self.groups[name]
                group.name = new_name
                self.groups[new_name] = group
            if new_members is not None:
                group.members = new_members
            return True
        return False

    def delete(self, name):
        group = self.read(name)
        if group:
            del self.groups[name]
            return True
        return False
