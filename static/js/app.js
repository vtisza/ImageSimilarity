$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip(); 
    // Add smooth scrolling to all links in navbar + footer link
    $(".navbar a, footer a[href='#top'], .container-fluid a[href='#third']").on('click', function(event) {
    // Make sure this.hash has a value before overriding default behavior
    if (this.hash !== "") {
      // Prevent default anchor click behavior
      event.preventDefault();
      // Store hash
      var hash = this.hash;
      // Using jQuery's animate() method to add smooth page scroll
      // The optional number (900) specifies the number of milliseconds it takes to scroll to the specified area
      $('html, body').animate({
        scrollTop: $(hash).offset().top
      }, 900, function(){
        // Add hash (#) to URL when done scrolling (default click behavior)
        window.location.hash = hash;
        });
      } // End if 
    });
    
    
    // Add onclick event
    $('#uploader').on('change', function() {
      var file_data = $('#uploader').prop('files')[0];   
      var form_data = new FormData();                  
      form_data.append('file', file_data);                             
      $.ajax({
                  url: './assessment', // point to server-side PHP script 
                  dataType: 'json',  // what to expect back from the PHP script, if anything
                  cache: false,
                  contentType: false,
                  processData: false,
                  data: form_data,                         
                  type: 'post',
                  success: function(response){
                      $("#simi1").attr('src', response.images[0]);
                      $("#simi2").attr('src', response.images[1]);
                      $("#simi3").attr('src', response.images[2]);
                      $("#simi4").attr('src', response.images[3]);
                      $("#simi5").attr('src', response.images[4]);
                      $("#simi6").attr('src', response.images[5]);

                      $('html, body').animate({
                        scrollTop: $("#third").offset().top
                    }, 2000);
                  }
       });
  });
    
    
  })