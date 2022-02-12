CREATE TABLE IF NOT EXISTS wallets (
    address     TEXT    PRIMARY KEY,
    balance     FLOAT   NOT NULL,
    currency    TEXT    NOT NULL,
    api_key     TEXT    NOT NULL,

    FOREIGN KEY (api_key) REFERENCES users(api_key)
);