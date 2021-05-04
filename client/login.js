$(document).ready(function () {
    let loginBox = $('#login-box');
    let registerBox = $('#register-box');
    let errorBox = $('#error-box');    
    registerBox.hide();
    errorBox.hide();

    $('#login-button').click(function () {
        errorBox.show();
        loginBox.hide();
    });

    $('#register-button').click(function () {
        registerBox.show();
        loginBox.hide();
    });

    $('#go-to-register-button').click(function () {
        registerBox.show();
        loginBox.hide();
    });

    $('#go-to-login-button').click(function () {
        registerBox.hide();
        loginBox.show();
    });
    
});