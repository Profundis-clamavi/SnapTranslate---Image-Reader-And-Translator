const fileInput = document.getElementById("fileUpload")
const imageOutput = document.getElementById("output");

fileInput.addEventListener("change", async () => {
    let [file] = fileInput.files

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
})

function languageDrop() {
    document.getElementById("myDropdown").classList.toggle("show");
  }
  
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }