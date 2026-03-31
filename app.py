from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import timedelta

app = Flask(__name__)
# Chave de segurança - Use a do ambiente ou a padrão
app.secret_key = os.environ.get('SECRET_KEY', 'pmce_secret_2026')

# 1. DEFINE O TEMPO DE SESSÃO (2 MINUTOS)
app.permanent_session_lifetime = timedelta(minutes=2)

# Cadastro de usuários para o LOGIN
ACESSO = {
    "admin": "31736",
    "fiscal": "12345"
}

@app.route('/')
def index():
    # 2. PROTEÇÃO SIMPLES
    if not session.get('logado'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_input = request.form.get('usuario')
        senha_input = request.form.get('senha')
        
        if ACESSO.get(user_input) == senha_input:
            # 3. ATIVA O TIMER DE 2 MINUTOS NO MOMENTO DO LOGIN
            session.permanent = True  
            session['logado'] = True
            return redirect(url_for('index'))
        
        return "Usuário ou senha incorretos! <a href='/login'>Tentar novamente</a>"
    return render_template('login.html')

@app.route('/gerar', methods=['POST'])
def gerar():
    # Proteção para ninguém gerar PDF sem estar logado
    if not session.get('logado'):
        return redirect(url_for('login'))
    
    try:
        # Mantive seus campos originais exatamente como estavam
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
