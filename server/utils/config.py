# server/utils/config.py  (덮어쓰기할 파일)
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

# .env 파일에서 환경 변수 로드
load_dotenv()


class Settings(BaseSettings):
    # Azure OpenAI 설정
    AOAI_API_KEY: str
    AOAI_ENDPOINT: str
    AOAI_DEPLOY_GPT4O: str
    AOAI_EMBEDDING_DEPLOYMENT: str
    AOAI_API_VERSION: str

    # Langfuse 설정 (옵션)
    LANGFUSE_PUBLIC_KEY: str | None = None
    LANGFUSE_SECRET_KEY: str | None = None
    LANGFUSE_HOST: str | None = None

    # SAP RFC 연결 설정
    SAP_USER: str | None = None
    SAP_PASSWD: str | None = None
    SAP_ASHOST: str | None = None
    SAP_SYSNR: str | None = None
    SAP_CLIENT: str | None = None
    SAP_LANG: str | None = "EN"

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "orchestrator API"

    API_BASE_URL: str | None = None

    # 기존 SQLite 데이터베이스 설정 (하위호환)
    DB_PATH: str = "history.db"
    SQLALCHEMY_DATABASE_URI: str = f"sqlite:///./{DB_PATH}"

    # 새로 추가된 (현재 에러를 일으킨) 설정들
    # Vector store persist dir
    VECTOR_DIR: str = "vectorstore/scope"

    # Standard DATABASE_URL (예: sqlite:///./agent.db)
    DATABASE_URL: str = "sqlite:///./history.db"
    # Pydantic 설정: .env 읽기, 대/소문자 구분, extra 허용(안전)
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

    def get_llm(self):
        """Azure OpenAI LLM 인스턴스를 반환합니다."""
        return AzureChatOpenAI(
            openai_api_key=self.AOAI_API_KEY,
            azure_endpoint=self.AOAI_ENDPOINT,
            azure_deployment=self.AOAI_DEPLOY_GPT4O,
            api_version=self.AOAI_API_VERSION,
            # temperature=0.7,
            streaming=True,  # 스트리밍 활성화
        )

    def get_embeddings(self):
        """Azure OpenAI Embeddings 인스턴스를 반환합니다."""
        return AzureOpenAIEmbeddings(
            model=self.AOAI_EMBEDDING_DEPLOYMENT,
            openai_api_version=self.AOAI_API_VERSION,
            api_key=self.AOAI_API_KEY,
            azure_endpoint=self.AOAI_ENDPOINT,
        )

    def get_sap_config(self) -> dict[str, str]:
        config = {
            "user": self.SAP_USER,
            "passwd": self.SAP_PASSWD,
            "ashost": self.SAP_ASHOST,
            "sysnr": self.SAP_SYSNR,
            "client": self.SAP_CLIENT,
            "lang": self.SAP_LANG,
        }
        return {k: v for k, v in config.items() if v is not None}


# 설정 인스턴스 생성
settings = Settings()


# 편의를 위한 함수들, 하위 호환성을 위해 유지
def get_llm():
    return settings.get_llm()


def get_embeddings():
    return settings.get_embeddings()


def get_sap_config():
    return settings.get_sap_config()
