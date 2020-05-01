#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_moment import Moment
from config import SQLALCHEMY_DATABASE_URI
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
engine = create_engine(SQLALCHEMY_DATABASE_URI)
conn = engine.connect()
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

from models import *

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
  groups=db.session.query(Venue.city, Venue.state).group_by(Venue.city, Venue.state).order_by(Venue.state, Venue.city).all()
  data=[]

  for group in groups:
    venues = []
    venues_q = Venue.query.filter(Venue.state==group.state).filter(Venue.city==group.city).all()
    for venue_q in venues_q:
      venues.append({
        "id": venue_q.id,
        "name": venue_q.name,
        "num_upcoming_shows": len(venue_q.shows)
      })

    data.append({
      "city": group.city,
      "state": group.state,
      "venues": venues
    })
  
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  searchdata = request.form.get('search_term', '')

  result = conn.execute('SELECT id, name FROM venue WHERE name ILIKE %s','%'+searchdata+'%')
  venues = result.fetchall()
  result.close()
  data = []

  for venue in venues:
    result = conn.execute('SELECT COUNT(*) FROM show WHERE date < NOW() AND venue_id = %s;',venue[0])
    num_upcoming_shows = result.fetchall()
    result.close()
    data.append({
      "id": venue[0],
      "name": venue[1],
      "num_upcoming_shows": num_upcoming_shows
    })

  response={
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  
  try:
    venue = Venue.query.get(venue_id)

    # Corrected PostgreSQL Queries
    past_shows = Venue.getPastShows(venue_id)
    upcoming_shows = Venue.getUpcomingShows(venue_id)


    # Deleted SQLAlchemy ORM Code
    # past_shows = Show.query.filter(Show.venue_id==venue_id).filter(Show.date<datetime.now()).order_by(Show.date)
    # upcoming_shows = Show.query.filter(Show.venue_id==venue_id).filter(Show.date>datetime.now()).order_by(Show.date)

    data={
      "id": venue.id,
      "name": venue.name,
      "genres": venue.genres,
      "address": venue.address,
      "city": venue.city,
      "state": venue.state,
      "phone": venue.phone,
      "website": venue.homepage_link,
      "facebook_link": venue.facebook_link,
      "seeking_talent": venue.seeking,
      "seeking_description": venue.seeking_description,
      "image_link": venue.image_link,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": len(past_shows),
      "upcoming_shows_count": len(upcoming_shows)
    }
    return render_template('pages/show_venue.html', venue=data)
  except:
    return render_template('errors/404.html')

  
  

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

  error = False
  try:
    venue = Venue()
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.phone = request.form['phone']
    venue.address = request.form['address']
    venue.genres = request.form.getlist('genres')
    venue.facebook_link = request.form['facebook_link']
    venue.seeking = True if 'seeking' in request.form else False
    venue.seeking_description = request.form['seeking_description']
    venue.image_link = request.form['image_link']
    venue.homepage_link = request.form['homepage_link']
    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
    if error==False:
      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    else:
      # on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):

  error = False
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()
    if error==False:
      flash('Venue was successfully deleted!')
    else:
      flash('An error occurred. Venue could not be deleted.')

  return redirect(url_for('venues'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data=Artist.query.all()

  if data==None:
    data=[{
        "id": 0,
        "name": "Nothing to find here, yet!",
      }]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  
  searchdata = request.form.get('search_term', '')
  result = conn.execute('SELECT id, name FROM artist WHERE name ILIKE %s','%'+searchdata+'%')
  artists = result.fetchall()
  result.close()
  data = []

  for artist in artists:
    result = conn.execute('SELECT COUNT(*) FROM show WHERE date < NOW() AND artist_id = %s;',artist[0])
    num_upcoming_shows = result.fetchall()
    result.close()
    data.append({
      "id": artist[0],
      "name": artist[1],
      "num_upcoming_shows": num_upcoming_shows
    })

  response={
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

  try:
    artist = Artist.query.get(artist_id)

    # Corrected PostgresSQL Queries
    past_shows = Artist.getPastShows(artist_id)
    upcoming_shows = Artist.getUpcomingShows(artist_id)
    
    # Deleted SQLAlchemy ORM Code
    #past_shows =  Show.query.filter(Show.artist_id==artist_id).filter(Show.date<datetime.now()).order_by(Show.date)
    #upcoming_shows = Show.query.filter(Show.artist_id==artist_id).filter(Show.date>datetime.now()).order_by(Show.date)

    data={
      "id": artist.id,
      "name": artist.name,
      "genres": artist.genres,
      "city": artist.city,
      "state": artist.state,
      "phone": artist.phone,
      "website": artist.homepage_link,
      "facebook_link": artist.facebook_link,
      "seeking_venue": artist.seeking,
      "seeking_description": artist.seeking_description,
      "image_link": artist.image_link,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
      "past_shows_count":len(past_shows),
      "upcoming_shows_count": len(upcoming_shows)
    }
    return render_template('pages/show_artist.html', artist=data)
  except:
    return render_template('errors/404.html')

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  try:
    artist = Artist.query.get(artist_id)

    data={
      "id": artist.id,
      "name": artist.name,
      "genres": artist.genres,
      "city": artist.city,
      "state": artist.state,
      "phone": artist.phone,
      "website": artist.homepage_link,
      "facebook_link": artist.facebook_link,
      "seeking_venue": artist.seeking,
      "seeking_description": artist.seeking_description,
      "image_link": artist.image_link,
    }
    form.name.data = artist.name
    form.genres.data = artist.genres
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.homepage_link.data = artist.homepage_link
    form.facebook_link.data = artist.facebook_link
    form.seeking.data = artist.seeking
    form.seeking_description.data = artist.seeking_description
    form.image_link.data = artist.image_link

    return render_template('forms/edit_artist.html', form=form, artist=data)
  except:
    return render_template('errors/404.html')

  
@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  error = False
  try:
    artist = Artist.query.get(artist_id)
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.genres = request.form.getlist('genres')
    artist.facebook_link = request.form['facebook_link']
    artist.seeking = True if 'seeking' in request.form else False
    artist.seeking_description = request.form['seeking_description']
    artist.image_link = request.form['image_link']
    artist.homepage_link = request.form['homepage_link']
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
    if error==False:
      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully updated!')
    else:
      # on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
  
  return redirect(url_for('show_artist', artist_id=artist_id))



@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  
  try:
    venue = Venue.query.get(venue_id)

    data={
      "id": venue.id,
      "name": venue.name,
      "genres": venue.genres,
      "address": venue.address,
      "city": venue.city,
      "state": venue.state,
      "phone": venue.phone,
      "website": venue.homepage_link,
      "facebook_link": venue.facebook_link,
      "seeking_talent": venue.seeking,
      "seeking_description": venue.seeking_description,
      "image_link": venue.image_link,
    }
    form.name.data = venue.name
    form.genres.data = venue.genres
    form.city.data = venue.city
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.homepage_link.data = venue.homepage_link
    form.facebook_link.data = venue.facebook_link
    form.seeking.data = venue.seeking
    form.seeking_description.data = venue.seeking_description
    form.image_link.data = venue.image_link
    form.address.data = venue.address

    return render_template('forms/edit_venue.html', form=form, venue=data)
  except:
    return render_template('errors/404.html')

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error = False
  try:
    venue = Venue.query.get(venue_id)
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.phone = request.form['phone']
    venue.address = request.form['address']
    venue.genres = request.form.getlist('genres')
    venue.facebook_link = request.form['facebook_link']
    venue.seeking = True if 'seeking' in request.form else False
    venue.seeking_description = request.form['seeking_description']
    venue.image_link = request.form['image_link']
    venue.homepage_link = request.form['homepage_link']
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
    if error==False:
      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully updated!')
    else:
      # on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
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
  error = False
  try:
    artist = Artist()
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.genres = request.form.getlist('genres')
    artist.facebook_link = request.form['facebook_link']
    artist.seeking = True if 'seeking' in request.form else False
    artist.seeking_description = request.form['seeking_description']
    artist.image_link = request.form['image_link']
    artist.homepage_link = request.form['homepage_link']
    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
    if error==False:
      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    else:
      # on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  

  return render_template('pages/home.html')
  
#  Delete Artists
#  ----------------------------------------------------------------

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):

  error = False
  try:
    artist = Artist.query.get(artist_id)
    db.session.delete(artist)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()
    if error==False:
      flash('Artist was successfully deleted!')
    else:
      flash('An error occurred. Artist could not be deleted.')

  return redirect(url_for('artists'))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  shows = Show.query.order_by(Show.date).all()
  data = []

  for show in shows:
    
    currdata={
      "venue_id": show.venue.id,
      "venue_name": show.venue.name,
      "artist_id": show.artist.id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.date.strftime("%Y-%m-%dT%H:%M:%S")
    }
    data.append(currdata)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():

  error = False
  venue_not_found = False
  artist_not_found = False
  show = Show()

  try:
    show = Show()
    show_artist = Artist.query.get(request.form['artist_id'])
    if show_artist == None: artist_not_found = True    
    show_venue = Venue.query.get(request.form['venue_id']) 
    if show_venue == None: venue_not_found = True
    
    show_date = request.form['start_time']
    

    show.artist = show_artist
    show.venue = show_venue 
    show.date = show_date

    db.session.add(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
    if error==False and venue_not_found==False and artist_not_found==False:
      # on successful db insert, flash success
      flash('Show was successfully listed!')
    else:
      errortext="An error occured. " 
      if venue_not_found:
        errortext = errortext + "The Venue Id doesn't exist! " 

      if artist_not_found:
        errortext = errortext + "The Artist Id doesn't exist! "

      errortext = errortext + "Your show could not be listed."
      flash(errortext)

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
