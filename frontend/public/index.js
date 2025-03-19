//Wait for DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function() {
  const fileInput = document.getElementById("fileUpload");
  const imageOutput = document.getElementById("output");
  let canvas = document.querySelector('#canvas')
  let context = canvas.getContext('2d')
  let video = document.querySelector('#video')
  let image = null;
  let oldImage = null;

//------------------------------------------------------------------------
//Taking a Photo
//Basic Tutorial @ https://www.youtube.com/watch?v=nhX9EUGIZ6o&ab_channel=ConorBailey

  //Checks if theres media deviceds
  if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia){
    navigator.mediaDevices.getUserMedia({video: true}).then(stream =>{
      //changes src of video to a stream from the device
      video.srcObject = stream;
      video.play()
    })
  }

  //Button to actually take photo
  document.getElementById('snap').addEventListener('click', ()=>{
    //get height and width from the video to use to draw image on canvas
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0,0, canvas.width, canvas.height)

    //convert canvas to a dataurl to use for image
    const dataUrl = canvas.toDataURL('image/png')
    //hide video feed after taking photo
    video.style.display = "none";
    //hide snap button after taking photo
    document.getElementById("snap").style.display = "none";
    //set img on website to the photo user took
    const imgElement = document.getElementById("output");
    imgElement.src = dataUrl
    imgElement.style.display = "block"
    let dataBlob = dataUrlToBlob(dataUrl);
    image = dataBlob
  })

  //button to decide to take photo instead of upload photo
  document.getElementById('takePicBtn').addEventListener('click', async () => {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        try {
            // Request camera permission
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });

            // Show necessary elements if permission is granted
            let videoElement = document.getElementById('video');
            let canvasElement = document.getElementById('canvas');
            let snapBtnElement = document.getElementById('snap');
            const imgElement = document.getElementById("output");

            canvasElement.style.display = "none";
            videoElement.style.display = "block";
            snapBtnElement.style.display = "block";
            imgElement.src = "";
            imgElement.style.display = "none";
            videoElement.srcObject = stream;
            await videoElement.play();

        } catch (error) {
            console.error("Camera access denied:", error);
            alert("Camera access is required to take a photo. Please allow camera permissions.");
        }
    } else {
        alert("Your browser does not support camera access.");
    }
});


  //Function Derived from different stackoverflow posts, used to change dataURL to blobs because
  //blobs are more size friendly, especially when used for axios requests to backends
  function dataUrlToBlob(dataUrl) {
    const [metadata, base64Data] = dataUrl.split(',');
    const binaryData = atob(base64Data);
    const byteArray = new Uint8Array(binaryData.length);
    for (let i = 0; i < binaryData.length; i++) {
        byteArray[i] = binaryData.charCodeAt(i);
    }
    const mimeType = metadata.match(/:(.*?);/)[1];
    return new Blob([byteArray], { type: mimeType });
}


//------------------------------------------------------------------------
//Image Upload
//Check for changes to fileInput then runs following code. 
  fileInput.addEventListener("change", async () => {
    let file = fileInput.files[0];

    //Check if fileInput.files length is greater than 0(meaning the file upload wasnt cancelled or interupted)
    if (fileInput.files.length > 0){
      //Save a copy of the image into oldImage for if image dialog is interupted next time
      oldImage = fileInput.files[0];
      //Set image to the image from the upload
      image = fileInput.files[0];
    } else {
      //else is entered if file input is interuppted or cancelled
      //sets file and image equal to the image that was there previously to let it continue to run
      file = oldImage;
      image = oldImage;
    }
    
    const reader = new FileReader();
    reader.onload = (e) => {
      imageOutput.src = e.target.result;
    };

    reader.onerror = (err) => {
      console.error("Error reading file:", err);
      alert("An error occurred while reading the file.");
    };

    //makes the element that holds the image visible. (was set to be invisble)
    var displayElement = document.getElementById("output");
    displayElement.style.display = "block";
    reader.readAsDataURL(file);
  });

//------------------------------------------------------------------------
//Language dropdowns
  window.languageDrop = function() {
    document.getElementById("myDropdown").classList.toggle("show");
  };
  
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      for (var i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  };
  //------------------------------------------------------------------------
  //Translate Button

  //function to scroll to bottom of the screen for after image is processed
  const scrollingElement = (document.scrollingElement || document.body);
  const scrollToBottom = () => {scrollingElement.scrollTop = scrollingElement.scrollHeight}

  window.translateBtn = function() {
    //check if theres an image
    if (image){

      let videoElement = document.getElementById('video');
      let canvasElement = document.getElementById('canvas');
      canvasElement.style.display ="none"
      let snapBtnElement = document.getElementById('snap');
      videoElement.style.display = "none";
      snapBtnElement.style.display = "none";

      imageUrl = URL.createObjectURL(image)
      document.getElementById('output').src = imageUrl;
      //disable the translate button to avoid multiple requests being made
      document.getElementById("translateBtn").disabled = true;
      //unhide the spinning circle to show users somethings happening
      document.getElementById("loader").style.display = "block";
      //hide any old images that were processed
      document.getElementById("translated-image").style.display = "none";


      //gather user inputs
      var inputMenu = document.getElementById("inputOptions");
      var inputValue = inputMenu.value;
      var outputMenu = document.getElementById("outputOptions");
      var outputValue = outputMenu.value;
      var imageFile = image

      //create form data from user inputs to send to backend
      const formData = new FormData();
      formData.append('inputLanguage', inputValue);
      formData.append('outputLanguage', outputValue);
      formData.append('image', imageFile);

        //send request to backend endpoint with formdata
        axios.post("http://localhost:5000/api", formData, { 
          withCredentials: true
        })
        .then(response => {
          //hide the spinning circle after the request is done
          document.getElementById("loader").style.display = "none";
          //reveal title for output area
          document.getElementById("outputTitle").style.display = "block";
        
          //display image to user
          const imgElement = document.getElementById("translated-image");
          imgElement.src = response.data.translatedImage;
          imgElement.style.display = "block";

          //re-enable button for next request
          document.getElementById("translateBtn").disabled = false;
          //set focus to image
          scrollToBottom();

        })
        .catch(error => {
          console.error("Error:", error);
        });
    } 
    //this else is if there is no file in image, displays an alert to the user and re-enables the button
    else {
      alert("Please upload an image.");
      document.getElementById("translateBtn").disabled = false;
    }
}})