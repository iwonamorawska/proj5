from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required

from .forms import CreatePostForm

from app.models import Post

blog= Blueprint('blog',__name__, template_folder="blog_templates")

from app.models import db
import requests as r 

@blog.route('/blog/main')
def blogHome():
    Iposts=Post.query.all()
    return render_template('blog.html', posts=Iposts)

@blog.route('/posts/create', methods = ["GET","POST"])
@login_required
def createPost():
    form = CreatePostForm()
    if request.method == "POST":
        if form.validate():
            
            title = form.title.data
            image = form.image.data
            content = form.content.data

            # create instance new post
            post = Post(title, image, content, current_user.id)
            # add instance to databse
            db.session.add(post)
            # commit to databse
            db.session.commit()

            return redirect(url_for('blog.blogHome'))
    return render_template('createpost.html', form = form)

@blog.route('/search/pokemon', methods = ['POST'])
def searchPokemon():
    if request.method == "POST":
        my_pokemon = request.form['poke']
        data = r.get(f'https://pokeapi.co/api/v2/pokemon/{my_pokemon}')
        if data.status_code == 200:
            my_data = data.json()

            pokemon = {
                'name': '',
                'image': '',
                'abilities': []
            }

            for ability in my_data['abilities']:
                pokemon['abilities'].append(ability['ability']['name'])
            pokemon['name'] = my_data['name']
            pokemon['image'] = my_data['sprites']['other']['dream_world']['front_default']
            

            # grab information and pass to a template.
            return render_template('pokemon.html', pokemon = pokemon)
        else:
            pokemon = ''
            return render_template('pokemon.html', pokemon = pokemon)
    return {'hi': 'there'}