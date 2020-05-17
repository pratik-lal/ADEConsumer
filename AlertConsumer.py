from azure.kusto.data.request import KustoClient, KustoConnectionStringBuilder
import time
import configparser
import logger


class SOCAlertConsumer:
    config = configparser.ConfigParser()
    config.read(".//app.config") # change to forward slash for linux (//)
    cluster = config.get("client", "cluster")
    db = config.get("client", "database")
    client_id = config.get("client", "client_id")
    client_secret = config.get("client", "client_secret")
    authority_id = config.get("client", "authority_id")

    @staticmethod
    def kusto_output():
        try:
            kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(SOCAlertConsumer.cluster,
                                                                                        SOCAlertConsumer.client_id,
                                                                                        SOCAlertConsumer.client_secret,
                                                                                        SOCAlertConsumer.authority_id)
            logger.AppLogging.auditlogger.info("Successfully loaded Kusto Connection Strings" + " " +
                                               SOCAlertConsumer.cluster+" with AppID "+SOCAlertConsumer.client_id)
        except RuntimeError as ie:
            logger.AppLogging.auditlogger.error("Unable to import Kusto Connection Strings. "
                                                "Please check your configuration"
                                                + SOCAlertConsumer.cluster + "with AppID" + SOCAlertConsumer.client_id)
            logger.AppLogging.auditlogger.error(str(ie))

        client = KustoClient(kcsb)
        kusto_query = open(".//KustoQuery//SOCAlerts.csl", "r") # change to forward slash for linux (//)
        query = kusto_query.read()
        kusto_query.close()
        try:
            response = client.execute(SOCAlertConsumer.db, query)
            logger.AppLogging.auditlogger.info("Successfully received response from Kusto")
            logger.AppLogging.auditlogger.info("Query output is saved to output folder")
        except RuntimeError as r:
            logger.AppLogging.auditlogger.error("There was an error in receiving response from Kusto")
            logger.AppLogging.auditlogger.error(str(r))

        for row in response.primary_results:
            filetime = time.strftime("%Y%m%d-%H%M%S")
            file = open(".//output//alerts-" + filetime + ".json", "x")  # forward slash works fine on Win & nix
            file.write(str(row))
            file.close()
