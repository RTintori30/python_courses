from tkinter import *
from tkinter import ttk
import sqlite3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser


janela = Tk()

class Relatorio():
    def print_cliente(self):
        webbrowser.open('cliente.pdf')
    
    def gerar_relatorio(self):
        self.cliente = canvas.Canvas("cliente.pdf") # Cria o arquivo PDF

        self.codigo_relatorio = self.codigo_entry.get()
        self.nome_relatorio = self.nome_entry.get()
        self.telefone_relatorio = self.telefone_entry.get()
        self.cidade_relatorio = self.cidade_entry.get()

        self.cliente.setFont('Helvetica-Bold', 24) # Tipo e Tamanho da Fonte do Título
        self.cliente.drawString(200, 790, 'Ficha do Cliente') # Posição e Nome do Título

        self.cliente.setFont('Helvetica-Bold', 12)
        self.cliente.drawString(50, 700, 'Codigo: ' + self.codigo_relatorio)
        self.cliente.drawString(50, 680, 'Nome: ' + self.nome_relatorio)
        self.cliente.drawString(50, 660, 'Telefone: ' + self.telefone_relatorio)
        self.cliente.drawString(50, 640, 'Cidade: ' + self.cidade_relatorio)

        self.cliente.showPage()
        self.cliente.save()
        self.print_cliente()

class Functions():
    def limpar_tela(self):
        
        self.codigo_entry.delete(first=0, last=END)
        self.nome_entry.delete(first=0, last=END)
        self.telefone_entry.delete(first=0, last=END)
        self.cidade_entry.delete(first=0, last=END)

    def conect_bd(self): # Conecta no Banco de Dados
        self.conn = sqlite3.connect('clientes.db')
        self.cursor = self.conn.cursor()
    
    def desconect_bd(self): # Desconecta do Banco de Dados
        self.conn.close()

    def montar_tabelas(self): # Monta as Tabelas
        self.conect_bd()
        
        # Criação da Tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY,
                nome_clientes CHAR(40) NOT NULL,
                telefone INTEGER(20),
                cidade CHAR(40)                
            );
        """)
        self.conn.commit(); print ("Banco de Dados criado com sucesso")
        
        self.desconect_bd()

    def variaveis(self):
        
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.telefone = self.telefone_entry.get()
        self.cidade = self.cidade_entry.get()
    
    def add_client(self): # Adiciona os dados ao Banco de Dados
        
        self.variaveis()
        self.conect_bd() # Para conectar ao Banco de Dados SQL
        
        self.cursor.execute("""INSERT INTO clientes (nome_clientes, telefone, cidade) 
                            VALUES (?, ?, ?)""", (self.nome, self.telefone, self.cidade))
        self.conn.commit()
        
        self.desconect_bd()
        self.select_lista()
        self.limpar_tela()

    def select_lista(self): # Seleciona os dados da Tabela
        
        self.lista_client.delete(*self.lista_client.get_children())
        self.conect_bd()
        lista = self.cursor.execute ("""SELECT cod, nome_clientes, telefone, cidade FROM clientes 
                                     ORDER BY cod ASC; """)
        
        for i in lista:
            self.lista_client.insert("", END, values=i)
        self.desconect_bd()
        
    def on_double_click(self, event): # Seleciona os dados da Treeview, para serem alterados
        
        self.limpar_tela()
        self.lista_client.selection()

        for n in self.lista_client.selection():
            col1, col2, col3, col4 = self.lista_client.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.telefone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)
    
    def delete_client(self): # Deleta os dados do cliente na tabela
        
        self.variaveis()
        self.conect_bd()
        
        self.cursor.execute ("""DELETE FROM clientes WHERE cod = ?""", (self.codigo))
        self.conn.commit()
        
        self.desconect_bd()
        self.limpar_tela()
        self.select_lista()

    def update_client(self): # Atualiza os dados do cliente na tabela

        self.variaveis()
        self.conect_bd()

        self.cursor.execute ("""UPDATE clientes SET nome_clientes = ?, telefone = ?, cidade = ?
                             WHERE cod = ?""", (self.nome, self.telefone, self.cidade, self.codigo))
        self.conn.commit()

        self.desconect_bd()
        self.limpar_tela()
        self.select_lista()

class Application(Functions, Relatorio):
    
    def __init__(self):
        self.janela = janela
        self.tela()
        self.frames_de_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montar_tabelas()
        self.select_lista()
        self.Menus()
        janela.mainloop() 
    
    def tela(self):
        self.janela.title('Cadastro dos Clientes')
        self.janela.configure(background='#1e3743')
        self.janela.geometry ('700x500')
        self.janela.resizable (True, True)
        self.janela.maxsize (width=900 ,height=700)
        self.janela.minsize (width=400 ,height=300)

    def frames_de_tela (self):
        
        # Criação do Frame Superior
        self.frame_1 = Frame(self.janela, bd= 4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=3)
        self.frame_1.place (relx = 0.02, rely = 0.03, relwidth=0.96, relheight=0.46)

        # Criação do Frame Inferior
        self.frame_2 = Frame(self.janela, bd= 4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=3)
        self.frame_2.place (relx = 0.02, rely = 0.51, relwidth=0.96, relheight=0.46)

    def widgets_frame1 (self):
        # Criando Botão de Limpar
        self.bt_limpar = Button(self.frame_1, text= 'Limpar', border=2, background= '#107db2', foreground= 'white', font= ('verdana', 8, 'bold'), command = self.limpar_tela)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.09, relheight=0.12)

        # Criando Botão de Buscar
        self.bt_buscar = Button(self.frame_1, text= 'Buscar', border=2, background= '#107db2', foreground= 'white', font= ('verdana', 8, 'bold'))
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.09, relheight=0.12)

        # Criando Botão de Novo
        self.bt_novo = Button(self.frame_1, text= 'Novo', border=2, background= '#107db2', foreground= 'white', font= ('verdana', 8, 'bold'), command = self.add_client)
        self.bt_novo.place(relx=0.65, rely=0.1, relwidth=0.09, relheight=0.12)

        # Criando Botão de Alterar
        self.bt_alterar = Button(self.frame_1, text= 'Alterar', border=2, background= '#107db2', foreground= 'white', font= ('verdana', 8, 'bold'), command= self.update_client)
        self.bt_alterar.place(relx=0.75, rely=0.1, relwidth=0.09, relheight=0.12)

        # Criando Botão de Apagar
        self.bt_apagar = Button(self.frame_1, text= 'Apagar', border=2, background= '#107db2', foreground= 'white', font= ('verdana', 8, 'bold'), command = self.delete_client)
        self.bt_apagar.place(relx=0.85, rely=0.1, relwidth=0.09, relheight=0.12)

        
        # Criando Label e Entrada de Código
        self.lb_codigo = Label(self.frame_1, text= 'Código', background= '#dfe3ee', foreground='#107db2', font= ('verdana', 8, 'bold'))
        self.lb_codigo.place(relx=0.05, rely=0.01, relwidth=0.09, relheight=0.10)

        self.codigo_entry = Entry(self.frame_1, font= ('verdana', 8))
        self.codigo_entry.place(relx=0.05, rely=0.12, relwidth=0.09, relheight=0.10)

        # Criando Label e Entrada de Nome
        self.lb_nome = Label(self.frame_1, text= 'Nome', background= '#dfe3ee', foreground='#107db2', font= ('verdana', 8, 'bold'))
        self.lb_nome.place(relx=0.05, rely=0.35, relwidth=0.09, relheight=0.10)

        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.8, relheight=0.10)

        # Criando Label e Entrada do Telefone
        self.lb_telefone = Label(self.frame_1, text= 'Telefone', background= '#dfe3ee', foreground='#107db2', font= ('verdana', 8, 'bold'))
        self.lb_telefone.place(relx=0.05, rely=0.65, relwidth=0.09, relheight=0.10)

        self.telefone_entry = Entry(self.frame_1, font= ('verdana', 8))
        self.telefone_entry.place(relx=0.05, rely=0.75, relwidth=0.16, relheight=0.10)

        # Criando Label e Entrada da Cidade
        self.lb_cidade = Label(self.frame_1, text= 'Cidade', background= '#dfe3ee', foreground='#107db2', font= ('verdana', 8, 'bold'))
        self.lb_cidade.place(relx=0.40, rely=0.65, relwidth=0.09, relheight=0.10)

        self.cidade_entry = Entry(self.frame_1)
        self.cidade_entry.place(relx=0.40, rely=0.75, relwidth=0.45, relheight=0.10)
    
    def lista_frame2 (self):
        
        # Criação da Treeview
        self.lista_client = ttk.Treeview(self.frame_2, height=3, columns=('col1', 'col2', 'col3', 'col4'))
        self.lista_client.heading('#0', text='')
        self.lista_client.heading('#1', text='Código')
        self.lista_client.heading('#2', text='Nome')
        self.lista_client.heading('#3', text='Telefone')
        self.lista_client.heading('#4', text='Cidade')
        
        # Definição das colunas
        self.lista_client.column('#0', width=1)
        self.lista_client.column('#1', width=50)
        self.lista_client.column('#2', width=200)
        self.lista_client.column('#3', width=125)
        self.lista_client.column('#4', width=125)

        # Posicionamento da Treeview
        self.lista_client.place(relx=0.01, rely=0.01, relwidth=0.96, relheight=0.98)

        # Criação da barra de rolagem
        self.scroolista = Scrollbar(self.frame_2, orient='vertical')
        self.lista_client.configure(yscroll=self.scroolista.set)
        self.scroolista.place(relx=0.97, rely=0.01, relwidth=0.03, relheight=0.98)

        self.lista_client.bind ('<Double-1>', self.on_double_click) # Ao Clicar duas vezes, chama a função "on_double_click"

    def Menus (self):
        menubar = Menu(self.janela) # Criando o Menu
        self.janela.config(menu=menubar)
        filemenu = Menu(menubar) # Primeiro Menu
        filemenu2 = Menu(menubar) # Segundo Menu

        def quit ():
            self.janela.destroy()

        # Criando itens e comandos do primeiro menu
        menubar.add_cascade(label='Opções', menu=filemenu)
        filemenu.add_command(label='Sair', command=quit)
        filemenu.add_command(label='Limpar Cliente', command=self.limpar_tela)

        # Criando itens e comandos do segundo menu
        menubar.add_cascade(label='Relatórios', menu=filemenu2)
        filemenu2.add_command(label='Ficha do Cliente', command=self.gerar_relatorio)
        

        

Application()