# Sample Agent2Agent Protocol Agent

```shell
MCP_SERVER_CLOUD_RUN_URL=`gcloud run services describe mcp-server \
    --project=$GOOGLE_CLOUD_PROJECT \
    --region $GOOGLE_CLOUD_LOCATION \
    --format='value(status.url)'`

gcloud run deploy a2a-server \
    --no-allow-unauthenticated \
    --project=$GOOGLE_CLOUD_PROJECT \
    --region=$GOOGLE_CLOUD_LOCATION \
    --set-env-vars=GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT \
    --set-env-vars=GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION \
    --set-env-vars=GOOGLE_GENAI_USE_VERTEXAI=TRUE \
    --set-env-vars=MCP_SERVER_CLOUD_RUN_URL=$MCP_SERVER_CLOUD_RUN_URL \
    --source .
```

```shell
gcloud run services proxy --project=$GOOGLE_CLOUD_PROJECT --region $GOOGLE_CLOUD_LOCATION --port=8080 a2a-server
```
