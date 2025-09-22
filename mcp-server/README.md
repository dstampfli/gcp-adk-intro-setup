# Sample Model Context Protocol Server

```shell
gcloud run deploy mcp-server \
    --no-allow-unauthenticated \
    --project=$GOOGLE_CLOUD_PROJECT \
    --region=$GOOGLE_CLOUD_LOCATION \
    --set-env-vars=GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT \
    --set-env-vars=GOOGLE_CLOUD_LOCATION=$REGION \
    --set-env-vars=GOOGLE_GENAI_USE_VERTEXAI=TRUE \
    --source .
```

```shell
gcloud run services proxy --project=$GOOGLE_CLOUD_PROJECT --region $GOOGLE_CLOUD_LOCATION --port=8888 mcp-server
```
