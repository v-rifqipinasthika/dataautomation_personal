function(element,input){
    document.getElementsByName("g-recaptcha-response").item(0).value=input;
    var button = document.getElementById('continue');
    button.click();
    //document.querySelector('form').submit();
}