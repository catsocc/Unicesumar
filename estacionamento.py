from datetime import datetime
#importando a classe datetime do módulo datetime para trabalhar com datas e horários no código

#Lista para armazenar os dados dos veículos em dicionários
estacionamento= []

#Função para retornar o dia da semana
def obter_dia_da_semana(data):
    dias = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    return dias[data.weekday()]

#Solicito que o usuário digite uma data, para não executar o programa no domingo
data_input = input("Por favor, insira a data no formato (dd/mm/aaaa): ")
try:
    data_usuario = datetime.strptime(data_input, "%d/%m/%Y")  # Converte a string para uma data
    dia_semana = obter_dia_da_semana(data_usuario)  # Obter o dia da semana

    #Condição se oo dia for domingo, encerra! Evita que execute o programa fora do dia de funcionamento
    if dia_semana == "Domingo":
        print("O estacionamento não funciona aos domingos. Programa encerrado.")
    else:
        print(f"Bem-vindo! Hoje é {dia_semana}. O sistema está funcionando normalmente.")

        #Função para não registrar hora de entrada/saida fora do horário de funcionamento
        def validar_horario():
            while True:
                horario_str = input("Digite o horário (HH:MM): ")
                if "08:00" <= horario_str <= "18:00":
                    return horario_str  # Retorna como string
                else:
                    print("[Horário fora do funcionamento permitido (8h às 18h). Tente novamente.")

        #Função que calcula o tempo de permanência em minutos entre a entrada e a saída
        def calcular_tempo(entrada, saida):
            tempo = saida - entrada
            if tempo.days < 0:
                print("Hora de saída anterior à de entrada. Corrija os dados.")
                return None
            return tempo.total_seconds() // 60

        # Função para validar o tipo de veículo
        # Apenas permite os tipos: motocicleta, carro de passeio ou caminhonete
        def validar_tipo_veiculo():
            tipos_validos = ["motocicleta", "carro de passeio", "caminhonete"]
            while True:
                tipo = input("Digite o tipo do veículo (motocicleta, carro de passeio, caminhonete): ").lower()
                #'if tipo in tipos_validos' verifica se tipo(variável) está na lista tipos_validos para retonar ao programa um tipo válido
                if tipo in tipos_validos:
                    return tipo

                #caso não seja inserido um tipo válido pelo usuário, é exiba a mensagem de erro, e devido ao loop (while) solicita novamente
                #apenas quando é inserido um tipo válido, o 'return' encerra o loop, e rotorna o tipo do veículo
                print("Tipo de veículo inválido. Use uma das opções: motocicleta, carro de passeio, caminhonete.")


        #Função para exibir os detalhes de um veiculo

        def exibir_detalhes_veiculo(veiculo):
            detalhes = f"Placa: {veiculo['placa']} / Tipo: {veiculo['tipo']} / Entrada: {veiculo['entrada'].strftime('%H:%M')}"
            if veiculo["saida"]:
                detalhes += f" / Saída: {veiculo['saida'].strftime('%H:%M')} / Tempo: {int(veiculo['tempo'])} min / Valor: R$ {veiculo['valor']:.2f}"
            else:
                detalhes += " / Saída: ---"
            print(detalhes)

        # Função para registrar a entrada de um veículo
        # Coleta placa, horário e tipo de veículo e adiciona à lista
        # Garante que não haja duplicidade sem saída registrada
        def registrar_entrada():
            placa = str(input('Digite a placa do veículo: ')).upper()

            # Conferir se a placa já está registrada e sem saída
            for veiculo in estacionamento:
                if veiculo["placa"] == placa and veiculo["saida"] is None:
                    print("Veículo com esta placa já está no estacionamento.")
                    return

            tipo = validar_tipo_veiculo()

            # Validar horário como string e converter para datetime
            entrada_str = validar_horario()
            entrada = datetime.strptime(entrada_str, "%H:%M")  # Converte para datetime

            estacionamento.append({
                "placa": placa,
                "tipo": tipo,
                "entrada": entrada,
                "saida": None,
                "tempo": None,
                "valor": None
            })
            print(f"\nEntrada registrada para {placa} às {entrada.strftime('%H:%M')}.\n")

        # Função para registrar a saída de um veículo
        # Atualiza tempo de permanência e valor a pagar, exibindo os dados ao final
        def registrar_saida():
            placa = input("Digite a placa do veículo que irá sair: ").upper()

            for veiculo in estacionamento:
                if veiculo["placa"] == placa and veiculo["saida"] is None:
                    saida_str = validar_horario()
                    saida = datetime.strptime(saida_str, "%H:%M")  # Convertendo para datetime

                    veiculo["saida"] = saida
                    minutos = calcular_tempo(veiculo["entrada"], saida)
                    if not minutos:
                        return
                    veiculo["tempo"] = minutos

                    minutos, valor = calcula_valor(veiculo["entrada"], saida)
                    veiculo["tempo"] = minutos
                    veiculo["valor"] = valor

                    print("Saída registrada.")
                    exibir_detalhes_veiculo(veiculo)
                    return

            print("Veículo não encontrado ou já saiu.")

        # Função que calcula o valor a ser cobrado com base no tempo de permanência
        def calcula_valor(entrada, saida):
            minutos = calcular_tempo(entrada, saida)

            if minutos <= 15:
                return minutos, 0
            elif minutos <= 60:
                return minutos, 1.50
            else:
                horas_adicionais = (minutos - 60) // 60
                valor = 1.50 + (horas_adicionais * 1.00)
                if (minutos - 60) % 60 > 0:
                    valor += 1.00  # Cobra por mais uma hora, mesmo que incompleta
                return minutos, valor

        # Função para listar os veículos registrados
        def listar_veiculos():
            #condição para caso não tenha veiculo registrado
            #'if not' verifica se a lista está vazia
            if not estacionamento:
                print("Nenhum veículo registrado.")
                return

            #loop para percorrer a lista "estacionamento"
            for v in estacionamento:
                exibir_detalhes_veiculo(v)

        # Função para contar veículos por tipo
        def contar_por_tipo():
            tipos = {"motocicleta": 0, "carro de passeio": 0, "caminhonete": 0}  # Corrigindo os nomes
            for v in estacionamento:
                if v["tipo"] in tipos and v["saida"] is None:
                    tipos[v["tipo"]] += 1  # Incrementando conforme o tipo

            print("\nVeículos atualmente no estacionamento:")
            for tipo, qtd in tipos.items():
                print(f"{tipo.capitalize()}: {qtd}")

        # Função para calcular valor total arrecadado
        def valor_total_arrecadado():
            total = sum(v["valor"] for v in estacionamento if v["valor"] is not None)
            print(f"\nValor total arrecadado até o momento: R$ {total:.2f}")

        # Função para contar veículos isentos
        def contar_isentos():
            isentos = sum(1 for v in estacionamento if v["valor"] == 0)
            print(f"\nTotal de veículos isentos até agora: {isentos}")

        #Função para encerrar o expediente e atualizar automaticamente a saida dos veiculos que ainda restaram
        #Define a saída como 18:00 e calcula o tempo e valor
        def encerrar_dia():
            print("\nEncerrando o dia. Relatório final dos veículos estacionados:")
            total_arrecadado = 0  # Variável para acumular o valor total do dia

            if not estacionamento:
                print("Nenhum veículo no estacionamento.")
            else:
                for veiculo in estacionamento:
                    # Verificar se o veículo não registrou saída
                    if veiculo["saida"] is None:
                        # Definir a saída como o horário de fechamento (18:00)
                        saida = datetime.strptime("18:00", "%H:%M")
                        veiculo["saida"] = saida
                        minutos = calcular_tempo(veiculo["entrada"], saida)
                        if minutos:
                            veiculo["tempo"] = minutos
                            _, valor = calcula_valor(veiculo["entrada"], saida)
                            veiculo["valor"] = valor
                            total_arrecadado += valor

                        # Exibir detalhes do veículo
                        exibir_detalhes_veiculo(veiculo)

            estacionamento.clear()  #limpa a lista de veiculos
            print(f"\nValor total arrecadado no dia: R$ {total_arrecadado:.2f}")
            print("Estacionamento fechado!")
            exit()

        #função principal que exibe o menu de opções
        def menu():
            op = '0'
            while op != '8':
                print("\n--- UniCesumar Parking ---")
                print("\n1 - Registrar Entrada")
                print("2 - Registrar Saída")
                print("3 - Listar Veículos")
                print("4 - Contar por Tipo")
                print("5 - Total Arrecadado")
                print("6 - Total de Isentos")
                print("7 - Encerrar o dia")
                print("8 - Sair\n")
                op = input('Digite uma opção: ')

                if op == '1':
                    registrar_entrada()
                elif op == '2':
                    registrar_saida()
                elif op == '3':
                    listar_veiculos()
                elif op == '4':
                    contar_por_tipo()
                elif op == '5':
                    valor_total_arrecadado()
                elif op == '6':
                    contar_isentos()
                elif op == '7':
                    encerrar_dia()
                elif op == '8':
                    print('Encerrando programa...\n')
                else:
                    print('Opção inválida.')

        #chamada da função principal para iniciar o programa do estacionamento
        menu()

#Garante que caso o usuário digite a data em formato inválido, solicite para digitar novamente
except ValueError:
    print("Data inválida! Tente novamente com o formato correto (dd/mm/aaaa).")

