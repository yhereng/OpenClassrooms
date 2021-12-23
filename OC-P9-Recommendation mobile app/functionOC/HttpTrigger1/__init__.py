#import logging
import json
import azure.functions as func


def main(req: func.HttpRequest, inputDocument: func.DocumentList) -> str:
    #logging.info('Python HTTP trigger function processed a request.')

    #Retrieve request body
    req_body = req.get_json()
    #retrieve user ID
    userID=int(req_body["userId"])
    #logging.warning("Found document %s", inputDocument)

    if not inputDocument:
        i=1
        #logging.warning("Document not found")
    else:
        reco=[inputDocument[0]['rec1'],
                inputDocument[0]['rec2'],
                inputDocument[0]['rec3'],
                inputDocument[0]['rec4'],
                inputDocument[0]['rec5']]
        #logging.warning("reco: %s", reco)

        return json.dumps(reco)
        

