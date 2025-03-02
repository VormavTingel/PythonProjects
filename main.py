import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

users_db = {
    "admin": "admin123",
    "usuario": "senha123"
}

def authenticate_with_drive():
    """
    Realiza a autenticação com o Google Drive via PyDrive2.
    Usa o arquivo 'client_secrets.json' para fazer OAuth2.
    """
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credentials.json")

    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile("credentials.json")
    return GoogleDrive(gauth)

def create_drive_folder(drive, folder_name, parent_id=None):
    """
    Cria uma pasta no Drive com o nome especificado.
    Retorna o ID da nova pasta.
    """
    folder_metadata = {
        'title': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        folder_metadata['parents'] = [{'id': parent_id}]

    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
    return folder['id']

def upload_recursive(drive, local_path, parent_id=None):
    """
    Faz upload recursivo de todos os arquivos e pastas em 'local_path'
    para o Google Drive, mantendo a estrutura de diretórios.
    """
    if parent_id is None:
        folder_name = os.path.basename(local_path)
        parent_id = create_drive_folder(drive, folder_name)

    for item in os.listdir(local_path):
        item_full_path = os.path.join(local_path, item)

        if os.path.isdir(item_full_path):
            new_folder_id = create_drive_folder(drive, item, parent_id)
            upload_recursive(drive, item_full_path, new_folder_id)
        else:
            file_drive = drive.CreateFile({
                'title': item,
                'parents': [{'id': parent_id}]
            })
            file_drive.SetContentFile(item_full_path)
            file_drive.Upload()


def do_backup():
    """
    Faz o processo de backup ao clicar no botão.
    """
    backup_folder = entry_folder.get().strip()
    user_email = entry_email.get().strip()
    user_pass = entry_pass.get().strip()

    if not backup_folder or not os.path.isdir(backup_folder):
        messagebox.showerror("Erro", "Selecione uma pasta de backup válida.")
        return

    print(f"[INFO] Usuário Google Drive: e-mail={user_email}, senha={user_pass} (não usado no OAuth)")

    try:
        drive = authenticate_with_drive()
        upload_recursive(drive, backup_folder)
        messagebox.showinfo("Sucesso", "Backup concluído com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro durante o backup:\n{str(e)}")

def select_folder():
    """Abre janela do sistema para o usuário selecionar a pasta."""
    folder_path = filedialog.askdirectory()
    entry_folder.delete(0, tk.END)
    entry_folder.insert(0, folder_path)

def open_backup_window():
    """
    Abre a janela principal de backup (segunda tela) após login.
    """
    backup_window = tk.Toplevel()
    backup_window.title("Backup Automático para Google Drive")
    backup_window.geometry("525x220")
    backup_window.resizable(False, False)

    try:
        backup_window.eval('tk::PlaceWindow . center')
    except:
        pass

    frm_main = ttk.Frame(backup_window, padding="15")
    frm_main.pack(fill="both", expand=True)

    lbl_folder = ttk.Label(frm_main, text="Pasta de Backup:")
    lbl_folder.grid(row=0, column=0, padx=5, pady=5, sticky="E")

    global entry_folder
    entry_folder = ttk.Entry(frm_main, width=40)
    entry_folder.grid(row=0, column=1, padx=5, pady=5, sticky="W")

    btn_browse = ttk.Button(frm_main, text="Selecionar Pasta", command=select_folder)
    btn_browse.grid(row=0, column=2, padx=5, pady=5, sticky="W")

    lbl_email = ttk.Label(frm_main, text="E-mail do Drive:")
    lbl_email.grid(row=1, column=0, padx=5, pady=5, sticky="E")

    global entry_email
    entry_email = ttk.Entry(frm_main, width=40)
    entry_email.grid(row=1, column=1, padx=5, pady=5, columnspan=2, sticky="W")

    lbl_pass = ttk.Label(frm_main, text="Senha do Drive:")
    lbl_pass.grid(row=2, column=0, padx=5, pady=5, sticky="E")

    global entry_pass
    entry_pass = ttk.Entry(frm_main, show="*", width=40)
    entry_pass.grid(row=2, column=1, padx=5, pady=5, columnspan=2, sticky="W")

    btn_backup = ttk.Button(frm_main, text="Fazer Backup", command=do_backup)
    btn_backup.grid(row=3, column=0, columnspan=3, pady=10)


def attempt_login():
    """
    Verifica se as credenciais digitadas na tela de login
    estão no 'users_db'. Se estiverem, abre a tela de backup.
    """
    username = login_user_entry.get().strip()
    password = login_pass_entry.get().strip()

    if username in users_db and users_db[username] == password:
        messagebox.showinfo("Login", f"Bem-vindo(a), {username}!")
        open_backup_window()
        login_window.withdraw()
    else:
        messagebox.showerror("Erro de Login", "Usuário ou senha inválidos.")

login_window = tk.Tk()
login_window.title("Login do Aplicativo de Backup")
login_window.geometry("360x200")
login_window.resizable(False, False)

try:
    login_window.eval('tk::PlaceWindow . center')
except:
    pass

frm_login = ttk.Frame(login_window, padding="10")
frm_login.pack(fill="both", expand=True)

title_label = ttk.Label(
    frm_login,
    text="Bem-vindo ao Aplicativo de Backup",
    font=("Helvetica", 12, "bold")
)
title_label.grid(row=0, column=0, columnspan=2, pady=(5,15))

lbl_user = ttk.Label(frm_login, text="Usuário:")
lbl_user.grid(row=1, column=0, padx=5, pady=5, sticky="E")

login_user_entry = ttk.Entry(frm_login, width=25)
login_user_entry.grid(row=1, column=1, padx=5, pady=5, sticky="W")

lbl_pass = ttk.Label(frm_login, text="Senha:")
lbl_pass.grid(row=2, column=0, padx=5, pady=5, sticky="E")

login_pass_entry = ttk.Entry(frm_login, show="*", width=25)
login_pass_entry.grid(row=2, column=1, padx=5, pady=5, sticky="W")

btn_login = ttk.Button(frm_login, text="Entrar", command=attempt_login)
btn_login.grid(row=3, column=0, columnspan=2, pady=10)

login_window.mainloop()
