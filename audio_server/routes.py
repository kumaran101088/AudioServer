import datetime
from .extensions import db
from .models import Song, Podcast, Audiobook
from flask import Blueprint, jsonify, request

main = Blueprint('main', __name__)

@main.route('/<audio_type>', methods=['GET'])
@main.route('/<audio_type>/<int:audio_id>', methods=['GET'])
def fetch(audio_type, audio_id=None):
    if audio_type.lower() in ['song', 'podcast', 'audiobook']:
        if audio_type.lower() == 'song' and audio_id == None:
            all_songs = [{'id':song.id, 'name':song.name, 'duration':song.duration, 'upload':song.upload} for song in Song.query.all()]
            return jsonify(songs=all_songs), 200
        elif audio_type.lower() == 'song' and audio_id != None:
            song = Song.query.filter_by(id=audio_id).first()
            if song:
                return jsonify({'id':song.id, 'name':song.name, 'duration':song.duration, 'upload':song.upload}), 200
            else:
                return jsonify({'Song not found':'400 bad request'}), 400
        elif audio_type.lower() == 'podcast' and audio_id == None:
            all_podcasts = [{'id':podcast.id, 'name':podcast.name, 'duration':podcast.duration, 'upload':podcast.upload, 'host':podcast.host, 'participants':podcast.participants} for podcast in Podcast.query.all()]
            return jsonify(podcasts=all_podcasts), 200
        elif audio_type.lower() == 'podcast' and audio_id != None:
            podcast = Podcast.query.filter_by(id=audio_id).first()
            if podcast:
                return jsonify({'id':podcast.id, 'name':podcast.name, 'duration':podcast.duration, 'upload':podcast.upload, 'host':podcast.host, 'participants':podcast.participants}), 200
            else:
                return jsonify({'Podcast not found': '400 bad request '}), 400
        elif audio_type.lower() == 'audiobook' and audio_id == None:
            all_audiobooks = [{'id':audiobook.id, 'title':audiobook.title, 'author':audiobook.author, 'narrator':audiobook.narrator, 'duration':audiobook.duration, 'upload':audiobook.upload} for audiobook in Audiobook.query.all()]
            return jsonify(audiobooks=all_audiobooks), 200
        elif audio_type.lower() == 'audiobook' and audio_id != None:
            audiobook = Audiobook.query.filter_by(id=audio_id).first()
            if audiobook:
                return jsonify({'id':audiobook.id, 'title':audiobook.title, 'author':audiobook.author, 'narrator':audiobook.narrator, 'duration':audiobook.duration, 'upload':audiobook.upload}), 200
            else:
                return jsonify({'Audiobook not found' : '400 bad request '}), 400
    else:
        return jsonify({'This request is invalid' : '400 bad request'}), 400

@main.route('/<audio_type>/add', methods=['POST'])
def add(audio_type):
    if audio_type.lower() in ['song', 'podcast', 'audiobook']:
        if audio_type.lower() == 'song':
            requests = request.get_json()
            name = requests['name']
            duration = requests['duration']
            if duration >= 0:
                new_song = Song(name=name, duration=duration, upload=datetime.datetime.now())
                db.session.add(new_song)
                db.session.commit()
                return jsonify({'Action is successful' : '200 OK'}), 200
            else:
                return jsonify({'Duration must be positive' : '400 bad request'}), 400
        elif audio_type.lower() == 'podcast':
            requests = request.get_json()
            name = requests['name']
            duration = requests['duration']
            host = requests['host']
            try:
                participants = requests['participants']
            except:
                participants = None
            if duration >= 0 and participants == None:
                new_podcast = Podcast(name=name, duration=duration, upload=datetime.datetime.now(), host=host)
                db.session.add(new_podcast)
                db.session.commit()
                return jsonify({'Action is successful' : '200 OK'}), 200
            elif duration >= 0 and participants != None:
                if 0 <= len(participants) <= 10:
                    new_podcast = Podcast(name=name, duration=duration, upload=datetime.datetime.now(), host=host, participants=str(participants))
                    db.session.add(new_podcast)
                    db.session.commit()
                    return jsonify({'Action is successful' : '200 OK'}), 200
                else:
                    return jsonify({'Participants should be 0 to 10' : '400 bad request '}), 400
            else:
                return jsonify({'Duration must be positive' : '400 bad request'}), 400
        elif audio_type.lower() == 'audiobook':
            requests = request.get_json()
            title = requests['title']
            author = requests['author']
            narrator = requests['narrator']
            duration = requests['duration']
            if duration >= 0:
                new_audiobook = Audiobook(title=title, author=author, upload=datetime.datetime.now(), narrator=narrator, duration=duration)
                db.session.add(new_audiobook)
                db.session.commit()
                return jsonify({'Action is successful' : '200 OK'}), 200
            else:
                return jsonify({'Duration must be positive' : '400 bad request'}), 400
    else:
        return jsonify({'This request is invalid' : '400 bad request'}), 400

@main.route('/<audio_type>/<int:audio_id>', methods=['DELETE'])
def delete(audio_type, audio_id):
    if audio_type.lower() in ['song', 'podcast', 'audiobook']:
        if audio_type.lower() == 'song':
            delete_song = Song.query.filter_by(id=audio_id).first()
            if delete_song:
                db.session.delete(delete_song)
                db.session.commit()
                return jsonify({'Action is successful' : '200 OK'}), 200
            else:
                return jsonify({'Song not found' : '400 bad request'}), 400
        elif audio_type.lower() == 'podcast':
            delete_podcast = Podcast.query.filter_by(id=audio_id).first()
            if delete_podcast:
                db.session.delete(delete_podcast)
                db.session.commit()
                return jsonify({'Action is successful' : '200 OK'}), 200
            else:
                return jsonify({'Podcast not found' : '400 bad request'}), 400
        elif audio_type.lower() == 'audiobook':
            delete_audiobook = Audiobook.query.filter_by(id=audio_id).first()
            if delete_audiobook:
                db.session.delete(delete_audiobook)
                db.session.commit()
                return jsonify({'Action is successful' : '200 OK'}), 200
            else:
                return jsonify({'Audiobook not found' : '400 bad request'}), 400
    else:
        return jsonify({'This request is invalid' : '400 bad request'}), 400

@main.route('/<audio_type>/<int:audio_id>', methods=['PUT'])
def update(audio_type, audio_id):
    if audio_type.lower() in ['song', 'podcast', 'audiobook']:
        if audio_type.lower() == 'song':
            edit_song = Song.query.filter_by(id=audio_id).first()
            if edit_song:
                requests = request.get_json()
                edit_song.name = requests['name']
                edit_song.duration = requests['duration']
                edit_song.upload = datetime.datetime.now()
                if edit_song.duration >= 0:
                    db.session.commit()
                    return jsonify({'Action is successful' : '200 OK'}), 200
                else:
                    return jsonify({'Duration must be positive' : '400 bad request'}), 400
            else:
                return jsonify({'Song not found' : '400 bad request'}), 400
        elif audio_type.lower() == 'podcast':
            edit_podcast = Podcast.query.filter_by(id=audio_id).first()
            if edit_podcast:
                requests = request.get_json()
                edit_podcast.name = requests['name']
                edit_podcast.duration = requests['duration']
                edit_podcast.upload = datetime.datetime.now()
                edit_podcast.host = requests['host']
                try:
                    if 0 <= len(requests['participants']) <= 10:
                        edit_podcast.participants = str(requests['participants'])
                    else:
                        return jsonify({'Participants should be 0 to 10' : '400 bad request'}), 400
                except:
                    pass
                if edit_podcast.duration >= 0:
                    db.session.commit()
                    return jsonify({'Action is successful' : '200 OK'}), 200
                elif edit_podcast.duration >= 0 and edit_podcast.participants == None:
                    db.session.commit()
                    return jsonify({'Action is successful' : '200 OK'}), 200
                else:
                    return jsonify({'Duration must be positive' : '400 bad request'}), 400
            else:
                return jsonify({'Podcast not found' : '400 bad request'}), 400
        elif audio_type.lower() == 'audiobook':
            edit_audiobook = Audiobook.query.filter_by(id=audio_id).first()
            if edit_audiobook:
                requests = request.get_json()
                edit_audiobook.title = requests['title']
                edit_audiobook.author = requests['author']
                edit_audiobook.narrator = requests['narrator']
                edit_audiobook.duration = requests['duration']
                edit_audiobook.upload = datetime.datetime.now()
                if edit_audiobook.duration >= 0:
                    db.session.commit()
                    return jsonify({'Action is successful' : '200 OK'}), 200
                else:
                    return jsonify({'Duration must be positive' : '400 bad request'}), 400
            else:
                return jsonify({'Audiobook not found' : '400 bad request'}), 400
    else:
        return jsonify({'This request is invalid' : '400 bad request'}), 400