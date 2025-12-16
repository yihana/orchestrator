from pyrfc import Connection

from server.utils.config import get_sap_config


class ERPAdapter:
    def __init__(self):
        self.conn = Connection(**get_sap_config())

    def call_bapi(self, bapi_name: str, params: dict):
        result = self.conn.call(bapi_name, **params)

        if bapi_name in {"BAPI_VENDOR_CREATE", "BAPI_VENDOR_EDIT"}:
            self.conn.call("BAPI_TRANSACTION_COMMIT")

        return result

    def call_rfc(self, rfc_name: str, params: dict):
        return self.conn.call(rfc_name, **params)
