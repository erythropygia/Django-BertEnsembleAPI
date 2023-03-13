function processText(auth_token) {
  var inputText = document.getElementById("input-text-process").value;
  var processButton = document.getElementById("process-button");

  // disable the button to prevent further processing
  processButton.disabled = true;

  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/process?text=" + inputText);
  xhr.setRequestHeader("Authorization", "Token "+auth_token);
  xhr.onload = function () {
    if (xhr.status === 200) {
      var response = JSON.parse(xhr.responseText);
      var result = response.result;
      document.getElementById("result").innerHTML = "Result: " + result;
    } else {
      console.log("Error:", xhr.statusText);
    }
  };
  xhr.onerror = function () {
    console.log("Error:", xhr.statusText);
  };
  xhr.send();
  }