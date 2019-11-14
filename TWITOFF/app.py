"""Build my app factory and do routes and configuration"""
from decouple import config
from dotenv import load_dotenv
from flask import Flask, render_template, request
from .models import DB, User
from .predict import predict_user
from .twitter import add_or_update_user, BASILICA, TWITTER


load_dotenv()


def create_app():
    app = Flask(__name__)

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

    # Adding in a new route to add users or get users
    @app.route('/user', methods=['POST'])  # uses form
    @app.route('/user/<name>', methods=['GET'])  # needs parameter
    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} successfully added!".format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error adding {}: {}".format(name,e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets,
        message=message)
    
    # Adding predictions route
    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1, user2 = sorted([request.values['user1'],
                               request.values['user2']])
        if user1 == user2:
            message = 'Must compare unique users'
        else:
            prediction = predict_user(user1, user2, request.values['tweet_text'])
            message = '"{}" is more likely from {} than {}'.format(
                request.values['tweet_text'], user1 if prediction else user2,
                user2 if prediction else user1)
        return render_template('prediction.html', title='Prediction', message=message)

    # @app.route('/user/<username>', methods=['GET'])
    # def show_user_profile(username):
    #     # Shows a user page with their tweets
    #     twitter_user = TWITTER.get_user(str(username))
    #     tweets = twitter_user.timeline(count=200, exclude_replies=True,
    #                                    include_rts=False)
    #     return render_template('user_tweets.html', username=username,
    #                            tweets=tweets)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('home.html', title='Reset', users=[])

    if __name__ == '__main__':
        app.run(debug=True)
    return app
