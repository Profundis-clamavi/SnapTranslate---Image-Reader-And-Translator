//Wait for DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function() {
  const fileInput = document.getElementById("fileUpload");
  const imageOutput = document.getElementById("output");
  let image = null;
  let oldImage = null;

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