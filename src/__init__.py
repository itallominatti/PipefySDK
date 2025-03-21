from pipefysdk.main import PipefySDK

__all__ = ["PipefySDK"]

if __name__ == "__main__":
    pipefy_sdk = PipefySDK(token="eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJQaXBlZnkiLCJpYXQiOjE3MzcwNDYxNTUsImp0aSI6ImNjOTlkM2U3LWRkOTUtNDc2Yi1hYmIwLWYxMjgyZDFlYjkzZSIsInN1YiI6MjI2OTA3LCJ1c2VyIjp7ImlkIjoyMjY5MDcsImVtYWlsIjoiYW5hbHl0aWNzLmlubm92YXRpb24uc3BAYWNjZW50dXJlLmNvbSJ9fQ.KbsiNDodOr6jryfGoPwpi28idutqiVuzp7ZW3P79YNmHCYIPzGJMc2O2DraHfn3mwIdZFiRsTWeXUllj5wsKHw",
        url="https://telefonicalogistica.pipefy.com/graphql")

    get_card_info = pipefy_sdk.get_card_info(card_id=465540876)
    print(get_card_info)