# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

from cog import BasePredictor, Input, Path
import requests

class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""
        # self.model = torch.load("./weights.pth")

    def predict(
        self,
        token: str = Input(description="Matrix password"),
        url: str = Input(description="Matrix serve rurl"),
        room: str = Input(description="Matrix room ex : !ZkngAyfszzfCqwNZUd:phys:phys.ethz.ch"),
        message: str = Input(description="Matrix message"),
        media: Path = Input(description="Matrix media image or video")
    ) -> str:
        
# curl --data-binary @image.png 'https://matrix.server/_matrix/media/v3/upload?filename=image.png' \
#   -X 'POST' \
#   -H 'Authorization: Bearer my_access_token' \
#   -H 'Content-Type: image/png' \
#   --compressed
        media = open(media, 'rb')
        media_type = ''

        images = ['png', 'jpg', 'jpeg', 'gif']
        videos = ['mp4', 'mov', 'avi', 'webm']
        if media.split('.')[-1] in images:
            media_type = 'image/' + media.split('.')[-1]
        elif media.split('.')[-1] in videos:
            media_type = 'video/' + media.split('.')[-1]
        else:
            return 'Error: media type not supported'



      
        media_url = url + '/_matrix/media/v1/upload?filename=' + media.name
        media_headers = {'Authorization': ' '.join(['Bearer', token])}
        media_data = {
            'file': media,
        }
        r = requests.post(media_url, files=media_data, headers=media_headers)
        media_id = r.json()['content_uri']
        message = message + '\n' + media_id



# curl 'https://matrix.server/_matrix/client/v3/rooms/!rVwmJkYsikYjnIeLNU:matrix.server/send/m.room.message/1212' \
#   -X 'PUT' \
#   -H 'Authorization: Bearer my_access_token' \
#   -H 'accept: application/json' \
#   -H 'content-type: application/json' \
#   --data-raw '{"info":{"mimetype":"image/png","size":512,"w":512,"h":512},"msgtype":"m.image","body":"tta.webp","url":"mxc://example.com/AQwafuaFswefuhsfAFAgsw"}' \
#   --compressed

        url = url + '/_matrix/client/r0/rooms/' + room + '/send/m.room.message'
        """Run a prediction on the input and return the result"""
        headers = {'Authorization': ' '.join(['Bearer', token])}
        data = {
            'msgtype': 'm.image',
            'body': message,
            'url': media_id,
        }


        r = requests.post(url, json=data, headers=headers)
        return r.text
