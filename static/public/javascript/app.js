//Efeito Máquina de escrever
function typeWrite(elemento) {
  const textoArray = elemento.innerHTML.split("");
  elemento.innerHTML = " ";
  textoArray.forEach(function (letra, i) {
    setTimeout(function () {
      elemento.innerHTML += letra;
    }, 150 * i);
  });
}
try {
  const titulo = document.querySelector(".titulo-principal");
  window.onload = typeWrite(titulo); 
} catch {
  console.log("Título Principal não está disponível ou alcançável...\nVocê abriu esta página diretamente?")
}

//PréLoader
function show_anything(evento) {
  let valor_input = document.querySelector("#id-search");
  let pre_loader = document.querySelector("#preloader");
  let alerta = document.querySelector("#alerta");
  let springerlink = document.querySelector("#id-springerlink").checked;
  let sciencedirect = document.querySelector("#id-sciencedirect").checked;
  const div_mensagem = document.querySelector("#alerta-mensagem");

  if (valor_input.value == "") {
    evento.preventDefault();
    alerta.classList.remove("hidden-anything");
    alerta.classList.add("show-anything");
    div_mensagem.innerHTML = `É necessário informar algum termo no campo de busca, exemplo: <strong>Technology</strong>`;
  } else if (springerlink == false && sciencedirect == false) {
    evento.preventDefault();
    alerta.classList.remove("hidden-anything");
    alerta.classList.add("show-anything");
    div_mensagem.innerHTML = `É necessário escolher uma base de dados!`;
  } else {
    pre_loader.classList.remove("hidden-anything");
    pre_loader.classList.add("show-anything");
  }
}
const btn = document.querySelector("#button-addon2");
btn.addEventListener("click", show_anything, false);

//arrasta e solta JS
function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData("text/plain", ev.target.id);
}

function drop(ev) {
  ev.preventDefault();
  let data = ev.dataTransfer.getData("text");
  ev.target.appendChild(document.getElementById(data));
}

let classificationBoxId = 0;

function createClassification() {
  let location = document.querySelector("#location-classification");
  let boxClassification = document.createElement("div")
  let headerClassification = document.createElement("div")
  let nameClassification = document.createElement("input")
  let bodyClassification = document.createElement("div")
  let footerClassification = document.createElement("div")
  let btnDownloadResult = document.createElement("button")
  let id = classificationBoxId

  btnDownloadResult.setAttribute("onclick", `printResult(${id})`)
  btnDownloadResult.setAttribute("id", `btn-download-classification-${id}`)
  btnDownloadResult.classList.add("btn-download-result")
  btnDownloadResult.innerHTML = "Download"

  footerClassification.classList.add("d-flex", "justify-content-end")

  bodyClassification.setAttribute("ondrop", "drop(event)")
  bodyClassification.setAttribute("ondragover", "allowDrop(event)")
  bodyClassification.setAttribute("id", `body-classification-${id}`)
  bodyClassification.classList.add("card-body", "text-primary", "conteudo")
  bodyClassification.style.minWidth = '100%'
  bodyClassification.style.padding = '2em'

  nameClassification.setAttribute("type", "text")
  nameClassification.setAttribute("placeholder", "Nome da classificação")
  nameClassification.setAttribute("id", `nameClassification-${id}`)
  nameClassification.classList.add("d-block", "w-100", "input-name-classification")

  headerClassification.classList.add("card-header", "d-flex", "justify-content-center", "w-100", "classification-header")
  headerClassification.append(nameClassification)

  boxClassification.setAttribute("id", `box-classification-${id}`)
  boxClassification.classList.add("card", "border-warning", "mb-3", "mt-3", "box-classification")
  boxClassification.append(headerClassification, bodyClassification, footerClassification)

  location.append(boxClassification)
  classificationBoxId += 1
}

let indiceDownloadTreemap = 0;

function printResult() {

  let allBoxList = document.querySelectorAll(`.box-classification`)
  let listaValores = []

  allBoxList.forEach((elem) => {

    let valores = []
    let titulo = elem.childNodes[0].childNodes[0].value;
    let conteudos = elem.childNodes[1].childNodes
    
    conteudos.forEach((elem) => {
      let texto = elem.childNodes[1].innerText;
      let quantidade = elem.childNodes[3].innerText
      let addValores = [texto, quantidade]
      valores.push(addValores)
    })

    let classificacao = {
      Classificação: titulo,
      Termos: valores
    }

    listaValores.push(classificacao)
  })

return listaValores
}

function generateZIP() {
  console.log('TEST');
  var zip = new JSZip();
  var count = 0;
  var zipFilename = "Pictures.zip";

  links.forEach(function (url, i) {
    var filename = links[i];
    filename = filename.replace(/[\/\*\|\:\<\>\?\"\\]/gi, '').replace("httpsi.imgur.com","");
    // loading a file and add it in a zip file
    JSZipUtils.getBinaryContent(url, function (err, data) {
      if (err) {
        throw err; // or handle the error
      }
      zip.file(filename, data, { binary: true });
      count++;
      if (count == links.length) {
        zip.generateAsync({ type: 'blob' }).then(function (content) {
          saveAs(content, zipFilename);
        });
      }
    });
  });
}

function baixarGraficos() {
  alert("Aguarde. Todos os TreeMaps serão baixados individualmente.");
  Highcharts.charts.forEach(chart => {
    chart.exportChart()
  })
}

function mostrarGraficoTreemapDownload(nomeClassificacao, objetosTreemap) {
  Highcharts.chart('graficoTreemapDownload', {
    plotOptions: {
      treemap: {
        stacking: 'normal',
        cropThreshold: 10,
        dataGrouping: {
          enabled: true
        }
      }
    },
    colorAxis: {
      minColor: '#FFFFFF',
      maxColor: Highcharts.getOptions().colors[0]
    },
    series: [{
      type: 'treemap',
      layoutAlgorithm: 'squarified',
      data: objetosTreemap
    }],
    title: {
      text: nomeClassificacao
    }
  });  
}

function parseDados(resultados) {
  let objetosTreemap = [];
  let nomeClassificacao;

  let elem = resultados[indiceDownloadTreemap]

  nomeClassificacao = elem['Classificação']
  for (let i = 0; i < elem['Termos'].length; i++) {
    objetosTreemap.push({name: elem['Termos'][i][0], value: parseInt(elem['Termos'][i][1]), colorValue: parseInt(elem['Termos'][i][1])})
  }
  
  mostrarGraficoTreemapDownload(nomeClassificacao, objetosTreemap);
}

function proximoGraficoTreemapDL() {
  qtdBoxClassification = document.querySelectorAll(`.box-classification`).length;
  if (indiceDownloadTreemap < qtdBoxClassification) {
    indiceDownloadTreemap += 1;
    parseDados(printResult());
  }  
}

function anteriorGraficoTreemapDL() {
  if (indiceDownloadTreemap > 0) {
    indiceDownloadTreemap -= 1;
    parseDados(printResult());
  }  
}
