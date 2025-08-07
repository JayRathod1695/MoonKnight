from ..DataBase.Usage_Database.CRUD_Usage import insert_usage


def log_usage(user_id: str, model: str, tokens: int, cost: float):
    insert_usage(user_id, model, tokens, cost)
