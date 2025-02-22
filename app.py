from app.dependency import Dependency
from app.custom_agent import CustomAgent
from app.config import Configs
from app.logger import Logger

def main(args, configs):
    logger = Logger(**configs["logger"])

    logger.debug("############ MODEL TRAINING CONFIGURATIONS ############")
    logger.debug(configs)

    dep = Dependency("ai agent")
    agent = CustomAgent(logger=logger)
    agent.run(dep)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--environment", type=str)
    parser.add_argument("--test", action= "store_true")


    args = parser.parse_args()

    configs = Configs().load(config_name=args.environment)

    main(args, configs)