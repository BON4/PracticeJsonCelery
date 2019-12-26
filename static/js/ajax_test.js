/*
$(document).ready(function () {
   $("#about-btn").click(function () {
       $.ajax({
           type: 'GET',
           async: true,
           url: 'task/',
          success: function (data) {
              $("#text-info").html(data['number']);
           },
           dataType: 'json',
       });
   });
});*/
$(document).ready(function () {
    $.ajax({
       url: '/users/list',
       type: 'GET',
        headers: { "X-CSRFToken": getCookie("csrftoken") },
       dataType: 'json',
       success: function (data) {
           let rows = ``;
           data.forEach(user =>{
               rows += `
               <tr>
                    <td>${user.id}</td>
                    <td>${user.name}</td>
                    <td>${user.email}</td>
                    <td>
                    <button class="btn deleteBtn" data-id="${user.id}">Delete</button>
                    </td>
                    <td>
                    <button class="btn updateBtn" data-id="${user.id}">Update</button>
                    </td>
               </tr>`;
           });
           $('#myTable').append(rows);
           $('.deleteBtn').each((i, element) =>{
               $(element).on('click', (e) => {
                   deleteUser($(element))
               })
           })
       }
    });
});

function deleteUser(element) {
    userId = $(element).data('id');
    $.ajax({
        url:`/users/delete/${userId}`,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            $(element).parents()[1].remove()
        }
    });
}

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }