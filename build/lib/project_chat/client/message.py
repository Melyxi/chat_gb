from dataclasses import dataclass


@dataclass
class Authenticate:
    account_name: str
    password: str

@dataclass
class Message:
    from_user: str
    message: str
    to: str
