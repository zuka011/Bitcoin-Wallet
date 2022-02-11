from infra import InMemoryUserRepository
from runner.web.setup import setup

app = setup(user_repository=InMemoryUserRepository())
