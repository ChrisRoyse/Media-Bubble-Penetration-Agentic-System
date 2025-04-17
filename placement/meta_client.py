import base64, tempfile
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.api import FacebookAdsApi

class MetaClient:  # pylint: disable=too-few-public-methods
    def __init__(self, app_id, app_secret):
        FacebookAdsApi.init(app_id=app_id, app_secret=app_secret)
        self._account = AdAccount("me")

    def _upload_image(self, img_b64: str):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as fp:
            fp.write(base64.b64decode(img_b64))
            fp.flush()
            img = self._account.create_ad_image()
            img[AdCreative.Field.name] = "cluster‑img"
            img[AdCreative.Field.filename] = fp.name
            img.remote_create()
            return img[AdCreative.Field.hash]

    def upload_asset(self, asset: dict):
        image_hash = self._upload_image(asset["image_b64"])
        creative = self._account.create_ad_creative(params={
            AdCreative.Field.name: f"Cluster {asset['cluster']} Creative",
            AdCreative.Field.title: asset["headline"],
            AdCreative.Field.body: asset["description"],
            AdCreative.Field.object_story_spec: {
                "page_id": "<YOUR_PAGE_ID>",
                "link_data": {
                    "message": asset["description"],
                    "link": "https://example.com",
                    "picture": image_hash,
                },
            },
        })
        print("[Meta] creative uploaded", creative["id"])