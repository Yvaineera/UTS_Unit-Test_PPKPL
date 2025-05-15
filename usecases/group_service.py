from domain.entities import KpopGroup

class GroupService:
    def __init__(self, repository):
        self.repo = repository

    def browse(self):
        return self.repo.browse()

    def read(self, name):
        return self.repo.read(name)

    def add(self, name, members):
        group = KpopGroup(name, members)
        return self.repo.add(group)

    def edit(self, name, new_name=None, new_members=None):
        return self.repo.edit(name, new_name, new_members)

    def delete(self, name):
        return self.repo.delete(name)
