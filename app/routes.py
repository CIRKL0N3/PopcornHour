from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Movie, Rating
from . import db
from .forms import LoginForm, SignupForm
from werkzeug.utils import secure_filename

# Define un Blueprint
routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registro exitoso. Ahora puedes iniciar sesión.')
        return redirect(url_for('routes.login'))
    return render_template('signup.html', form=form)

@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('routes.dashboard'))
        flash('Credenciales incorrectas.')
    return render_template('login.html', form=form)

@routes.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@routes.route('/manage_movies')
@login_required
def manage_movies():
    if current_user.role != 'moderator':
        flash("No tienes permiso para gestionar películas.")
        return redirect(url_for('routes.dashboard'))
    
    movies = Movie.query.filter_by(moderator_id=current_user.id).all()
    return render_template('manage_movies.html', movies=movies)

@routes.route('/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    if current_user.role != 'moderator':
        flash("No tienes permiso para agregar películas.")
        return redirect(url_for('routes.dashboard'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        image = request.files.get('image')

        if not title or not description:
            flash("Todos los campos son obligatorios.")
            return redirect(url_for('routes.add_movie'))

        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
        else:
            filename = None

        new_movie = Movie(title=title, description=description, image=filename, moderator_id=current_user.id)
        db.session.add(new_movie)
        db.session.commit()
        flash("Película agregada exitosamente.")
        return redirect(url_for('routes.dashboard'))

    return render_template('add_movie.html')

@routes.route('/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit_movie(movie_id):
    if current_user.role != 'moderator':
        flash("No tienes permiso para editar películas.")
        return redirect(url_for('routes.dashboard'))
    
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        movie.title = request.form.get('title')
        movie.description = request.form.get('description')
        db.session.commit()
        flash("Película actualizada exitosamente.")
        return redirect(url_for('routes.manage_movies'))
    
    return render_template('edit_movie.html', movie=movie)

@routes.route('/delete_movie/<int:movie_id>', methods=['POST'])
@login_required
def delete_movie(movie_id):
    if current_user.role != 'moderator':
        flash("No tienes permiso para eliminar películas.")
        return redirect(url_for('routes.dashboard'))
    
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("Película eliminada.")
    return redirect(url_for('routes.manage_movies'))

@routes.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    ratings = Rating.query.filter_by(movie_id=movie_id).all()
    return render_template('movie_details.html', movie=movie, ratings=ratings)

@routes.route('/movies')
def list_movies():
    movies = Movie.query.all()
    return render_template('movies.html', movies=movies)

@routes.route('/rate_movie/<int:movie_id>', methods=['POST'])
@login_required
def rate_movie(movie_id):
    if current_user.role != 'standard':
        flash("Solo los usuarios estándar pueden calificar.")
        return redirect(url_for('routes.movie_details', movie_id=movie_id))

    movie = Movie.query.get_or_404(movie_id)
    rating = request.form.get('rating')
    comment = request.form.get('comment')

    if not rating:
        flash("La calificación es obligatoria.")
        return redirect(url_for('routes.movie_details', movie_id=movie_id))

    new_rating = Rating(user_id=current_user.id, movie_id=movie_id, rating=rating, comment=comment)
    db.session.add(new_rating)
    db.session.commit()
    flash("Tu calificación y comentario han sido agregados.")
    return redirect(url_for('routes.movie_details', movie_id=movie_id))


@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))
