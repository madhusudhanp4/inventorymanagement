from dotenv import load_dotenv

load_dotenv()

from langsmith import traceable


@traceable
def test_function():
    return "hello"


print(test_function())