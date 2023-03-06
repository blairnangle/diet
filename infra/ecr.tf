resource "aws_ecr_repository" "pocket" {
  name                 = "pocket"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "information-diet image registry"
  }
}
