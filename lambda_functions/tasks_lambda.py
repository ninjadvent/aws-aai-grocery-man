from crewai import Task
import json

def define_tasks(grocery_manager, demand_forecaster, waste_reduction_specialist, inventory_optimization_analyst):
    # Define tasks for the Grocery Manager
    manage_inventory_task = Task(
        description="""Manage the grocery inventory by monitoring stock levels,
        tracking product demand, and ensuring efficient stock rotation. Provide
        guidance to other agents on optimizing inventory and reducing waste.
        Pay attention to the insights provided by the Demand Forecaster and the
        Waste Reduction Specialist to make informed decisions.""",
        agent=grocery_manager
    )

    # Define tasks for the Demand Forecaster
    forecast_demand_task = Task(
        description="""Forecast future demand for grocery products based on
        historical data and current trends. Provide insights to the Grocery
        Manager and Inventory Optimization Analyst to optimize inventory levels
        and reduce waste. Analyze sales data, market trends, and seasonal
        variations to predict future demand accurately.""",
        agent=demand_forecaster
    )

    # Define tasks for the Waste Reduction Specialist
    waste_reduction_task = Task(
        description="""Minimize waste of grocery products by implementing
        strategies to reduce spoilage and improve shelf life. Provide
        recommendations to the Grocery Manager and Inventory Optimization
        Analyst on how to reduce waste and improve sustainability. Analyze
        current waste levels, identify areas for improvement, and recommend
        effective waste reduction strategies.""",
        agent=waste_reduction_specialist
    )

    # Define tasks for the Inventory Optimization Analyst
    optimize_inventory_task = Task(
        description="""Optimize grocery inventory levels to minimize holding
        costs and maximize product availability. Provide recommendations to the
        Grocery Manager and Demand Forecaster on how to improve inventory
        levels and reduce costs. Analyze current inventory levels, identify areas
        for optimization, and recommend effective inventory optimization
        strategies.""",
        agent=inventory_optimization_analyst
    )
    return manage_inventory_task, forecast_demand_task, reduce_waste_task, optimize_inventory_task

def lambda_handler(event, context):
    """
    Handles requests to the tasks Lambda function.
    """
    grocery_manager = event.get('grocery_manager')
    demand_forecaster = event.get('demand_forecaster')
    waste_reduction_specialist = event.get('waste_reduction_specialist')
    inventory_optimization_analyst = event.get('inventory_optimization_analyst')

    if not grocery_manager or not demand_forecaster or not waste_reduction_specialist or not inventory_optimization_analyst:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing agent parameters'})
        }

    try:
        manage_inventory_task, forecast_demand_task, reduce_waste_task, optimize_inventory_task = define_tasks(grocery_manager, demand_forecaster, waste_reduction_specialist, inventory_optimization_analyst)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'manage_inventory_task': manage_inventory_task.description,
                'forecast_demand_task': forecast_demand_task.description,
                'reduce_waste_task': reduce_waste_task.description,
                'optimize_inventory_task': optimize_inventory_task.description
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
