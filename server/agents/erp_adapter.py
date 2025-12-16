from pyrfc import Connection

from server.utils.config import get_sap_config


class ERPAdapter:
    def __init__(self):
        self.conn: Connection | None = None

    def _ensure_connection(self) -> Connection:
        if self.conn is not None:
            return self.conn

        config = get_sap_config()
        required_keys = {"user", "passwd", "ashost", "sysnr", "client"}
        missing = sorted(key for key in required_keys if key not in config or not config[key])
        if missing:
            missing_envs = ", ".join(f"SAP_{key.upper()}" for key in missing)
            raise RuntimeError(
                "SAP RFC connection is not configured. Please set the following environment "
                f"variables: {missing_envs}"
            )

        self.conn = Connection(**config)
        return self.conn

    def call_bapi(self, bapi_name: str, params: dict):
        conn = self._ensure_connection()
        result = conn.call(bapi_name, **params)

        if bapi_name in {"BAPI_VENDOR_CREATE", "BAPI_VENDOR_EDIT"}:
            conn.call("BAPI_TRANSACTION_COMMIT")

        return result

    def call_rfc(self, rfc_name: str, params: dict):
        conn = self._ensure_connection()
        return conn.call(rfc_name, **params)
