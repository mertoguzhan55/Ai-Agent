from app.dependency import Dependency
from app.custom_agent import CustomAgent

def main():
    dep = Dependency("Mert", 25)
    agent = CustomAgent()
    agent.run(dep)


if __name__ == "__main__":
    main()