import re


class Syntax:
    def __init__(content, tokens):
        content.tokens = tokens
        content.current_token = None
        content.index = 1
        content.grammars = [
            ('PROGRAMA', ['programa', 'id', ';', 'CUERPO', '.']),
            ('CUERPO', ['DECLARACIONES', 'PRINCIPAL']),
            ('CUERPO', ['PRINCIPAL']),
            ('DECLARACIONES', ['variable', 'LISTAID', ':', 'TIPOS', ';', 'AUX1']),
            ('AUX1', ['LISTAID', ':', 'TIPOS', ';', 'AUX1']),
            ('AUX1', []),
            ('LISTAID', ['id', 'AUX2']),
            ('AUX2', [',', 'id', 'AUX2']),
            ('AUX2', []),
            ('TIPOS', ['ESTANDAR']),
            ('TIPOS', ['VECTORES']),
            ('ESTANDAR', ['enteros']),
            ('ESTANDAR', ['real']),
            ('ESTANDAR', ['cadena']),
            ('ESTANDAR', ['byte']),
            ('ESTANDAR', ['caracter']),
            ('ESTANDAR', ['booleano']),
            ('VECTORES', ['arreglo', '[', 'enteros', '..', 'enteros', ']', 'de', 'ESTANDAR']),
            ('PRINCIPAL', ['{', 'ESTATUTOS', '}']),
            ('ESTATUTOS', ['ESTATUTO', ';', 'AUX3']),
            ('AUX3', ['ESTATUTO', ';', 'AUX3']),
            ('AUX3', []),
            ('ESTATUTO', ['ASIGNACION']),
            ('ESTATUTO', ['CICLOREPETIR']),
            ('ESTATUTO', ['CICLOPARA']),
            ('ESTATUTO', ['CICLOMIENTRAS']),
            ('ESTATUTO', ['ENTRADA']),
            ('ESTATUTO', ['SALIDA']),
            ('ESTATUTO', ['CONDICIONALSI']),
            ('ASIGNACION', ['VARIABLES', '=', 'EXPRESION']),
            ('VARIABLES', ['id', 'AUX5']),
            ('AUX5', [',', 'EXPRESION', 'AUX5']),
            ('AUX5', []),
            ('CICLOREPETIR', ['repetir', 'ESTATUTO', 'hasta', 'EXPRESION']),
            ('CICLOPARA', ['para', 'CONTADOR', 'do', '{', 'ESTATUTOS', '}']),
            ('CONTADOR', ['id', '=', 'EXPRESION', 'para', 'EXPRESION']),
            ('CICLOMIENTRAS', ['mientras', 'EXPRESION', 'hacer', '{', 'ESTATUTOS', '}']),
            ('ENTRADA', ['leer', '(', 'VARIABLES', 'AUX6']),
            ('AUX6', [',', 'VARIABLES', 'AUX6']),
            ('AUX6', [')']),
            ('SALIDA', ['escribir', '(', 'EXPRESION', 'AUX7']),
            ('AUX7', [',', 'EXPRESION', 'AUX7']),
            ('AUX7', [')']),
            ('CONDICIONALSI', ['si', 'EXPRESION', 'entonces', '{', 'ESTATUTOS', '}', 'AUX8']),
            ('AUX8', ['sino', '{', 'ESTATUTOS', '}', 'fin_sino']),
            ('AUX8', ['fin_sino']),
            ('EXPRESION', ['EXP', 'RELACIONAL', 'EXP']),
            ('EXPRESION', ['EXP']),
            ('EXP', ['TERMINO', 'AUX9']),
            ('AUX9', ['+', 'TERMINO', 'AUX9']),
            ('AUX9', ['-', 'TERMINO', 'AUX9']),
            ('AUX9', ['o', 'TERMINO', 'AUX9']),
            ('AUX9', []),
            ('RELACIONAL', ['=']),
            ('RELACIONAL', ['<']),
            ('RELACIONAL', ['>']),
            ('RELACIONAL', ['<=']),
            ('RELACIONAL', ['>=']),
            ('RELACIONAL', ['<>']),
            ('TERMINO', ['FACTOR', 'AUX10']),
            ('AUX10', ['*', 'FACTOR', 'AUX10']),
            ('AUX10', ['/', 'FACTOR', 'AUX10']),
            ('AUX10', ['division', 'FACTOR', 'AUX10']),
            ('AUX10', ['modulo', 'FACTOR', 'AUX10']),
            ('AUX10', ['y', 'FACTOR', 'AUX10']),
            ('AUX10', []),
            ('FACTOR', ['(', 'EXPRESION', ')']),
            ('FACTOR', ['VARIABLES']),
            ('FACTOR', ['CONSTANTES']),
            ('FACTOR', ['no', 'EXPRESION']),
            ('CONSTANTES', ['entero']),
            ('CONSTANTES', ['real']),
            ('CONSTANTES', ['cadena']),
            ('CONSTANTES', ['caracter']),
            ('CONSTANTES', ['verdadero']),
            ('CONSTANTES', ['falso']),
        ]

    def __init__(content, tokens):
        content.tokens = tokens
        content.current_token = None
        content.index = 1

    def parse(content):
        if tokens[0] == '$':
            content.current_token = content.tokens[1]
            content.programa()
            print("Syntax is valid.")
        else:
            print(
                f"Syntax error: Expected $ at first position, found '{tokens[0]}'")

    def match(content, expected_token):
        if content.current_token == expected_token:
            content.advance()
        else:
            raise SyntaxError(
                f"Syntax error: Expected '{expected_token}', found '{content.current_token}'")

    def advance(content):
        content.index += 1
        if content.index < len(content.tokens):
            content.current_token = content.tokens[content.index]
        else:
            content.current_token = None

    def programa(content):
        # Production rule: PROGRAMA -> programa id ; CUERPO .
        content.match('programa')
        content.match('id')
        content.match(';')
        content.cuerpo()
        content.match('.')

    def cuerpo(content):
        # Production rule: CUERPO -> DECLARACIONES PRINCIPAL | PRINCIPAL
        if content.current_token == 'variable':
            content.declaraciones()
            content.principal()
        elif content.current_token == '{':
            content.principal()
        else:
            raise SyntaxError(
                f"Syntax error: Unexpected token {content.current_token}")

    def declaraciones(content):
        # Production rule: DECLARACIONES -> variable LISTAID : TIPOS ; AUX1
        content.match('variable')
        content.listaid()
        content.match(':')
        content.tipos()
        content.match(';')
        content.aux1()

    def aux1(content):
        # Production rule: AUX1 -> LISTAID : TIPOS ; AUX1 | EPSILON
        if content.current_token == 'variable':
            content.match('variable')
            content.listaid()
            content.match(':')
            content.tipos()
            content.match(';')
            content.aux1()

    def listaid(content):
        # Production rule: LISTAID -> id AUX2
        content.match('id')
        content.aux2()

    def aux2(content):
        # Production rule: AUX2 -> , id AUX2 | EPSILON
        if content.current_token == ',':
            content.match(',')
            content.match('id')
            content.aux2()

    def tipos(content):
        # Production rule: TIPOS -> ESTANDAR | VECTORES
        if content.current_token in ['entero', 'real', 'cadena', 'byte', 'caracter', 'booleano']:
            content.estandar()
        elif content.current_token == 'arreglo':
            content.vectores()
        else:
            raise SyntaxError(
                f"Syntax error: Unexpected token {content.current_token}")

    def estandar(content):
        # Production rule: ESTANDAR -> entero | real | cadena | byte | caracter | booleano
        if content.current_token in ['entero', 'real', 'cadena', 'byte', 'caracter', 'booleano']:
            content.match(content.current_token)
        else:
            raise SyntaxError(
                f"Syntax error: Expected a standard type, found {content.current_token}")

    def vectores(content):
        # Production rule: VECTORES -> arreglo [ entero .. entero ] de ESTANDAR
        content.match('arreglo')
        content.match('[')
        content.match('entero')
        content.match('..')
        content.match('entero')
        content.match(']')
        content.match('de')
        content.estandar()

    def principal(content):
        # Production rule: PRINCIPAL -> { ESTATUTOS }
        content.match('{')
        content.estatutos()
        content.match('}')

    def estatutos(content):
        # Production rule: ESTATUTOS -> ESTATUTO ; AUX3
        content.estatuto()
        content.match(';')
        content.aux3()

    def aux3(content):
        # Production rule: AUX3 -> ESTATUTO ; AUX3 | EPSILON
        if content.current_token in ['id', 'leer', 'escribir', 'si', 'repetir', 'para', 'mientras']:
            content.estatuto()
            content.match(';')
            content.aux3()

    def estatuto(content):
        # Production rule: ESTATUTO -> ASIGNACION | CICLOPARA | CICLOMIENTRAS | CICLOREPETIR | ENTRADA | SALIDA | CONDICIONALSI
        if content.current_token == 'id':
            content.asignacion()
        elif content.current_token == 'repetir':
            content.ciclorepetir()
        elif content.current_token == 'para':
            content.ciclopara()
        elif content.current_token == 'mientras':
            content.ciclomientras()
        elif content.current_token == 'leer':
            content.entrada()
        elif content.current_token == 'escribir':
            content.salida()
        elif content.current_token == 'si':
            content.condicionalsi()
        else:
            raise SyntaxError(
                f"Syntax error: Unexpected token {content.current_token}")

    def asignacion(content):
        # Production rule: ASIGNACION -> VARIABLES = EXPRESION | VARIABLES [ EXPRESION ] = EXPRESION
        content.variables()
        if content.current_token == '=':
            content.match('=')
            content.expresion()
        elif content.current_token == '[':
            content.match('[')
            content.expresion()
            content.match(']')
            content.match('=')
            content.expresion()
        else:
            raise SyntaxError(
                f"Syntax error: Invalid assignment syntax at {content.current_token}")

    def variables(content):
        # Production rule: VARIABLES -> id AUX5
        content.match('id')
        content.aux5()

    def aux5(content):
        # Production rule: AUX5 -> , EXPRESION AUX5 | EPSILON
        if content.current_token == ',':
            content.match(',')
            content.expresion()
            content.aux5()

    def ciclorepetir(content):
        # Production rule: CICLOREPETIR -> repetir ESTATUTO hasta EXPRESION
        content.match('repetir')
        content.estatuto()
        content.match('hasta')
        content.expresion()

    def ciclopara(content):
        # Production rule: CICLOPARA -> para CONTADOR hacer { ESTATUTOS }
        content.match('para')
        content.contador()
        content.match('hacer')
        content.match('{')
        content.estatutos()
        content.match('}')

    def contador(content):
        # Production rule: CONTADOR -> id = EXPRESION para EXPRESION
        content.match('id')
        content.match('=')
        content.expresion()
        content.match('para')
        content.expresion()

    def ciclomientras(content):
        # Production rule: CICLOMIENTRAS -> mientras EXPRESION hacer { ESTATUTOS }
        content.match('mientras')
        content.expresion()
        content.match('hacer')
        content.match('{')
        content.estatutos()
        content.match('}')

    def entrada(content):
        # Production rule: ENTRADA -> leer ( VARIABLES AUX6
        content.match('leer')
        content.match('(')
        content.variables()
        content.aux6()

    def aux6(content):
        # Production rule: AUX6 -> , VARIABLES AUX6 | )
        if content.current_token == ',':
            content.match(',')
            content.variables()
            content.aux6()
        elif content.current_token == ')':
            content.match(')')

    def salida(content):
        # Production rule: SALIDA -> escribir ( EXPRESION AUX7
        content.match('escribir')
        content.match('(')
        content.expresion()
        content.aux7()

    def aux7(content):
        # Production rule: AUX7 -> , EXPRESION AUX7 | )
        if content.current_token == ',':
            content.match(',')
            content.expresion()
            content.aux7()
        elif content.current_token == ')':
            content.match(')')

    def condicionalsi(content):
        # Production rule: CONDICIONALSI -> si EXPRESION entonces { ESTATUTOS } AUX8
        content.match('si')
        content.expresion()
        content.match('entonces')
        content.match('{')
        content.estatutos()
        content.match('}')
        content.aux8()

    def aux8(content):
        # Production rule: AUX8 -> Sino { ESTATUTOS } fin_sino | fin_sino
        if content.current_token == 'Sino':
            content.match('Sino')
            content.match('{')
            content.estatutos()
            content.match('}')
            content.match('fin_sino')
        elif content.current_token == 'fin_sino':
            content.match('fin_sino')

    def expresion(content):
        # Production rule: EXPRESION -> EXP | EXP RELACIONAL EXP
        content.exp()
        if content.current_token in ['=', '<', '>', '<=', '>=', '<>']:
            content.relacional()
            content.exp()

    def exp(content):
        # Production rule: EXP -> TERMINO AUX9
        content.termino()
        content.aux9()

    def aux9(content):
        # Production rule: AUX9 -> + TERMINO AUX9 | - TERMINO AUX9 | o TERMINO AUX9 | EPSILON
        if content.current_token in ['+', '-', 'o']:
            content.match(content.current_token)
            content.termino()
            content.aux9()

    def relacional(content):
        # Production rule: RELACIONAL -> = | < | > | <= | >= | <>
        if content.current_token in ['=', '<', '>', '<=', '>=', '<>']:
            content.match(content.current_token)
        else:
            raise SyntaxError(
                f"Syntax error: Expected a relational operator, found {content.current_token}")

    def termino(content):
        # Production rule: TERMINO -> FACTOR AUX10
        content.factor()
        content.aux10()

    def aux10(content):
        # Production rule: AUX10 -> * FACTOR AUX10 | / FACTOR AUX10 | division FACTOR AUX10 | modulo FACTOR AUX10 | y FACTOR AUX10 | EPSILON
        if content.current_token in ['*', '/', 'division', 'modulo', 'y']:
            content.match(content.current_token)
            content.factor()
            content.aux10()

    def factor(content):
        # Production rule: FACTOR -> ( EXPRESION ) | VARIABLES | CONSTANTES | no EXPRESION
        if content.current_token == '(':
            content.match('(')
            content.expresion()
            content.match(')')
        elif content.current_token == 'id':
            content.variables()
        elif content.current_token in ['entero', 'real', 'cadena', 'caracter', 'verdadero', 'falso']:
            content.constantes()
        elif content.current_token == 'no':
            content.match('no')
            content.expresion()
        else:
            raise SyntaxError(
                f"Syntax error: Unexpected token {content.current_token}")

    def constantes(content):
        # Production rule: CONSTANTES -> entero | real | cadena | caracter | verdadero | falso
        if content.current_token in ['entero', 'real', 'cadena', 'caracter', 'verdadero', 'falso']:
            content.match(content.current_token)
        else:
            raise SyntaxError(
                f"Syntax error: Expected a constant value, found {content.current_token}")

with open('lexical.txt', 'r') as file:
    content = file.read()

tokens = content.split()
syntax = Syntax(tokens)
syntax.parse()
