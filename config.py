#operation identifiers
ACCOUNT_IDENTIFIER = "account"
TRANSACTION_IDENTIFIER = "transaction"

# violations
NO_VIOLATIONS = ""
DUPLICATED_VIOLATION = "account-already-initialized"

NO_FOUNDS_VIOLATION = "insufficient-limit"
NOT_ACTIVE_VIOLATION = "card-not-active"
INTERVAL_VIOLATION = "high-frequency-small-intervall"
DOUBLED_TRANSACTION_VIOLATION = "doubled-transaction"

# datetime_configs
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

# rules parameters
MIN_CREDIT_LIMIT = 0
MIN_SECONDS_INTERVAL = 120
MIN_PREVIOUS_TRANSACTIONS = 2
