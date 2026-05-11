variable "aws_region" {
  description = "AWS region to deploy in"
  type        = string
  default     = "ap-south-1"  # Mumbai — lowest latency from India
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "devops-demo"
}

variable "public_key_path" {
  description = "Path to your SSH public key"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "allowed_ssh_cidr" {
  description = "Your IP for SSH access (run: curl ifconfig.me)"
  type        = string
  default     = "0.0.0.0/0"  # Replace with your IP/32 in production
}

variable "github_repo" {
  description = "GitHub repo in owner/repo format"
  type        = string
  default     = "yourusername/devops-project"
}
