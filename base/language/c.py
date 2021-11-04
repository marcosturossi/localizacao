class C:
    def __init__(self):
        self.oif = "if"
        self.ident = " " * 4
        self.owhile = "while"
        self.oelif = "elif"
        self.oelse = "else"
        self.new_line = "\n"
        self.comment = "//"

    def o_import(self, biblioteca):
        return f"#include<{biblioteca}>{self.new_line}"

    def o_if(self, condition, action, ident=0):
        return f"{self.ident * ident}{self.oif}({condition}){{{self.new_line}" \
               f"{self.ident * (ident + 1)}{action}{self.new_line}" \
               f"}}{self.new_line}"

    def o_loop(self, condition, action, ident=0):
        return f"{self.ident * ident}{self.owhile}({condition}){{{self.new_line}" \
               f"{self.ident * (ident + 1)}{action}{self.new_line}" \
               f"{self.ident * ident}}}{self.new_line}"

    def o_while(self, condition, action, ident=0):
        return self.o_loop(condition, action)

    def o_declare_var(self, var_type, name, value, ident=0):
        if value:
            return f"{self.ident * ident}{var_type} {name} = {value};{self.new_line}"
        else:
            return f"{self.ident * ident}{var_type} {name};{self.new_line}"

    def o_declare_function(self, func_type, name, value, parameters='void', ident=0):
        return f"{self.ident * ident}{func_type} {name}({parameters}){{{self.new_line}" \
               f"{self.ident * (ident + 1)}{value};{self.new_line}" \
               f"{self.ident * ident}}}{self.new_line}"

    def o_if_else(self, condition, action_if, action_else, ident=0):
        return f"{self.ident * ident}{self.oif}({condition}){{{self.new_line}" \
               f"{self.ident * (ident + 1)}{action_if}{self.new_line}" \
               f"}}{self.new_line}" \
               f"{self.ident * ident}{self.oelse}{{{self.new_line}" \
               f"{self.ident * (ident + 1)}{action_else}{self.new_line}" \
               f"{self.ident * ident}}}{self.new_line}"

    def o_if_elif(self, condition, action, ident=0):
        count = 0
        code = ""
        for key, valeu in action:
            if count == 0:
                code += f"{self.ident * ident}{self.oif}({condition}){{{self.new_line}"
            else:
                code += f"{self.ident * ident}{self.oelif}({condition}){{{self.new_line}"
            code += f"{self.ident * (ident + 1)}{key}{self.new_line}" \
                    f"}}{self.new_line}" \
                    f"{self.ident * ident}{self.oelse}{{{self.new_line}" \
                    f"{self.ident * (ident + 1)}{valeu}{self.new_line}" \
                    f"{self.ident * ident}}}{self.new_line}"
        return code


class Arduino(C):
    def o_loop(self,  action, condition=None, ident=0):
        return f"{self.ident*ident}void loop(){{{self.new_line}" \
               f"{self.ident*(ident+1)}{action}{self.new_line}" \
               f"}}{self.new_line}"
