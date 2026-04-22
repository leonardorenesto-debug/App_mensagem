import flet as ft
import requests
import dashboard

# Configurações de conexão
URL_BASE = "https://cjetrolpbbrtpqruvzxp.supabase.co/rest/v1/usuarios"
CHAVE_API = "sb_publishable_9VuJVoqitNxXxrrqITOnFQ_jYDRgnKq"
HEADERS = {
    "apikey" : CHAVE_API,
    "Authorization": f"BEARER {CHAVE_API}",
    "Content-Type": "application/json"
}


def main(page: ft.Page):
    page.title = "App - Mensageiro"
    page.theme_mode = "light"
    page.window_width, page.window_height = 450, 700
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    def exibir_login(e=None):
        page.clean()
        txt_email = ft.TextField(label="E-mail", width=350, border_radius=10)
        txt_senha = ft.TextField(label="Senha", width=350, password=True, can_reveal_password=True, border_radius=10)
        lbl_status = ft.Text("", weight="bold")

        def logar(e):
            lbl_status.value = ""
            btn_entrar.disabled = True
            page.update()

            try:
                #AQUI VAMOS FAZER O GET
                
                res = requests.get(F"{URL_BASE}?email=eq. {txt_email.value}", headers=HEADERS)
                                
                dados = res.json()
                
                if res.status_code == 200 and len(dados) > 0:
                    dashboard.exibir_dashboard(page, dados[0], exibir_login)
                else:
                    lbl_status.value, lbl_status.color = "❌ Login incorreto!", "red"
            except:
                lbl_status.value, lbl_status.color = "⚠️ Erro de conexão!", "orange"
            
            btn_entrar.disabled = False
            page.update()

        btn_entrar = ft.FilledButton("Entrar no Sistema", width=300, on_click=logar)
        page.add(
            ft.Icon(ft.Icons.LOCK_PERSON, size=80, color="blue"),
            ft.Text("Login MMPass", size=30, weight="bold"),
            txt_email, txt_senha, lbl_status, btn_entrar,
            ft.TextButton("Criar nova conta", on_click=exibir_cadastro)
        )
        page.update()

    def exibir_cadastro(e=None):
        page.clean()
        txt_nome = ft.TextField(label="Nome Completo", width=350, border_radius=10)
        txt_email = ft.TextField(label="E-mail", width=350, border_radius=10)
        txt_senha = ft.TextField(label="Senha", width=350, password=True, border_radius=10)
        lbl_status = ft.Text("", weight="bold")

        def cadastrar(e):
            if not txt_nome.value or not txt_email.value: return
            corpo = {"nome": txt_nome.value, "email": txt_email.value, "senha": txt_senha.value}
            try:
                #REQUEST
                res = requests.post(URL_BASE,json=corpo,
                headers=HEADERS)
                if res.status_code == 201:exibir_login()
                
                
            except: pass

        page.add(
            ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=80, color="blue"),
            ft.Text("Cadastro", size=30, weight="bold"),
            txt_nome, txt_email, txt_senha, lbl_status,
            ft.FilledButton("Cadastrar", width=300, on_click=cadastrar),
            ft.TextButton("Voltar ao Login", on_click=exibir_login)
        )
        page.update()

    exibir_login()

if __name__ == "__main__":
    import os
    # Captura a porta que o Render vai fornecer ou usa a 8080 por padrão
    port = int(os.getenv("PORT", 8080))
    # Iniciamos o Flet como um servidor Web
    ft.app(target=main, port=port)
    ft.run(main)