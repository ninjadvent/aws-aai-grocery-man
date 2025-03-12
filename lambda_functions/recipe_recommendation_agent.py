import os
from crewai import Agent
from crewai_tools import WebsiteSearchTool

def lambda_handler(event, context):
    items = event['items']

    recipe_web_tool = WebsiteSearchTool(website='https://www.americastestkitchen.com/recipes')

    # Optimized Grocery Recipe Recommendation Agent
    rest_grocery_recipe_agent = Agent(
        role="Grocery Recipe Recommendation Specialist",
        goal=(
            "Provide recipe recommendations using the remaining groceries in the inventory. "
            "Avoid using items with a count of 0 and prioritize recipes that maximize the use of available ingredients. "
            "If ingredients are insufficient, suggest restocking recommendations."
        ),
        backstory=(
            "As a Grocery Recipe Recommendation Specialist, your mission is to help the household make the most out of their remaining groceries. "
            "Your role is to search the web for easy, delicious recipes that utilize available ingredients while minimizing waste. "
            "Ensure that the recipes are simple to follow and use as many of the remaining ingredients as possible."
        ),
        personality=(
            "Creative, resourceful, and efficient. This agent is dedicated to helping the household create enjoyable meals with what they have on hand."
        ),
        allow_delegation=False,
        verbose=False, # Set to False for Lambda function
        tools=[recipe_web_tool],
        human_input=False # Set to False for Lambda function
    )

    # TODO: Implement the logic to recommend recipes based on available ingredients
    # This is a placeholder, replace with actual implementation
    recipes = [
        {
            "recipe_name": "Placeholder Recipe",
            "ingredients": [
                {"item_name": "Placeholder Item", "quantity": "1", "unit": "pcs"}
            ],
            "steps": [
                "Step 1: Do something",
                "Step 2: Do something else"
            ],
            "source": "https://www.example.com"
        }
    ]

    restock_recommendations = [
        {
            "item_name": "Placeholder Item",
            "quantity_needed": 1,
            "unit": "pcs"
        }
    ]

    return {
        "recipes": recipes,
        "restock_recommendations": restock_recommendations
    }
