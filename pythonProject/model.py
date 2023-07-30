from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)

    Ideas = db.relationship("Ideas", backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username} {self.email}>'


class Ideas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idea = db.Column(db.String(128), index=True, unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    def __repr__(self):
        return f'<Idea {self.idea}>'

