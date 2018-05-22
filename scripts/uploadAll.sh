echo "Uploading readyToUpload lectures"
cd "${0%/*}"
for semester in $(ls /home/paol/recordings/readyToUpload)
do
    echo "Semester:	$semester"
    for course in $(ls /home/paol/recordings/readyToUpload/$semester)
    do
    	echo ">Course:	$course"
    	for lecture in $(ls /home/paol/recordings/readyToUpload/$semester/$course)
    	do
    	    echo ">>Lecture:	$lecture"
    	    # /home/paol/paol-code/scripts/upload/createThumbnails.sh "/home/paol/recordings/readyToUpload/$semester/$course/$lecture"
          ./uploadcurl.sh "/home/paol/recordings/readyToUpload/$semester/$course/$lecture"
      		echo
      done
    done
done
