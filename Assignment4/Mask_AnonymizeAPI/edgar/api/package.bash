root_dir='/Users/prudhvichandra/PycharmProjects/fastapi_lambda/cryptoAPI'
venv_dir="/Users/prudhvichandra/PycharmProjects/fastapi_lambda/venv/lib/python3.7/site-packages"
bucket_name="prudhvics"
function_name="fastAPI"
cd $venv_dir && zip -r9 "$root_dir/lambda.zip" . \
&& cd "$root_dir/api" && zip -g ../lambda.zip -r .

cd $root_dir && aws s3 cp lambda.zip s3://$bucket_name/lambda.zip
aws lambda update-function-code --function-name $function_name \
--s3-bucket $bucket_name --s3-key lambda.zip