variable "prefix" {
  description = "The prefix used for all resources in this environment"
  default = ""
}
variable "location" {
  description = "The Azure location where all resources in this deployment should be created"
  default     = "uksouth"
}
variable "CLIENT_ID" {
  description = "The GitHub CLIENT_ID for application authentication"
  sensitive   = true
}
variable "CLIENT_SECRET" {
  description = "The GitHub CLIENT_SECRET for application authentication"
  sensitive   = true
}