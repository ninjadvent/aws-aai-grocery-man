import json
import boto3
from decimal import Decimal
import os

# Load necessary tools
dynamodb = boto3.resource('dynamodb', region_name=os.environ.get("AWS_REGION"))
table_name = os.environ.get("DYNAMODB_TABLE_NAME")
table = dynamodb.Table(table_name)


def replace_decimals(obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = replace_decimals(v)
        return obj
    elif isinstance(obj, Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj


def add_grocery_item(item_details: str) -> str:
    """Adds a new grocery item to the inventory. Provide the item details in JSON format."""
    try:
        item = json.loads(item_details)
        # Check if required keys exist and have values
        required_keys = ['item_id', 'name', 'category', 'quantity', 'unit_price']
        if not all(key in item and item[key] for key in required_keys):
            return "Error: Required fields ('item_id', 'name', 'category', 'quantity', 'unit_price') cannot be empty."

        # Convert quantity and unit_price to Decimal
        item['quantity'] = Decimal(str(item['quantity']))
        item['unit_price'] = Decimal(str(item['unit_price']))

        # Use the item_id as the primary key
        table.put_item(Item=item)

        return f"Successfully added grocery item: {item['name']}"
    except json.JSONDecodeError:
        return "Error: Invalid JSON format. Please provide item details in JSON format."
    except Exception as e:
        return f"Error adding grocery item: {str(e)}"


def update_grocery_item(item_update: str) -> str:
    """Updates the details of an existing grocery item in the inventory. Provide the item update in JSON format."""
    try:
        update = json.loads(item_update)
        item_id = update.get('item_id')

        if not item_id:
            return "Error: item_id is required to update an item."

        # Prepare the update expression and attribute values
        update_expression = "SET "
        expression_attribute_values = {}
        for key, value in update.items():
            if key != 'item_id':
                update_expression += f"{key} = :{key}, "
                expression_attribute_values[f":{key}"] = Decimal(str(value)) if isinstance(value, (int, float)) else value

        # Remove the trailing comma and space
        update_expression = update_expression.rstrip(", ")

        # Ensure there is something to update
        if not expression_attribute_values:
            return "Error: No updates provided for the item."

        # Update the item in DynamoDB
        table.update_item(
            Key={'item_id': item_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )

        return f"Successfully updated grocery item with item_id: {item_id}"
    except json.JSONDecodeError:
        return "Error: Invalid JSON format. Please provide the item update in JSON format."
    except Exception as e:
        return f"Error updating grocery item: {str(e)}"


def remove_grocery_item(item_id: str) -> str:
    """Removes a grocery item from the inventory based on its item_id."""
    try:
        if not item_id:
            return "Error: item_id is required to remove an item."

        # Delete the item from DynamoDB
        table.delete_item(Key={'item_id': item_id})

        return f"Successfully removed grocery item with item_id: {item_id}"
    except Exception as e:
        return f"Error removing grocery item: {str(e)}"


def get_grocery_item_details(item_id: str) -> str:
    """Retrieves the details of a specific grocery item from the inventory based on its item_id."""
    try:
        if not item_id:
            return "Error: item_id is required to retrieve item details."

        # Retrieve the item from DynamoDB
        response = table.get_item(Key={'item_id': item_id})

        if 'Item' in response:
            item = response['Item']
            # Convert Decimal types to Python native types
            item = replace_decimals(item)
            return json.dumps(item, indent=2)
        else:
            return f"Grocery item with item_id '{item_id}' not found."
    except Exception as e:
        return f"Error retrieving grocery item details: {str(e)}"


def list_all_grocery_items(category: str = None) -> str:
    """Lists all grocery items in the inventory. Optionally, filter by category."""
    try:
        if category:
            response = table.scan(FilterExpression=boto3.dynamodb.conditions.Attr('category').eq(category))
        else:
            response = table.scan()

        items = response.get('Items', [])
        if items:
            items = replace_decimals(items)
            return json.dumps(items, indent=2)
        else:
            return "No grocery items found."
    except Exception as e:
        return f"Error listing grocery items: {str(e)}"


def adjust_inventory_quantity(item_id: str, quantity_change: int) -> str:
    """Adjusts the inventory quantity of a grocery item. Provide the item_id and the quantity_change (positive or negative)."""
    try:
        if not item_id or not isinstance(quantity_change, int):
            return "Error: item_id and quantity_change (integer) are required."

        # Update the item in DynamoDB
        response = table.update_item(
            Key={'item_id': item_id},
            UpdateExpression="SET quantity = quantity + :quantity_change",
            ExpressionAttributeValues={':quantity_change': Decimal(str(quantity_change))},
            ReturnValues="UPDATED_NEW"
        )

        if response and 'Attributes' in response:
            return f"Successfully adjusted inventory quantity for item_id: {item_id}. New quantity: {response['Attributes']['quantity']}"
        else:
            return "Failed to adjust inventory quantity."
    except Exception as e:
        return f"Error adjusting inventory quantity: {str(e)}"

def lambda_handler(event, context):
    action = event.get('action')

    if action == 'add_grocery_item':
        item_details = event.get('item_details')
        result = add_grocery_item(item_details)
    elif action == 'get_grocery_item_details':
        item_id = event.get('item_id')
        result = get_grocery_item_details(item_id)
    elif action == 'update_grocery_item':
        item_update = event.get('item_update')
        result = update_grocery_item(item_update)
    elif action == 'remove_grocery_item':
        item_id = event.get('item_id')
        result = remove_grocery_item(item_id)
    elif action == 'list_all_grocery_items':
        category = event.get('category')
        result = list_all_grocery_items(category)
    elif action == 'adjust_inventory_quantity':
        item_id = event.get('item_id')
        quantity_change = event.get('quantity_change')
        result = adjust_inventory_quantity(item_id, quantity_change)
    else:
        result = "Invalid action"

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
