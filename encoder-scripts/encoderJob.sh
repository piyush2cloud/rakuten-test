export AWS_PROFILE=cloud
echo $1
echo $2
echo $3
echo $4
echo $5
mkdir $4
cd $4
BUCKET_NAME="rakuten-prod-video-data"
curl -o "video.mp4" $1
../bento/bin/mp4fragment video.mp4 video-fragmented.mp4
../bento/bin/mp4encrypt --method MPEG-CENC --key 1:${2}:random --property 1:KID:${3} --global-option mpeg-cenc.eme-pssh:true video-fragmented.mp4 video-encrypted.mp4
../bento/bin/mp4dash -o rakuten-output video-encrypted.mp4
IS_SUCCESS="$?"
echo ${IS_SUCCESS}

if [ "$IS_SUCCESS" -eq "0" ]
then
echo "Update Status and Upload to S3"
videoStatus="ENCODE_COMPLETE"
cd ..
echo $4
echo ${PWD}
aws s3 cp "./$4" s3://"${BUCKET_NAME}/${4}" --recursive --acl public-read-write
s3DashPath="https://${BUCKET_NAME}.s3.amazonaws.com/${4}/rakuten-output/stream.mpd"
echo $s3DashPath
BODY_DATA="{\"packagingId\":\"$5\",\"videoStatus\":\"$videoStatus\", \"dashUrl\":\"$s3DashPath\", \"key\":\"$2\", \"kid\":\"$3\"}"
echo $BODY_DATA
curl -H 'Content-Type: application/json' -X POST -d "$BODY_DATA" "https://c35gbfabih.execute-api.us-east-1.amazonaws.com/prod/video_encode_status"

else
videoStatus="ENCODE_FAILURE"
echo "Media Packaging Failed"
s3DashPath="NULL"
BODY_DATA="{\"packagingId\":\"$5\",\"videoStatus\":\"$videoStatus\", \"dashUrl\":\"$s3DashPath\", \"key\":\"$2\", \"kid\":\"$3\"}"
echo $BODY_DATA
curl -H 'Content-Type: application/json' -X POST -d "$BODY_DATA" "https://c35gbfabih.execute-api.us-east-1.amazonaws.com/prod/video_encode_status"
fi

rm -r "./${4}"