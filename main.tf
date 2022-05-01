terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>2.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "random_password" "password" {
  length = 8
  min_upper = 1
  min_lower = 1
  min_numeric = 1
}

data "azurerm_resource_group" "main" {
  name = "CreditSuisse21_JacquelineUngerer_ProjectExercise"
}