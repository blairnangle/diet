terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.23.1"
    }
  }
}

provider "aws" {
  region = "eu-west-2"
}

terraform {
  backend "s3" {
    bucket         = "terraform-state-blair-nangle"
    key            = "information-diet/terraform.tfstate"
    region         = "eu-west-2"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
