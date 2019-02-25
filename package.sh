mkdir tmp411

COPY ./briefer_folder /

python3 -m pip install REPO/DIR tmp411

rm -f /io/lambda.zip
cp -r /io/* tmp411

cd tmp411
zip -r /io/lambda.zip *