from flask_login import UserMixin, login_user, logout_user, current_user
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, url_for



@login_manager.user_loader
def get_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement = True, primary_key=True)
    name = db.Column(db.String(84), nullable= False)
    email = db.Column(db.String(84), nullable= False, unique=True)
    password = db.Column(db.String(126),nullable= False)
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)
    
    def create_user(name, email, password):
        user = User(name, email, password)
        db.session.add(user)
        db.session.commit()

    def m_login(email, password):
        user = User.query.filter_by(email=email).first()
        print(user)

        if not user or not user.verify_password(password):
            return redirect(url_for('login'))
        
        login_user(user, remember=True, duration=None, force=True, fresh=True)

class Itens (db.Model):
    __tablename__ = 'itens'
    id = db.Column(db.Integer, autoincrement = True, primary_key=True)
    name = db.Column(db.String(126), nullable= False)
    quantidade = db.Column(db.String(126),nullable= False)
    preço = db.Column(db.String(126), nullable= False)
    marca = db.Column(db.String(126),nullable= False)
    tipo = db.Column(db.String(126),nullable= False)

    def __init__(self, name, quantidade, preço, marca, tipo):
        self.name = name
        self.quantidade = quantidade
        self.preço = preço
        self.marca = marca
        self.tipo = tipo

    def create_iten(name, quantidade, preço, marca, tipo):
        iten= Itens(name, quantidade, preço, marca, tipo)
        db.session.add(iten)
        db.session.commit()

    def excluir_do_estoque(item_excluido):
        db.session.delete(item_excluido)
        db.session.commit()

    def update_item(item_atualizado, name, quantidade, preço, marca, tipo):
        item_atualizado.name = name
        item_atualizado.quantidade = quantidade
        item_atualizado.preço = preço
        item_atualizado.marca = marca
        item_atualizado.tipo = tipo
        
        db.session.commit()
        return redirect(url_for('lista'))
    
class Carrinho(db.Model):
    __tablename__ = 'carrinho'
    id = db.Column(db.Integer, autoincrement = True, primary_key=True)
    name = db.Column(db.String(126), nullable= False)
    quantidade = db.Column(db.String(126),nullable= False)
    preço = db.Column(db.String(126), nullable= False)
    marca = db.Column(db.String(126),nullable= False)
    tipo = db.Column(db.String(126),nullable= False)
