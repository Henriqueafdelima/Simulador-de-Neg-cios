from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget, QLineEdit, QPushButton, QStackedWidget
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import random


class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.preco_produto = 0
        self.quant_vendedores = 0
        self.quant_produto = 0
        self.investimento_publicidade = 0
        self.salario_vendedor = 2000  # Salário por vendedor
        self.aluguel_espaco = 5000  # Aluguel do espaço
        self.custo_producao = 2000  # Custo de produção por unidade
        self.custo_estocagem = 2  # Custo de estocagem por unidade não vendida
        self.faturamento = 0
        self.quantidade_vendida = 0

    def calcular_faturamento(self, media_preco_produto, media_vendedores, media_publicidade, sazonalidade_media):
        # Fator preço
        fator_preco = 1 - abs(self.preco_produto - media_preco_produto) / media_preco_produto
        fator_preco = max(0, fator_preco)  # Garantir que o fator não seja negativo

        # Fator vendedores
        fator_vendedores = self.quant_vendedores / media_vendedores

        # Fator publicidade
        fator_publicidade = self.investimento_publicidade / media_publicidade

        # Calcular faturamento bruto
        self.faturamento = fator_preco * fator_vendedores * fator_publicidade * sazonalidade_media

        # Calcular quantidade vendida
        self.calcular_quantidade_vendida()

        # Calcular custos
        custo_salarios = self.salario_vendedor * self.quant_vendedores
        custo_aluguel = self.aluguel_espaco
        custo_producao = self.custo_producao * self.quant_produto
        custo_estocagem = self.custo_estocagem * max(0, self.quant_produto - self.quantidade_vendida)

        custos_totais = custo_salarios + custo_aluguel + custo_producao + custo_estocagem

        # Subtrair os custos do faturamento
        self.faturamento -= custos_totais

    def calcular_quantidade_vendida(self):
        if self.preco_produto > 0:
            self.quantidade_vendida = self.faturamento / self.preco_produto
        else:
            self.quantidade_vendida = 0


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jogo de Simulação de Empresa")
        self.setGeometry(100, 100, 1920, 1080)

        # QStackedWidget para gerenciar páginas
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Criar as páginas
        self.pagina_jogo = QWidget(self)
        self.pagina_ranking = QWidget(self)
        self.pagina_fim_jogo = QWidget(self)

        # Adicionar páginas ao QStackedWidget
        self.stacked_widget.addWidget(self.pagina_jogo)
        self.stacked_widget.addWidget(self.pagina_ranking)
        self.stacked_widget.addWidget(self.pagina_fim_jogo)

        # Inicializar as páginas
        self.criar_tela_jogo()
        self.criar_tela_ranking("Ranking-rodada-1.png")
        self.criar_tela_fim_jogo("Fim.png")

        # Lista de jogadores e variáveis
        self.jogadores = []
        self.rodada_atual = 1
        self.sazonalidades = [250000.0, 350000.0, 100000.0, 1000000.0]

    def criar_tela_jogo(self):
        # Fundo da tela de jogo
        self.background_label = QLabel(self.pagina_jogo)
        self.pixmap = QPixmap("Monitor.png")
        self.background_label.setPixmap(self.pixmap)
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        # Campos para os jogadores
        self.line_edits_nome = []
        self.line_edits_produto = []
        self.line_edits_vendedores = []
        self.line_edits_publicidade = []

        # Criar campos de entrada
        self.criar_campos_jogador(1, 350, 250)
        self.criar_campos_jogador(2, 1250, 250)
        self.criar_campos_jogador(3, 350, 600)
        self.criar_campos_jogador(4, 1250, 600)

        # Botão de iniciar jogo
        self.submit_button = QPushButton("Iniciar Jogo", self.pagina_jogo)
        self.submit_button.setFixedWidth(300)
        self.submit_button.setFixedHeight(40)
        self.submit_button.move(820, 520)
        self.submit_button.clicked.connect(self.iniciar_jogo)

    def criar_tela_ranking(self, background_image):
        # Fundo da tela de ranking
        self.background_label_ranking = QLabel(self.pagina_ranking)
        self.pixmap_ranking = QPixmap(background_image)
        self.background_label_ranking.setPixmap(self.pixmap_ranking)
        self.background_label_ranking.setScaledContents(True)
        self.background_label_ranking.setGeometry(0, 0, self.width(), self.height())

        # Texto do NPC
        self.dialogo_npc = QLabel(self.pagina_ranking)
        self.dialogo_npc.setWordWrap(True)
        self.dialogo_npc.setAlignment(Qt.AlignLeft)
        self.dialogo_npc.setGeometry(100, 820, 1800, 300)
        self.dialogo_npc.setStyleSheet("""
            color: white;
            font-size: 50px;
            font-family: Arial;
            background-color: rgba(0, 0, 0, 0);
            border-radius: 0px;
            padding: 0px;
        """)

        # Caixa de ranking (inicialmente oculta)
        self.ranking_label = QLabel(self.pagina_ranking)
        self.ranking_label.setGeometry(300, 320, 1300, 500)
        self.ranking_label.setAlignment(Qt.AlignCenter)
        self.ranking_label.setStyleSheet("""
            color: black;
            font-size: 50px;
            font-family: Verdana;
        """)
        self.ranking_label.hide()

        # Botão continuar/voltar
        self.continuar_button = QPushButton("Continuar", self.pagina_ranking)
        self.continuar_button.setFixedWidth(300)
        self.continuar_button.setFixedHeight(40)
        self.continuar_button.move(820, 700)
        self.continuar_button.clicked.connect(self.alternar_ranking)

        # Estado de exibição (inicia com o NPC)
        self.mostrando_dialogo = True

    def criar_tela_fim_jogo(self, background_image):
        # Fundo da tela de fim de jogo
        self.background_label_fim_jogo = QLabel(self.pagina_fim_jogo)
        self.pixmap_fim_jogo = QPixmap(background_image)
        self.background_label_fim_jogo.setPixmap(self.pixmap_fim_jogo)
        self.background_label_fim_jogo.setScaledContents(True)
        self.background_label_fim_jogo.setGeometry(0, 0, self.width(), self.height())

        # Botão sair
        self.sair_button = QPushButton("Sair do Jogo", self.pagina_fim_jogo)
        self.sair_button.setFixedWidth(300)
        self.sair_button.setFixedHeight(40)
        self.sair_button.move(820, 700)
        self.sair_button.clicked.connect(self.sair_jogo)

    def criar_campos_jogador(self, jogador_num, pos_x, pos_y):
        line_edit_nome = QLineEdit(self.pagina_jogo)
        line_edit_nome.setPlaceholderText(f"Nome da empresa - Jogador {jogador_num}")
        line_edit_nome.setFixedWidth(300)
        line_edit_nome.setFixedHeight(40)
        line_edit_nome.move(pos_x, pos_y)
        self.line_edits_nome.append(line_edit_nome)

        line_edit_produto = QLineEdit(self.pagina_jogo)
        line_edit_produto.setPlaceholderText(f"Preço do Produto - Jogador {jogador_num}")
        line_edit_produto.setFixedWidth(300)
        line_edit_produto.setFixedHeight(40)
        line_edit_produto.move(pos_x, pos_y + 60)
        self.line_edits_produto.append(line_edit_produto)

        line_edit_vendedores = QLineEdit(self.pagina_jogo)
        line_edit_vendedores.setPlaceholderText(f"Vendedores - Jogador {jogador_num}")
        line_edit_vendedores.setFixedWidth(300)
        line_edit_vendedores.setFixedHeight(40)
        line_edit_vendedores.move(pos_x, pos_y + 120)
        self.line_edits_vendedores.append(line_edit_vendedores)

        line_edit_publicidade = QLineEdit(self.pagina_jogo)
        line_edit_publicidade.setPlaceholderText(f"Publicidade - Jogador {jogador_num}")
        line_edit_publicidade.setFixedWidth(300)
        line_edit_publicidade.setFixedHeight(40)
        line_edit_publicidade.move(pos_x, pos_y + 180)
        self.line_edits_publicidade.append(line_edit_publicidade)

    def iniciar_jogo(self):
        self.jogadores.clear()  # Limpar a lista de jogadores antes de iniciar o jogo
        for i in range(4):
            nome = self.line_edits_nome[i].text()
            jogador = Jogador(nome)
            self.jogadores.append(jogador)

        self.jogar_rodadas()

    def jogar_rodadas(self):
        if self.rodada_atual <= 4:
            sazonalidade = random.choice(self.sazonalidades)
            sazonalidade_media = sazonalidade / 4

            total_preco_produto = 0
            total_vendedores = 0
            total_publicidade = 0
            num_jogadores = len(self.jogadores)

            for i in range(num_jogadores):
                jogador = self.jogadores[i]
                if self.line_edits_produto[i].text():
                    jogador.preco_produto = float(self.line_edits_produto[i].text())
                    jogador.quant_vendedores = int(self.line_edits_vendedores[i].text())
                    jogador.investimento_publicidade = float(self.line_edits_publicidade[i].text())
                    total_preco_produto += jogador.preco_produto
                    total_vendedores += jogador.quant_vendedores
                    total_publicidade += jogador.investimento_publicidade

            media_preco_produto = total_preco_produto / num_jogadores
            media_vendedores = total_vendedores / num_jogadores
            media_publicidade = total_publicidade / num_jogadores

            for jogador in self.jogadores:
                jogador.calcular_faturamento(media_preco_produto, media_vendedores, media_publicidade, sazonalidade_media)

            # Atualizar o fundo da tela de ranking com base na rodada atual
            background_image = f"Ranking-rodada-{self.rodada_atual}.png"
            self.criar_tela_ranking(background_image)

            self.dialogo_npc.setText("Gatinhos e gatinhas, chegou a hora de ver o ranking da rodada!")
            self.stacked_widget.setCurrentWidget(self.pagina_ranking)

            self.rodada_atual += 1

    def alternar_ranking(self):
        if self.mostrando_dialogo:
            # Ocultar o diálogo do NPC e exibir o ranking
            self.dialogo_npc.hide()
            self.ranking_label.show()
            self.continuar_button.setText("Próximo")
            self.mostrando_dialogo = False

            # Atualizar o ranking
            ranking_text = "\n".join(
                [f"{jogador.nome}: R$ {jogador.faturamento:,.2f}" for jogador in sorted(self.jogadores, key=lambda x: x.faturamento, reverse=True)]
            )
            self.ranking_label.setText(ranking_text)
        elif not self.mostrando_dialogo and self.continuar_button.text() == "Próximo":
            # Encontrar o jogador com o maior faturamento
            jogador_top = max(self.jogadores, key=lambda x: x.faturamento)
            
            # Mostrar o segundo diálogo do NPC
            self.dialogo_npc.setText(f"Parabéns {jogador_top.nome}, você está muito próximo de se tornar um empreendedor de suuuuuuucessoo! Mas ainda temos muito trabalho pela frente, vamos ver como vocês se saem na próxima rodada!")
            self.dialogo_npc.show()
            self.continuar_button.setText("Voltar ao Jogo")
        else:
            # Verificar se deve ir para a próxima rodada ou finalizar o jogo
            if self.rodada_atual <= 4:
                self.voltar_ao_jogo()
            else:
                self.stacked_widget.setCurrentWidget(self.pagina_fim_jogo)

    def voltar_ao_jogo(self):
        self.stacked_widget.setCurrentWidget(self.pagina_jogo)

    def sair_jogo(self):
        QApplication.instance().quit()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()