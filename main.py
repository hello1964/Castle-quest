import time as tm

def clear():
  print("\033[H\033[2J", end="")

health = 0
hunger = 0
floor = 0
level = 1

def indexRange(listVar: list):
  dictionary = {}
  for indexPos in range(0, len(listVar)):
    dictionary[indexPos] = listVar[indexPos]
  return dictionary.items()

def write(string: str, interval: float, onSpace: float = 0, newLine: bool = True):
  for i in string:
    if i != " ":
      tm.sleep(interval)
    else:
      tm.sleep(onSpace)
    print(i, end="", flush=True)
  if newLine:
    print("")

def endGame():
  clear()
  write("Game Over", 0.1, 0.3, False)
  while True:
    input()
    clear()
    print("Game Over", end="")

activeEffects = []
effectTypes = {}
class Effect():
  name = ""
  health = 0
  hunger = 0
  damage = 0
  length = 0

  @staticmethod
  def types():
    global effectTypes
    return effectTypes
  
  @staticmethod
  def damage():
    damageVar = 0
    for i in effectTypes:
      damageVar += i.damage
    return damageVar

  @staticmethod
  def print(clearBefore: bool = False, clearAfter: bool = False):
    if len(activeEffects) > 0:
      if clearBefore:
        clear()

      print("Your effects:")
      print("")
      total = [0, 0, 0]
      for i in activeEffects:
        print(" " + i.name)
        if i.health != 0:
          print("  +%d health every cycle" % i.health if i.health > 0 else "  %d health every cycle" % i.health)
          total[0] += i.health
        if i.hunger != 0:
          print("  +%d hunger every cycle" % i.hunger if i.hunger > 0 else "  %d health every cycle" % i.hunger)
          total[1] += i.hunger
        if i.damage != 0:
          print("  +%d damage every cycle" % i.hunger if i.damage > 0 else "  %d health every cycle" % i.damage)
          total[2] += i.damage
        print("  Remaining cycles: %d" % i.length)

      for p, i in indexRange(total):
        currentStat = ""
        if p == 0:
          currentStat = "health"
        elif p == 1:
          currentStat = "hunger"
        elif p == 2:
          currentStat = "damage"
        print(" Total %s effect: +%d" % (currentStat, i) if i >= 1 else " Total %s effect: %d" % (currentStat, i))
      if clearAfter:
        clear()

  def __init__(self, name: str, health: int, hunger: int, damage: int, length: int):
    self.name = name
    self.health = health
    self.hunger = hunger
    self.damage = damage
    self.length = length

    effectTypes[name] = self

  def run(self):
    global health
    global hunger
    global activeEffects

    health += self.health
    hunger += self.hunger

    self.length -= 1
    if self.length <= 0:
      for p, i in indexRange(activeEffects):
        if i.name == self.name:
          del activeEffects[p]

inventory = []

weaponTypes = {}
class Weapon():
  name = ""
  minDamage = 0
  maxDamage = 0
  avgDamage = 0
  durability = None
  melee = True
  effects = []
  oneTime = False

  @staticmethod
  def types():
    global weaponTypes
    return weaponTypes

  def __init__(self, name: str, minDamage: int, maxDamage: int, durability: int, melee: bool, effects, oneTime: bool = False):
    self.name = name
    self.minDamage = minDamage
    self.maxDamage = maxDamage
    if not(oneTime):
      self.durability = durability
    self.melee = melee
    self.effects = effects
    self.oneTime = oneTime
    self.avgDamage = (self.minDamage + self.maxDamage) / 2

    weaponTypes[self.name] = self

consumableTypes = {}
class Comsumable():
  name = ""
  healthRestore = 0
  hungerRestore = 0
  effects = []

  @staticmethod
  def types():
    global consumableTypes
    return consumableTypes

  def __init__(self, name: str, healthRestore: int, hungerRestore: int, effects):
    self.name = name
    self.healthRestore = healthRestore
    self.hungerRestore = hungerRestore
    self.effects = effects

    consumableTypes[self.name] = self

enemyTypes = {}
class Enemy():
  name = ""
  health = 0
  minDamage = 0
  maxDamage = 0
  avgDamage = 0
  effects = []

  @staticmethod
  def types():
    global enemyTypes
    return enemyTypes

  def __init__(self, name: str, health: int, minDamage: int, maxDamage: int):
    self.name = name
    self.health = health
    self.minDamage = minDamage
    self.maxDamage = maxDamage
    self.avgDamage = (minDamage + maxDamage) / 2

    enemyTypes[self.name] = self

rooms = []
class Room():
  text = ""
  options = []
  oneTime = []

  @staticmethod
  def rooms():
    global rooms
    return rooms

Effect("Poison", -5, 2, 4, 30)
activeEffects.append(Effect.types()["Poison"])
Effect.print()