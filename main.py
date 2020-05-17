import AlertConsumer
import time
import configparser
import logger


class Program:
    @staticmethod
    def main():
        config = configparser.ConfigParser()
        config.read(".//app.config")
        frequency = config.get("client", "execution_frequency")
        while True:
            logger.AppLogging.auditlogger.info("Application execution frequency (in seconds):" + str(frequency))
            AlertConsumer.SOCAlertConsumer.kusto_output()
            time.sleep(float(frequency))


if __name__ == '__main__':
    Program.main()
