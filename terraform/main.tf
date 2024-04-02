terraform {
  required_version = ">= 1.7.4"
  backend "local" {}
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.22.0"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
  // credentials = file(var.credentials)  # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}

# Data Lake Bucket
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "data-lake-bucket" {
  name     = "${local.data_lake_bucket}_${var.project}" # Concatenating DL bucket & Project name for unique naming
  location = var.region

  # Optional, but recommended settings:
  storage_class               = var.gcs_storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 // days
    }
  }

  force_destroy = true
}

# DWH
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.bq_dataset_name
  project    = var.project
  location   = var.region

  # (Optional) If set to true, delete all the tables
  # in the dataset when destroying the resource;
  # otherwise, destroying the resource will fail if tables are present.
  // delete_contents_on_destroy = true
}
