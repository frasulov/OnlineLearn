document.addEventListener("DOMContentLoaded", function(){
    tinymce.init({
    selector: 'textarea',
    menubar: false,
    plugins: 'bold italic link codesample linkchecker lists tinymcespellchecker',
    toolbar: 'spellchecker link codesample bold italic numlist bullist',
    setup: function (editor) {
      editor.on('init', function (e) {
        editor.setContent("");
      });
    },
    codesample_languages: [
    { text: 'HTML/XML', value: 'markup' },
    { text: 'JavaScript', value: 'javascript' },
    { text: 'CSS', value: 'css' },
    { text: 'PHP', value: 'php' },
    { text: 'Ruby', value: 'ruby' },
    { text: 'Python', value: 'python' },
    { text: 'Java', value: 'java' },
    { text: 'C', value: 'c' },
    { text: 'C#', value: 'csharp' },
    { text: 'C++', value: 'cpp' }
  ],
    toolbar_mode: 'floating',
    spellchecker_language: 'en',
    spellchecker_dialog: true,
    content_css: [
      '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
      '//www.tinymce.com/css/codepen.min.css']
  });
  buttons = document.querySelectorAll('.section-btn');
  buttons.forEach(button => {
      button.onclick = () => {
          button.childNodes[1].childNodes[3].childNodes[0].classList.toggle('fa-arrow-down')
          button.childNodes[1].childNodes[3].childNodes[0].classList.toggle('fa-arrow-up')
      }
  });

  getQuestion()
  document.getElementById('add-reply').onsubmit = () => {
      body = tinymce.get("tiny-question-body-add-reply").getContent();
      question_id = document.getElementById('add-reply').dataset.question;
      fetch(`/course/content/addanswer/${question_id}`,{
          method: 'POST',
          credentials: "same-origin",
          headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Accept": "application/json",
          'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              body:  body,
          })
      })
      .then(response => response.json())
      .then(result => {
          console.log(result)
          tinymce.get("tiny-question-body-add-reply").setContent("");
          createReply(result.answer)
          let numberOfreplies = document.querySelector('.hgjd span').innerHTML;
          numberOfreplies = parseInt(numberOfreplies)
          document.querySelector('.hgjd span').innerHTML = numberOfreplies+1;

      })
      return false;
  }

  document.getElementById('asknewquestion').onsubmit = () => {
      title = document.querySelector('#asknewquestion input').value
      body = tinymce.get("tiny-question-body").getContent();
      course_id = document.getElementById('qa').dataset.course;
      fetch(`/course/content/addquestion/${course_id}`,{
          method: 'POST',
          credentials: "same-origin",
          headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Accept": "application/json",
          'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              title: title,
              body:  body,
          })
      })
      .then(response => response.json())
      .then(result => {
          console.log(result)
          document.querySelector('#asknewquestion input').value = ''
          tinymce.get("tiny-question-body").setContent("");
          document.getElementById('all-questions').innerHTML = ''
          getQuestion()
          document.getElementById('askquestion').classList.add('d-none')
          document.getElementById('question-info').classList.add('d-none')
          document.getElementById('questions').classList.remove('d-none')
      })
      return false;
  }
  button_back = document.querySelector('#askquestion .zzz');
  button_back.onclick = () => {
      document.getElementById('all-questions').innerHTML = ''
      getQuestion()
      document.getElementById('askquestion').classList.add('d-none')
      document.getElementById('questions').classList.remove('d-none')
      document.getElementById('question-info').classList.add('d-none')

  }
  document.querySelector('#question-info .zzz').onclick = () => {
      document.getElementById('all-questions').innerHTML = ''
      getQuestion()
      document.getElementById('askquestion').classList.add('d-none')
      document.getElementById('questions').classList.remove('d-none')
      document.getElementById('question-info').classList.add('d-none')
  }
  document.getElementById('add-question').onclick = () => {
      document.getElementById('askquestion').classList.remove('d-none')
      document.getElementById('question-info').classList.add('d-none')
      document.getElementById('questions').classList.add('d-none')
  }
})
function getCookie(name) {
   var cookieValue = null;
   if (document.cookie && document.cookie !== '') {
       var cookies = document.cookie.split(';');
       for (var i = 0; i < cookies.length; i++) {
           var cookie = jQuery.trim(cookies[i]);
           // Does this cookie string begin with the name we want?
           if (cookie.substring(0, name.length + 1) === (name + '=')) {
               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
               break;
           }
       }
   }
   return cookieValue;
}

function getQuestion(){
   course = document.getElementById('qa').dataset.course;
   fetch(`/course/content/qa/${course}`)
   .then(respnse => respnse.json())
   .then(result => {
       document.getElementById('reply-number').innerHTML = result.qa.length
       result.qa.forEach(question => {
           createQuestion(question)
       })
   })
}

function createQuestion(question){
   const question_ = document.createElement('div')
   question_.classList.add('per-question')
   question_.onclick = () => {
       document.getElementById('askquestion').classList.add('d-none')
       document.getElementById('question-info').classList.remove('d-none')
       document.getElementById('questions').classList.add('d-none')
       document.querySelector('#question-info .question-title').innerHTML = question.title
       document.querySelector('#question-info .question-body').innerHTML = question.body
       document.querySelector('#question-info span').innerHTML = question.created
       document.querySelector('#question-info a').innerHTML = question.user.first_name;
       document.querySelector('#question-info a').href = `/profile/${question.user.email}`
       document.querySelector('#question-info .profile-text').innerHTML = `<img src="${question.user.image}" alt="">`
       document.querySelector('#question-info .hgjd').innerHTML = `<span>${question.answers.length}</span> replies`
       document.getElementById('add-reply').dataset.question = question.id
       document.getElementById('rreee').innerHTML = ''
       question.answers.forEach(answer => {
           createReply(answer)
       })

   }
   const row = document.createElement('div')
   row.classList.add('row')
   const col_1 = document.createElement('div')
   col_1.classList.add('col-1')
   const profile = document.createElement('div')
   profile.classList.add('profile-text')
   profile.innerHTML = `<img src="${question.user.image}" alt="">`
   col_1.append(profile)

   const col_11 = document.createElement('div')
   col_11.classList.add('col-11')

   const q_title = document.createElement('div')
   q_title.classList.add('question-title')
   if (question.title.length >= 80)
       q_title.innerHTML = `${question.title.substring(0,80)}...`
   else
       q_title.innerHTML = question.title;

   const q_body = document.createElement('div')
   q_body.classList.add('question-body')
   if (question.body.length >= 90)
       q_body.innerHTML = `${question.body.substring(0,90)}...`
   else
       q_body.innerHTML = question.body

   const awagi = document.createElement('div')
   awagi.classList.add('awagi')
   awagi.innerHTML = `<a class="to-profile" href="/profile/${question.user.email}">${question.user.first_name}</a>
           <button class="b-2">${question.answers.length}<i class="ml-1 fas fa-comments"></i></button>
           <span>${question.created}</span>`

   col_11.append(q_title)
   col_11.append(q_body)
   col_11.append(awagi)
   row.append(col_1)
   row.append(col_11)
   question_.append(row)
   document.getElementById('all-questions').append(question_)
}

function createReply(answer)
{
   console.log('show me please 1')
   const reply = document.createElement('div')
   reply.classList.add('replies')
   const row = document.createElement('div')
   row.classList.add('row')
   const col_1 = document.createElement('div')
   col_1.classList.add('col-1')
   const profile = document.createElement('div')
   profile.classList.add('profile-text')
   profile.style.width = '50px'
   profile.style.height = '50px'
   profile.innerHTML = `<img src="${answer.user.image}" alt="">`
   col_1.append(profile)
   const col_11 = document.createElement('div')
   col_11.classList.add('col-11')
   col_11.innerHTML = `<a href="/profile/${answer.user.email}" class="to-prof">${answer.user.first_name}</a>
       <p class="date">${answer.created}</p>
       <div class="per-reply">
       ${answer.body}
       </div>`
   row.append(col_1)
   row.append(col_11)
   reply.append(row)
   document.getElementById('rreee').append(reply)
}
