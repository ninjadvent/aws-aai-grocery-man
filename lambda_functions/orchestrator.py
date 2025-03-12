import json
import boto3
import os

# Initialize AWS clients
lambda_client = boto3.client('lambda', region_name=os.environ.get("AWS_REGION"))
openai_api_key = os.environ.get("OPENAI_API_KEY")
dynamodb_table_name = os.environ.get("DYNAMODB_TABLE_NAME")


def invoke_lambda_function(function_name, payload):
    """Invokes a Lambda function and returns the response."""
    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        response_payload = json.loads(response['Payload'].read().decode('utf-8'))
        return response_payload
    except Exception as e:
        return {'error': str(e)}


def lambda_handler(event, context):
    """Main Lambda handler to orchestrate the grocery management system."""
    try:
        # Define agent and task function names (assumes you've deployed them as separate Lambda functions)
        agent_function_names = {
            "grocery_manager": os.environ.get("GROCERY_MANAGER_LAMBDA_NAME"),
            "demand_forecaster": os.environ.get("DEMAND_FORECASTER_LAMBDA_NAME"),
            "waste_reduction_specialist": os.environ.get("WASTE_REDUCTION_SPECIALIST_LAMBDA_NAME"),
            "inventory_optimization_analyst": os.environ.get("INVENTORY_OPTIMIZATION_ANALYST_LAMBDA_NAME")
        }

        # Tasks function
        tasks_function_name = os.environ.get("TASKS_LAMBDA_NAME")
        # database function
        database_function_name = os.environ.get("DATABASE_LAMBDA_NAME")

        # 1. Initialize Agents and Tasks
        # This is a simplified example. You might need to pass specific configurations.
        agents = {agent_name: invoke_lambda_function(agent_function_names[agent_name], {})
                  for agent_name in agent_function_names}

        tasks = invoke_lambda_function(tasks_function_name, {
            "grocery_manager": agents["grocery_manager"],
            "demand_forecaster": agents["demand_forecaster"],
            "waste_reduction_specialist": agents["waste_reduction_specialist"],
            "inventory_optimization_analyst": agents["inventory_optimization_analyst"]
        })

        # 2. Example Task: Add a new grocery item
        item_details = {
            "item_id": "601",
            "name": "Coconut",
            "category": "Fruit",
            "quantity": 100,
            "unit_price": 1.50
        }
        add_item_result = invoke_lambda_function(database_function_name, {
            "action": "add_grocery_item",
            "item_details": json.dumps(item_details)
        })

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Grocery Management System executed successfully!',
                'add_item_result': add_item_result,
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
