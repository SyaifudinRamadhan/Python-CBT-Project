$(document).ready(function(){
        $('#pagination').after('<div id="nav" class="btn-group"></div>');
        var currPage = 0;
        var rowsShown = parseInt($('#num_shown').val());
        var rowsTotal = $('#data tbody tr').length;
        var numPages = rowsTotal/rowsShown;
        $('#nav').append('<button class="btn btn-outline-primary" rel="-1">Prev</button> ');
        for(i = 0;i < numPages;i++) {
            var pageNum = i + 1;
            $('#nav').append('<button class="btn btn-outline-primary" id="pag'+i+'" rel="'+i+'">'+pageNum+'</button> ');
        }
        $('#nav').append('<button class="btn btn-outline-primary" rel="-2">Next</button> ');
        $('#data tbody tr').hide();
        $('#data tbody tr').slice(0, rowsShown).show();
        $("button[rel="+0+"]").addClass('active');
        $('#inf').append("Showing "+(rowsTotal).toString()+" of "+parseInt(rowsShown).toString()+" entries")
        $('#nav button').bind('click', function(){
             console.log("Lama : "+currPage);
            if (parseInt($(this).attr('rel')) == (-1)){
               if (currPage > 0){
                 currPage = currPage-1;
                 }
                else{
                    currPage = currPage+0;
                 }
                 $('#nav button').removeClass('active');
                 $("button[rel="+currPage+"]").addClass('active');
            }else if (parseInt($(this).attr('rel')) == (-2)){
                if (currPage >= 0 && currPage < (numPages-1)){
                 currPage = currPage+1;
                 }
                else{
                    currPage = currPage+0;
                 }
                 $('#nav button').removeClass('active');
                 $("button[rel="+currPage+"]").addClass('active');
            }else{
                currPage = parseInt($(this).attr('rel'));
                $('#nav button').removeClass('active');
                $(this).addClass('active');
            }
            
            console.log("Baru : "+currPage);
            var startItem = currPage * rowsShown;
            var endItem = startItem + rowsShown;
            $('#data tbody tr').css('opacity','0.0').hide().slice(startItem, endItem).
                    css('display','table-row').animate({opacity:1}, 300);
        });
    });