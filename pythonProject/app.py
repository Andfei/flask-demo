from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from marshmallow import ValidationError

from shemas import IdeaSchema
from model import db, User, Ideas


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return 'Home'

@app.route('/home', methods=["GET"])
def show_home():
    return render_template("home.html", user=User.query.all())


@app.route('/create_user', methods=["POST", "GET"])
def create_user():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        # create new user
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("show_home"))
    else:
        return render_template("create_user.html")

@app.route('/idea/<int:user_id>', methods=["GET"])
def show_ideas(user_id):
    return render_template("idea.html", idea=Ideas.query.filter_by(user_id=user_id).all(),
    user=User.query.get(user_id))

@app.route('/create_idea', methods=["POST", "GET"])
def create_idea():
    if request.method == "POST":
        data = request.form
        schema = IdeaSchema()

        try:
            result = schema.load(data)
        except ValidationError as error:
            return render_template("create_idea.html", errors=error, data=data)
        # create new idea
        new_idea = Ideas(idea=result["idea"], user_id=result["user_id"])
        db.session.add(new_idea)
        db.session.commit()
        return redirect(url_for("show_home"))
    else:
        return render_template("create_idea.html", user=User.query.all())

if __name__ == '__main__':
    app.run(debug=True)
