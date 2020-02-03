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
                    <td><input id="checkbox${user.id}" type="checkbox" name="foo"/></td>
                    <td><input readonly="True" form="myForm" type="text" value="${user.id}"/></td>
                    <td><input id="nameInput${user.id}" form="myForm" type="text" value="${user.name}"/></td>
                    <td><input id="emailInput${user.id}" form="myForm" type="text" value="${user.email}"/></td>
                    <td> 
                    <button class="btn deleteBtn" data-id="${user.id}">Delete</button>
                    </td>
                    <td>
                    <button class="btn updateBtn" 
                    data-id="${user.id}">
                    Update
                    </button>
                    </td>
               </tr>`;
           });
           rows +=`<tr>
                        <td></td>
                        <td><input id="name_create" type="text" value=""/></td>
                        <td><input id="email_create" type="text" value=""/></td>
                   </tr>
                    `;
           $('#myTable').append(rows);
           $('.deleteBtn').each((i, element) =>{
               $(element).on('click', (e) => {
                   deleteUser($(element))
               })
           });
           $('.updateBtn').each((i, element) =>{
               $(element).on('click', (e) => {
                   updateUser($(element))
               })
           });

           $('.createBtn').on('click', function (e) {
               userName = document.getElementById('name_create').value;
               userEmail = document.getElementById('email_create').value;
               document.getElementById('email_create').value = "";
               document.getElementById('email_create').value = "";

                $.ajax({
                    url: `/users/create/`,
                    type:'POST',
                    data: {'name': userName, 'email': userEmail},
                    dataType: 'json',
                    success: function (data) {
                       let rows =``;
                       rows = `<tr>
                                    <td><input id="checkbox${data['id']}" type="checkbox" name="foo"/></td>
                                    <td><input readonly="True" form="myForm" type="text" value="${data['id']}"/></td>
                                    <td><input id="nameInput${data['id']}" form="myForm" type="text" value="${data['name']}"/></td>
                                    <td><input id="emailInput${data['id']}" form="myForm" type="text" value="${data['email']}"/></td>
                                    <td> 
                                    <button class="btn deleteBtn" data-id="${data['id']}">Delete</button>
                                    </td>
                                    <td>
                                    <button class="btn updateBtn" 
                                    data-id="${data['id']}">
                                    Update
                                    </button>
                                    </td>
                               </tr>`;
                       $('#myTable').append(rows);
                    }

                });
           });
           
           $(".sendBtn").on("click", function () {
               if(document.getElementById("loader").hidden == true)
               {
                   document.getElementById("loader").hidden = false;
               }
                sendEmail()
           });
       }
    });
});

function sendEmail() {
    let text = document.getElementById("textsend").value;
    $.ajax({
        url:'/users/send/',
        type:'POST',
        dataType:'json',
        data: {'text': text},
        success: function (response) {
             var taskUrl = `/users/task/${response.task_id}/`;
            var timer = setInterval(function() {
          axios.get(taskUrl)
          .then(function(response) {
            var taskStatus = response.data.task_status;
            if(taskStatus === "SUCCESS")
            {
                clearTimer("Message`s has been sent");
                alert(response.data.results)
            }
            else if (taskStatus === 'FAILURE') {
                clearTimer('An error occurred');
            }
          })
          .catch(function(err){
            console.log('err', err);
            clearTimer('An error occurred');
          });
            }, 800);

            function clearTimer(message) {
               document.getElementById("loader").hidden = true;
               clearInterval(timer);
               alert(message);
            }
        }
    });
}

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

function updateUser(element) {
    userId = $(element).data('id');
    userName = document.getElementById(`nameInput${userId}`).value;
    userEmail = document.getElementById(`emailInput${userId}`).value;
    $.ajax({
        url:`/users/update/${userId}`,
        type: 'POST',
        data: {'id': userId, 'name': userName, 'email': userEmail},
        dataType: 'json',
        success: function (data) {
            $(element).data('id').replaceWith(data['id']);
            $(element).data('name').replaceWith(data['name']);
            $(element).data('email').replaceWith(data['email']);
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
