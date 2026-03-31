from flask import Flask, render_template, request, make_response, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from weasyprint import HTML
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = "uma_chave_secreta_qualquer"  # troca pra algo seguro

# ===== Usuários cadastrados manualmente =====
# Senhas já hashadas
usuarios = {
    "carlos": generate_password_hash("1234"),
    "joana": generate_password_hash("abcd")
}

# ===== Decorator para proteger rotas =====
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "usuario" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# ===== Login / Logout =====
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        if usuario in usuarios and check_password_hash(usuarios[usuario], senha):
            session["usuario"] = usuario
            return redirect(url_for("index"))
        else:
            return "Usuário ou senha incorretos", 401
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))

# ===== Rotas do app original =====
@app.route('/')
@login_required
def index():
    usuario_logado = session["usuario"]
    return render_template('index.html', usuario=usuario_logado)

@app.route('/gerar', methods=['POST'])
@login_required
def gerar():
    assinatura_req_file = request.form['assinatura_req_file']
    assinatura_sub_file = request.form['assinatura_sub_file']

    html = render_template(
        'permuta.html',
        posto_req=request.form['posto_req'],
        nome_req=request.form['nome_req'],
        num_req=request.form['num_req'],
        posto_sub=request.form['posto_sub'],
        nome_sub=request.form['nome_sub'],
        num_sub=request.form['num_sub'],
        data=request.form['data'],
        assinatura_req_file=assinatura_req_file,
        assinatura_sub_file=assinatura_sub_file
    )

    pdf = HTML(string=html, base_url=os.getcwd()).write_pdf()

    data_formatada = request.form['data'].replace("/", "").replace("-", "")
    nome_pdf = f"permuta{data_formatada}.pdf"

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={nome_pdf}'

    return response

# ===== Execução =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
