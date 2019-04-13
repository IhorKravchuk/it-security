variable "skunkworks-project_name" {default="skunkworks-project"}


# ------------------------------------------------
# Creating required usrs and groups inside G-Suite
#-------------------------------------------------


provider "gsuite" {
  credentials = "/Users/thor/.config/gcloud/infosec-terraform-admin.json"
  impersonated_user_email = "ingvar_ua@company-test.com"
  oauth_scopes = [
  "https://www.googleapis.com/auth/admin.directory.group",
  "https://www.googleapis.com/auth/admin.directory.user"
]
}

resource "gsuite_group" "skunkworks-team" {
  email       = "skunkworks-team@company-test.com"
  name        = "skunkworks-team@company-test.com"
  description = "skunkworks team"
}

# Creating users :

# Creating Ivan Mazepa user
resource "gsuite_user" "ivan_mazepa" {
  # advise to set this field to true on creation, then false afterwards
  change_password_next_login = false
  name {
    family_name = "Mazepa"
    given_name = "Ivan"
  }
  # on creation this field is required
#  password = "7864648UI&83g*&^89te"
  primary_email = "ivan.mazepa@company-test.com"
}

resource "gsuite_group_member" "ivan_mazepa" {
  group = "${gsuite_group.skunkworks-team.email}"
  email = "${gsuite_user.ivan_mazepa.primary_email}"
  role = "MEMBER" # OWNER/MANAGER/MEMBER
}

# Creating Simon Petlura user
resource "gsuite_user" "simon_petlura" {
  # advise to set this field to true on creation, then false afterwards
  change_password_next_login = false
  name {
    family_name = "Petlura"
    given_name = "Simon"
  }
  # on creation this field is required
#  password = "rrjji944UI&83g*&^89tf"
  primary_email = "simon.petlura@company-test.com"
}

resource "gsuite_group_member" "simon_petlura" {
  group = "${gsuite_group.skunkworks-team.email}"
  email = "${gsuite_user.simon_petlura.primary_email}"
  role = "MEMBER" # OWNER/MANAGER/MEMBER
}



# ---------------------------
# Creating GCP Project
#----------------------------


provider "google" {
 region = "${var.region}"
 credentials = "${file("/Users/thor/.config/gcloud/infosec-terraform-admin.json")}"
}

resource "random_id" "id" {
 byte_length = 4
 prefix      = "${var.skunkworks-project_name}-"
}

resource "google_project" "skunkworks-project" {
 name            = "${var.skunkworks-project_name}"
 project_id      = "${random_id.id.hex}"
 billing_account = "${var.billing_account}"
 org_id          = "${var.org_id}"
}

resource "google_project_services" "skunkworks-project" {
 project = "${google_project.skunkworks-project.project_id}"
 services = [
   "storage-api.googleapis.com"
 ]
}

resource "google_project_iam_binding" "skunkworks-project" {
  project = "${google_project.skunkworks-project.project_id}"
  role    = "roles/editor"

  members = [
    "group:${gsuite_group.skunkworks-team.email}",
  ]
}





output "project_id" {
 value = "${google_project.skunkworks-project.project_id}"
}
