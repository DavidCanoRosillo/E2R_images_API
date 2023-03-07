let imageFile = null;

async function generateCaption() {
  if (!imageFile){
    alert("Please insert image");
    return;
  }

  const formData = new FormData();
  formData.append('file', imageFile);

  const response = await fetch('/generate_caption', {
    method: 'POST',
    body: formData
  });

  const result = await response.text();

  var element = document.getElementById("caption_result");
   element.innerHTML = result;
}


async function classifyImage() {
  if (!imageFile){
    alert("Please insert image");
    return;
  }

  const formData = new FormData();
  formData.append('file', imageFile);

  const response = await fetch('/predict_type', {
    method: 'POST',
    body: formData
  });

  const result = await response.text();

  var element = document.getElementById("caption_result");
   element.innerHTML = result;
}

async function calculateSimilarity() {
  if (!imageFile){
    alert("Please insert image");
    return;
  }
  const query_text = document.getElementById("form").elements;
  const formData = new FormData();
  formData.append('file', imageFile);

  const response = await fetch('/compute_similarity?text='+query_text[0].value, {
    method: 'POST',
    body: formData
  });

  const result = await response.text();

  var element = document.getElementById("caption_result");
  element.innerHTML = result;
}

function loadImage(event){
  const file = event.target.files[0];
  const reader = new FileReader();
  image = document.getElementById("output");
  reader.onload = function(event) {
    image.src = event.target.result;
    imageFile = file;
  };
  reader.readAsDataURL(file);
}

