# coding=UTF-8
# Vanessa Alves do Nascimento 10882848

#EXERCICIO PROGRAMA: EMULAÇÃO DE AFN

# limpa arquivo de saída sempre que roda o programa
open('saida.txt', 'w').close()

# estados_com_cadeia_vazia: retorna os estados com cadeia vazia representado por -1
def estados_com_cadeia_vazia(estados_finais, estado):
    estados = {'-1'}
    if estado == '-1':
        return '-1'
    for q in estado:
       qf = estados_finais[q][-1]
       for i in qf:
           estados.add(i)
    estados.remove('-1')
    return tuple(sorted(estados, key = int))

# checa_cadeia_vazia: valida se o estado tem cadeia vazia
def checa_cadeia_vazia(transicoes, estado):
    estados = []
    for transicao in transicoes:
        if transicao[0] == estado and transicao[1] == '0':
            estados.append(transicao[2])
    return estados

# cadeia_valida: percorre a cadeia de símbolos, testando estados do afn
def cadeia_valida(estados_finais, estado, simbolos):
    conjunto_estados = ['-1']
    if '0' in simbolos:
        simbolos.remove('0')
    if estado == '-1':
        for i in range(len(simbolos)-1):
            conjunto_estados.append('-1')
        return conjunto_estados
    estados = []
    for simbolo in simbolos:
        aux = []
        for i in estado:
            temp_estado = estados_finais[i][int(simbolo)]
            if temp_estado == '-1':
                continue
            strings_vazias = estados_com_cadeia_vazia(estados_finais, temp_estado)
            for e in strings_vazias:
                aux.append(e)
        if aux:
            if len(aux) == 1:
                estados.append(aux[0])
            else:
                aux = list(set(aux))
                estados.append(tuple(sorted(aux, key = int)))
        else:
            estados.append('-1')
    conjunto_estados.append(estados)
    conjunto_estados.remove('-1')
    return list(conjunto_estados)[0]

# transicoes_estado: retorna transições de um estado do afn
def transicoes_estado(transicoes, estado, num_simbolos):
    resultado = []
    for s in num_simbolos:
        aux = []
        for transicao in transicoes:
            if (transicao[0] == estado) and (transicao[1] == s):
                aux.append(str(transicao[2]))
        if not aux:
            resultado.append('-1')
        elif len(aux) == 1:
            resultado.append(aux[0])
        else:
            resultado.append(tuple(sorted(aux, key = int)))
    return resultado

# estados_adj: retorna quais estados posso encontrar a partir de um determinado estado
def estados_adj(transicoes, estado):
    aux = [estado]
    for i in aux:
        estados = checa_cadeia_vazia(transicoes, i)
        for estado in estados:
            if estado not in aux:
                aux.append(estado)
    if len(aux) == 1:
        return str(list(aux)[0])
    return tuple(sorted(aux, key = int))

# gera_afn: gera um arquivo de saida.txt para cadeias testadas
def gera_afn(transicoes_validas, estado_inicial, estados_aceitos, cadeias):
    with open('saida.txt', 'a') as resultado:
        for cadeia in cadeias:
            num_estados = [estado_inicial]
            if cadeia != ['0']:
                for simbolo in cadeia:
                    num_estados.append(transicoes_validas[num_estados[-1]][int(simbolo)-1])

            estado_final = num_estados[-1]
            cadeia_aceita = False
            for estado_aceito in estados_aceitos:
                if type(estado_final) == str:
                    if estado_final == estado_aceito:
                        resultado.write('1 ')
                        cadeia_aceita = True
                        break
                else:
                    if estado_aceito in estado_final:
                        resultado.write('1 ')
                        cadeia_aceita = True
                        break
            if not cadeia_aceita:
                resultado.write('0 ')
        resultado.write("\n")
    resultado.close()

# constroi_automato: constroi um automato com base nas informações do entrada.txt
def constroi_automato(transicoes, estados, simbolos, estado_inicial):
    constroiAfn = {}
    for estado in estados:
        constroiAfn[estado] = transicoes_estado(transicoes, estado, simbolos)
        constroiAfn[estado].append(estados_adj(transicoes, estado))

    if checa_cadeia_vazia(transicoes, estado_inicial):
        estado_inicial = estados_adj(transicoes, estado_inicial)

    estados_validos = [estado_inicial]
    transicoes_validas = {}
    for estado in estados_validos:
        transicoes = cadeia_valida(constroiAfn, estado, simbolos)
        transicoes_validas[estado] = transicoes
        for t in transicoes:
            if len(t) == 1:
                t_afn = ''.join(t)
            else:
                t_afn = t
            if t_afn not in estados_validos:
                estados_validos.append(t_afn)

    num_cadeias = input.readline()
    cadeias = []
    for cadeia in range(int(num_cadeias)):
        cadeias.append(input.readline().rstrip().split(' '))
    gera_afn(transicoes_validas, estado_inicial, estados_aceitacao, cadeias)

# lendo propriedades do arquivo entrada.txt e passando para as variáveis para construção do autômato
try:
    with open('entrada.txt', 'r') as input:
        num_automatos = input.readline()

        for automato in list(range(int(num_automatos))):

            leituraLinha = input.readline().rstrip().split(' ')
            estado_inicial = leituraLinha[3]

            estados = list(range(int(leituraLinha[0])))
            for i in estados:
                estados[i] = str(estados[i])

            simbolos = list(range(int(leituraLinha[1])))
            for i in simbolos:
                simbolos[i] = str(simbolos[i])

            estados_aceitacao = input.readline().rstrip().split(' ')

            transicoes = []
            num_transicoes = leituraLinha[2]
            for transicao in range(int(num_transicoes)):
                transicoes.append(input.readline().rstrip().split(' '))

            constroi_automato(transicoes, estados, simbolos, estado_inicial)
        input.close()
except IOError:
    print("Necessário o arquivo entrada.txt")