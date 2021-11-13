class C:
    def __init__(self):
        self.oif = "if"
        self.ident = " " * 4
        self.owhile = "while"
        self.oelif = "elif"
        self.oelse = "else"
        self.new_line = "\n"
        self.comment = "//"
        self.oand = '&&'
        self.oequal = '=='

    def o_create_header(self, data, univesidade, person):
        return f"/{'*' * 50} {self.new_line}" \
               f"Data:{data}{self.new_line}" \
               f"{univesidade}{self.new_line}" \
               f"{person}{self.new_line}" \
               f"{'*' * 50}\\{self.new_line}"

    def o_import(self, biblioteca):
        return f"#include<{biblioteca}>{self.new_line}"

    def o_loop(self, action, condition, ident=0):
        return f"{self.ident * ident}{self.owhile}({condition}){{{self.new_line}" \
               f"{self.ident * ident}{action}{self.new_line}" \
               f"{self.ident * ident}}}{self.new_line}"

    def o_while(self, condition, action, ident=0):
        return f"{self.ident * ident}{self.o_loop(condition, action)}"

    def o_declare_var(self, var_type, name, value=None, ident=0):
        if value is not None:
            return f"{self.ident * ident}{var_type} {name} = {value};{self.new_line}"
        else:
            return f"{self.ident * ident}{var_type} {name};{self.new_line}"

    def o_declare_function(self, func_type, name, action, parameters='void', ident=0):
        return f"{self.ident * ident}{func_type} {name}({parameters}){{{self.new_line}" \
               f"{self.ident * (ident + 1)}{action}{self.new_line}" \
               f"{self.ident * ident}}}{self.new_line}"

    def o_if_else(self, condition, action_if, action_else, ident=0):
        return f"{self.ident * ident}{self.oif}({condition}){{{self.new_line}" \
               f"{self.ident * (ident + 1)}{action_if};{self.new_line}" \
               f"{self.ident * ident}}}{self.new_line}" \
               f"{self.ident * ident}{self.oelse}{{{self.new_line}" \
               f"{self.ident * (ident + 1)}{action_else};{self.new_line}" \
               f"{self.ident * ident}}}{self.new_line}"

    def o_if(self, op, condiction, action, ident=0):
        code = f"{self.ident * ident}{op}({condiction}){{{self.new_line}"
        for key, value in action.items():
            code += f"{self.ident * (ident + 1)}{key} = {value};{self.new_line}"
        return code + f"{self.ident * ident}}}{self.new_line}"

    def o_create_array(self, name, data, ident=0):
        return f"{self.ident * ident}{name}[{len(data)}] = {{{self.vetor_state(data)}}};{self.new_line}"

    def o_array_name(self, name, position, ident=0):
        return f"{self.ident * ident}{name}[{position}]"

    def o_call_function(self, name, parameters, var="", ident=0):
        code = ""
        for i in range(len(parameters)):
            if i != len(parameters) - 1:
                code += str(parameters[i]) + ', '
            else:
                code += str(parameters[i])
        if var != "":
            var += " = "
        return f"{self.ident * ident}{var}{name}({code}){self.new_line}"

    @staticmethod
    def vetor_state(state):
        """"Cria uma string com os valores do vetor de state"""
        vetor_state = ""
        for i in range(len(state)):
            if i == 0:
                vetor_state += '1,'
            elif i == len(state) - 1:
                vetor_state += '0'
            else:
                vetor_state += '0,'
        return vetor_state


class Arduino(C):
    def o_loop(self, action, condition=None, ident=0):
        return f"{self.ident * ident}void loop(){{{self.new_line}" \
               f"{self.ident * (ident + 1)}{action}{self.new_line}" \
               f"{self.ident * ident}}}{self.new_line}"
