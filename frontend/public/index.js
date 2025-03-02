document.addEventListener("DOMContentLoaded", function() {
  const fileInput = document.getElementById("fileUpload");
  const imageOutput = document.getElementById("output");

  fileInput.addEventListener("change", async () => {
    let [file] = fileInput.files;

    const reader = new FileReader();
    reader.onload = (e) => {
      imageOutput.src = e.target.result;
    };

    reader.onerror = (err) => {
      console.error("Error reading file:", err);
      alert("An error occurred while reading the file.");
    };

    var displayElement = document.getElementById("image-container");
    displayElement.style.display = "block";
    reader.readAsDataURL(file);
  });

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

  window.translateBtn = function() {
    var inputMenu = document.getElementById("inputOptions");
    var inputValue = inputMenu.value;
    var outputMenu = document.getElementById("outputOptions");
    var outputValue = outputMenu.value;
    var imageElement = document.getElementById("fileUpload");
    var imageFile = imageElement.files[0];

    const formData = new FormData();
    formData.append('inputLanguage', inputValue);
    formData.append('outputLanguage', outputValue);
    formData.append('image', imageFile);
    
    axios.post("http://localhost:5000/api", formData, { 
      withCredentials: true
    })
    .then(response => {
      console.log(response.data);
      const imgElement = document.getElementById("translated-image");
      imgElement.src = response.data.translatedImage;

    })
    .catch(error => {
      console.error("Error:", error);
    });
  };
});