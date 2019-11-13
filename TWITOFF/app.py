""" """
from decouple import config
from flask import Flask, escape, render_template, request, url_for
from twitter_scraper import get_tweets
from .models import DB, User
from .twitter import BASILICA, TWITTER

# elons_tweets = []
# for tweet in get_tweets('elonmusk', pages=2):
#     elons_tweets.append(tweet['text'])

# Now we want to make an app factory


def create_app():
    app = Flask(__name__)
    if __name__ == '__main__':
        app.run(debug=True)

    # Add our config
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Now have database
    DB.init_app(app) 

    @app.route('/')
    def home():
        # Home page which shows all users and tweets
        users = User.query.all()
        return render_template('home.html', title='Home', users=users)

    # Adds users or gets user
    @app.route('/user', methods=['POST']) # uses form
    @app.route('/user/<name>', methods=['GET']) # needs name param
    # methods is plural here, singular in template
    def user(name=None, message=''):
        try:
            if request.method == 'POST':
                add_or_update_user(name):
                message = "User {} successfully added!".format(name)
            tweets = User.query.filter(User.name==name).one().tweets
        except Exception as e:
            message = "Error adding {}: {}.".format(name,e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets,
        message=message)


    @app.route('/user/<username>', methods=['GET'])
    def show_user_profile(username):
        # Shows a user page with their tweets
        twitter_user = TWITTER.get_user(str(username))
        tweets = twitter_user.timeline(count=200, exclude_replies=True,
                                       include_rts=False)
        return render_template('user_tweets.html', username=username,
                               tweets=tweets)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('home.html', title='Reset', users=[])

    return app
