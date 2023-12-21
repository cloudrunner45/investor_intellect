
from sqlalchemy import create_engine, Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
# look into user mixin 
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt

from . import db, app

# creation of three database's 

# holds user info 
class User_cred(UserMixin, db.Model):
    __tablename__ = 'user_cred'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    user_email = db.Column(db.String(15), unique=True, nullable=False)
    password_hash = db.Column(db.String(200),  nullable=False)
    # Relationship to user_stock_info table
    stock_info = relationship('User_notes', backref='user_cred', lazy=True)
    watchlists = relationship('Watchlist', backref='user_cred', lazy=True) 
    def __repr__(self):
        return f'<User {self.username}>'
    
    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
    






# holds user notes on stocks
class User_notes(db.Model):
    __tablename__ = 'user_notes'
    user_id = db.Column(db.Integer, ForeignKey('user_cred.id'), nullable=False, primary_key=True)
    ticker = db.Column(db.String(15), nullable=False, primary_key=True)
    ticker_notes = db.Column(db.String(10000), nullable=False)


#holds the user's watchlist
class Watchlist(db.Model):
    __tablename__ = 'watchlist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user_cred.id'), nullable=False)
    ticker = db.Column(db.String(15), nullable=False) 


with app.app_context():
    db.create_all()





# watchlist #

# functions for add and removing tickers to watchlist
def check_if_already_in_watchlist(ticker, user_id):
    ticker_list = []
    user_tickers = db.session.query(Watchlist).filter(Watchlist.user_id == user_id).all()
    for tic in user_tickers:
        ticker_list.append(tic.ticker)
    
    if ticker in ticker_list:
        return True
    else:
        return False

 
def save_to_watchlist_db(ticker, user_id):

    if check_if_already_in_watchlist(ticker, user_id) == False:
        new_record = Watchlist(user_id=user_id, ticker=ticker)
        db.session.add(new_record)
        db.session.commit()

def remove_from_watchlist(ticker, user_id):
    stonk_to_remove = db.session.query(Watchlist).filter(Watchlist.user_id == user_id, Watchlist.ticker == ticker).first()
    db.session.delete(stonk_to_remove)
    db.session.commit()



def get_user_watchlist(user_id):
        ticker_list = []
        user_tickers = db.session.query(Watchlist).filter(Watchlist.user_id == user_id).all()
        for tic in user_tickers:
            ticker_list.append(tic.ticker)
        return ticker_list


#watchlist #



#notes#

#fucntions for hadllineng the users notes
def save_to_note_db(user_id, ticker, note):
    if check_if_note_exist(user_id, ticker) == False:
        create_new_note(user_id, ticker, note)
    else:
        update_note(user_id, ticker, note)


def check_if_note_exist(user_id, ticker):
    check_note = db.session.query(User_notes).filter(User_notes.user_id == user_id, User_notes.ticker == ticker).first()
    if check_note == None:
        return False
    else:
        return True



def create_new_note(user_id, ticker, note):
    new_record = User_notes(user_id=user_id, ticker=ticker, ticker_notes=note)
    db.session.add(new_record)
    db.session.commit()

def update_note(user_id, ticker, note):
    get_note = db.session.query(User_notes).filter(User_notes.user_id == user_id, User_notes.ticker == ticker).first()
    get_note.ticker_notes = note
    db.session.commit()
    print("succes from update ")


        
      
