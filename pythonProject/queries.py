from flask import request
from model import User, Ideas
from sqlalchemy import func, Integer


def get_all_groups():
    return User.query.all()


def get_idea_by_name():
    return Ideas.query.filter_by(name="1").all()


def select_user_with_gte_5_ideas():
    return db.session.query(User).outerjoin(User.idea).group_by(User).having(func.count(Ideas.id) > 5).all()


def user_count_ideas():
    return db.session.query(db.func.count(Ideas.id)).filter_by(user_id=Ideas.user_id).scalar()


def max_ideas_count():
    return db.session.query(db.func.max(db.func.count(Ideas.id))).join(User).group_by(User.id).scalar()


def delete():
    ideas_to_delete = Ideas.query.filter(Ideas.participants.contains("1")).all()
    for idea in ideas_to_delete:
        db.session.delete(idea)
    db.session.commit()


def update_idea(user_id, idea_id):
    idea = Ideas.query.filter_by(id=idea_id, user_id=user_id).first()
    if not idea:
        return f'Idea with id {idea_id} not found for user with id {user_id}'
    idea = request.form.get('idea')
    if idea:
        Ideas.idea = idea
    db.session.commit()
    return f'Idea with id {idea_id} updated for user with id {user_id}'


if __name__ == "__main__":
    from app import db, app

    with app.app_context():
        result = User.query.all()
        print(result)