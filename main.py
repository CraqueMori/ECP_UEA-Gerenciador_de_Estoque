from flask import render_template, request, redirect, url_for, make_response
from app import app, db
from app.models import User , Itens , Carrinho
from flask_login import login_user, logout_user, login_required, current_user
from fpdf import FPDF, HTMLMixin
import urllib.request
#view -> controller -> model

#view -> model

@app.route('/login', methods =['GET', 'POST'])
def login_route():
    return render_template('login.html')

#Controler e Rota do Login 
@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('home'))
        
    return render_template(url_for('lista'))

#Controler e Rota do Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_route'))

#Rota e controler do Cadastro de Usuarios
@app.route('/cadastro', methods =['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        #função do model
        User.create_user(name, email, password)

    return render_template('cadastro.html')

#Rota da Home
@app.route('/index', methods = ['GET', 'POST'])
def rota_index():
    return(render_template('index.html'))

#Rota do Update Item
@app.route('/update_item', methods = ['GET', 'POST'])
def rota_update():
    return render_template('update_item.html')

#Controler + Rota do Estoque
@app.route('/estoque')
def lista():
    estoque = Itens.query.all()
    return render_template('estoque.html', estoque=estoque)

#Controler + Rota do  cadastro de Itens
@app.route('/cadastro_itens', methods = ['GET', 'POST'])
def cadastro_item():
    if request.method == 'POST':
        name= request.form['name']
        quantidade = request.form['quantidade']
        preço = request.form['preço']
        marca = request.form['marca']
        tipo = request.form['tipo']
        
        #função do models
        Itens.create_iten(name, quantidade, preço, marca, tipo)
    return render_template('cadastro_itens.html')

#Controler + da Exclusão dos itens
@app.route('/estoque')
def excluir_estoque(id):
    item_excluido = Itens.query.filter_by(id=id).first()
    Itens.excluir_do_estoque(item_excluido)
    return redirect(url_for('lista'))

@app.route('/carrinho')
def carrinho():
    carrinho = Carrinho.query.all()
    return render_template('carrinho.html', carrinho=carrinho)

@app.route('/add_carrinho/<int:iten_id>')
def add_carrinho(iten_id):
    iten = Itens.query.get_or_404(iten_id)
    item_carrinho = Carrinho(name=iten.name, quantidade=iten.quantidade, preço=iten.preço, marca=iten.marca, tipo=iten.tipo)
    db.session.add(item_carrinho)
    db.session.commit()
    return redirect(url_for('lista'))


@app.route('/estoque')
def excluir_carrinho(id):
    item_excluido = Carrinho.query.filter_by(id=id).first()
    Carrinho.excluir_do_carro(item_excluido)
    return redirect(url_for('carrinho_rota'))

#Controler + Rota de Update de Item
@app.route("/update_item/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
    item_atualizado = Itens.query.filter_by(id=id).first()
    
    if request.method == 'POST':
        name= request.form['name']
        quantidade = request.form['quantidade']
        preço = request.form['preço']
        marca = request.form['marca']
        tipo = request.form['tipo']

        Itens.update_item(item_atualizado, name, quantidade, preço, marca, tipo)

        return redirect(url_for("lista"))
    
    return render_template("update_item.html", item_atualizado=item_atualizado)


@app.route('/generate_pdf',methods=['GET', 'POST'] )
def generate_pdf_controler():
    items = Carrinho.query.all() # Retrieve all items from your database using SQLAlchemy
    data = [['ID', 'Nome', 'Quantidade', 'Preço', 'Marca', 'Tipo']] # Initialize data list with header row
    for item in items:
        data.append([item.id, item.name, item.quantidade, item.preço, item.marca, item.tipo]) # Add data rows to list
    
    # Create FPDF object and set up document
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Carrinho')
    pdf.ln(10)
    pdf.cell(40, 10, 'ID', 1)
    pdf.cell(40, 10, 'Nome', 1)
    pdf.cell(40, 10, 'Quantidade', 1)
    pdf.cell(40, 10, 'Preço', 1)
    pdf.cell(40, 10, 'Marca', 1)
    pdf.cell(40, 10, 'Tipo', 1)
    pdf.ln()
    
    # Add data to document
    for row in data:
        for item in row:
            pdf.cell(40, 10, str(item), 1)
        pdf.ln()
    
    # Retrieve the selected payment option from the form
    payment_option = request.form.get('forma-pagamento')
    
    # Add payment option to document
    pdf.cell(40, 10, 'Forma de pagamento:', 0)
    pdf.cell(40, 10, payment_option, 1)
    
    # Create response and return PDF document
    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers.set('Content-Disposition', 'attachment', filename='carrinho.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    return response

app.run(debug=True)