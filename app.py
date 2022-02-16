from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from typing import Callable
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField
from flask_bootstrap import Bootstrap


class CreatePostForm(FlaskForm):
    name = StringField("Cafe name", validators=[DataRequired()])
    map_url = StringField("map url URL", validators=[DataRequired()])
    img_url = StringField("img url URL", validators=[DataRequired()])
    location = StringField("location", validators=[DataRequired()])
    seats = StringField("seats", validators=[DataRequired()])
    has_toilet = StringField("has_toilet", validators=[DataRequired()])
    has_wifi = StringField("has_wifi", validators=[DataRequired()])
    has_sockets = StringField("has_sockets", validators=[DataRequired()])
    can_take_calls = StringField("can_take_calls", validators=[DataRequired()])
    coffee_price = StringField("coffee_price", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

class MyAlchemy(SQLAlchemy):
    Column: Callable
    String: Callable
    Integer: Callable
    Float: Callable
    Boolean: Callable


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database = MyAlchemy(app)


class Cafe(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(250), unique=True, nullable=False)
    map_url = database.Column(database.String(500), nullable=False)
    img_url = database.Column(database.String(500), nullable=False)
    location = database.Column(database.String(250), nullable=False)
    seats = database.Column(database.String(250), nullable=False)
    has_toilet = database.Column(database.String(250), nullable=False)
    has_wifi = database.Column(database.String(250), nullable=False)
    has_sockets = database.Column(database.String(250), nullable=False)
    can_take_calls = database.Column(database.String(250), nullable=False)
    coffee_price = database.Column(database.String(250), nullable=True)


all_cafe = database.session.query(Cafe).all()


@app.route("/")
def home():
    return render_template("index.html", all_cafe=all_cafe)


@app.route("/post/<int:cafe_id>", methods=["POST", "GET"])
def show_post(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    return render_template("post.html", id=cafe_id, cafe=cafe)


@app.route("/new-post", methods=["POST", "GET"])
def add_new_cafe():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            seats=form.seats.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            has_sockets=form.has_sockets.data,
            can_take_calls=form.can_take_calls.data,
            coffee_price=form.coffee_price.data
        )
        database.session.add(new_post)
        database.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", form=form)


@app.route("/edit-post/<int:cafe_id>", methods=["POST", "GET"])
def edit_post(cafe_id):
    post = Cafe.query.get(cafe_id)
    edit_form = CreatePostForm(
        name=post.name,
        map_url=post.map_url,
        img_url=post.img_url,
        location=post.location,
        seats=post.seats,
        has_toilet=post.has_toilet,
        has_wifi=post.has_wifi,
        has_sockets=post.has_sockets,
        can_take_calls=post.can_take_calls,
        coffee_price=post.coffee_price
    )
    if edit_form.validate_on_submit():
        post.name = edit_form.name.data
        post.map_url = edit_form.map_url.data
        post.img_url = edit_form.img_url.data
        post.location = edit_form.location.data
        post.seats = edit_form.seats.data
        post.has_toilet = edit_form.has_toilet.data
        post.has_wifi = edit_form.has_wifi.data
        post.has_sockets = edit_form.has_sockets.data
        post.can_take_calls = edit_form.can_take_calls.data
        post.coffee_price = edit_form.coffee_price.data
        database.session.commit()
        return redirect(url_for("home", post_id=post.id))

    return render_template("edit.html", form=edit_form)


@app.route("/delete/<int:cafe_id>")
def delete_post(cafe_id):
    post_to_delete = Cafe.query.get(cafe_id)
    database.session.delete(post_to_delete)
    database.session.commit()
    return redirect(url_for('home'))


app.run(debug=False, host="0.0.0.0")
