from settings import *
import pygame as pg
import moderngl as mgl
import glm
import numpy as np




class Chat:
    def __init__(self, app):
        self.app = app
        self.font = pg.font.Font("freesansbold.ttf", 32)
        self.render_list = []
        self.index = 1
        self.counter = 0
        self.on = False
        self.pending_messadge = ""
    

    @property
    def on(self):
        return not self.app.player.on
    
    @on.setter
    def on(self, x):
        self.app.player.on = not x

    
    def update(self):
        if self.counter == 10000 and self.index < len(self.render_list):
            del self.render_list[self.index]
            self.counter = 0

        self.counter += 1

        if self.on:
            self.render_list[0] = self.pending_messadge + "_"

        else:
            if len(self.render_list) > 0:
                del self.render_list[0]

    

    def handle_input(self, event:pg.event.Event):
        key = pg.key.get_pressed()
        if key[pg.K_KP_ENTER] and self.on:
            self.on = False
            if self.pending_messadge.startswith("/"):
                self.chat_command(self.pending_messadge)
            else:
                self.add_messadge("player", self.pending_messadge)
            self.pending_messadge = ""
            return 

        if self.on:
            if key[pg.K_BACKSPACE]:
                self.pending_messadge = self.pending_messadge[:-1] if len(self.pending_messadge) != 0 else ""
            elif event.type == pg.KEYDOWN and event.key < 127:
                
                if key[pg.K_LSHIFT] or key[pg.K_RSHIFT]:
                    self.pending_messadge += self._deform_shift_key(event.unicode)

                else:
                    self.pending_messadge += event.unicode
        
    def render(self):
        self._render_text("hello", (3, 0, 0))
        return
        for key, item in enumerate(self.render_list):
            self._render_at_index(key, item)


    def chat_command(self, chat_input):
        if len(chat_input) < 2: self.add_messadge("game", "command_status:Unsucces, No text supplied")
        chat_input = chat_input[1:]

        level = 0
        if GAMEMODE != SURIVAL:
            level = 2


        self.add_messadge("game", ":".join(*self.app.commands.call(chat_input, self.app.player.as_dict(), level)))

    def add_messadge(self, owner, messadge):
        actual_messadge = f"[{owner}]: {messadge}"
        self.render_list[self.index] = actual_messadge
        self.index += 1

    def _deform_shift_key(self, char:str):
        if char.isalpha(): return char.upper()

        shift = {
            "`":"~",
            ";": ":",
            "=": "+",
            "-":"_",
            "1":"!",
            "2":"@",
            "[":"{",
            "]":"}",
        
        }
        return shift.get(char, char)


    def _render_at_index(self, index, text):
        self._render_text(text, (-0.999, -0.99 + index * (1 / 15), 0.2))

    def _render_text(self, text, position):
        if len(text) > 30: return False
        deform_x = 30 // len(text) * 3 if len(text) != 0 else 1
        deform_y = 17

        final_surface = self.font.render(text, False, "white", "black") 
        final_surface = pg.transform.flip(final_surface, flip_x=False, flip_y=True)
        mgl_texture = self.app.ctx.texture(
            final_surface.get_size(),
            4,
            pg.image.tobytes(final_surface, "RGBA")
        )

        mgl_texture.filter = (mgl.NEAREST, mgl.NEAREST)
        mgl_texture.use(location = 5)

        

        vertex_shader = """
        #version 330 core
        layout (location = 0) in vec3 pos;
        layout (location = 0) in vec2 in_uv;
        uniform vec3 chg;

        out vec2 uv;
        void main(){
            uv =  in_uv;
            gl_Position = vec4(pos  + chg, 1);
        }
        """
        fragment_shader = """
        #version 330 core
        layout (location = 0) out vec4 fragColor;
        uniform sampler2D tex;
        in vec2 uv;
        void main(){
            vec3 color = texture(tex, uv).rgb;
            fragColor = vec4(color, color.r);
        }
        """


        program = self.app.ctx.program(vertex_shader, fragment_shader)

        program['chg'].write(glm.vec3(position))
        program['tex'] = 5
      


        data = np.array([
            0.0, 0.0, 0.0, 0.0, 0.0,   
            1.0, 1.0 / 17.0, 0.0, 1.0, 1.0,
            0.0, 1.0 / 17.0, 0.0, 0.0, 1.0,

            1.0, 1.0 / 17.0, 0.0, 1.0, 1.0,
            0.0, 0.0, 0.0, 0.0, 0.0,
            1.0, 0.0, 0.0, 1.0, 0.0



        ], dtype="float32")

        vbo = self.app.ctx.buffer(data)

        vao = self.app.ctx.vertex_array(
            program, [(vbo, "3f 2f", "pos","in_uv")]
        )

        vao.render()

        return True




