import sys
from ruamel.yaml import YAML

# please see the docs: https://yaml.readthedocs.io/en/latest/example.html

inp = """\
- name: Ogre
  position: [0, 5, 0]
  powers:
    - name: Club
      damage: 10
    - name: Fist
      damage: 8
- name: Dragon
  position: [1, 0, 10]
  powers:
    - name: Fire Breath
      damage: 25
    - name: Claws
      damage: 15
- name: Wizard
  position: [5, -3, 0]
  powers:
    - name: Acid Rain
      damage: 50
    - name: Staff
      damage: 3
"""

yaml = YAML()
code = yaml.load(inp)

#print(code[0]["powers"])


for i in code:
    #print(i["powers"])
    for power_name in i["powers"]:
        print(power_name["name"])

code.append({"name": "Knight"})
#code[3] = { "name": "Knight"} # IndexError: list assignment index out of range
code[3]["position"] = [-2, 4, 7]
code[3]["powers"] = [ { "name": "Sword", "damage": 9}, { "name": "Dirty Socks", "damage": 1 } ]

print(code[2])
print(code[3]) # difference in data structure ! other way creates: ordereddict


code.append({"name": "Dwarf"})
s = None
yaml.dump({'position': [-2, 2, 5]}, s)
code[4]["position"] = s
code[4]["powers"] = [ { "name": "Hammer", "damage": 16}, { "name": "Horn", "damage": 25 } ]

yaml.dump(code, sys.stdout)
