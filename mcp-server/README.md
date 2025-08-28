# Sample Model Context Protocol Server

```shell
REGION=us-central1
gcloud run deploy mcp-server \
    --no-allow-unauthenticated \
    --region=$REGION \
    --set-env-vars=GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT \
    --set-env-vars=GOOGLE_CLOUD_LOCATION=$REGION \
    --set-env-vars=GOOGLE_GENAI_USE_VERTEXAI=TRUE \
    --source .
```
