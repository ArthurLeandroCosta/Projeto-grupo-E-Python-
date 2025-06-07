import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
from datetime import datetime

# Arquivos de dados
USUARIOS_FILE = "usuarios.txt"
ANIMAIS_FILE = "animais.txt"
ADOCAO_FILE = "adocoes.txt"

# Chave de segurança para cadastro de administrador
CHAVE_ADMIN = "@dM1n2025n0Vo"

# Funções para manipular arquivos
def carregar_dados(arquivo):
    dados = []
    if os.path.exists(arquivo):
        with open(arquivo, 'r') as f:
            for linha in f:
                if linha.strip():
                    try:
                        dados.append(eval(linha.strip()))
                    except:
                        continue
    return dados

def salvar_dados(arquivo, dados):
    with open(arquivo, 'w') as f:
        for item in dados:
            f.write(str(item) + '\n')

# Classe principal da aplicação
class AdotaPetzApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AdotaPetz - Sistema de Adoção")
        self.root.geometry("1000x700")
        self.usuario_logado = None
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#006400')
        
        # Container principal
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.mostrar_tela_inicial()
    
    def limpar_tela(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def mostrar_tela_inicial(self):
        self.limpar_tela()
        
        # Logo e título
        ttk.Label(self.main_frame, text="🐾 AdotaPetz 🐾", style='Title.TLabel').pack(pady=20)
        ttk.Label(self.main_frame, text="Sistema de Adoção e Acompanhamento de Pets").pack(pady=10)
        
        # Botões
        ttk.Button(self.main_frame, text="Cadastrar Usuário", command=self.mostrar_tela_cadastro).pack(pady=10, ipadx=20, ipady=5)
        ttk.Button(self.main_frame, text="Login", command=self.mostrar_tela_login).pack(pady=10, ipadx=20, ipady=5)
        ttk.Button(self.main_frame, text="Sair", command=self.root.quit).pack(pady=10, ipadx=20, ipady=5)
    
    def mostrar_tela_cadastro(self):
        self.limpar_tela()
        
        ttk.Label(self.main_frame, text="Cadastro de Usuário", style='Title.TLabel').pack(pady=20)
        
        # Formulário
        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(pady=10)
        
        ttk.Label(form_frame, text="Email:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.email_entry = ttk.Entry(form_frame, width=30)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Senha:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.senha_entry = ttk.Entry(form_frame, width=30, show="*")
        self.senha_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Nome completo:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.nome_entry = ttk.Entry(form_frame, width=30)
        self.nome_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Telefone:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.telefone_entry = ttk.Entry(form_frame, width=30)
        self.telefone_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Tipo de usuário:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.tipo_usuario_var = tk.StringVar(value="comum")
        ttk.Radiobutton(form_frame, text="Usuário Comum", variable=self.tipo_usuario_var, value="comum").grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Radiobutton(form_frame, text="Administrador", variable=self.tipo_usuario_var, value="admin").grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Botões
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Cadastrar", command=self.cadastrar_usuario).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Voltar", command=self.mostrar_tela_inicial).pack(side=tk.LEFT, padx=10)
    
    def cadastrar_usuario(self):
        email = self.email_entry.get()
        senha = self.senha_entry.get()
        nome = self.nome_entry.get()
        telefone = self.telefone_entry.get()
        tipo_usuario = self.tipo_usuario_var.get()
        
        if not all([email, senha, nome, telefone]):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return
        
        # Verificar chave de segurança se for admin
        if tipo_usuario == "admin":
            tentativas = 3
            chave_correta = False
            
            while tentativas > 0:
                chave = simpledialog.askstring("Chave de Segurança", 
                                             f"Digite a chave de segurança para administrador ({tentativas} tentativas restantes):", 
                                             show='*')
                
                if chave == CHAVE_ADMIN:
                    chave_correta = True
                    break
                    
                tentativas -= 1
                if tentativas > 0:
                    messagebox.showerror("Erro", f"Chave de segurança incorreta! Você tem {tentativas} tentativa(s) restante(s).")
            
            if not chave_correta:
                messagebox.showerror("Erro", "Número máximo de tentativas excedido. Cadastro cancelado.")
                return
        
        usuarios = carregar_dados(USUARIOS_FILE)
        if any(isinstance(u, dict) and u.get('email') == email for u in usuarios):
            messagebox.showerror("Erro", "Email já cadastrado!")
            return
        
        novo_usuario = {
            'email': email,
            'senha': senha,
            'nome': nome,
            'telefone': telefone,
            'tipo': tipo_usuario
        }
        
        usuarios.append(novo_usuario)
        salvar_dados(USUARIOS_FILE, usuarios)
        
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        self.mostrar_tela_inicial()
    
    def mostrar_tela_login(self):
        self.limpar_tela()
        
        ttk.Label(self.main_frame, text="Login", style='Title.TLabel').pack(pady=20)
        
        # Formulário
        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(pady=10)
        
        ttk.Label(form_frame, text="Email:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.login_email_entry = ttk.Entry(form_frame, width=30)
        self.login_email_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Senha:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.login_senha_entry = ttk.Entry(form_frame, width=30, show="*")
        self.login_senha_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Botões
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Entrar", command=self.fazer_login).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Voltar", command=self.mostrar_tela_inicial).pack(side=tk.LEFT, padx=10)
    
    def fazer_login(self):
        email = self.login_email_entry.get()
        senha = self.login_senha_entry.get()
        
        usuarios = carregar_dados(USUARIOS_FILE)
        for usuario in usuarios:
            if isinstance(usuario, dict) and usuario.get('email') == email and usuario.get('senha') == senha:
                self.usuario_logado = usuario
                self.mostrar_menu_principal()
                return
        
        messagebox.showerror("Erro", "Email ou senha incorretos!")
    
    def mostrar_menu_principal(self):
        self.limpar_tela()
        
        ttk.Label(self.main_frame, text=f"Bem-vindo, {self.usuario_logado.get('nome', 'Usuário')}", style='Title.TLabel').pack(pady=20)
        
        # Botões do menu
        if self.usuario_logado.get('tipo') == 'admin':
            ttk.Button(self.main_frame, text="Cadastrar Animal", command=self.mostrar_tela_cadastro_animal).pack(pady=10, ipadx=20, ipady=5)
            ttk.Button(self.main_frame, text="Gerenciar Usuários", command=self.mostrar_gerenciar_usuarios).pack(pady=10, ipadx=20, ipady=5)
        
        ttk.Button(self.main_frame, text="Listar Animais Disponíveis", command=self.mostrar_lista_animais).pack(pady=10, ipadx=20, ipady=5)
        ttk.Button(self.main_frame, text="Adotar Animal", command=self.mostrar_tela_adocao).pack(pady=10, ipadx=20, ipady=5)
        ttk.Button(self.main_frame, text="Acompanhamento Pós-Adoção", command=self.mostrar_acompanhamento).pack(pady=10, ipadx=20, ipady=5)
        ttk.Button(self.main_frame, text="Sair", command=self.fazer_logout).pack(pady=20, ipadx=20, ipady=5)
    
    def mostrar_gerenciar_usuarios(self):
        if self.usuario_logado.get('tipo') != 'admin':
            messagebox.showerror("Acesso negado", "Apenas administradores podem gerenciar usuários!")
            return
            
        self.limpar_tela()
        
        ttk.Label(self.main_frame, text="Gerenciar Usuários", style='Title.TLabel').pack(pady=20)
        
        usuarios = carregar_dados(USUARIOS_FILE)
        
        if not usuarios:
            ttk.Label(self.main_frame, text="Nenhum usuário cadastrado.").pack(pady=20)
        else:
            # Criar Treeview (tabela)
            tree_frame = ttk.Frame(self.main_frame)
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            scrollbar = ttk.Scrollbar(tree_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            self.tree_usuarios = ttk.Treeview(tree_frame, 
                                           columns=('Email', 'Nome', 'Telefone', 'Tipo'), 
                                           show='headings', 
                                           yscrollcommand=scrollbar.set)
            
            # Configurar colunas
            self.tree_usuarios.column('Email', width=200, anchor=tk.W)
            self.tree_usuarios.column('Nome', width=200, anchor=tk.W)
            self.tree_usuarios.column('Telefone', width=150, anchor=tk.W)
            self.tree_usuarios.column('Tipo', width=100, anchor=tk.W)
            
            # Cabeçalhos
            self.tree_usuarios.heading('Email', text='Email')
            self.tree_usuarios.heading('Nome', text='Nome')
            self.tree_usuarios.heading('Telefone', text='Telefone')
            self.tree_usuarios.heading('Tipo', text='Tipo')
            
            # Adicionar dados
            for usuario in usuarios:
                if isinstance(usuario, dict):
                    self.tree_usuarios.insert('', tk.END, values=(
                        usuario.get('email', ''),
                        usuario.get('nome', ''),
                        usuario.get('telefone', ''),
                        usuario.get('tipo', '')
                    ), tags=(usuario.get('tipo', ''),))
            
            self.tree_usuarios.pack(fill=tk.BOTH, expand=True)
            scrollbar.config(command=self.tree_usuarios.yview)
            
            # Botão para alterar tipo de usuário
            ttk.Button(self.main_frame, text="Alterar Tipo de Usuário", command=self.alterar_tipo_usuario).pack(pady=10)
        
        ttk.Button(self.main_frame, text="Voltar", command=self.mostrar_menu_principal).pack(pady=20)
    
    def alterar_tipo_usuario(self):
        selected = self.tree_usuarios.focus()
        if not selected:
            messagebox.showerror("Erro", "Selecione um usuário na tabela!")
            return
        
        item = self.tree_usuarios.item(selected)
        email = item['values'][0]
        
        if email == self.usuario_logado.get('email'):
            messagebox.showerror("Erro", "Você não pode alterar seu próprio tipo de usuário!")
            return
        
        usuarios = carregar_dados(USUARIOS_FILE)
        usuario = next((u for u in usuarios if isinstance(u, dict) and u.get('email') == email), None)
        
        if not usuario:
            messagebox.showerror("Erro", "Usuário não encontrado!")
            return
        
        novo_tipo = "admin" if usuario.get('tipo') == "comum" else "comum"
        
        # Se for para tornar admin, pedir chave de segurança com 3 tentativas
        if novo_tipo == "admin":
            tentativas = 3
            chave_correta = False
            
            while tentativas > 0:
                chave = simpledialog.askstring("Chave de Segurança", 
                                             f"Digite a chave de segurança para tornar administrador ({tentativas} tentativas restantes):", 
                                             show='*')
                
                if chave == CHAVE_ADMIN:
                    chave_correta = True
                    break
                    
                tentativas -= 1
                if tentativas > 0:
                    messagebox.showerror("Erro", f"Chave de segurança incorreta! Você tem {tentativas} tentativa(s) restante(s).")
            
            if not chave_correta:
                messagebox.showerror("Erro", "Número máximo de tentativas excedido. Operação cancelada.")
                return
        
        usuario['tipo'] = novo_tipo
        salvar_dados(USUARIOS_FILE, usuarios)
        
        # Atualizar a exibição
        self.tree_usuarios.item(selected, values=(
            usuario.get('email', ''),
            usuario.get('nome', ''),
            usuario.get('telefone', ''),
            usuario.get('tipo', '')
        ))
        
        messagebox.showinfo("Sucesso", f"Tipo de usuário alterado para {novo_tipo}!")
        self.mostrar_gerenciar_usuarios()
    
    def mostrar_tela_cadastro_animal(self):
        if self.usuario_logado.get('tipo') != 'admin':
            messagebox.showerror("Acesso negado", "Apenas administradores podem cadastrar animais!")
            return
            
        self.limpar_tela()
        
        ttk.Label(self.main_frame, text="Cadastro de Animal", style='Title.TLabel').pack(pady=20)
        
        # Formulário
        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(pady=10)
        
        ttk.Label(form_frame, text="Tipo (cachorro/gato):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.tipo_animal = tk.StringVar()
        ttk.Combobox(form_frame, textvariable=self.tipo_animal, values=["cachorro", "gato"], width=27).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Nome:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.nome_animal_entry = ttk.Entry(form_frame, width=30)
        self.nome_animal_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Idade (anos):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.idade_animal_entry = ttk.Entry(form_frame, width=30)
        self.idade_animal_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Raça:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.raca_animal_entry = ttk.Entry(form_frame, width=30)
        self.raca_animal_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Temperamento:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.temperamento_animal_entry = ttk.Entry(form_frame, width=30)
        self.temperamento_animal_entry.grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Características:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.caracteristicas_animal_entry = ttk.Entry(form_frame, width=30)
        self.caracteristicas_animal_entry.grid(row=5, column=1, padx=5, pady=5)
        
        # Botões
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Cadastrar", command=self.cadastrar_animal).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Voltar", command=self.mostrar_menu_principal).pack(side=tk.LEFT, padx=10)
    
    def cadastrar_animal(self):
        if self.usuario_logado.get('tipo') != 'admin':
            messagebox.showerror("Acesso negado", "Apenas administradores podem cadastrar animais!")
            return
            
        tipo = self.tipo_animal.get().lower()
        nome = self.nome_animal_entry.get()
        idade = self.idade_animal_entry.get()
        raca = self.raca_animal_entry.get()
        temperamento = self.temperamento_animal_entry.get()
        caracteristicas = self.caracteristicas_animal_entry.get()
        
        if not all([tipo, nome, idade, raca, temperamento]):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return
        
        try:
            idade = int(idade)
        except ValueError:
            messagebox.showerror("Erro", "Idade deve ser um número!")
            return
        
        animais = carregar_dados(ANIMAIS_FILE)
        
        novo_animal = {
            'id': len(animais) + 1,
            'tipo': tipo,
            'nome': nome,
            'idade': idade,
            'raca': raca,
            'temperamento': temperamento,
            'caracteristicas': caracteristicas,
            'disponivel': True,
            'data_cadastro': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'cadastrado_por': self.usuario_logado.get('email')
        }
        
        animais.append(novo_animal)
        salvar_dados(ANIMAIS_FILE, animais)
        
        messagebox.showinfo("Sucesso", "Animal cadastrado com sucesso!")
        self.mostrar_menu_principal()
    
    def mostrar_lista_animais(self):
        self.limpar_tela()
        
        ttk.Label(self.main_frame, text="Animais Disponíveis", style='Title.TLabel').pack(pady=20)
        
        animais = carregar_dados(ANIMAIS_FILE)
        disponiveis = [a for a in animais if isinstance(a, dict) and a.get('disponivel', False)]
        
        if not disponiveis:
            ttk.Label(self.main_frame, text="Nenhum animal disponível no momento.").pack(pady=20)
        else:
            # Criar Treeview (tabela)
            tree_frame = ttk.Frame(self.main_frame)
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            scrollbar = ttk.Scrollbar(tree_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Adicionei mais colunas para mostrar as características
            self.tree = ttk.Treeview(tree_frame, 
                                   columns=('ID', 'Nome', 'Tipo', 'Idade', 'Raça', 'Temperamento', 'Características'), 
                                   show='headings', 
                                   yscrollcommand=scrollbar.set)
            
            # Configurar colunas
            self.tree.column('ID', width=50, anchor=tk.CENTER)
            self.tree.column('Nome', width=150, anchor=tk.W)
            self.tree.column('Tipo', width=100, anchor=tk.W)
            self.tree.column('Idade', width=50, anchor=tk.CENTER)
            self.tree.column('Raça', width=150, anchor=tk.W)
            self.tree.column('Temperamento', width=150, anchor=tk.W)
            self.tree.column('Características', width=200, anchor=tk.W)
            
            # Cabeçalhos
            self.tree.heading('ID', text='ID')
            self.tree.heading('Nome', text='Nome')
            self.tree.heading('Tipo', text='Tipo')
            self.tree.heading('Idade', text='Idade')
            self.tree.heading('Raça', text='Raça')
            self.tree.heading('Temperamento', text='Temperamento')
            self.tree.heading('Características', text='Características')
            
            # Adicionar dados
            for animal in disponiveis:
                self.tree.insert('', tk.END, values=(
                    animal.get('id', ''),
                    animal.get('nome', ''),
                    animal.get('tipo', '').capitalize(),
                    animal.get('idade', ''),
                    animal.get('raca', ''),
                    animal.get('temperamento', ''),
                    animal.get('caracteristicas', '')
                ))
            
            self.tree.pack(fill=tk.BOTH, expand=True)
            scrollbar.config(command=self.tree.yview)
        
        # Botão voltar
        ttk.Button(self.main_frame, text="Voltar", command=self.mostrar_menu_principal).pack(pady=20)
    
    def mostrar_tela_adocao(self):
        self.limpar_tela()
        
        ttk.Label(self.main_frame, text="Adotar Animal", style='Title.TLabel').pack(pady=20)
        
        animais = carregar_dados(ANIMAIS_FILE)
        disponiveis = [a for a in animais if isinstance(a, dict) and a.get('disponivel', False)]
        
        if not disponiveis:
            ttk.Label(self.main_frame, text="Nenhum animal disponível no momento.").pack(pady=20)
        else:
            # Criar Treeview (tabela)
            tree_frame = ttk.Frame(self.main_frame)
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            scrollbar = ttk.Scrollbar(tree_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Treeview com todas as informações
            self.tree_adocao = ttk.Treeview(tree_frame, 
                                          columns=('ID', 'Nome', 'Tipo', 'Idade', 'Raça', 'Temperamento', 'Características'), 
                                          show='headings', 
                                          yscrollcommand=scrollbar.set)
            
            # Configurar colunas
            self.tree_adocao.column('ID', width=50, anchor=tk.CENTER)
            self.tree_adocao.column('Nome', width=150, anchor=tk.W)
            self.tree_adocao.column('Tipo', width=100, anchor=tk.W)
            self.tree_adocao.column('Idade', width=50, anchor=tk.CENTER)
            self.tree_adocao.column('Raça', width=150, anchor=tk.W)
            self.tree_adocao.column('Temperamento', width=150, anchor=tk.W)
            self.tree_adocao.column('Características', width=200, anchor=tk.W)
            
            # Cabeçalhos
            self.tree_adocao.heading('ID', text='ID')
            self.tree_adocao.heading('Nome', text='Nome')
            self.tree_adocao.heading('Tipo', text='Tipo')
            self.tree_adocao.heading('Idade', text='Idade')
            self.tree_adocao.heading('Raça', text='Raça')
            self.tree_adocao.heading('Temperamento', text='Temperamento')
            self.tree_adocao.heading('Características', text='Características')
            
            # Adicionar dados
            for animal in disponiveis:
                self.tree_adocao.insert('', tk.END, values=(
                    animal.get('id', ''),
                    animal.get('nome', ''),
                    animal.get('tipo', '').capitalize(),
                    animal.get('idade', ''),
                    animal.get('raca', ''),
                    animal.get('temperamento', ''),
                    animal.get('caracteristicas', '')
                ))
            
            self.tree_adocao.pack(fill=tk.BOTH, expand=True)
            scrollbar.config(command=self.tree_adocao.yview)
            
            # Frame para seleção de animal
            select_frame = ttk.Frame(self.main_frame)
            select_frame.pack(pady=10)
            
            ttk.Label(select_frame, text="Digite o ID do animal que deseja adotar:").pack(side=tk.LEFT, padx=5)
            
            self.id_animal_adocao = tk.StringVar()
            ttk.Entry(select_frame, textvariable=self.id_animal_adocao, width=10).pack(side=tk.LEFT, padx=5)
            
            ttk.Button(select_frame, text="Adotar", command=self.realizar_adocao).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(self.main_frame, text="Voltar", command=self.mostrar_menu_principal).pack(pady=20)
    
    def realizar_adocao(self):
        try:
            animal_id = int(self.id_animal_adocao.get())
        except ValueError:
            messagebox.showerror("Erro", "ID inválido!")
            return
        
        animais = carregar_dados(ANIMAIS_FILE)
        animal = next((a for a in animais if isinstance(a, dict) and a.get('id') == animal_id and a.get('disponivel', False)), None)
        
        if not animal:
            messagebox.showerror("Erro", "Animal não encontrado ou indisponível!")
            return
        
        # Mostrar informações completas do animal antes de confirmar
        confirmacao = messagebox.askyesno(
            "Confirmar Adoção",
            f"Você está prestes a adotar:\n\n"
            f"Nome: {animal.get('nome', 'N/A')}\n"
            f"Tipo: {animal.get('tipo', 'N/A').capitalize()}\n"
            f"Idade: {animal.get('idade', 'N/A')} anos\n"
            f"Raça: {animal.get('raca', 'N/A')}\n"
            f"Temperamento: {animal.get('temperamento', 'N/A')}\n"
            f"Características: {animal.get('caracteristicas', 'N/A')}\n\n"
            "Deseja confirmar a adoção?"
        )
        
        if not confirmacao:
            return
        
        # Registrar adoção
        adocoes = carregar_dados(ADOCAO_FILE)
        nova_adocao = {
            'id_animal': animal_id,
            'email_adotante': self.usuario_logado.get('email', ''),
            'data': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'status': 'em andamento',
            'relatorios': [],
            'info_animal': {  # Adicionando informações do animal no registro de adoção
                'nome': animal.get('nome', ''),
                'tipo': animal.get('tipo', ''),
                'raca': animal.get('raca', ''),
                'caracteristicas': animal.get('caracteristicas', '')
            }
        }
        
        adocoes.append(nova_adocao)
        salvar_dados(ADOCAO_FILE, adocoes)
        
        # Marcar animal como indisponível
        animal['disponivel'] = False
        salvar_dados(ANIMAIS_FILE, animais)
        
        messagebox.showinfo("Sucesso", f"Parabéns! Você adotou {animal.get('nome', 'o animal')}!")
        self.mostrar_menu_principal()
    
    def mostrar_acompanhamento(self):
        self.limpar_tela()
        
        # Título principal centralizado
        ttk.Label(self.main_frame, text="Acompanhamento Pós-Adoção", style='Title.TLabel').pack(pady=20)    
        
        # Verificar se o usuário está logado corretamente
        if not self.usuario_logado or 'email' not in self.usuario_logado:
            messagebox.showerror("Erro", "Usuário não logado corretamente!")
            self.mostrar_menu_principal()
            return
        
        # Criar um frame principal que conterá o canvas e a barra de rolagem
        container = ttk.Frame(self.main_frame)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Criar um canvas
        canvas = tk.Canvas(container)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Adicionar barra de rolagem
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configurar o canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Criar um frame dentro do canvas para colocar os widgets
        scrollable_frame = ttk.Frame(canvas)
        
        # Centralizar o scrollable_frame dentro do canvas.
        # Definir a largura do scrollable_frame para ser igual à do canvas
        # e ligar o evento de redimensionamento do canvas para ajustar o scrollable_frame.
        def _on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Ensure the scrollable_frame's width matches the canvas's width
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())

        scrollable_frame.bind("<Configure>", _on_frame_configure)
        
        # Para encontrar a adoção correta, precisamos do email do adotante, não do nome exibido na tabela
        # Precisamos buscar o email do adotante a partir do nome, ou melhor, armazenar o email na tabela de adoções
        # Por enquanto, vamos assumir que o email do adotante é o mesmo que o nome exibido na tabela (se for email)
        # Melhoria: Adicionar o email do adotante como uma coluna oculta ou um atributo na Treeview
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw") # Keeping "nw" for top-left alignment for the scrollable content

        # Update the width of the canvas window when the canvas is resized
        def _on_canvas_resize(event):
            canvas.itemconfig(canvas_window, width=event.width)
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind('<Configure>', _on_canvas_resize)
        
        adocoes = carregar_dados(ADOCAO_FILE)
        animais = carregar_dados(ANIMAIS_FILE) 
        usuarios = carregar_dados(USUARIOS_FILE)
        
        # Se for admin, mostra todas as adoções, senão mostra apenas as do usuário
        if self.usuario_logado.get('tipo') == 'admin':
            minhas_adocoes = [a for a in adocoes if isinstance(a, dict)]
            # Título do administrador centralizado
            ttk.Label(scrollable_frame, text="VISÃO DO ADMINISTRADOR - TODAS AS ADOÇÕES", style='Title.TLabel', foreground='red').pack(pady=10, anchor=tk.CENTER)   
        else:
            minhas_adocoes = [a for a in adocoes if isinstance(a, dict) and a.get('email_adotante') == self.usuario_logado['email']]
        
        if not minhas_adocoes:
            ttk.Label(scrollable_frame, text="Nenhuma adoção registrada.").pack(pady=20)
        else:
            for adocao in minhas_adocoes:
                # Usar as informações do animal que foram salvas no registro de adoção
                info_animal = adocao.get('info_animal', {})
                
                # Obter informações do adotante
                adotante = next((u for u in usuarios if isinstance(u, dict) and u.get('email') == adocao.get('email_adotante')), None)
                nome_adotante = adotante.get('nome', 'N/A') if adotante else 'N/A'
                
                frame = ttk.LabelFrame(scrollable_frame, 
                                     text=f"{info_animal.get('nome', 'N/A')} ({info_animal.get('tipo', 'N/A').capitalize()}) - Adotado por: {nome_adotante}")
                frame.pack(fill=tk.X, padx=20, pady=10)
                
                # Mostrar informações detalhadas do animal (mantidas à esquerda para legibilidade)
                info_frame = ttk.Frame(frame)
                info_frame.pack(fill=tk.X, padx=10, pady=5)
                
                ttk.Label(info_frame, text=f"Raça: {info_animal.get('raca', 'N/A')}", width=20).pack(side=tk.LEFT, padx=5)
                ttk.Label(info_frame, text=f"Características: {info_animal.get('caracteristicas', 'N/A')}").pack(side=tk.LEFT, padx=5)
                
                ttk.Label(frame, text=f"Data da adoção: {adocao.get('data', 'N/A')}").pack(anchor=tk.W, padx=10)
                ttk.Label(frame, text=f"Status: {adocao.get('status', 'N/A')}").pack(anchor=tk.W, padx=10)
                
                if 'relatorios' in adocao:
                    ttk.Label(frame, text="Relatórios:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, padx=10, pady=(10, 0))
                    for relatorio in adocao['relatorios']:
                        if isinstance(relatorio, dict):
                            rel_frame = ttk.Frame(frame, borderwidth=1, relief=tk.SOLID)
                            rel_frame.pack(fill=tk.X, padx=10, pady=5)
                            
                            ttk.Label(rel_frame, 
                                    text=f"{relatorio.get('data', 'N/A')} - {relatorio.get('autor', 'N/A')}:",
                                    font=('Arial', 9, 'italic')).pack(anchor=tk.W)
                            ttk.Label(rel_frame, 
                                    text=relatorio.get('texto', 'N/A'),
                                    wraplength=700).pack(anchor=tk.W)
                
                # Se for admin ou o dono da adoção, pode adicionar relatório
                if self.usuario_logado.get('tipo') == 'admin' or adocao.get('email_adotante') == self.usuario_logado.get('email'):
                    ttk.Button(frame, text="Adicionar Relatório", 
                             command=lambda a=adocao: self.adicionar_relatorio(a)).pack(pady=5)
        
        # Botão voltar fora do frame rolável
        ttk.Button(self.main_frame, text="Voltar", command=self.mostrar_menu_principal).pack(pady=20)

    def adicionar_relatorio(self, adocao):
        texto = simpledialog.askstring("Novo Relatório", "Descreva como está sendo a adaptação:")
        if texto:
            if 'relatorios' not in adocao:
                adocao['relatorios'] = []
            
            adocao['relatorios'].append({
                'data': datetime.now().strftime("%d/%m/%Y %H:%M"),
                'texto': texto,
                'autor': self.usuario_logado.get('email')  # Registrar quem adicionou o relatório
            })
            
            # Atualizar arquivo
            todas_adocoes = carregar_dados(ADOCAO_FILE)
            for i, a in enumerate(todas_adocoes):
                if isinstance(a, dict) and a.get('id_animal') == adocao.get('id_animal') and a.get('email_adotante') == adocao.get('email_adotante'):
                    todas_adocoes[i] = adocao
                    break
            
            salvar_dados(ADOCAO_FILE, todas_adocoes)
            messagebox.showinfo("Sucesso", "Relatório adicionado com sucesso!")
            self.mostrar_acompanhamento()
    
    def fazer_logout(self):
        self.usuario_logado = None
        self.mostrar_tela_inicial()

# Iniciar aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = AdotaPetzApp(root)
    root.mainloop()