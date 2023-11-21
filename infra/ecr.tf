resource "aws_ecr_repository" "pocket" {
  name                 = "pocket"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "pocket"
  }
}

resource "aws_ecr_repository" "goodreads" {
  name                 = "goodreads"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "goodreads"
  }
}

resource "aws_ecr_repository" "letterboxd" {
  name                 = "letterboxd"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "letterboxd"
  }
}
