function(element,input){
    document.getElementsByName("g-recaptcha-response").item(0).value=input;
    var button = document.getElementById('btnSbmt');
    button.click();
    //document.querySelector('form').submit();
}