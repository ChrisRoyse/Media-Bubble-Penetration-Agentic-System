from google.ads.googleads.client import GoogleAdsClient as _GAC
from google.ads.googleads.errors import GoogleAdsException

class GoogleAdsClient:  # pylint: disable=too-few-public-methods
    def __init__(self, cred_json):
        self._client = _GAC.load_from_storage(str(cred_json))
        self._cust_id = self._client.login_customer_id
        self._asset_service = self._client.get_service("AssetService")
        self._ad_group_asset_service = self._client.get_service("AdGroupAssetService")

    def _create_text_asset(self, text: str):
        asset_op = self._client.get_type("AssetOperation")
        asset = asset_op.create
        asset.text_asset.text = text
        res = self._asset_service.mutate_assets(customer_id=self._cust_id, operations=[asset_op])
        return res.results[0].resource_name

    def _create_image_asset(self, image_b64: str):
        asset_op = self._client.get_type("AssetOperation")
        asset = asset_op.create
        asset.image_asset.data = image_b64.encode()
        asset.image_asset.mime_type = self._client.enums.MimeTypeEnum.PNG
        res = self._asset_service.mutate_assets(customer_id=self._cust_id, operations=[asset_op])
        return res.results[0].resource_name

    def upload_asset(self, asset: dict):
        try:
            headline_rn = self._create_text_asset(asset["headline"])
            desc_rn = self._create_text_asset(asset["description"])
            img_rn = self._create_image_asset(asset["image_b64"])
            print("[Google] uploaded assets", headline_rn, desc_rn, img_rn)
            # Note: attach assets to P‑Max campaign / asset group via additional mutate ops.
        except GoogleAdsException as exc:
            for err in exc.failure.errors:
                print("GoogleAds error", err)