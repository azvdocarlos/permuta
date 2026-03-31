from flask import Flask, render_template, request, make_response
from weasyprint import HTML
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar', methods=['POST'])
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
