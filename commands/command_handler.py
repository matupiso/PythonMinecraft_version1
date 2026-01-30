from commands.parser import Parser
from world_objects.entity import entity
from commands.random_command import commands

class Commands:
    def __init__(self, app):
        self.app = app
        self.parser = Parser(app)
        
    def _prepare_commands(self, level, is_none_entity):
        cmd = []
        if is_none_entity:
            cmds = commands
        match level:
            case 0:
                cmds = []
            case 1:
                cmds = ["tp", "say", "playsound"]
            case 2:
                cmds = ["tp", "say", "playsound", "setblock", "summon"]
            case 3:
                cmds = ["tp", "say", "playsound", "setblock", "kill", "fill", "summon", "data"]

        

        



        return cmds
    def call(self, game_command:str, entity:entity | None, permission_level:int):
        try:
            return self._call(game_command, entity, permission_level)
        except Exception as e:
            if hasattr(e, "messadge"):
                messadge = e.messadge

            else:
                messadge = e
            return "UnknownException", f"Internal exception hapend ({messadge}, {e.__traceback__.tb_lineno}"

    def _call(self, game_command:str, entity:entity | None, permission_level:int):
        available_commands = self._prepare_commands(permission_level, entity==None)

        pending = ""
        cmds = []
        for i in game_command:
            if i != " ":
                pending += i

            else:
                cmds.append(pending)
                pending = ""

        if pending != "":
            cmds.append(pending)

        while "" in cmds:
            cmds.remove("")

        
        if len(cmds) < 2:
            return "LexerError","Text for command not found"
        
        if not cmds[0] in available_commands:
            return "PermissionError", "Not enoutgh permission level" 
        cmd_object, args, error_type, error_messadge = self.parser.parse(cmds[0], cmds[1:], entity)

        if error_type:
            return error_type, error_messadge
        

        error_type, error_messadge = cmd_object(*args)
        if error_type:
            return error_type, error_messadge
        
        return "Success", "Succesfully executed command"
        
