import os

from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient, RecognizeCustomEntitiesAction
from dotenv import load_dotenv


load_dotenv()


def sample_recognize_custom_entities():

    endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
    key = os.getenv("AZURE_LANGUAGE_KEY")
    project_name = os.getenv("CUSTOM_ENTITIES_PROJECT_NAME")
    deployment_name = os.getenv("CUSTOM_ENTITIES_DEPLOYMENT_NAME")

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    document = ["el Señor Wilberth Ferney Córdoba con C.C 1.053.793.468"]

    poller = text_analytics_client.begin_analyze_actions(
        document,
        actions=[
            RecognizeCustomEntitiesAction(
                project_name=project_name, deployment_name=deployment_name
            )
        ],
    )

    document_results = poller.result()
    for result in document_results:
        custom_entitities_resuelt = result[0]
        if not custom_entitities_resuelt.is_error:
            for entity in custom_entitities_resuelt.entities:
                print(
                    "Entity '{}' has category '{}' with confidence score of '{}'".format(
                        entity.text, entity.category, entity.confidence_score
                    )
                )
        else:
            print(
                "... Is an error with code '{}' and message '{}'".format(
                    custom_entitities_resuelt.code, custom_entitities_resuelt.message
                )
            )


if __name__ == "__main__":
    sample_recognize_custom_entities()
