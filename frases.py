import flet as ft
import requests
import urllib.parse

# Credenciais
URL_BASE  = "https://nozlniqtbymvcktcalhe.supabase.co/rest/v1/usuarios"
CHAVE_API = "sb_publishable_HiNzXFPm9dgAuBXalvUy-w_Xw1DHJSt"
HEADERS = {
    "apikey": CHAVE_API,
    "Authorization": f"Bearer {CHAVE_API}",
    "Content-Type": "application/json"
}



# --- 1. TELA DO QR CODE ---
def exibir_qr_final(page: ft.Page, nome, frase, voltar_funcao):
    page.clean()
    page.bgcolor = "white"
    
    frase_url = urllib.parse.quote(str(frase))
    url_qr = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={frase_url}"

    img_qrcode = ft.Image(src=url_qr, width=300, height=300)

    # USANDO O FORMATO COMPLETO (ft.Icons.NOME) QUE FUNCIONOU NO DASHBOARD
    layout = ft.Column(
        controls=[
            ft.Row([
                ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=voltar_funcao, icon_color="blue"),
                ft.Text(f"QR de {nome}", size=22, weight="bold", color="black")
            ]),
            ft.Divider(height=40, color="transparent"),
            ft.Container(
                content=img_qrcode,
                padding=10,
                border=ft.border.all(2, "blue"),
                border_radius=15
            ),
            ft.Divider(height=20, color="transparent"),
            ft.Text("Aponte a câmera para ler", color="grey", size=14)
        ],
        horizontal_alignment="center"
    )

    page.add(layout)
    page.update()

# --- 2. TELA DA LISTA ---
def exibir_lista_frases(page: ft.Page, aluno_logado, voltar_dashboard):
    page.clean()
    page.bgcolor = "white"
    
    lista = ft.ListView(expand=True, spacing=10, padding=20)

    try:
        #GET TRAZER OS USUÁRIOS
        res = requests.get(URL_BASE, headers=HEADERS)
        usuarios = res.json()
        usuarios_ordenados = sorted(usuarios, key=lambda x: x['nome'].lower())
        
        for u in usuarios_ordenados:
            nome_u = u.get('nome')
            frase_u = u.get('frase')
            
            if frase_u:
                lista.controls.append(
                    ft.Container(
                        content=ft.ListTile(
                            leading=ft.Icon(ft.Icons.PERSON_PIN, color="blue"),
                            title=ft.Text(nome_u, color="black", weight="bold", size=18),
                            trailing=ft.Icon(ft.Icons.QR_CODE, color="blue"),
                        ),
                        border=ft.border.all(1, "grey300"),
                        border_radius=10,
                        ink=True,
                        on_click=lambda e, n=nome_u, f=frase_u: exibir_qr_final(
                            page, n, f, 
                            lambda _: exibir_lista_frases(page, aluno_logado, voltar_dashboard)
                        )
                    )
                )
    except Exception as err:
        print(f"Erro ao carregar: {err}")

    # BARRA SUPERIOR COM ÍCONE COMPLETO
    page.add(
        ft.Row([
            ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=voltar_dashboard),
            ft.Text("Mural da Turma", size=25, weight="bold", color="black")
        ]),
        ft.Divider(),
        lista
    )
    page.update()