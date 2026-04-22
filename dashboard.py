import flet as ft
import requests
import frases

# Credenciais (Padrão Projeto_sesi2A)
URL_BASE  = "https://nozlniqtbymvcktcalhe.supabase.co/rest/v1/usuarios"
CHAVE_API = "sb_publishable_HiNzXFPm9dgAuBXalvUy-w_Xw1DHJSt"
HEADERS = {
    "apikey": CHAVE_API,
    "Authorization": f"Bearer {CHAVE_API}",
    "Content-Type": "application/json"
}



def exibir_dashboard(page: ft.Page, aluno, voltar_login_funcao):
    # Try/Except gigante para você ver o erro no terminal se algo quebrar
    try:
        page.clean()
        page.bgcolor = "white"
        page.vertical_alignment = "center"
        page.horizontal_alignment = "center"

        id_usuario = aluno.get('id')

        # 1. Componentes de entrada
        txt_frase = ft.TextField(
            label="O que você está pensando?",
            hint_text="Digite sua frase aqui...", 
            value=aluno.get('frase', ""),
            width=380,
            border_radius=10,
            color="black",
            multiline=True
        )
        
        lbl_status = ft.Text("", weight="bold")

        # 2. Lógica de salvar
        def salvar_frase_banco(e):
            btn_salvar.disabled = True
            btn_salvar.content = ft.ProgressRing(width=20, height=20)
            page.update()

            try:
                #REQUESTS
                url_patch = f"{URL_BASE}?id=eq.{id_usuario}"
                res = requests.patch(url_patch, json= {"frase": txt_frase.value}, headers=HEADERS)
                
                if res.status_code in [200, 204]:
                    lbl_status.value, lbl_status.color = "✅ Frase salva com sucesso!", "green"
                    aluno['frase'] = txt_frase.value 
                else:
                    lbl_status.value, lbl_status.color = f"❌ Erro: {res.status_code}", "red"
            except:
                lbl_status.value, lbl_status.color = "⚠️ Erro de conexão", "orange"

            btn_salvar.disabled = False
            btn_salvar.content = ft.Text("Salvar no Mural")
            page.update()

        # 3. Botões
        btn_salvar = ft.FilledButton(
            "Salvar no Mural", 
            width=300, 
            height=50, 
            on_click=salvar_frase_banco
        )

        btn_ver_todos = ft.OutlinedButton(
            "Ver Mural da Turma", 
            width=300, 
            height=50,
            on_click=lambda _: frases.exibir_lista_frases(
                page, 
                aluno, 
                lambda _: exibir_dashboard(page, aluno, voltar_login_funcao)
            )
        )

        # 4. Montagem Direta (Sem Columns extras para não bugar)
        page.add(
            ft.Icon(ft.Icons.CHAT_ROUNDED, size=70, color="blue"),
            ft.Text(f"Olá, {aluno['nome']}!", size=28, weight="bold", color="black"),
            ft.Divider(height=20, color="transparent"),
            txt_frase,
            lbl_status,
            btn_salvar,
            ft.Divider(height=10, color="transparent"),
            btn_ver_todos,
            ft.Divider(height=20, color="transparent"),
            ft.TextButton(
                "Sair do Sistema", 
                on_click=voltar_login_funcao, 
                style=ft.ButtonStyle(color="red")
            )
        )
        
        page.update()

    except Exception as e:
        print(f"ERRO NO DASHBOARD: {e}")