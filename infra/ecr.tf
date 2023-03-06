resource "aws_ecr_repository" "information_diet_image_registry" {
  name                 = "information-diet-image-registry"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "information-diet image registry"
  }
}
