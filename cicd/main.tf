provider "aws" {
  region = "us-east-1"
}

# -----------------------------
# Key Pair
# -----------------------------
resource "aws_key_pair" "checklist_key" {
  key_name   = "checklist-key"
  public_key = file("~/.ssh/checklist-key.pub")
}

# -----------------------------
# Security Group
# -----------------------------
resource "aws_security_group" "checklist_sg" {
  name        = "checklist-sg"
  description = "Allow SSH, HTTP, 8000"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# -----------------------------
# Free Tier EC2 Instance
# -----------------------------
resource "aws_instance" "checklist_ec2" {
  ami                         = "ami-0bbdd8c17ed981ef9" # Ubuntu 22.04 LTS Free Tier AMI
  instance_type               = "t2.micro"
  key_name                    = aws_key_pair.checklist_key.key_name
  vpc_security_group_ids      = [aws_security_group.checklist_sg.id]
  associate_public_ip_address = true

  user_data = <<-EOF
              #!/bin/bash
              apt-get update -y
              apt-get upgrade -y
              apt-get install -y git curl wget docker.io

              systemctl start docker
              systemctl enable docker
              usermod -aG docker ubuntu

              # Install Docker Compose
              DOCKER_COMPOSE_VERSION="2.27.0"
              curl -L "https://github.com/docker/compose/releases/download/v$DOCKER_COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
              chmod +x /usr/local/bin/docker-compose
              
              EOF

  tags = {
    Name = "ChecklistApp-FreeTier"
  }
}

output "ec2_public_ip" {
  value = aws_instance.checklist_ec2.public_ip
}
