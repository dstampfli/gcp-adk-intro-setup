# Sample Agent2Agent Protocol Agent

```shell
REGION=us-central1
gcloud run deploy a2a-server \
    --no-allow-unauthenticated \
    --region=$REGION \
    --set-env-vars=GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT \
    --set-env-vars=GOOGLE_CLOUD_LOCATION=$REGION \
    --set-env-vars=GOOGLE_GENAI_USE_VERTEXAI=TRUE \
    --source .
```
