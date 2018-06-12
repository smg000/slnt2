$(document).ready(function() {

        if(localStorage.getItem('popState') != 'shown'){
            setTimeout(function() {
                $("#subscriptionModal").modal();
            }, 3500);
        } localStorage.setItem('popState','shown');

});