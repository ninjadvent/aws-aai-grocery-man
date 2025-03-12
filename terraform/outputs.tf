output "orchestrator_lambda_arn" {
  description = "The ARN of the orchestrator Lambda function"
  value       = aws_lambda_function.orchestrator.arn
}

output "api_gateway_url" {
  description = "The URL of the API Gateway"
  value       = aws_api_gateway_rest_api.grocery_api.execution_arn
}
