from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with # marshal with is the datacorator
import json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # this line will create the database file in the same folder
db = SQLAlchemy(app)

# after that we need to create the model or the schema of the tables of the database
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    likes = db.Column(db.Integer, nullable = False)
    views = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Video( name = {self.name}, likes = {self.likes}, views = {self.views})"

# initialize the database it need to be run only once
with app.app_context():
    db.drop_all()

with app.app_context(): # create_all requires the app context and 
    db.create_all()

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("likes",type=int, help="Likes field is required", required = True)
video_put_args.add_argument("name",type=str, help="name field is required", required = True)
video_put_args.add_argument("views",type=int, help="views field is required", required = True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("likes",type=int, help="Likes field")
video_update_args.add_argument("name",type=str, help="name field")
video_update_args.add_argument("views",type=int, help="views field")


response_deco = {
    'id': fields.Integer,
    'name': fields.String(100),
    'likes': fields.Integer,
    'views': fields.Integer
}


class Video(Resource):
    @marshal_with(response_deco) # it will decorate with response_deco response helps in serializing the response
    def get(self, video_id):
        # result will return the instance of the VideoModel with the filter marshal with will decorate the object with the field response_deco
        result = VideoModel.query.filter_by(id = video_id).first()
        if not result:
            abort(404, message='Video not found...')
        return result, 200
    
    @marshal_with(response_deco)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(415, message='This video already exists..')
        video = VideoModel(id = video_id, name = args['name'], likes = args['likes'], views = args['views'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(response_deco)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(415, message="This video doesn't exist")
        
        result.name = args['name']
        result.likes = args['likes']
        result.views = args['views']
        db.session.add(result)
        db.session.commit()
        return result
    
    def post(self):
        pass

    
    # def delete(self, video_id):
    #     abort_ifnotexist(video_id)
    #     del videos[video_id]
    #     return "", 202


api.add_resource(Video, "/video/<int:video_id>")

@app.route("/")
def home():
    return "HOME PAGE"


if __name__ == "__main__":
    app.run(debug=True)