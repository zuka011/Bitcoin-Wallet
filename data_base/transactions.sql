CREATE TABLE IF NOT EXISTS transactions (
    associated_wallet   TEXT    NOT NULL,
    associated_api_key  TEXT    NOT NULL,
    id                  TEXT    NOT NULL,
    source_address      TEXT    NOT NULL,
    destination_address TEXT    NOT NULL,
    amount              FLOAT   NOT NULL,
    timestamp           TEXT    NOT NULL,

    UNIQUE (associated_wallet, id),

    FOREIGN KEY (associated_wallet) REFERENCES wallets(address),
    FOREIGN KEY (associated_api_key) REFERENCES users(api_key),
    FOREIGN KEY (source_address) REFERENCES wallets(address),
    FOREIGN KEY (destination_address) REFERENCES wallets(address)
);