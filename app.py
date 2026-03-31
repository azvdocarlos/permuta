from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'pmce_secret_2026')

# CADASTRO CONTROLADO POR VOCÊ
USUARIOS = {
    "31736": {
        "senha": "123", 
        "nome": "C. AZEVEDO", 
        "num": "31736", 
        "posto": "CB",
        "assinatura": "https://raw.githubusercontent.com/azvdocarlos/permuta/main/assinaturas/azevedo.png"
    },
    "36338": {
        "senha": "456", 
        "nome": "BRUNO", 
        "num": "36338", 
        "posto": "SD",
        "assinatura": "https://raw.githubusercontent.com/azvdocarlos/permuta/main/assinaturas/bruno.png"
    }
}

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    dados_militar = USUARIOS.get(session['user'])
    return render_template('index.html', militar=dados_militar)

# --- NOVA ROTA QUE ESTAVA FALTANDO ---
@app.route('/gerar', methods=['POST'])
def gerar():
    try:
        # Pega os dados do formulário
        dados = {
            "posto_req": request.form.get('posto_req'),
            "nome_req": request.form.get('nome_req'),
            "num_req": request.form.get('num_req'),
            "posto_sub": request.form.get('posto_sub'),
            "nome_sub": request.form.get('nome_sub'),
            "num_sub": request.form.get('num_sub'),
            "data": request.form.get('data'),
            "assinatura_req_file": request.form.get('assinatura_req_file'),
            "assinatura_sub_file": request.form.get('assinatura_sub_file')
        }
        
        # O Flask vai preencher o código do PDF que você me mandou
        # Certifique-se de que o arquivo do PDF se chama 'layout_pdf.html' na pasta templates
        return render_template('layout_pdf.html', **dados)
    
    except Exception as e:
        return f"Erro ao processar dados: {str(e)}"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_input = request.form.get('usuario')
        senha_input = request.form.get('senha')
        
        if user_input in USUARIOS and USUARIOS[user_input]['senha'] == senha_input:
            session['user'] = user_input
            return redirect(url_for('index'))
        return "Usuário ou senha incorretos. <a href='/login'>Tentar novamente</a>"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
