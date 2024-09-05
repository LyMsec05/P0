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
T_TURNTOMY = 'TURNTO'
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

T_VALIDVAR = 'VALIDVAR'


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
            if self.current_char in ' \t': #ignorar espacios y tabulaciones
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
        if word_str == 'EXEC':
            return Token(T_EXEC, 'EXEC')
        elif word_str == 'NEW':
            return Token(T_NEW, 'NEW')
        elif word_str == 'VAR':
            return Token(T_VAR, 'VAR')
        elif word_str == 'MACRO':
            return Token(T_MACRO, 'MACRO')
        else: 
            return Token(T_VALIDVAR, 'VALIDVAR') #Hay que agregar un return false si no es valido

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
        else: self.current_tok = None #no esta en el video
        return self.current_tok # no es necesario a menos de que necesitemos validar algo
    
    def parse(self):
        while self.current_tok is not None:
            if not (self.exec() or self.new()):
                return False
            self.advance()
        return True
   
    def exec(self):
        tok = self.current_tok
        if tok.type == T_EXEC:
            self.advance()
            # Llamado al bloque
            if self.current_tok.type == T_LCOR:
                if not self.block():
                    return False
                return True
        else: return False
    
    def new(self):
        if self.current_tok.type == T_NEW:
            self.advance()
            if self.current_tok.type == T_VAR:
                self.advance()
                if self.current_tok.type == T_VALIDVAR:
                    self.advance()
                    if self.current_tok == T_IGUAL:
                        self.advance()
                        if self.current_tok == T_INT: 
                            # no se termina con advance porq parse lo llama
                            return True
                return False # Falso cuando NEW VAR no esta correcto
            elif self.current_tok.type == T_MACRO:
                self.advance()
                macro_name = self.current_tok
                self.advance()
                #Llamado al bloque
                if self.current_tok.type == T_LCOR:
                    if not self.block():
                        return False
                return True
                
        return False
    
    def block(self):
        if self.current_tok.type == T_LCOR:
            self.advance()
            corchete_abierto = 1
            while corchete_abierto > 0:
                
                #Para no entrar en un loop infinito porque no  haya un par 
                # completo de corchetes O no haya mas tokens
                if self.current_tok.type is None:
                    return False
                
                if self.current_tok.type == T_LCOR:
                    corchete_abierto += 1
                elif self.current_tok.type == T_RCOR:
                    corchete_abierto -= 1
                    if corchete_abierto == 0: 
                        self.advance()
                        return True
                
                if not (self.new() or self.exec()):
                    return False
                self.advance()
                
        
#######
#RUN
###################
def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    
    parser = Parser(tokens)
    result = parser.parse()

    return tokens, error, result