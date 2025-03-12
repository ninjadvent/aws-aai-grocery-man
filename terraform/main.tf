resource "aws_api_gateway_rest_api" "grocery_api" {
  name        = "GroceryAPI"
  description = "API Gateway for Grocery Management System"
}

resource "aws_api_gateway_resource" "add_item_resource" {
  rest_api_id = aws_api_gateway_rest_api.grocery_api.id
  parent_id   = aws_api_gateway_rest_api.grocery_api.root_resource_id
  path_part   = "add-item"
}

resource "aws_api_gateway_method" "add_item_method" {
  rest_api_id   = aws_api_gateway_rest_api.grocery_api.id
  resource_id   = aws_api_gateway_resource.add_item_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "add_item_integration" {
  rest_api_id             = aws_api_gateway_rest_api.grocery_api.id
  resource_id             = aws_api_gateway_resource.add_item_resource.id
  http_method             = aws_api_gateway_method.add_item_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.dynamodb_lambda.invoke_arn
}

resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.dynamodb_lambda.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "arn:aws:execute-api:us-east-1:203918878138:${aws_api_gateway_rest_api.grocery_api.id}/*/*"
}

resource "aws_lambda_permission" "apigw_lambda_get_item" {
  statement_id  = "AllowAPIGatewayInvoke_get_item"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.dynamodb_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:us-east-1:203918878138:${aws_api_gateway_rest_api.grocery_api.id}/POST/get-item"
}

resource "aws_lambda_permission" "apigw_lambda_update_item" {
  statement_id  = "AllowAPIGatewayInvoke_update_item"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.dynamodb_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:us-east-1:203918878138:${aws_api_gateway_rest_api.grocery_api.id}/POST/update-item"
}

resource "aws_lambda_permission" "apigw_lambda_remove_item" {
  statement_id  = "AllowAPIGatewayInvoke_remove_item"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.dynamodb_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:us-east-1:203918878138:${aws_api_gateway_rest_api.grocery_api.id}/POST/remove-item"
}

resource "aws_lambda_permission" "apigw_lambda_list_items" {
  statement_id  = "AllowAPIGatewayInvoke_list_items"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.dynamodb_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:us-east-1:203918878138:${aws_api_gateway_rest_api.grocery_api.id}/*/*"
}

resource "aws_api_gateway_deployment" "grocery_api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.grocery_api.id
  stage_name  = "uat"

  depends_on = [
    aws_api_gateway_integration.add_item_integration,
    aws_api_gateway_integration.get_item_integration,
    aws_api_gateway_integration.update_item_integration,
    aws_api_gateway_integration.remove_item_integration,
    aws_api_gateway_integration.list_items_integration,
  ]
}

resource "aws_api_gateway_stage" "dev" {
  deployment_id = aws_api_gateway_deployment.grocery_api_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.grocery_api.id
  stage_name    = "dev"
}

# Create Lambda functions
resource "aws_lambda_function" "receipt_interpreter_agent" {
  function_name = "receipt-interpreter-agent"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_role.arn
  handler       = "receipt_interpreter_agent.lambda_handler"
  filename      = "../lambda_functions/receipt_interpreter_agent.zip"
  source_code_hash = filebase64sha256("../lambda_functions/receipt_interpreter_agent.zip")
  depends_on = [aws_iam_policy_attachment.lambda_policy_attachment]
}

resource "aws_api_gateway_resource" "get_item_resource" {
  rest_api_id = aws_api_gateway_rest_api.grocery_api.id
  parent_id   = aws_api_gateway_rest_api.grocery_api.root_resource_id
  path_part   = "get-item"
}

resource "aws_api_gateway_method" "get_item_method" {
  rest_api_id   = aws_api_gateway_rest_api.grocery_api.id
  resource_id   = aws_api_gateway_resource.get_item_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_item_integration" {
  rest_api_id             = aws_api_gateway_rest_api.grocery_api.id
  resource_id             = aws_api_gateway_resource.get_item_resource.id
  http_method             = aws_api_gateway_method.get_item_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.dynamodb_lambda.invoke_arn
}

resource "aws_api_gateway_resource" "update_item_resource" {
  rest_api_id = aws_api_gateway_rest_api.grocery_api.id
  parent_id   = aws_api_gateway_rest_api.grocery_api.root_resource_id
  path_part   = "update-item"
}

resource "aws_api_gateway_method" "update_item_method" {
  rest_api_id   = aws_api_gateway_rest_api.grocery_api.id
  resource_id   = aws_api_gateway_resource.update_item_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "update_item_integration" {
  rest_api_id             = aws_api_gateway_rest_api.grocery_api.id
  resource_id             = aws_api_gateway_resource.update_item_resource.id
  http_method             = aws_api_gateway_method.update_item_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.dynamodb_lambda.invoke_arn
}

resource "aws_api_gateway_resource" "remove_item_resource" {
  rest_api_id = aws_api_gateway_rest_api.grocery_api.id
  parent_id   = aws_api_gateway_rest_api.grocery_api.root_resource_id
  path_part   = "remove-item"
}

resource "aws_api_gateway_method" "remove_item_method" {
  rest_api_id   = aws_api_gateway_rest_api.grocery_api.id
  resource_id   = aws_api_gateway_resource.remove_item_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "remove_item_integration" {
  rest_api_id             = aws_api_gateway_rest_api.grocery_api.id
  resource_id             = aws_api_gateway_resource.remove_item_resource.id
  http_method             = aws_api_gateway_method.remove_item_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.dynamodb_lambda.invoke_arn
}

resource "aws_api_gateway_resource" "list_items_resource" {
  rest_api_id = aws_api_gateway_rest_api.grocery_api.id
  parent_id   = aws_api_gateway_rest_api.grocery_api.root_resource_id
  path_part   = "list-items"
}

resource "aws_api_gateway_method" "list_items_method" {
  rest_api_id   = aws_api_gateway_rest_api.grocery_api.id
  resource_id   = aws_api_gateway_resource.list_items_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "list_items_integration" {
  rest_api_id             = aws_api_gateway_rest_api.grocery_api.id
  resource_id             = aws_api_gateway_resource.list_items_resource.id
  http_method             = aws_api_gateway_method.list_items_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.dynamodb_lambda.invoke_arn
}

resource "aws_lambda_function" "expiration_date_estimation_agent" {
  function_name = "expiration-date-estimation-agent"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_role.arn
  handler       = "expiration_date_estimation_agent.lambda_handler"
  filename      = "../lambda_functions/expiration_date_estimation_agent.zip"
  source_code_hash = filebase64sha256("../lambda_functions/expiration_date_estimation_agent.zip")
  depends_on = [aws_iam_policy_attachment.lambda_policy_attachment]
}

resource "aws_lambda_function" "grocery_tracker_agent" {
  function_name = "grocery-tracker-agent"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_role.arn
  handler       = "grocery_tracker_agent.lambda_handler"
  filename      = "../lambda_functions/grocery_tracker_agent.zip"
  source_code_hash = filebase64sha256("../lambda_functions/grocery_tracker_agent.zip")
  depends_on = [aws_iam_policy_attachment.lambda_policy_attachment]
}

resource "aws_lambda_function" "recipe_recommendation_agent" {
  function_name = "recipe-recommendation-agent"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_role.arn
  handler       = "recipe_recommendation_agent.lambda_handler"
  filename      = "../lambda_functions/recipe_recommendation_agent.zip"
  source_code_hash = filebase64sha256("../lambda_functions/recipe_recommendation_agent.zip")
  depends_on = [aws_iam_policy_attachment.lambda_policy_attachment]
}

resource "aws_lambda_function" "database_tools_lambda" {
  function_name = "database-tools-lambda"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_role.arn
  handler       = "database_tools_lambda.lambda_handler"
  filename      = "../lambda_functions/database_tools_lambda.zip"
  source_code_hash = filebase64sha256("../lambda_functions/database_tools_lambda.zip")
  depends_on = [aws_iam_policy_attachment.lambda_policy_attachment]
}

resource "aws_lambda_function" "orchestrator" {
  function_name = "orchestrator"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_role.arn
  handler       = "orchestrator.lambda_handler"
  filename      = "../lambda_functions/orchestrator.zip"
  source_code_hash = filebase64sha256("../lambda_functions/orchestrator.zip")
  environment {
    variables = {
      RECEIPT_INTERPRETER_FUNCTION_NAME = aws_lambda_function.receipt_interpreter_agent.function_name
      EXPIRATION_DATE_ESTIMATION_FUNCTION_NAME = aws_lambda_function.expiration_date_estimation_agent.function_name
      GROCERY_TRACKER_FUNCTION_NAME = aws_lambda_function.grocery_tracker_agent.function_name
      RECIPE_RECOMMENDATION_FUNCTION_NAME = aws_lambda_function.recipe_recommendation_agent.function_name
      DATABASE_TOOLS_LAMBDA_NAME = aws_lambda_function.database_tools_lambda.function_name
      TASKS_LAMBDA_NAME = aws_lambda_function.tasks_lambda.function_name
      DATABASE_LAMBDA_NAME = aws_lambda_function.dynamodb_lambda.function_name
    }
  }
  depends_on = [aws_lambda_function.receipt_interpreter_agent, aws_lambda_function.expiration_date_estimation_agent, aws_lambda_function.grocery_tracker_agent, aws_lambda_function.recipe_recommendation_agent, aws_lambda_function.database_tools_lambda, aws_lambda_function.tasks_lambda, aws_lambda_function.dynamodb_lambda, aws_iam_policy_attachment.lambda_policy_attachment]
}

resource "aws_lambda_function" "tasks_lambda" {
  function_name = "tasks-lambda"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_role.arn
  handler       = "tasks_lambda.lambda_handler"
  filename      = "../lambda_functions/tasks_lambda.zip"
  source_code_hash = filebase64sha256("../lambda_functions/tasks_lambda.zip")
  depends_on = [aws_iam_policy_attachment.lambda_policy_attachment]
}

resource "aws_lambda_function" "dynamodb_lambda" {
  function_name = "dynamodb-lambda"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_role.arn
  handler       = "dynamodb_lambda.lambda_handler"
  filename      = "../lambda_functions/dynamodb_lambda.zip"
  source_code_hash = filebase64sha256("../lambda_functions/dynamodb_lambda.zip")
  environment {
    variables = {
      DYNAMODB_TABLE_NAME = "grocery-items"
    }
  }
  depends_on = [aws_iam_policy_attachment.lambda_policy_attachment]
}