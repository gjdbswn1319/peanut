import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artists.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id="048596e668f6462aac3d4c1e680cf083", 
        client_secret="29f72ea1157c4026831a73e1b1047905"
    )
)

# Artist Model for SQLite Database
class Artist(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    artist_id = db.Column(db.String(100), unique=True, nullable=False)
    album_length = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Artist {self.artist_id}>"

@app.route('/search', methods=['GET'])
def search_artists():
    search_term = request.args.get('q', '')
    if not search_term:
        return jsonify({'error': 'Search term is required'}), 400

    # Search for the artist using Spotify API
    results = sp.search(q=search_term, type='artist', limit=1)
    artists = results['artists']['items']

    if not artists:
        return jsonify({'error': 'Artist not found'}), 404

    artist = artists[0]
    artist_info = {
        'name': artist['name'],
        'id': artist['id'],
        'image_url': artist['images'][0]['url'] if artist['images'] else None,
        'album_length': len(sp.artist_albums(artist['id'], album_type='album')['items'])
    }

    return jsonify(artist_info)

@app.route('/add', methods=['POST'])
def add_artist():
    data = request.json
    artist_id = data.get('artist_id')
    album_length = data.get('album_length')
    image_url = data.get('image_url')

    # Check if artist already exists
    existing_artist = Artist.query.filter_by(artist_id=artist_id).first()
    if existing_artist:
        return jsonify({'message': 'Artist already exists in the database'}), 400

    # Add the artist to the database
    new_artist = Artist(artist_id=artist_id, album_length=album_length, image_url=image_url)
    db.session.add(new_artist)
    db.session.commit()

    return jsonify({'message': 'Artist added successfully'}), 201

with app.app_context():
    # Create the database and tables if they don't exist
    if not os.path.exists('artists.db'):
        db.create_all()
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)