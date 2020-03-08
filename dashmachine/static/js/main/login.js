$( document ).ready(function() {
   $(".login-form").on('submit', function(e) {
       e.preventDefault();
       $.ajax({
           url: $(this).attr('data-url'),
           type: 'POST',
           data: $(this).serialize(),
           success: function(data){
               if (data.data.err){
                   M.toast({html: data.data.err, classes: 'theme-warning'})
               } else {
                   $(location).attr('href', data.data.url)
               }
           }
       });
   });
});