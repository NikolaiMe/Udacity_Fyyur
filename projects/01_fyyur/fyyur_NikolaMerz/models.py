from app import db, conn



class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    seeking = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(), nullable=True)
    homepage_link = db.Column(db.String(120), nullable=True)
    shows = db.relationship('Show', backref='venue', cascade="all, delete-orphan", lazy=True)

    @staticmethod
    def getPastShows(venue_id):
        result = conn.execute('''
            SELECT 
                artist.id,
                artist.image_link,
                artist.name,
                show.date 
            FROM 
                show 
            INNER JOIN 
                artist 
            ON (show.artist_id = artist.id) 
            WHERE 
                show.venue_id = %s 
            AND
                show.date < NOW()
            ORDER BY 
                show.date;'''
        , venue_id)

        showList = result.fetchall()
        result.close()

        pastShows = []

        for show in showList:
            pastShows.append({
                "artist_id" : show[0],
                "artist_image_link" : show[1],
                "artist_name" : show[2],
                "show_date" : show[3]
            })

        return pastShows

    @staticmethod
    def getUpcomingShows(venue_id):
        result = conn.execute('''
            SELECT 
                artist.id,
                artist.image_link,
                artist.name,
                show.date 
            FROM 
                show 
            INNER JOIN 
                artist 
            ON (show.artist_id = artist.id) 
            WHERE 
                show.venue_id = %s 
            AND
                show.date > NOW()
            ORDER BY 
                show.date;'''
        , venue_id)

        showList = result.fetchall()
        result.close()

        pastShows = []

        for show in showList:
            pastShows.append({
                "artist_id" : show[0],
                "artist_image_link" : show[1],
                "artist_name" : show[2],
                "show_date" : show[3]
            })

        return pastShows


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    seeking = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(), nullable=True)
    homepage_link = db.Column(db.String(120), nullable=True)
    shows = db.relationship('Show', backref='artist', cascade="all, delete-orphan", lazy=True)

    @staticmethod
    def getPastShows(artist_id):
        result = conn.execute('''
            SELECT 
                venue.id,
                venue.image_link,
                venue.name,
                show.date 
            FROM 
                show 
            INNER JOIN 
                venue 
            ON (show.venue_id = venue.id) 
            WHERE 
                show.artist_id = %s 
            AND
                show.date < NOW()
            ORDER BY 
                show.date;'''
        , artist_id)

        showList = result.fetchall()
        result.close()

        pastShows = []

        for show in showList:
            pastShows.append({
                "venue_id" : show[0],
                "venue_image_link" : show[1],
                "venue_name" : show[2],
                "show_date" : show[3]
            })

        return pastShows

    @staticmethod
    def getUpcomingShows(artist_id):
        result = conn.execute('''
            SELECT 
                venue.id,
                venue.image_link,
                venue.name,
                show.date 
            FROM 
                show 
            INNER JOIN 
                venue 
            ON (show.venue_id = venue.id) 
            WHERE 
                show.artist_id = %s 
            AND
                show.date > NOW()
            ORDER BY 
                show.date;'''
        , artist_id)

        showList = result.fetchall()
        result.close()

        pastShows = []

        for show in showList:
            pastShows.append({
                "venue_id" : show[0],
                "venue_image_link" : show[1],
                "venue_name" : show[2],
                "show_date" : show[3]
            })

        return pastShows

    

class Show(db.Model):
  __tablename__ = 'show'

  id = db.Column(db.Integer, primary_key = True)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable = False)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable = False)
  date = db.Column(db.DateTime(), nullable = False )
