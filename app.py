from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
# Chave para manter a sessão ativa no celular
app.secret_key = os.environ.get('SECRET_KEY', 'pmce_seguro_2026')

# LISTA DE QUEM PODE ENTRAR NO SISTEMA
# "usuario": "senha"
ACESSO = {
    "admin": "31736",
    "fiscal": "12345",
    "carlos": "senhapm"
}

@app.route('/')
def index():
    # Se não estiver logado, manda para a tela de login
    if not session.get('logado'):
        return redirect(url_for('login'))
    
    # Se estiver logado, abre o seu formulário original (index.html)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_input = request.form.get('usuario')
        senha_input = request.form.get('senha')
        
        # Verifica se o usuário e senha batem com a lista ACESSO
        if ACESSO.get(user_input) == senha_input:
            session['logado'] = True
            return redirect(url_for('index'))
        
        return "Acesso negado! <a href='/login'>Tentar novamente</a>"
    
    # Se for GET, mostra a tela de login
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
