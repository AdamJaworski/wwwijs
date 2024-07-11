class Org:
    org_name:   str
    access_lvl: int

    def __init__(self, org_name, access_lvl):
        self.org_name = org_name
        self.access_lvl = access_lvl

    def __str__(self):
        return f"Org: name: {self.org_name}, user access lvl: {self.access_lvl}"
