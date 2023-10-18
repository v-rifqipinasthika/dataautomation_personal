function(element, input) {
    document.getElementById('actionDate').value = input;
    document.getElementById('endDate').value = input;
    document.getElementById('actionTimeStart').value = "00:00";
    document.getElementById('actionTimeStop').value = "23:59";
    return "done"
}