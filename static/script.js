function callPredictAPI() {
    fetch('http://127.0.0.1:5000/predict', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            updateTableWithResults(data);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

function updateTableWithResults(results) {
    var tableBody = document.querySelector('#resultTable tbody');
    clearTable(tableBody);
    populateTable(tableBody, results);
}

function clearTable(tableBody) {
    tableBody.innerHTML = '';
}

function populateTable(tableBody, results) {
    for (var i = 0; i < results.length; i++) {
        var labels = results[i].labels;
        var text = results[i].text;
        var sentiment = results[i].sentiment;

        var newRow = tableBody.insertRow();
        var cell1 = newRow.insertCell(0);
        var cell2 = newRow.insertCell(1);
        var cell3 = newRow.insertCell(2);
        var cell4 = newRow.insertCell(3);
        var cell5 = newRow.insertCell(4);

        cell1.textContent = i + 1;

        // Tạo các phần văn bản với màu sắc tương ứng
        var coloredText = getColoredText(text, labels);
        cell2.innerHTML = coloredText;

        for (var j = 0; j < labels.length; j++) {
            var labelValue = labels[j][2];

            var labelRow = cell3.appendChild(document.createElement("div"));
            labelRow.textContent = labelValue.split("#")[0];

        }
        
        // Tạo các hàng nhỏ trong cột Labels
        for (var j = 0; j < labels.length; j++) {
            var labelValue = labels[j][2];
            var labelColor = getLabelColor(labelValue);

            var labelRow = cell4.appendChild(document.createElement("div"));
            labelRow.textContent = labelValue.split("#")[1];

            labelRow.style.color = labelColor;
        }

        labelRow = cell5.appendChild(document.createElement("div"));
        labelRow.textContent = sentiment;
        labelColor = getLabelColor(sentiment);
        labelRow.style.color = labelColor;
    }
}

function getColoredText(text, labels) {
    // Sắp xếp các nhãn theo vị trí để áp dụng màu sắc cho văn bản
    labels.sort((a, b) => a[0] - b[0]);

    var coloredText = "";
    var lastIndex = 0;

    // Tạo các phần văn bản với màu sắc tương ứng
    for (var i = 0; i < labels.length; i++) {
        var labelStart = labels[i][0];
        var labelEnd = labels[i][1];
        var labelValue = labels[i][2];
        var labelColor = getTextColor(labelValue);

        // Thêm văn bản trước nhãn
        coloredText += text.substring(lastIndex, labelStart);

        // Thêm nhãn với màu sắc
        coloredText += `<sub style="font-size: 0.7em; position: relative;top: -0.8em; color:${labelColor};">#${labelValue.split("#")[0]}</sub>
        <span style="color:${labelColor}">${text.substring(labelStart, labelEnd)}</span>`;

        lastIndex = labelEnd;
    }

    // Thêm phần còn lại của văn bản
    coloredText += text.substring(lastIndex);

    return coloredText;
}

function getLabelColor(labelValue) {
    var color;
    if (labelValue.includes("POS")) {
        color = "#40916c";
    } else if (labelValue.includes("NEG")) {
        color = "#ff5c8a";
    } else {
        color = "#827081";
    }
    return color;
}

function getTextColor(labelValue) {
    var color;
    if (labelValue.includes("SCREEN")) {
        color = "#52b788";
    } else if (labelValue.includes("CAMERA")) {
        color = "#0077b6";
    } else if (labelValue.includes("FEATURES")) {
        color = "#5a189a";
    } else if (labelValue.includes("BATTERY")) {
        color = "#40916c";
    } else if (labelValue.includes("PERFORMANCE")) {
        color = "#3772ff";
    } else if (labelValue.includes("STORAGE")) {
        color = "#ff9e00";
    } else if (labelValue.includes("DESIGN")) {
        color = "#7c6a0a";
    } else if (labelValue.includes("PRICE")) {
        color = "#ff7900";
    } else if (labelValue.includes("GENERAL")) {
        color = "#7f4f24";
    } else if (labelValue.includes("SER&ACC")) {
        color = "#9d4edd";
    }
    return color;
}

function startModelPrediction() {
    setInterval(callPredictAPI, 1000);
}

window.onload = startModelPrediction;

document.getElementById('runModelBtn').addEventListener('click', callPredictAPI);
