import logging
import configparser


class AppLogging:
    config = configparser.ConfigParser()
    config.read(".//app.config")
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        filename=".//logs//AlertConsumer.log",
                        filemode='a')

    auditlogger = logging.getLogger('SOCAlertConsumer')
