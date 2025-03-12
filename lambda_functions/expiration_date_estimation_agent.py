import os
from crewai import Agent
from crewai_tools import WebsiteSearchTool

def lambda_handler(event, context):
    items = event['items']
    date_of_purchase = event['date_of_purchase']

    # Use website search tool to search the website "www.stilltasty.com"
    expiration_date_search_web_tool = WebsiteSearchTool(website='https://www.stilltasty.com/')

    expiration_date_search_agent = Agent(
        role="Expiration Date Estimation Specialist",
        goal=(
            "Accurately estimate the expiration dates of items extracted by the Receipt Markdown Interpreter Agent. "
            "Utilize online sources to determine typical shelf life when refrigerated and add the estimated number of days to the purchase date."
        ),
        backstory=(
            "As the Expiration Date Estimation Specialist, your role is to ensure the household's groceries are consumed before expiration. "
            "You use your access to online resources to search for the best estimates on how long each item typically lasts when stored properly."
        ),
        personality=(
            "Meticulous, resourceful, and reliable. This agent ensures the household maintains a well-stocked but efficiently used inventory, minimizing waste."
        ),
        allow_delegation=False,
        verbose=False, # Set to False for Lambda function
        tools=[expiration_date_search_web_tool]
    )

    # TODO: Implement the logic to estimate expiration dates for each item
    # This is a placeholder, replace with actual implementation
    estimated_items = []
    for item in items:
        estimated_items.append({
            "item_name": item['item_name'],
            "count": item['count'],
            "unit": item['unit'],
            "expiration_date": "2024-11-30" # Placeholder expiration date
        })

    return {
        "items": estimated_items
    }
