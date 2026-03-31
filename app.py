from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import timedelta

app = Flask(__name__)
# Chave de segurança para as sessões
app.secret_key = os.environ.get('SECRET_KEY', 'pmce_secret_2026')

# Configura o tempo de sessão para 2 minutos
app.permanent_session_lifetime = timedelta(minutes=2)

# Cadastro de usuários para o LOGIN (independente dos militares)
ACESSO = {
    "admin": "31736",
    "fiscal": "12345"
}

@app.route('/')
def index():
    if not session.get('logado'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_input = request.form.get('usuario')
        senha_input = request.form.get('senha')
        
        if ACESSO.get(user_input) == senha_input:
            session.permanent = True  # Ativa o timer de 2 min
            session['logado'] = True
            return redirect(url_for('index'))
        
        return "Usuário ou senha incorretos! <a href='/login'>Tentar novamente</a>"
    return render_template('login.html')

# --- ESTA É A ROTA QUE GERA O PDF E ESTAVA FALTANDO ---
@app.route('/gerar', methods=['POST'])
def gerar():
    if not session.get('logado'):
        return redirect(url_for('login'))
    
    try:
        # Pega todos os dados vindos do formulário do index.html
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
        
        # Usa o seu arquivo permuta.html para exibir o resultado
        return render_template('permuta.html', **dados)
    
    except Exception as e:
        return f"Erro ao gerar documento: {str(e)}"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
