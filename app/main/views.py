from flask import render_template
from . import main
from .. import db
from ..models import Pitch
from flask_login import login_required

# Views
@main.route('/')
def index():
    '''
    View page function that returns the pitch titles on the index page
    '''
    # interviews = Pitch.query.get('interviews)
    # inspirational = get_pitch('inspirational')
    # general = get_pitch('general')



    title = 'Welcome to the Pitch Page'
    return render_template('index.html', title=title)

@main.route('/pitch/<int:id>')
def pitch(id):
    '''
    View pitch function that returns the details of the pitch as well as enable the reation of a comment
    '''
    pitch = Pitch.query.get(id)

    title = 'Welcome to the Pitch Page'

    if pitch is None:
        abort(404)

    comment =  Comments.get_comments(id)
    
    return render_template('pitch.html', title=title)


@main.route('/pitch/comments/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_comment(id):
    form = CommentsForm()
    pitch = Pitch.query.filter_by(id)
    if form.validate_on_submit():
        title = form.title.data
        comment = form.comment.data

        # Updated review instance
        new_pitch = Pitch(pitch_id=pitch.id,pitch_title=title,pitch_comment=comment,user=current_user)

        # save review method
        new_pitch.save_review()
        return redirect(url_for('.pitch',id = pitch.id ))

    title = f'{pitch.title} comment'
    return render_template('new_comment.html',title = title, comment_form=form, pitch=pitch)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)



