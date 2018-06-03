$(document).ready(function() {

        if(localStorage.getItem('popState') != 'shown'){
            setTimeout(function() {
                $("#subscriptionModal").modal();
            }, 10000);
        } localStorage.setItem('popState','shown');

});