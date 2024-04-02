function(element,input){
document.getElementsByName("h-captcha-response").item(0).value=input;
document.getElementsByName("g-recaptcha-response").item(0).value=input;
}