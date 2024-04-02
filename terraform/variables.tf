locals {
  data_lake_bucket = "myanimelist_data_lake"
}

# variable "credentials" {
#   description = "My Credentials"
#   default     = "<Path to your Service Account json file>"
#   #ex: if you have a directory where this file is called keys with your service account json file
#   #saved there as my-creds.json you could use default = "./keys/my-creds.json"
# }

variable "project" {
  description = "Project"
  # default     = "<Your Project ID>"
}

variable "region" {
  description = "Region"
  #Update the below to your desired region
  default = "asia-southeast1"
}

# Argument name location has been set to use var.region
# instead of the values defined at var.location
# variable "location" {
#   description = "Project Location"
#   #Update the below to your desired location
#   default = "Jurong West, Singapore, APAC"
# }

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  #Update the below to what you want your dataset to be called
  default = "myanimelist_data"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}
