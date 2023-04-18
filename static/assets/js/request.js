function processText(auth_token) {
  clear();
  var inputText = document.getElementById("input-text-process").value;
  var processButton = document.getElementById("process-button");
  // disable the button to prevent further processing
  //processButton.disabled = true;

  var xhr = new XMLHttpRequest();
  xhr.open("GET", "http://localhost:8000/process?text=" + inputText);
  xhr.setRequestHeader("Authorization", "Token " + auth_token);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        var response = xhr.responseText;
        try {

          var result = JSON.parse(response);
          var entities = result["ner"]; // NER entity group 
          var nerWords = [];
          var usedEntities = new Set();
          entities.forEach(function(entity) {
            var word = entity["word"].replace(" ' " , "'");
            var entity_group = entity["entity_group"];
            var color = getColor(entity_group);
            var nerColor = getColorNer(entity_group);
            if (!usedEntities.has(entity_group)) {
                usedEntities.add(entity_group);
                nerWords.push({"word": word, "color": color, "nercolor": nerColor, "entity":entity_group});
            }
        });
        

          if(entities.length != 0){
            nerWords.forEach(function(nerWord) {
              inputText = inputText.replace(new RegExp("\\b" + nerWord["word"] + "\\b", "g"), "<span style='" + nerWord["color"] + "'>" + nerWord["word"] + "<span style='" + nerWord["nercolor"] + "'>" + nerWord["entity"]+ "</span>" + "</span>");
            });
          }else{
              inputText = "Not Found";
          }

          
          document.getElementById("result_sentiment").innerHTML = "<strong>Sentiment:</strong> " + result.sentiment.sentiment + ", <strong>Score:</strong> " + result.sentiment.score;
          document.getElementById("result_subject").innerHTML = "<strong>Subject:</strong> " + result.subject.subject + ", <strong>Score:</strong> " + result.subject.score;
          document.getElementById("result_summarize").innerHTML = "<strong>Summary:</strong> " + result.summarize.summary;
          document.getElementById("result_ner").innerHTML = "<strong>Entities:</strong> " + inputText;
          getVisible(1);
        } catch (e) {
          console.log("Error parsing response:", e);
          document.getElementById("result").innerHTML = "<strong>Error parsing response.</strong>";
          getVisible(0);
        }
      } else {
        console.log("Error:", xhr.statusText);
        document.getElementById("result").innerHTML = "<strong>Error: " + xhr.statusText + "</strong>";
        getVisible(0);
      }
      
    }
  };
  xhr.send();
}


function getColor(entity_group) {
  if (entity_group == "LOC") {
    return "background-color: #BFE6FF; color: #222; border-radius: 3px; padding: 2px;";
  } else if (entity_group == "ORG") {
    return "background-color: #8DB5E6; color: #222; border-radius: 3px; padding: 2px;";
  } else if (entity_group == "PER") {
    return "background-color: #ADD8E6; color: #222; border-radius: 3px; padding: 2px;";
  } 
}

function getColorNer(entity_group) {
  if (entity_group == "LOC") {
    return "background-color: #FFC0CB; color: #222; border-radius: 3px; padding: 2px; font-size:13px;";
  } else if (entity_group == "ORG") {
    return "background-color: #FFD700; color: #222; border-radius: 3px; padding: 2px; font-size:13px; ";
  } else if (entity_group == "PER") {
    return "background-color: #00CED1; color: #222; border-radius: 3px; padding: 2px; font-size:13px;";
  } 
}

function getVisible(error_number){

    if(error_number == 0){
      document.getElementById("result").style.display = "block";
    }
    else{
      document.getElementById("result_sentiment").style.display = "block";
      document.getElementById("result_subject").style.display = "block";
      document.getElementById("result_summarize").style.display = "block";
      document.getElementById("result_ner").style.display = "block";
    }
}


function clear(){
  document.getElementById("result").style.display = "none";
  document.getElementById("result_sentiment").style.display = "none";
  document.getElementById("result_subject").style.display = "none";
  document.getElementById("result_summarize").style.display = "none";
  document.getElementById("result_ner").style.display = "none";

}