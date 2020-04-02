import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.fetch import fetch_data as fetch_data_func
from app.fetch import fetch_players as fetch_players_func
from app.fetch import test_firebase as test_firebase_func
from app.fetch import test_process_user as test_process_new_match_function

from app import create_app, db

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def fetch_data():
    fetch_data_func(app, db)

@manager.command
def fetch_players():
    fetch_players_func(app, db)

@manager.command
def test_firebase():
    test_firebase_func()

@manager.command
def test_process_new_match():
    test_process_new_match_function()

if __name__ == '__main__':
    manager.run()