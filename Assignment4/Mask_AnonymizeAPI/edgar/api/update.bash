root_dir='/Users/prudhvichandra/PycharmProjects/fastapi_lambda'
venv_dir="/Users/prudhvichandra/PycharmProjects/fastapi_lambda/venv/lib/python3.7/site-packages"
# ensure that if we added new packages, they will also be added to the zip file
cd $venv_dir && zip -r9 "$root_dir/lambda.zip" . && cd "$root_dir/api" && zip -g ../lambda.zip -r .
# -r means recursive, 9 means: compress better, -g Grow (append to) the specified zip archive, instead of creating a new one.
zip -g ../lambda.zip -r .
# upload to S3
function_name="FastAPI"
bucket="prudhvics"
aws s3 cp ../lambda.zip s3://$bucket/lambda.zip
aws lambda update-function-code --function-name $function_name --s3-bucket $bucket --s3-key lambda.zip
