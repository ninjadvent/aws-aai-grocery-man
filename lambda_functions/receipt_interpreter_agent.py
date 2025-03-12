import os
from crewai import Agent

def lambda_handler(event, context):
    receipt_markdown = event['receipt_markdown']
    today = event['today']

    receipt_interpreter_agent = Agent(
        role="Receipt Markdown Interpreter",
        goal=(
            "Accurately extract items, their counts, and weights with units from a given receipt in markdown format. "
            "Provide structured data to support the grocery management system."
        ),
        backstory=(
            "As a key member of the grocery management crew for the household, your mission is to meticulously extract "
            "details such as item names, quantities, and weights from receipt markdown files. Your role is vital for the "
            "grocery tracker agent, which monitors the household's inventory levels."
        ),
        personality=(
            "Diligent, detail-oriented, and efficient. The Receipt Markdown Interpreter is committed to providing accurate "
            "and structured information to support effective grocery management. It is particularly focused on clarity and precision."
        ),
        allow_delegation=False,
        verbose=False # Set to False for Lambda function
    )

    # TODO: Implement the logic to extract item details from the receipt_markdown
    # This is a placeholder, replace with actual implementation
    extracted_items = {
        "items": [
            {"item_name": "Placeholder Item", "count": 1, "unit": "pcs"}
        ],
        "date_of_purchase": today
    }

    return extracted_items
