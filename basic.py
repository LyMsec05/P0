#Este archivo contiene todo el codigo de un lenguaje basico 

###########################################
#ERRORES
###########################################

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        result  = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result
    
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)



#######################################
# POSITION
#######################################

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


#########################################
#TOKENS
#########################################

T_EXEC = 'EXEC'
T_NEW = 'NEW'
T_VAR = 'VAR'
T_MACRO = 'MAACRO'
T_LPAR = 'LPAR'  # Left Parenthesis
T_RPAR = 'RPAR'
T_LCOR = 'LCOR'  # Left Corchete
T_RCOR = 'RCOR'
T_IGUAL = 'IGUAL'     # Igual
T_TURNTOMY = 'TURNTOMY'
T_TURNTOTHE = 'TURNTOTHE'
T_WALK = 'WALK'
T_JUMP = 'JUMP'
T_DROP = 'DROP'
T_PICK = 'PICK'
T_GRAB = 'GRAB'
T_LETGO = 'LETGO'
T_POP = 'POP'
T_MOVES = 'MOVES'
T_NOP = 'NOP'
T_SAFEEXE = 'SAFEEXEC'
T_IF = 'IF'
T_THEN = 'THEN'
T_ELSE = 'ELSE'
T_FI = 'FI'
T_DO = 'DO'
T_OD = 'OD'
T_QUESTION = '?'
T_TIMES = 'TIMES'
T_REPEAT = 'REPEAT'
T_ISBLOCKLED = 'ISBLOCKED?'
T_ISFACING = 'ISFACING?'
T_ZERO = 'ZERO?'
T_NOT = 'NOT'
T_SEMICOLON = 'SEMICOLON' # ;
DIGITS = '0123456789'
LETRAS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' 
T_INT = 'INT'
T_FLOAT = 'FLOAT'
T_QUESTION = '?'
T_VALIDVAR = 'VALIDVAR'
T_COMA = ','
#Para 'TURNTOMY' y 'MOVES'
T_LEFT = 'LEFT'
T_RIGHT = 'RIGHT'
T_BACK = 'BACK'
# Para 'TURNTOTHE'
T_NORTH = 'NORTH'
T_SOUTH = 'SOUTH'
T_EAST = 'EAST'
T_WEST = 'WEST'
#Para 'MOVES'
T_FORWARD = 'FORWARD'
T_BACKWARDS = 'BACKWARDS'



class Token:
    def __init__(self, type_, value=None): #El token es un objeto simple que tiene un tipo y opcionalmente un valor.
        self.type = type_
        self.value = value  

    def __repr__(self): 
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type} '

###################################################
#LEXER 
####################################################3
class Lexer:
    def __init__(self, fn, text): #metodo de inicializacion y tomamos el texto 
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text) 
        self.current_char = None #seguimiento del caracter actual
        self.advance()

    def advance(self): #metodo para avanzar al siguiente caracter en el texto de entrada
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None  
        #establecer el caracter actual al caracter en esa posicion dentro del texto,
        #  solo si la posicion es menor que la longitud del texto

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t\n': #ignorar espacios y tabulaciones
                self.advance()

            elif self.current_char in DIGITS:
                tokens.append(self.make_number()) #identificar si un caracter esta en 'digitos' 
                #ya que el numero puede tener mas de un caracter y arrojara un entero o un flotante
            
            elif self.current_char in LETRAS:
                tokens.append(self.make_word())
            
            elif self.current_char == ';':
                tokens.append(Token(T_SEMICOLON))
                self.advance()
            elif self.current_char == '=':
                tokens.append(Token(T_IGUAL))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(T_RCOR))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(T_LCOR))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(T_LPAR))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(T_RPAR))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(T_COMA))
                self.advance()
            elif self.current_char == '?':
                tokens.append(Token(T_QUESTION))
                self.advance()
            else: #si no encontramso el caracter q estamos buscando debemos arrojar un error
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return tokens, None
    
    def make_number(self): 
        num_str = '' 
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':  #seguimiento del numero en forma de cadena
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(T_INT, int(num_str))
        else:
            return Token(T_FLOAT, float(num_str))
        
    def make_word(self):
        word_str = ''
        while self.current_char != None and self.current_char in LETRAS:
            word_str += self.current_char
            self.advance()
        
        word_str = word_str.upper()
        
        if word_str == 'EXEC':
            return Token(T_EXEC, 'EXEC')
        elif word_str == 'NEW':
            return Token(T_NEW, 'NEW')
        elif word_str == 'VAR':
            return Token(T_VAR, 'VAR')
        elif word_str == 'MACRO':
            return Token(T_MACRO, 'MACRO')
        elif word_str == 'TURNTOMY':
            return Token(T_TURNTOMY, 'TURNTOMY')
        elif word_str == 'LEFT':
            return Token(T_LEFT, 'LEFT')
        elif word_str == 'RIGHT':
            return Token(T_RIGHT, 'RIGHT')
        elif word_str == 'BACK':
            return Token(T_BACK, 'BACK')
        elif word_str == 'TURNTOTHE':
            return Token(T_TURNTOMY, 'TURNTOTHE')
        elif word_str == 'NORTH':
            return Token(T_NORTH, 'NORTH')
        elif word_str == 'SOUTH':
            return Token(T_SOUTH, 'SOUTH')
        elif word_str == 'EAST':
            return Token(T_EAST, 'EAST')
        elif word_str == 'WEST':
            return Token(T_WEST, 'WEST')
        elif word_str == 'WALK':
            return Token(T_WALK, 'WALK')
        elif word_str == "JUMP":
            return Token(T_JUMP, 'JUMP')
        elif word_str == 'DROP':
            return Token(T_DROP, 'DROP')
        elif word_str == 'PICK':
            return Token(T_PICK, 'PICK')
        elif word_str == 'LETGO':
            return Token(T_LETGO, 'LETGO')
        elif word_str == 'GRAB':
            return Token(T_GRAB, "GRAB")
        elif word_str == 'POP':
            return Token(T_POP, 'GRAB')
        elif word_str == 'NOP':
            return Token(T_NOP, 'NOP')
        elif word_str == 'MOVES':
            return Token(T_MOVES, 'MOVES')
        elif word_str == 'FORWARD':
            return Token(T_FORWARD, 'FORWARD')
        elif word_str == 'BACKWARDS':
            return Token(T_BACKWARDS, 'BACKWARDS')
        
        elif word_str == 'IF':
            return Token(T_IF, 'IF')
        elif word_str == 'THEN':
            return Token(T_THEN, 'THEN')
        elif word_str == 'ELSE':
            return Token(T_ELSE, 'ELSE')
        elif word_str == 'FI':
            return Token(T_FI, 'FI')
        
        else: 
            return Token(T_VALIDVAR, 'VALIDVAR') #Hay que agregar un return false si no es valido?

####
# PARSER
###
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.current_tok = None
        self.advance()
        
    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        else: 
            self.current_tok = None #no esta en el video
        return self.current_tok # no es necesario a menos de que necesitemos validar algo
    
    def parse(self):
        while self.current_tok is not None:
            if (self.exec() or self.new() or  self.parse_if_statement() or 
                self.parse_do_while_loop() or self.parse_repeat_times_loop()):
                return True
        return False
   
    def exec(self):
        tok = self.current_tok
        if tok.type == T_EXEC:
            self.advance()
            # Llamado al bloque
            if self.current_tok.type == T_LCOR:
                if not (self.block()):
                    return False
                return True
        return False
    
    def new(self):
        if self.current_tok is None:
            return False  # Verifica si no hay tokens 
        
        if self.current_tok.type == T_NEW:
            self.advance()
            if self.current_tok.type == T_VAR:
                self.advance()
                if self.current_tok.type == T_VALIDVAR:
                    self.advance()
                    if self.current_tok.type == T_IGUAL:
                        self.advance()
                        if self.current_tok.type == T_INT: 
                            self.advance()
                            return True
                return False # Falso cuando NEW VAR no esta correcto
            elif self.current_tok.type == T_MACRO:
                self.advance()
                if self.current_tok.type == T_VALIDVAR: # nombre del macro
                    self.advance()
                    if self.current_tok.type == T_LPAR:
                        self.advance()
                        # Para revisar los parametros
                        while self.current_tok.type == T_VALIDVAR:
                            self.advance()
                            if self.current_tok.type == T_COMA:  # espera una coma para más parámetros
                                self.advance()
                                if self.current_tok.type != T_VALIDVAR:  # después de una coma debe venir otro parámetro
                                    return False
                            elif self.current_tok.type == T_RPAR:  # fin de los parámetros
                                break
                            else:
                                return False # Si el prox token no es valido o es None
                            
                    if self.current_tok.type == T_RPAR:
                        self.advance()
                    else:
                        return False    
                              
                    if self.current_tok.type == T_LCOR:
                        if self.current_tok == None:
                            return True
                        
                        return self.block()

                return False  # Falso cuando NEW MACRO no esta correcto    
                          
        return False # Falso cuando NEW no est correcto
    
    def block(self):
        if self.current_tok.type != T_LCOR:
            return False
        self.advance()
        corchete_abierto = 1
            
        while corchete_abierto > 0:
            #Para no entrar en un loop infinito porque no  haya un par 
            # completo de corchetes O no haya mas tokens
            if self.current_tok is None:
                return False
                
            if self.current_tok.type == T_LCOR:
                corchete_abierto += 1
            elif self.current_tok.type == T_RCOR:
                corchete_abierto -= 1
                if corchete_abierto == 0:
                    break
            else: 
                if not self.instrucciones():
                    return False  # si falla algun instruccion
                
                if self.current_tok.type != T_SEMICOLON:
                    return False  
            
            if corchete_abierto != 0:
                self.advance()    
        
        if corchete_abierto != 0:
            return False        
        
        return True
    
    def instrucciones(self):
        if self.current_tok.type == T_EXEC:
            return self.exec()
        elif self.current_tok.type == T_NEW:
            return self.new()
        elif self.current_tok.type == T_TURNTOMY:
            return self.turntomy()
        elif self.current_tok.type == T_TURNTOTHE:
            return self.turntothe()
        elif self.current_tok.type == T_WALK:
            return self.walk()
        elif self.current_tok.type == T_JUMP:
            return self.jump()
        elif self.current_tok.type == T_DROP:
            return self.drop()
        elif self.current_tok.type == T_PICK:
            return self.pick()
        elif self.current_tok.type == T_GRAB:
            return self.grab()
        elif self.current_tok.type == T_LETGO:
            return self.letgo()
        elif self.current_tok.type == T_POP:
            return self.pop()
        elif self.current_tok.type == T_NOP:
            return self.nop()
        elif self.current_tok.type == T_MOVES:
            return self.moves()
                
    def turntomy(self):
        if self.current_tok.type != T_TURNTOMY:
            return False
        self.advance()
        if self.current_tok.type == T_LPAR:
            self.advance()
            if self.current_tok.type in [T_LEFT, T_RIGHT, T_BACK]:
                self.advance()
                if self.current_tok.type == T_RPAR:
                    return True
        return False # Si no es correcto
    
    def turntothe(self):
        if self.current_tok.type != T_TURNTOTHE:
            return False
        self.advance()
        if self.current_tok.type == T_LPAR:
            self.advance()
            if self.current_tok.type in [T_NORTH, T_SOUTH, T_EAST, T_WEST]:
                self.advance()
                if self.current_tok.type == T_RPAR:
                    return True
        
        return False # Si no es correcto
        
    def walk(self):
        if self.current_tok.type != T_WALK:
            return False
        self.advance()
        if self.current_tok.type == T_LPAR:
            self.advance()
            if self.current_tok.type == T_INT:
                self.advance() 
                if self.current_tok.type == T_RPAR:
                    return True
        
        return False
    
    def jump(self):
        if self.current_tok.type != T_JUMP:
            return False
        self.advance()
        if self.current_tok.type == T_LPAR:
            self.advance()
            if self.current_tok.type == T_INT:
                self.advance() 
                if self.current_tok.type == T_RPAR:
                    return True
        
        return False
    
    def drop(self):
        if self.current_tok.type != T_DROP:
            return False
        self.advance()
        if self.current_tok.type == T_LPAR:
            self.advance()
            if self.current_tok.type == T_INT:
                self.advance() 
                if self.current_tok.type == T_RPAR:
                    return True
        
        return False
    
    def pick(self):
        if self.current_tok.type != T_PICK:
            return False
        self.advance()
        if self.current_tok.type == T_LPAR:
            self.advance()
            if self.current_tok.type == T_INT:
                self.advance() 
                if self.current_tok.type == T_RPAR:
                    return True
        
        return False
    
    def grab(self):
        if self.current_tok.type != T_GRAB:
            return False
        self.advance()
        if self.current_tok.type == T_LPAR:
            self.advance()
            if self.current_tok.type == T_INT:
                self.advance() 
                if self.current_tok.type == T_RPAR:
                    return True
        
        return False
    
    def letgo(self):
        if self.current_tok.type != T_LETGO:
            return False
        self.advance()
        if self.current_tok.type == T_LPAR:
            self.advance()
            if self.current_tok.type == T_INT:
                self.advance() 
                if self.current_tok.type == T_RPAR:
                    return True
        
        return False
    
    def pop(self):
        if self.current_tok.type != T_POP:
            return False
        self.advance()
        if self.current_tok.type == T_LPAR:
            self.advance()
            if self.current_tok.type == T_INT:
                self.advance() 
                if self.current_tok.type == T_RPAR:
                    return True
        
        return False
    
    def nop(self):
        return True
    
    def moves(self):
        if self.current_tok.type != T_MOVES:
            return False
    
        self.advance()
        
        if self.current_tok.type == T_LPAR:
            self.advance() # primera direccion o RPAR si es vacio
            
            if self.current_tok.type == T_RPAR: # Lista de direcciones vacia
                return True 
            
            while self.current_tok.type != T_RPAR:
                if self.current_tok.type in [T_LEFT, T_RIGHT, T_FORWARD, T_BACKWARDS]:
                    self.advance()
                    if self.current_tok.type == T_COMA:
                        self.advance()
                        if self.current_tok.type == T_RPAR:
                            return False
                    elif self.current_tok.type == T_RPAR:
                        return True
                    
        return False # si no esta correcto
              
    def parse_if_statement(self):
        if self.current_tok.type != T_IF:
            return False
        self.advance()
        
        if self.current_tok.type == T_LPAR:
            self.advance()
            # Evaluación de la condición
            if not self.parse_condition():
                return False
            if self.current_tok.type != T_RPAR:
                return False
            self.advance()
            
            #  IF
            if self.current_tok.type != T_THEN:
                return False
            self.advance()
            if not self.block():
                return False
            
            # ELSE
            if self.current_tok.type == T_ELSE:
                self.advance()
                if not self.block():
                    return False
            
            # FI
            if self.current_tok.type != T_FI:
                return False
            self.advance()
            return True
        
        return False

    def parse_do_while_loop(self):
        if self.current_tok.type != T_DO:
            return False
        self.advance()
        
        if self.current_tok.type != T_LPAR:
            return False
        self.advance()
        
        # Condición
        if not self.parse_condition():
            return False
        
        if self.current_tok.type != T_RPAR:
            return False
        self.advance()
        
        #  DO
        if not self.block():
            return False
        
        # OD
        if self.current_tok.type != T_OD:
            return False
        self.advance()
        
        return True

    def parse_repeat_times_loop(self):
        if self.current_tok.type == T_INT:
            count = self.current_tok.value
            self.advance()
            if self.current_tok.type != T_TIMES:
                return False
            self.advance()
            
            # Procesar el contenido del bucle
            if not self.block():
                return False
            
            return True

    def parse_condition(self):
        condition = []
        while self.current_tok.type in [T_VALIDVAR, T_FLOAT, T_NOT, T_QUESTION]:
            if self.current_tok.type == T_NOT:
                condition.append('NOT ')
                self.advance()
            elif self.current_tok.type == T_QUESTION:
                condition.append('?')
                self.advance()
            
            if self.current_tok.type == T_VALIDVAR:
                var_name = self.current_tok.value
                self.advance()
                condition.append(var_name)
            elif self.current_tok.type == T_FLOAT:
                value = self.current_tok.value
                self.advance()
                condition.append(str(value))
        
        return ' '.join(condition)                
            
            
#######
#RUN
###################
def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    
    parser = Parser(tokens)
    ToF_parse = parser.parse()

    return tokens, error, ToF_parse
