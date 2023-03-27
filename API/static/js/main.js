let imageFile = null;

async function generateCaption() {
  if (!imageFile){
    alert("Porfavor inserte imagen");
    return;
  }

  const formData = new FormData();
  formData.append('file', imageFile);

  var element = document.getElementById("caption_result");
  
  element.innerHTML = "Espere mientras se genera su descripción...";
  
  const response = await fetch('/generate_caption', {
    method: 'POST',
    body: formData
  });

  const result = await response.json();
  element.innerHTML = result;
}


async function classifyImage() {
  if (!imageFile){
    alert("Porfavor inserte imagen");
    return;
  }

  const formData = new FormData();
  formData.append('file', imageFile);

  const ul = document.getElementById('clases');
  const listItems = ul.getElementsByTagName('li');

  listItems[0].innerHTML = "Sin gráfico: " + "Espere mientras se calcula la predicción...";
  listItems[1].innerHTML = "Gráfico de barras: " + "Espere mientras se calcula la predicción...";
  listItems[2].innerHTML = "Diagrama: " + "Espere mientras se calcula la predicción...";
  listItems[3].innerHTML = "Gráfico de flujo: " + "Espere mientras se calcula la predicción...";
  listItems[4].innerHTML = "Gráfico de ejes: " + "Espere mientras se calcula la predicción...";
  listItems[5].innerHTML = "Gráfico de crecimiento: " + "Espere mientras se calcula la predicción...";
  listItems[6].innerHTML = "Gráfico circular: " + "Espere mientras se calcula la predicción...";
  listItems[7].innerHTML = "Gráfico de tabla: " + "Espere mientras se calcula la predicción...";
  
  const response = await fetch('/predict_type', {
    method: 'POST',
    body: formData
  });

  const result = await response.json();
  
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

  var element = document.getElementById("similarity_result");
  element.innerHTML = "Espere mientras se calcula la similitud semántica...";
  
  const response = await fetch('/compute_similarity?text='+query_text[0].value, {
    method: 'POST',
    body: formData
  });

  const result = await response.json();
  element.innerHTML = "Porcentaje obtenido " + result['max_score'] + "% \n" + "Texto adecuado a imagen " + result['adequate'] + ".\n Limite usado para decidirlo " + result["limit_used"] + "%.";
}

async function reset_outputs(){
  // reset caption
  var element = document.getElementById("caption_result");
  element.innerHTML = "";

  // reset predictions
  const ul = document.getElementById('clases');
  const listItems = ul.getElementsByTagName('li');

  listItems[0].innerHTML = "Sin gráfico: ";
  listItems[1].innerHTML = "Gráfico de barras: ";
  listItems[2].innerHTML = "Diagrama: ";
  listItems[3].innerHTML = "Gráfico de flujo: ";
  listItems[4].innerHTML = "Gráfico de ejes: ";
  listItems[5].innerHTML = "Gráfico de crecimiento: ";
  listItems[6].innerHTML = "Gráfico circular: ";
  listItems[7].innerHTML = "Gráfico de tabla: ";
  
  // reset similarity
  var element = document.getElementById("similarity_result");
  element.innerHTML = "";
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
  reset_outputs();
}

