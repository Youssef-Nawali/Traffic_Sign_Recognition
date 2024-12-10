function detectTrafficSign() {
    const fileInput = document.getElementById("imageInput");
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    // Sending the image to the server using fetch
    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Update the result section with prediction
        const resultDiv = document.getElementById("result");
        document.getElementById("prediction").textContent = data.result;
        resultDiv.style.display = "block";
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Error occurred during prediction!");
    });
}
