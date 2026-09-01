# reputation_managment_domain

venv/Scripts/activate
pip install -r services\media-service\requirements.txt -r services\api-gateway\requirements.txt -r services\review-service\requirements.txt

curl.exe -X PUT `
  -H "Content-Type: image/jpeg" `
  --upload-file ".\test.jpg" `
  "http://localhost:9000/review-media/media/6386ce31-3d5b-4adb-9a91-3d7ef89ea2d3/original.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=minio%2F20260831%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260831T203125Z&X-Amz-Expires=900&X-Amz-SignedHeaders=content-type%3Bhost&X-Amz-Signature=60345bb4f3e0363b20b5bc7f98f5a0ddbd7464e82b1c77db5040dd2ae6a03f19"

  {
  "media_id": "6386ce31-3d5b-4adb-9a91-3d7ef89ea2d3",
  "upload_url": "http://localhost:9000/review-media/media/6386ce31-3d5b-4adb-9a91-3d7ef89ea2d3/original.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=minio%2F20260831%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260831T203125Z&X-Amz-Expires=900&X-Amz-SignedHeaders=content-type%3Bhost&X-Amz-Signature=60345bb4f3e0363b20b5bc7f98f5a0ddbd7464e82b1c77db5040dd2ae6a03f19",
  "expires_in": 900
}