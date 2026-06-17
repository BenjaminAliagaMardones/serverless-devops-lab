resource "aws_ecr_repository" "mi_repositorio" {
  name = "mi-app-lambda"
}

resource "aws_iam_role" "iam_for_lambda" {

assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_lambda_function" "mi_lambda_docker" {
  function_name = "mi_funcion_docker"
  role          = aws_iam_role.iam_for_lambda.arn
  package_type  = "Image"

  image_uri = "${aws_ecr_repository.mi_repositorio.repository_url}:latest"

}