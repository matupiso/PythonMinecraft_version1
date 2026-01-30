from settings import *
from commands.random_command import commands
from utils import valid_cmd_position_spec
from world_objects.entity import get_from_type

class RelInt:
    def __init__(self, number):
        self.number = number

class Parser:
    class Cmd_playsound:
        def __init__(self, app, exec_pos):
            self.app = app
            self.exec_pos = exec_pos
        def __call__(self, *args):
            args = list(args)
            if len(args) == 0:
                return "NotEnoutghArgError",f"playsound expects 1 arg but got just 0"
            
            if len(args) > 1:
                return "TooManyArgError",f"playsound expects 1 arg but got more '{len(args)}'"
            self.app.sound.playsound(args[0])
            return None, None
    class Cmd_tp:
        def __init__(self, app, exec_pos):
            self.app = app
            self.exec_pos = exec_pos
        def __call__(self, *args):
            args = list(args)
            if len(args) < 4:
                return "NotEnoutghArgError",f"tp expects 4 args but got just {len(args)}"
            if len(args) > 4:
                return "TooManyArgError",f"tp expects 4 args but got more '{len(args)}'"
            x,y,z = self.exec_pos.x, self.exec_pos.y, self.exec_pos.z
            entity = args[0]

            if isinstance(args[1], RelInt):
                x += args[1].number

            else:
                x = args[1]
            if isinstance(args[2], RelInt):
                y += args[2].number
            else:
                y = args[2]

            if isinstance(args[3], RelInt):
                z += args[3].number

            else:
                z = args[3]       

            if isinstance(entity, list):
                for e in entity:       
                    e["x"] = x
                    e["y"] = y
                    e["z"] = z
                    
                return None, None
            else     :
                entity["x"] = x
                entity["y"] = y
                entity["z"] = z
                return None, None
    class Cmd_setblock:
        def __init__(self, app, exec_pos):
            self.app = app
            self.exec_pos = exec_pos
        def __call__(self, *args):
            args = list(args)
            if len(args) < 4:
                return "NotEnoutghArgError",f"setblock expects 4 args but got just {len(args)}"
            if len(args) > 4:
                return "TooManyArgError",f"setblock expects 4 args but got more '{len(args)}'"
            if args[3] == GLASS:
                return "InvalidArgumentError", "cannot setblock a glitchy block"
            

            for index, value in enumerate(args):
                if isinstance(value, RelInt):
                    args[index] = args[index].number
                    args[index] += self.exec_pos.x if index == 0 else self.exec_pos.y if index == 1 else self.exec_pos.z if index == 2 else 0
                args[index] = int(args[index])

            self.app.voxel_handler.setblock(*args)
            
            return None, None
    class Cmd_kill:
        def __init__(self, app, exec_pos):
            self.app = app

        def __call__(self, *args):
            args = list(args)
            if len(args) < 1:
                return "NotEnoutghArgError",f"kill expects 1 arg but got just {len(args)}"
            if len(args) > 1:
                return "TooManyArgError",f"kill expects 1 arg but got more '{len(args)}'"
            for e in args[0]:
                e.kill()
            return None, None
    class Cmd_fill:
        def __init__(self, app, exec_pos):
            self.app = app
            self.exec_pos = exec_pos
        def __call__(self, *args):
            args = list(args)

            if len(args) < 7:
                return "NotEnoutghArgError",f"fill expects 7 args but got just {len(args)}"
            if len(args) > 7:
                return "TooManyArgError",f"fill expects 7 args but got more '{len(args)}'"
            

         

            for index, value in enumerate(args[:-1]):
                if isinstance(value, RelInt):
                    args[index] = args[index].number
                    args[index] += self.exec_pos.x if index in [0, 1] else self.exec_pos.y if index == [2, 3] else self.exec_pos.z if index in [4, 5] else 0
                args[index] = int(args[index])

            for x in range(int(args[0]), int(args[1])):
                for y in range(int(args[2]), int(args[3])):
                    for z in range(int(args[4]), int(args[5])):
                        self.app.voxel_handler.setblock(x, y, z, args[6])





            return None, None
    class Cmd_data:
        def __init__(self, app, exec_pos):
            self.app = app

        def __call__(self, *args):
            args = list(args)
            if len(args) < 3:
                return "NotEnoutghArgError",f"data expects 3 args  but got just {len(args)}"
            if len(args) > 3:
                return "TooManyArgError",f"data expects 3 args but got more '{len(args)}'"
            
            if not args[0] in ['merge', 'get']:
                return "InvalidArgumentError", f"first argument must be merge or get not '{str(args[0])}'"
            
            if not isinstance(args[1], list):
                if args[0] == "merge":
                    for (key, value) in args[2].items():
                        args[1][key] = value
                elif args[0] == "get":
                    for (key, _) in args[2].items():
                        print(args[1][key])
                return None, None
            
            
                

            if args[0] == "merge":
                for entity in args[1]:
                    for (key, value) in args[2].items():
                        entity[key] = value

            elif args[0] == "get":
                for entity in args[1]:
                    for (key, _) in args[2].items():
                        print(entity[key])

            return None, None
                
        




    class Cmd_summon:
        def __init__(self, app, exec_pos):
            self.app = app
            self.exec_pos = exec_pos

        def __call__(self, *args):
            args = list(args)
            if len(args) < 1:
                return "NotEnoutghArgError",f"summon expects at least 1 arg but got just {len(args)}"
            if not len(args) in [1, 4, 5, 2] :
                return "TooManyArgError",f"summon expects  4, 5, 1 or 2 args but got  '{len(args)}'"
            

            Entity = get_from_type(args[0]['type'])
            if not Entity:
                return "InvalidArgumentError",f"'{args[0]['type']}' is not an entity type"
            for index, value in enumerate(args):
                if isinstance(value, RelInt):
                    args[index] = args[index].number
                    args[index] += self.exec_pos.x if index == 0 else self.exec_pos.y if index == 1 else self.exec_pos.z if index == 2 else 0


            position = glm.vec3(*args[1:]) if len(args) == 4 else self.exec_pos + glm.vec3(0, 2, 0)
            e = Entity(self.app, *position, args[0]["name"] if "name" in args[0].keys() else " ")

            for (key, value) in args[0].items():
                e[key] = value
            if len(args) == 5:
                for (key, value) in args[4].items():
                    e[key] = value
            elif len(args) == 2:
                for (key, value) in args[1].items():
                    e[key] = value  
            

            self.app.entity_handler.add_e(e)
            return None , None

    def __init__(self, app):
        self.app = app


    def parse(self, command:str, args:list[str], entity):
        command_object = None if command not in commands else getattr(self, f"Cmd_{command}", None)

        if not command_object:
            return None, None, "InvalidArgumentError", "Invalid command"
        

        if entity:
            command_object = command_object(self.app, glm.vec3(entity.x, entity.y, entity.z))
        else:
            command_object = command_object(self.app, DEFAULT_CMD_EXEC_POS)

        converted_args = []


        for i in args:
            if valid_cmd_position_spec(i):
                if i.startswith("~") and i != "~":
                    converted_args.append(RelInt(int(i[1:])))
                elif i == "~":
                    converted_args.append(RelInt(0))
                else:
                    converted_args.append(int(i))

            elif i.count(".") >= 1 and (i.startswith("minecraft.") or i.startswith("avm.") or i.startswith("util.")):
                converted_args.append(i)


            elif  i.startswith("minecraft:") and len(i) > 9:
                block_name = i[10:].upper()
                if block_name in BLOCK_NAMES:
                    converted_args.append(BLOCKS[BLOCK_NAMES.index(block_name)])
                elif block_name in ENTITIES:
                    converted_args.append(globals()[block_name])
                else:
                    converted_args.append(block_name)
            elif i.upper() in BLOCK_NAMES:
                converted_args.append(BLOCKS[BLOCK_NAMES.index(i.upper())])
            elif i in ENTITIES:
                if isinstance(command_object, self.Cmd_summon):
                    converted_args.append({"type":i})
                else:
                    if not self.app.entity_handler.get_from_gche(f"@e[type={i},]"):
                        return None, None, "", ""
                    converted_args.append(self.app.entity_handler.get_from_gche(f"@e[type={i},]"))
            elif i == self.app.player.name:
                converted_args.append(self.app.player.as_entity())
            elif isinstance(command_object, self.Cmd_data) and i in ['merge', 'get']:
                converted_args.append(i)
            elif i.startswith("{") and i.endswith("}"):
                if i[-2] == ",":
                    i = i[:-2] + i[-1]
                i = i.replace(" ", "")
                d = i[1:-1].split(",")
                data = {}
                for dat in d:
                    key = dat.split(":")[0]
                    value = dat.split(":")[1]
                    if value.isdigit(): data[key] = int(value)
                    elif value.replace(".", "").isdigit(): data[key] = float(value)
                    else:
                        data[key] = value

                converted_args.append(data)
            
            elif i.startswith("@"):
                if i == "@s":
                    converted_args.append([entity, ])
                else:
                    if isinstance(command_object, self.Cmd_summon):
                        if not self.app.entity_handler.get_args(i):
                            return None, None, "InvalidArgumentError", f"Invalid entity specifier ({i})"
                        converted_args.append(self.app.entity_handler.get_args(i))
                    else:
                        if not self.app.entity_handler.get_from_gche(i):
                            return None, None, "InvalidArgumentError", f"Invalid entity specifier ({i})"
                        converted_args.append(self.app.entity_handler.get_from_gche(i))
            else:
                return None, None, "InvalidArgumentError", f"Unexpected argument {i}"
            

        return command_object, converted_args, None, None
    



