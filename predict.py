# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

from cog import BasePredictor, Input, Path
import requests
import mimetypes
import time

class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""
        # self.model = torch.load("./weights.pth")

    def predict(
        self,
        token: str = Input(description="Matrix password"),
        url: str = Input(description="Matrix serve server ulr ex : https://matrix.org"),
        room: str = Input(description="Matrix room ex : !ZkngAyfszzfCqwNZUd:phys:phys.ethz.ch"),
        message: str = Input(description="Matrix message"),
        media: Path = Input(description="Matrix media image or video"),
    ) -> str:
        
        media = open(media, 'rb')
        media_type = mimetypes.guess_type(media.name)[0]
        print(media_type)

# curl -X POST "https://matrix.org/_matrix/media/v3/upload?filename=War+and+Peace.pdf&access_token=syt_eWFzc2luc2lvdWRh_EotvLCnkTTdQlaMwaBJJ_2gikwe" \
#  -H "Accept: application/json" \
#  -H "Content-Type: application/pdf" \
#  -H "Content-Type: application/octet-stream" \
#  --data-binary @1693991358598.jpeg 

        headers = {
            'Content-Type': media_type,
            'Content-Type': 'application/octet-stream',
        }

        request = requests.post(
            f"{url}/_matrix/media/v3/upload?filename={media.name}&access_token={token}",
            headers=headers,
            data=media
        )
        media_response = request.json()


        headers = {
            'Authorization': f"Bearer {token}",
            'accept': 'application/json',
            'content-type': 'application/json',
        }

        if media_type.startswith("image"):
            data = {
                "msgtype": "m.image",
                "body": message,
                "url": media_response['content_uri']
            }
        elif media_type.startswith("video"):
            data = {
                "msgtype": "m.video",
                "body": message,
                "url": media_response['content_uri']
            }
        
        tansaction_id =  time.time()

        request = requests.put(
            f"{url}/_matrix/client/v3/rooms/{room}/send/m.room.message/{tansaction_id}",
            headers=headers,
            json=data
        )

        return media_response['content_uri']