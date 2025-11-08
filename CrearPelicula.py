import boto3
import uuid
import os
import json
import traceback

def lambda_handler(event, context):
    try:
        # ======== ENTRADA ========
        print(json.dumps({
            "tipo": "INFO",
            "log_datos": {"mensaje": "Evento recibido", "event": event}
        }))
        
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]
        
        # ======== PROCESO ========
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)

        # ======== LOG DE ÉXITO ========
        print(json.dumps({
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Película creada correctamente",
                "tenant_id": tenant_id,
                "pelicula_datos": pelicula_datos
            }
        }))

        # ======== SALIDA ========
        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }

    except Exception as e:
        # ======== MANEJO DE ERROR ========
        error_trace = traceback.format_exc()
        print(json.dumps({
            "tipo": "ERROR",
            "log_datos": {
                "mensaje": str(e),
                "detalle": error_trace,
                "event": event
            }
        }))

        return {
            'statusCode': 500,
            'error': str(e)
        }
