import random, string
#from settings import *
BLOCK_NAMES = ["stone", "wood"]


commands = ["setblock", "tp", "playsound", "summon", "kill", "fill", "data"]
signatures = ["pos_sig,minecraft_block", "entity,pos_sig", "entity", "entity", "pos_sig,pos_sig,pos_sig,pos_sig,pos_sig,pos_sig,pos_sig,pos_sig", ""]


class Signature:
    def __init__(self, wx, wy, wz):
        self.wx = wx
        self.wy = wy
        self.wz = wz
        
    def get_signature_function(self, name):
        func = getattr(self, f"signature_{name}", None)

        if func: return func

        def efunc():
            return "error"
        

        return efunc
    
    def signature_pos_sig(self):
        x,y,z = random.randint(0, self.wx), random.randint(-self.wy // 2, self.wy // 2), random.randint(0, self.wz)
        rel = random.randint(0, 1)
        return f"{x} {y} {z}" if rel == 1 else f"~{x} ~{y} ~{z}"
    def signature_siz_sig(self):
        x,y,z = random.randint(-100, 100), random.randint(-100, 100), random.randint(-100, 100)
        return f"{x} {y} {z}"
    def signature_minecraft_item(self):
        return random.choice([
            "diamond", "emerald", "wooden_picaxe", "wooden_shovel"
        ]) + " "
    
    def signature_who(self):
        return random.choices(string.ascii_letters, k=random.randint(1, 10))
    def signature_plain_text(self):
        return random.choices(string.ascii_letters + " ", k = random.randint(10, 40))
    
    def signature_count_sig(self):
        return f"{random.randint(0, 128)} "
    
    def signature_sound_sig(self):
        return "avm.royal_staff.command_block_staff_used"
    def signature_entity(self):
        entities = ['@s', '@e', '@a']
        types = ["spider", "ravager", "cat", "dog"]


        entity = random.choice(entities)

        if entity == "@a":
            name = random.choice(["Steve", "Warden", "King_Orange"])
            entity += f"[name={name}]" if random.random() < 0.4 else ""

        elif entity == "@e" and random.random() < 0.6:
            type = random.choice(types)
            sort = random.choice(["nearest", "farthest", "random", "all"])
            limit = random.randint(0, 100)
            x = random.randint(0, self.wx)
            y = random.randint(0, self.wy)
            z = random.randint(0, self.wz)
            r = random.randint(0, self.wx // 10)

            

            entity += "["

            for i in ["type", "sort", "limit", "x", "y", "z", "r"]:
                if random.random() < 0.4:
                    entity += f"{i} = {locals()[i]},"


            entity = entity[:-1]
            entity += "]"

        elif entity == "@s" and random.random() > 0.3:
            entity = "@[type=dog, limit=90, x = 0]"        

        return entity
    def signature_minecraft_block(self):
        blocks = [i.lower() for i in BLOCK_NAMES]
        return f"minecraft:{random.choice(blocks)}"
    
    

def random_command():
    sig_com = Signature(10, 10, 10)
    command_index = random.choice([0, 0, 0, 0, 0, 0, 0,0 , 1, 1])

    command, signature = commands[command_index], signatures[command_index].split(",")

    result = ""
    result += command + " "

    for sig in signature:
        func = sig_com.get_signature_function(sig)
        result += func()
        result += " "

    return result

if __name__ == "__main__":
    print(random_command())