import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Configuration settings for the application, sourced from environment variables or defaults.
    """

    # MongoDB settings
    MONGO_HOST: str = os.environ.get("MONGO_HOST", "localhost")
    MONGO_PORT: int = os.environ.get("MONGO_PORT", 27017)
    MONGO_DB: str = os.environ.get("MONGO_DB", "sarscov2_standalone")
    MONGO_USER: str = os.environ.get("MONGO_USER", "")
    MONGO_PASS: str = os.environ.get("MONGO_PASS", "")
    MONGO_AUTH_SOURCE: str = os.environ.get("MONGO_AUTH_SOURCE", "admin")
    MONGO_AUTH_MECHANISM: str = os.environ.get("MONGO_AUTH_MECHANISM", "SCRAM-SHA-256")

    # Database configs
    DATABASE_NAME: str = os.environ.get("DATABASE_NAME", "sarscov2_standalone")
    VIRUS_TYPE: str = os.environ.get("VIRUS_TYPE", "SARS-CoV-2")
    VARIANTS_OF_BIOLOGICAL_SIGNIFICANCE: list = os.environ.get(
        "VARIANTS",
        [
            "S:N501Y",
            "S:N501T",
            "S:N501S",
            "S:E484K",
            "S:K417T",
            "S:F157L",
            "S:V367F",
            "S:Q613H",
            "S:P681R",
            "S:Q677H",
            "S:F888L",
            "S:H69_V70del",
            "S:N439K",
            "S:Y453F",
            "S:S98F",
            "S:L452R",
            "S:D80Y",
            "S:A626S",
            "S:V1122L",
            "S:A222V",
            "S:S477N",
        ],
    )
    PANGO_LINEAGES_OF_CONCERN: list = os.environ.get(
        "PANGO_TYPES",
        [
            "B.1.351",
            "P.1",
            "A.23.1",
            "B.1.525",
            "B.1.1.28.1",
            "B.1.427",
            "B.1.429",
            "B.1.617",
        ],
    )
    POSITIONS_OF_BIOLOGICAL_SIGNIFICANCE: list = os.environ.get(
        "POSITIONS", ["S:501", "S:484"]
    )

    # Authentication settings
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"

    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD: str = os.environ.get("ADMIN_PASSWORD", "admin")
    ADMIN_FULLNAME = os.environ.get("ADMIN_FULLNAME", "Admin")
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@localhost")

    # Application settings
    PROJECT_NAME: str = "SARS-CoV-2 Standalone"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = (
        "SARS-CoV-2 Standalone is a standalone version of the SARS-CoV-2 API"
    )
    ROOT_PATH: str = os.environ.get("ROOT_PATH", "/")

    class Config:
        env_file = ".env"


settings = Settings()
