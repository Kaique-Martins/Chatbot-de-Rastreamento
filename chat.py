import random
from datetime import datetime, timedelta

class PedidoSimulado:
    def __init__(self, id_pedido):
        self.id_pedido = id_pedido
        self.produto = self._gerar_produto()
        self.status = "Em processamento"
        self.data_compra = datetime.now() - timedelta(days=random.randint(1, 5))
        self.data_envio = self.data_compra + timedelta(days=random.randint(1, 3)) if random.random() > 0.3 else None
        self.data_entrega = self.data_envio + timedelta(days=random.randint(7, 21)) if self.data_envio else None
        self.codigo_rastreio = f"TR{random.randint(100000000, 999999999)}BR" if self.data_envio else None
        self.etapas = self._gerar_etapas()
    
    def _gerar_produto(self):
        produtos = [
            "Smartphone XIAOMI Redmi Note 12",
            "Fone de Ouvido Bluetooth",
            "Relógio Inteligente GT3",
            "Câmera DSLR 24MP",
            "Tablet Android 10''",
            "Teclado Mecânico RGB"
        ]
        return random.choice(produtos)
    
    def _gerar_etapas(self):
        etapas = []
        etapas.append(("Pedido realizado", self.data_compra))
        
        if self.data_envio:
            etapas.append(("Pedido enviado", self.data_envio))
            
            # Simular atualizações de transporte
            if random.random() > 0.7:
                data_chegada_alfandega = self.data_envio + timedelta(days=random.randint(2, 5))
                etapas.append(("Chegou na alfândega", data_chegada_alfandega))
                
                if random.random() > 0.3:
                    data_liberacao = data_chegada_alfandega + timedelta(days=random.randint(1, 3))
                    etapas.append(("Liberado pela alfândega", data_liberacao))
            
            if self.data_entrega:
                etapas.append(("Saiu para entrega", self.data_entrega - timedelta(days=1)))
                etapas.append(("Entregue", self.data_entrega))
                self.status = "Entregue"
            else:
                self.status = "Em transporte"
        else:
            self.status = "Em processamento"
        
        return etapas
    
    def atualizar_status(self):
        # Simular possível atualização de status
        if random.random() > 0.8 and self.status != "Entregue":
            if self.status == "Em processamento" and not self.data_envio:
                self.data_envio = datetime.now() - timedelta(days=random.randint(0, 2))
                self.codigo_rastreio = f"TR{random.randint(100000000, 999999999)}BR"
                self.etapas.append(("Pedido enviado", self.data_envio))
                self.status = "Em transporte"
            elif self.status == "Em transporte" and not self.data_entrega:
                if random.random() > 0.6:
                    self.data_entrega = datetime.now() + timedelta(days=random.randint(1, 3))
                    self.etapas.append(("Saiu para entrega", datetime.now()))
        
        self.etapas = self._gerar_etapas()  # Regenerar para manter consistência

class ChatbotAliExpress:
    def __init__(self):
        self.pedidos = {}  # Simulando "banco de dados" em memória
        self.respostas_padrao = {
            "saudacao": "Olá! Sou o assistente virtual de rastreamento de pedidos. Como posso ajudar?",
            "ajuda": "Você pode me perguntar sobre:\n- Status do pedido\n- Código de rastreio\n- Tempo de entrega\n- Informações do produto",
            "despedida": "Obrigado por usar nosso serviço! Volte sempre.",
            "sem_pedido": "Não encontrei nenhum pedido associado. Por favor, verifique o número do pedido.",
            "default": "Desculpe, não entendi. Você pode reformular sua pergunta?"
        }
    
    def criar_pedido_simulado(self):
        id_pedido = f"AE{random.randint(100000000, 999999999)}"
        self.pedidos[id_pedido] = PedidoSimulado(id_pedido)
        return id_pedido
    
    def responder(self, mensagem, id_pedido=None):
        mensagem = mensagem.lower().strip()
        
        # Respostas padrão
        if any(palavra in mensagem for palavra in ["olá", "oi", "ola", "bom dia"]):
            return self.respostas_padrao["saudacao"]
        
        if any(palavra in mensagem for palavra in ["ajuda", "help", "socorro"]):
            return self.respostas_padrao["ajuda"]
        
        if any(palavra in mensagem for palavra in ["tchau", "adeus", "até logo"]):
            return self.respostas_padrao["despedida"]
        
        # Consultas sobre pedidos
        if not id_pedido:
            return "Por favor, forneça o número do pedido para que eu possa ajudar."
        
        pedido = self.pedidos.get(id_pedido)
        if not pedido:
            return self.respostas_padrao["sem_pedido"]
        
        pedido.atualizar_status()  # Simular possível atualização
        
        if any(palavra in mensagem for palavra in ["status", "situação", "andamento"]):
            return self._gerar_resposta_status(pedido)
        
        if any(palavra in mensagem for palavra in ["rastreio", "código", "rastreamento"]):
            return self._gerar_resposta_rastreio(pedido)
        
        if any(palavra in mensagem for palavra in ["produto", "item", "comprou"]):
            return f"Você comprou: {pedido.produto}"
        
        if any(palavra in mensagem for palavra in ["tempo", "entrega", "chegar", "previsão"]):
            return self._gerar_resposta_previsao(pedido)
        
        return self.respostas_padrao["default"]
    
    def _gerar_resposta_status(self, pedido):
        resposta = f"Status do pedido {pedido.id_pedido}: {pedido.status}\n\nHistórico:\n"
        for etapa, data in pedido.etapas:
            resposta += f"- {etapa} em {data.strftime('%d/%m/%Y %H:%M')}\n"
        
        if pedido.status == "Em processamento":
            resposta += "\nSeu pedido está sendo preparado para envio."
        elif pedido.status == "Em transporte":
            resposta += "\nSeu pedido está a caminho!"
        elif pedido.status == "Entregue":
            resposta += "\nSeu pedido foi entregue com sucesso!"
        
        return resposta
    
    def _gerar_resposta_rastreio(self, pedido):
        if pedido.codigo_rastreio:
            return (f"Código de rastreio: {pedido.codigo_rastreio}\n"
                    f"Você pode rastrear no site dos Correios: https://www.correios.com.br")
        else:
            return "Seu pedido ainda não foi enviado. O código de rastreio será disponibilizado quando o pedido for despachado."
    
    def _gerar_resposta_previsao(self, pedido):
        if pedido.status == "Entregue":
            return "Seu pedido já foi entregue!"
        
        if pedido.data_entrega:
            dias_restantes = (pedido.data_entrega - datetime.now()).days
            return f"Previsão de entrega: {pedido.data_entrega.strftime('%d/%m/%Y')} ({dias_restantes} dias restantes)"
        
        if pedido.data_envio:
            previsao = pedido.data_envio + timedelta(days=random.randint(15, 30))
            dias_restantes = (previsao - datetime.now()).days
            return f"Previsão estimada de entrega: {previsao.strftime('%d/%m/%Y')} ({dias_restantes} dias restantes)"
        
        return "Seu pedido ainda está em processamento. A previsão de entrega será disponibilizada após o envio."

# Função para simular interação
def simular_interacao():
    bot = ChatbotAliExpress()
    
    # Criar alguns pedidos simulados
    pedido1 = bot.criar_pedido_simulado()
    pedido2 = bot.criar_pedido_simulado()
    
    print("=== Simulador de Chatbot AliExpress ===")
    print("Pedidos simulados criados:")
    print(f"- Pedido 1: {pedido1}")
    print(f"- Pedido 2: {pedido2}")
    print("\nDigite 'sair' para encerrar\n")
    
    while True:
        pedido = input("Digite o número do pedido (ou deixe em branco para criar um novo): ").strip()
        
        if pedido.lower() == 'sair':
            break
        
        if not pedido:
            novo_pedido = bot.criar_pedido_simulado()
            print(f"Novo pedido criado: {novo_pedido}")
            pedido = novo_pedido
        
        while True:
            mensagem = input(f"\nVocê está consultando o pedido {pedido}. O que gostaria de saber? ").strip()
            
            if mensagem.lower() == 'sair':
                break
            if mensagem.lower() == 'voltar':
                print("Retornando à seleção de pedidos...")
                break
            
            resposta = bot.responder(mensagem, pedido)
            print("\nAssistente:", resposta)

if __name__ == "__main__":
    simular_interacao()