

var numberofItems= $("#loop .list-group").length;

var limitPerPage = 10;

$("#loop .list-group:gt(" + (limitPerPage-1) + ") ").hide();

var totalPages = Math.round(numberofItems / limitPerPage);

$('.pagination').append("<li class='current-page active'><a class='page-link' href='javascript:void(0)'>" + 1 + "</a></li>");

for (var i=2; i<= totalPages; i++){
    $('.pagination').append("<li class='current-page' ><a  class='page-link' href='javascript:void(0)'>" + i + "</a></li>");
}

$('.pagination').append("<li class='page-item' id ='next-page'><a class='page-link' href='javascript:void(0)' aria-label='Next'><span aria-hidden='true'>&raquo;</span></a></li>");

$(".pagination li.current-page").on("click",function (){
    if($(this).hasClass("active")){
        return false;
    }
    else{
        
        var currentPage = $(this).index();
        $(".pagination li").removeClass("active");
        $(this).addClass("active");
        $("#loop .list-group").hide();

        var grandTotal = limitPerPage * currentPage;
        for (var i = grandTotal - limitPerPage; i < grandTotal; i++){
            $("#loop .list-group:eq(" + i + ") ").show();
        }
    }
});

$("#next-page").on("click", function() {
    var currentPage = $(".pagination li.active").index();
    if (currentPage == totalPages){
        return false;
    } else {
        currentPage++;
        $(".pagination li").removeClass("active");
        $("#loop .list-group").hide();

        var grandTotal = limitPerPage * currentPage;

        for (var i = grandTotal - limitPerPage; i < grandTotal; i++){
            $("#loop .list-group:eq(" + i + ") ").show();
        }
        $(".pagination li.current-page:eq(" + (currentPage - 1) + ")").addClass("active");
    }
});

$("#previous-page").on("click", function() {
    var currentPage = $(".pagination li.active").index(); // Identify the current active page
    // Check to make sure that users is not on page 1 and attempting to navigating to a previous page
    if (currentPage === 1) {
      return false; // Return false (i.e., cannot navigate to a previous page because the current page is page 1)
    } else {
      currentPage--; // Decrement page by one
      $(".pagination li").removeClass('active'); // Remove the 'activate' status class from the previous active page number
      $("#loop .list-group").hide(); // Hide all items in the pagination loop
      var grandTotal = limitPerPage * currentPage; // Get the total number of items up to the page that was selected
  
      // Loop through total items, selecting a new set of items based on page number
      for (var i = grandTotal - limitPerPage; i < grandTotal; i++) {
        $("#loop .list-group:eq(" + i + ")").show(); // Show items from the new page that was selected
      }
  
      $(".pagination li.current-page:eq(" + (currentPage - 1) + ")").addClass('active'); // Make new page number the 'active' page
    }
  });