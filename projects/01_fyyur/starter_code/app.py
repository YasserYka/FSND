#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, and_
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

# Done: connect to a local postgresql database
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app, session_options={"expire_on_commit": False})
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Utils.
#----------------------------------------------------------------------------#

def tuple_to_dict(result):
  return [r._asdict() for r in result]

# convert ORM object intp dict
def object_to_dict(result):
  return result.__dict__

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

Show = db.Table('Show',
    db.Column('Artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
    db.Column('Venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
    db.Column('start_time', db.DateTime)
)

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))
    artists = db.relationship('Artist', secondary=Show, backref=db.backref('venues', lazy=True))

    def __repr__(self):
      return f'<id={self.id}, name={self.name}>'

    # Done: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))

    def __repr__(self):
      return f'<id={self.id}, name={self.name}>' 

    # Done: implement any missing fields, as a database migration using Flask-Migrate

# Done Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # Done: replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.

  query_result = tuple_to_dict(Venue.query.with_entities(Venue.city, Venue.state).distinct().all())
  
  for result in query_result:
    
    result['venues'] = tuple_to_dict(Venue.query.filter_by(city=result['city'], state=result['state']).with_entities(Venue.id, Venue.name).all())
    
    for venue in result['venues']:

      venue['num_upcoming_shows'] = db.session.query(Show).filter(and_(Show.c.Venue_id==venue['id'], Show.c.start_time > datetime.now())).count()

  return render_template('pages/venues.html', areas=query_result)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # Done: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')

  result = {'count': 0, 'data': []}

  result['data'] = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  result['count'] = len(result['data'])

  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=result, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # Done: replace with real venue data from the venues table, using venue_id

  query_result = object_to_dict(Venue.query.filter(Venue.id==venue_id).first())

  query_result['past_shows'] = tuple_to_dict(db.session.query(Show.c.start_time, Artist.id.label("artist_id"), Artist.name.label("artist_name"), Artist.image_link.label("artist_image_link")).filter(and_(Show.c.Venue_id==query_result['id'], Show.c.start_time < datetime.now())).all())

  # convert datetime object into iso string format
  for past_show in query_result['past_shows']:
      past_show['start_time'] = past_show['start_time'].isoformat()

  query_result['past_shows_count'] = len(query_result['past_shows'])

  query_result['upcoming_shows'] = tuple_to_dict(db.session.query(Show.c.start_time, Artist.id.label("artist_id"), Artist.name.label("artist_name"), Artist.image_link.label("artist_image_link")).filter(and_(Show.c.Venue_id==query_result['id'], Show.c.start_time > datetime.now())).all())

  # convert datetime object into iso string format
  for upcoming_show in query_result['upcoming_shows']:
      upcoming_show['start_time'] = upcoming_show['start_time'].isoformat()

  query_result['upcoming_shows_count'] = len(query_result['upcoming_shows'])

  return render_template('pages/show_venue.html', venue=query_result)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # Done: insert form data as a new Venue record in the db, instead
  # Done: modify data to be the data object returned from db insertion

  form = VenueForm()
  error = False

  if not form.validate():
    flash(form.errors)
    return redirect(url_for('create_venue_submission'))
  
  try:
    venue = Venue(name=form.name.data, city=form.city.data, state=form.state.data, address=form.address.data, phone=form.phone.data, genres=form.genres.data, image_link=form.image_link.data, facebook_link=form.facebook_link.data)
    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally: 
    db.session.close()

  if not error:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  else:
    flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')

  # on successful db insert, flash success
  # Done: on unsuccessful db insert, flash an error instead.
  # e.g., 
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # Done: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    venue = Venue.query.filter(Venue.id==venue_id).first()
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # Done: replace with real data returned from querying the database

  query_result = tuple_to_dict(Artist.query.with_entities(Artist.id, Artist.name).all())

  return render_template('pages/artists.html', artists=query_result)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # Done: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_term = request.form.get('search_term', '')

  result = {'count': 0, 'data': []}

  result['data'] = tuple_to_dict(Artist.query.with_entities(Artist.id, Artist.name).filter(Artist.name.ilike(f'%{search_term}%')).all())
  result['count'] = len(result['data'])

  for artist in result['data']:
    artist['num_upcoming_shows'] = db.session.query(Show).filter(and_(Show.c.Artist_id==artist['id'], Show.c.start_time > datetime.now())).count()

  return render_template('pages/search_artists.html', results=result, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # Done: replace with real venue data from the venues table, using venue_id
  
  query_result = object_to_dict(Artist.query.filter(Artist.id==artist_id).first())

  query_result['past_shows'] = tuple_to_dict(db.session.query(Show.c.start_time, Venue.id.label("venue_id"), Venue.name.label("venue_name"), Venue.image_link.label("venue_image_link")).filter(and_(Show.c.Artist_id==query_result['id'], Show.c.start_time < datetime.now())).all())

  # convert datetime object into iso string format
  for past_show in query_result['past_shows']:
      past_show['start_time'] = past_show['start_time'].isoformat()

  query_result['past_shows_count'] = len(query_result['past_shows'])

  query_result['upcoming_shows'] = tuple_to_dict(db.session.query(Show.c.start_time, Venue.id.label("venue_id"), Venue.name.label("venue_name"), Venue.image_link.label("venue_image_link")).filter(and_(Show.c.Artist_id==query_result['id'], Show.c.start_time > datetime.now())).all())

  # convert datetime object into iso string format
  for upcoming_show in query_result['upcoming_shows']:
      upcoming_show['start_time'] = upcoming_show['start_time'].isoformat()

  query_result['upcoming_shows_count'] = len(query_result['upcoming_shows'])

  return render_template('pages/show_artist.html', artist=query_result)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  
  artist = Artist.query.filter(Artist.id==artist_id).first()

  if artist is None:
    flash(f'Artist with ID {artist_id} not found.')
    return redirect(url_for('index'))

  form = ArtistForm(obj=artist)

  # Done: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # Done: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm()

  if not form.validate():
    flash(form.errors)
    return redirect(url_for('edit_artist'))


  artist = Artist.query.filter(Artist.id==artist_id).first()

  if artist is None:
    flash(f'Artist with ID {artist_id} not found.')
    return redirect(url_for('index'))

  artist.name = form.name.data
  artist.city = form.city.data
  artist.state = form.state.data
  artist.phone = form.phone.data
  artist.genres = form.genres.data
  artist.facebook_link = form.facebook_link.data

  db.session.commit()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.filter(Venue.id==venue_id).first()

  if venue is None:
    flash(f'Venue with ID {venue_id} not found.')
    return redirect(url_for('index'))

  form = VenueForm(obj=venue)
  # Done: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # Done: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  form = VenueForm()

  if not form.validate():
    flash(form.errors)
    return redirect(url_for('edit_venue'))


  venue = Venue.query.filter(Venue.id==venue_id).first()

  if venue is None:
    flash(f'Venue with ID {venue_id} not found.')
    return redirect(url_for('index'))

  venue.address = form.address.data
  venue.name = form.name.data
  venue.city = form.city.data
  venue.state = form.state.data
  venue.phone = form.phone.data
  venue.genres = form.genres.data
  venue.facebook_link = form.facebook_link.data

  db.session.commit()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # Done: insert form data as a new Venue record in the db, instead
  # Done: modify data to be the data object returned from db insertion

  form = ArtistForm()
  error = False

  if not form.validate():
    flash(form.errors)
    return redirect(url_for('create_artist_submission'))

  try:
    artist = Artist(name=form.name.data, city=form.city.data, state=form.state.data, phone=form.phone.data, genres=form.genres.data, image_link=form.image_link.data, facebook_link=form.facebook_link.data)
    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally: 
    db.session.close()

  if not error:
    flash('Artist ' + form.name.data + ' was successfully listed!')
  else:
    flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')

  # on successful db insert, flash success
  # Done: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # Done: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  query_result = tuple_to_dict(db.session.query(Show.c.start_time, Venue.id.label("venue_id"), Venue.name.label("venue_name"),  Artist.id.label("artist_id"), Artist.name.label("artist_name"), Artist.image_link.label("artist_image_link")).filter(and_(Show.c.Artist_id==Artist.id, Show.c.Venue_id==Venue.id)).all())

 # convert datetime object into iso string format
  for upcoming_show in query_result:
      upcoming_show['start_time'] = upcoming_show['start_time'].isoformat()


  return render_template('pages/shows.html', shows=query_result)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # Done: insert form data as a new Show record in the db, instead

  form = ShowForm()
  error = False

  if not form.validate():
    flash(form.errors)
    return redirect(url_for('create_show_submission'))

  try:
    show = Show.insert().values(Venue_id=form.venue_id.data, Artist_id=form.artist_id.data, start_time=form.start_time.data)
    db.session.execute(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally: 
    db.session.close()

  if not error:
    flash('Show was successfully listed!')
  else:
    flash('An error occurred. Show could not be listed.')


  # on successful db insert, flash success
  # Done: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
