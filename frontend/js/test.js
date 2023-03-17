let imageFile = null;

async function generateCaption() {
  if (!imageFile){
    alert("Porfavor inserte imagen");
    return;
  }

  const formData = new FormData();
  formData.append('file', imageFile);

  const response = await fetch('/generate_caption', {
    method: 'POST',
    body: formData
  });

  const result = await response.json();
  var element = document.getElementById("caption_result");
  element.innerHTML = result;
}


async function classifyImage() {
  if (!imageFile){
    alert("Porfavor inserte imagen");
    return;
  }

  const formData = new FormData();
  formData.append('file', imageFile);

  const response = await fetch('/predict_type', {
    method: 'POST',
    body: formData
  });

  const result = await response.json();
  
  const ul = document.getElementById('clases');
  const listItems = ul.getElementsByTagName('li');
  
  listItems[0].innerHTML = "Sin gráfico: " + result["just_image"] + "%";
  listItems[1].innerHTML = "Gráfico de barras: " + result["bar_chart"] + "%";
  listItems[2].innerHTML = "Diagrama: " + result["diagram"] + "%";
  listItems[3].innerHTML = "Gráfico de flujo: " + result["flow_chart"] + "%";
  listItems[4].innerHTML = "Gráfico de ejes: " + result["graph"] + "%";
  listItems[5].innerHTML = "Gráfico de crecimiento: " + result["growth_chart"] + "%";
  listItems[6].innerHTML = "Gráfico circular: " + result["pie_chart"] + "%";
  listItems[7].innerHTML = "Gráfico de tabla: " + result["table"] + "%";
}

async function calculateSimilarity() {
  if (!imageFile){
    alert("Porfavor inserte imagen");
    return;
  }
  const query_text = document.getElementById("form").elements;
  if (!query_text[0].value){
    alert("Porfavor inserte texto");
    return;
  }
  const formData = new FormData();
  formData.append('file', imageFile);

  const response = await fetch('/compute_similarity?text='+query_text[0].value, {
    method: 'POST',
    body: formData
  });

  const result = await response.json();
  var element = document.getElementById("similarity_result");
  element.innerHTML = "Porcentaje obtenido " + result['max_score'] + "% \n" + "Texto adecuado a imagen " + result['adequate'] + ".\n Limite usado para decidirlo " + result["limit_used"] + "%.";
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

