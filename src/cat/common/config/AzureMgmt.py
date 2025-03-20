import logging
import random

from openai import AzureOpenAI

from src.cat.common.config.ApolloMgmt import ApolloMgmt
from src.cat.common.tools.str_tools import StrTools


class AzureMgmt:
    SERVER_URL = ApolloMgmt.get_property('llm.azure.openai.serverUrl', None)

    if SERVER_URL is not None:
        SERVER_URL = StrTools.split_string_if_has_comma(SERVER_URL)

    API_KEY = ApolloMgmt.get_property('llm.azure.openai.appKey', None)
    if API_KEY is not None:
        API_KEY = StrTools.split_string_if_has_comma(API_KEY)

    API_VERSION = ApolloMgmt.get_property('llm.azure.openai.apiVersion', "2025-01-01-preview")

    CURRENT_IDX = 0

    def __init__(self):
        self.clients = []

        for i in range(len(self.SERVER_URL)):
            self.clients.append(AzureOpenAI(
                api_key=self.API_KEY[i],
                azure_endpoint=self.SERVER_URL[i],
                api_version=self.API_VERSION
            ))
            logging.info(f"init azure openai client {i} with url {self.SERVER_URL[i]}")

    def get_client(self):
        client_idx = len(self.SERVER_URL) - 1
        if len(self.SERVER_URL) > 1:
            client_idx = random.randint(0, len(self.SERVER_URL) - 1)

        return self.clients[client_idx]
