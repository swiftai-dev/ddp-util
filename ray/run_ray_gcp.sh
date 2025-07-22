# install gcloud
curl https://sdk.cloud.google.com | bash

export GOOGLE_PROJECT_ID=be-loo-prototyping
# login to gcloud
gcloud init

gcloud config set project $GOOGLE_PROJECT_ID

# install ray and dependencies
pip install -U "ray[default]" google-cloud-compute
