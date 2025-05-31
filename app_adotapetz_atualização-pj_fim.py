import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
from datetime import datetime

# Arquivos de dados
USUARIOS_FILE = "usuarios.txt"
ANIMAIS_FILE = "animais.txt"
ADOCAO_FILE = "adocoes.txt"

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
        self.root.geometry("800x600")
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
        
        if not all([email, senha, nome, telefone]):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return
        
        usuarios = carregar_dados(USUARIOS_FILE)
        if any(isinstance(u, dict) and u.get('email') == email for u in usuarios):
            messagebox.showerror("Erro", "Email já cadastrado!")
            return
        
        novo_usuario = {
            'email': email,
            'senha': senha,
            'nome': nome,
            'telefone': telefone
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
        ttk.Button(self.main_frame, text="Cadastrar Animal", command=self.mostrar_tela_cadastro_animal).pack(pady=10, ipadx=20, ipady=5)
        ttk.Button(self.main_frame, text="Listar Animais Disponíveis", command=self.mostrar_lista_animais).pack(pady=10, ipadx=20, ipady=5)
        ttk.Button(self.main_frame, text="Adotar Animal", command=self.mostrar_tela_adocao).pack(pady=10, ipadx=20, ipady=5)
        ttk.Button(self.main_frame, text="Acompanhamento Pós-Adoção", command=self.mostrar_acompanhamento).pack(pady=10, ipadx=20, ipady=5)
        ttk.Button(self.main_frame, text="Sair", command=self.fazer_logout).pack(pady=20, ipadx=20, ipady=5)
    
    def mostrar_tela_cadastro_animal(self):
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
            'data_cadastro': datetime.now().strftime("%d/%m/%Y %H:%M")
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
            
            self.tree = ttk.Treeview(tree_frame, columns=('ID', 'Nome', 'Tipo', 'Idade', 'Raça'), show='headings', yscrollcommand=scrollbar.set)
            
            # Configurar colunas
            self.tree.column('ID', width=50, anchor=tk.CENTER)
            self.tree.column('Nome', width=150, anchor=tk.W)
            self.tree.column('Tipo', width=100, anchor=tk.W)
            self.tree.column('Idade', width=50, anchor=tk.CENTER)
            self.tree.column('Raça', width=150, anchor=tk.W)
            
            # Cabeçalhos
            self.tree.heading('ID', text='ID')
            self.tree.heading('Nome', text='Nome')
            self.tree.heading('Tipo', text='Tipo')
            self.tree.heading('Idade', text='Idade')
            self.tree.heading('Raça', text='Raça')
            
            # Adicionar dados
            for animal in disponiveis:
                self.tree.insert('', tk.END, values=(
                    animal.get('id', ''),
                    animal.get('nome', ''),
                    animal.get('tipo', '').capitalize(),
                    animal.get('idade', ''),
                    animal.get('raca', '')
                ))
            
            self.tree.pack(fill=tk.BOTH, expand=True)
            scrollbar.config(command=self.tree.yview)
        
        # Botão voltar
        ttk.Button(self.main_frame, text="Voltar", command=self.mostrar_menu_principal).pack(pady=20)
    
    def mostrar_tela_adocao(self):
        self.mostrar_lista_animais()  # Reutiliza a tela de listagem
        
        animais = carregar_dados(ANIMAIS_FILE)
        disponiveis = [a for a in animais if isinstance(a, dict) and a.get('disponivel', False)]
        
        if disponiveis:
            ttk.Label(self.main_frame, text="Digite o ID do animal que deseja adotar:").pack(pady=10)
            
            self.id_animal_adocao = tk.StringVar()
            ttk.Entry(self.main_frame, textvariable=self.id_animal_adocao, width=10).pack(pady=5)
            
            ttk.Button(self.main_frame, text="Adotar", command=self.realizar_adocao).pack(pady=10)
        
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
        
        # Registrar adoção
        adocoes = carregar_dados(ADOCAO_FILE)
        nova_adocao = {
            'id_animal': animal_id,
            'email_adotante': self.usuario_logado.get('email', ''),
            'data': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'status': 'em andamento',
            'relatorios': []
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
        
        ttk.Label(self.main_frame, text="Acompanhamento Pós-Adoção", style='Title.TLabel').pack(pady=20)
        
        # Verificar se o usuário está logado corretamente
        if not self.usuario_logado or 'email' not in self.usuario_logado:
            messagebox.showerror("Erro", "Usuário não logado corretamente!")
            self.mostrar_menu_principal()
            return
        
        adocoes = carregar_dados(ADOCAO_FILE)
        animais = carregar_dados(ANIMAIS_FILE)
        
        # Filtrar adoções com verificação de chave
        minhas_adocoes = []
        for a in adocoes:
            if isinstance(a, dict) and a.get('email_adotante') == self.usuario_logado['email']:
                minhas_adocoes.append(a)
        
        if not minhas_adocoes:
            ttk.Label(self.main_frame, text="Você não possui adoções registradas.").pack(pady=20)
        else:
            for adocao in minhas_adocoes:
                # Verificar se o animal existe
                animal = next((a for a in animais if isinstance(a, dict) and a.get('id') == adocao.get('id_animal')), None)
                
                if animal:
                    frame = ttk.LabelFrame(self.main_frame, text=f"{animal.get('nome', 'N/A')} ({animal.get('tipo', 'N/A').capitalize()})")
                    frame.pack(fill=tk.X, padx=20, pady=10)
                    
                    ttk.Label(frame, text=f"Data da adoção: {adocao.get('data', 'N/A')}").pack(anchor=tk.W)
                    ttk.Label(frame, text=f"Status: {adocao.get('status', 'N/A')}").pack(anchor=tk.W)
                    
                    if 'relatorios' in adocao:
                        ttk.Label(frame, text="Relatórios:").pack(anchor=tk.W)
                        for relatorio in adocao['relatorios']:
                            if isinstance(relatorio, dict):
                                ttk.Label(frame, text=f"{relatorio.get('data', 'N/A')}: {relatorio.get('texto', 'N/A')}", 
                                        wraplength=700).pack(anchor=tk.W)
                    
                    ttk.Button(frame, text="Adicionar Relatório", 
                             command=lambda a=adocao: self.adicionar_relatorio(a)).pack(pady=5)
        
        ttk.Button(self.main_frame, text="Voltar", command=self.mostrar_menu_principal).pack(pady=20)
    
    def adicionar_relatorio(self, adocao):
        texto = simpledialog.askstring("Novo Relatório", "Descreva como está sendo a adaptação:")
        if texto:
            if 'relatorios' not in adocao:
                adocao['relatorios'] = []
            
            adocao['relatorios'].append({
                'data': datetime.now().strftime("%d/%m/%Y %H:%M"),
                'texto': texto
            })
            
            # Atualizar arquivo
            todas_adocoes = carregar_dados(ADOCAO_FILE)
            for i, a in enumerate(todas_adocoes):
                if isinstance(a, dict) and a.get('id_animal') == adocao.get('id_animal'):
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