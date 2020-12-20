document.addEventListener("DOMContentLoaded", () =>{
    let main = document.querySelector('.main');
    let inside = document.querySelector('.inside');
    let inside2 = document.querySelector('.double-inside');
    let text = document.querySelector('.ctgr-text');
    let input = document.querySelector('.search-box form input');
    let next = document.querySelector('.next');
    let toggle = document.querySelector('.toggler');
    let lis = document.querySelectorAll('.for-more-click');
    let second_side = document.querySelector('.second-side');
    let p_img = document.querySelector('.pp');
    let p_tho = document.querySelector('.profile-tho');
    let logged = document.querySelector('.s-first-logged');
    let search = document.getElementById('ss-result');
    let search_phone_btn = document.getElementById('s-phone-btn');
    let close_phone_btn = document.getElementById('close-phone');
    let search_phone = document.getElementById('search-phone');
    let s_r = document.querySelector('.search_phone_result');
    search_phone_btn.onclick = () => {
      search_phone.classList.remove('d-none');
    }
    close_phone_btn.onclick = () => {
      search_phone.classList.add('d-none');
    }

    document.getElementById('my-phone-input').addEventListener('input', () => {
      let val = document.getElementById('my-phone-input').value;
      s_r.classList.remove('d-none')
      if (val == ''){
        s_r.classList.add('d-none')
      }else{
        fetch(`/search/query/${val}`)
        .then(response => response.json())
        .then(result => {
            if (!result.error){
              document.getElementById('phone-res').innerHTML = ''
              result.queries.forEach(query => {
                li = document.createElement('li')
                li.classList.add('row')
                li.innerHTML = `<div class="col-1"><i class="fas fa-search"></i></div>
                <div class="col-11"><a class='s-result m-0 p-0' href='/search?q=${query}'>${query}</a></div>`;
                document.getElementById('phone-res').append(li)
              })
            }
        })
      }
    })

    input.addEventListener("input", () => {
        let val = input.value;
        next.classList.remove('d-none')
        if (val == ''){
          next.classList.add('d-none')
        }else{
          fetch(`/search/query/${val}`)
          .then(response => response.json())
          .then(result => {
              if (!result.error){
                search.innerHTML = ''
                result.queries.forEach(query => {
                  li = document.createElement('li')
                  li.innerHTML = `<i class="fas fa-search"></i><a class='s-result' href='/search?q=${query}'>${query}</a>`;
                  search.append(li)
                })
              }
          })
        }
    })
    document.addEventListener('click', (e) => {
      if (e.target != next && e.target != input){
        next.classList.add('d-none')
      }
      if (e.target != s_r){
        s_r.classList.add('d-none')
      }
    })
    main.onmouseover = () => {
        inside.classList.remove('d-none');
        text.classList.add('toblue');
        inside.style.animationPlayState = 'running'
    }
    main.onmouseout = () => {
        inside.classList.add('d-none');
        text.classList.remove('toblue');
    }
    inside.onmouseover = () => {
        inside2.classList.remove('d-none');
        inside2.style.animationPlayState = 'running'

    }
    inside.onmouseout = () => {
        inside2.classList.add('d-none');

    }
    if (p_img){
        p_img.onmouseover = () => {
            p_tho.classList.remove('d-none');
            p_tho.style.animationPlayState = 'running'

        }
        p_img.onmouseout = () => {
            p_tho.classList.add('d-none');

        }
    }
    lis.forEach(li => {
        li.onclick = () => {
            fetch(`/category/${li.dataset.categoryid}`)
            .then(response => response.json())
            .then(result => {
                sub_ul = document.getElementById('category');
                sub_ul.innerHTML = ''
                li = document.createElement('li')
                li.id = 'mobile-firstone'
                li.innerHTML = result.category
                sub_ul.append(li)
                result.subcategories.forEach(category => {
                    li = document.createElement('li')
                    li.innerHTML = `<a href="/search?q=${category.text}">${category.text}</a>`
                    sub_ul.append(li)
                })
            })
            second_side.style.animationPlayState = 'running'
            setTimeout(() => {
              second_side.style.animationPlayState = 'paused'
            }, 1000)
            second_side.classList.remove('d-none');
            document.getElementById('category').classList.remove('d-none')
        }
    })
    document.getElementById('back').onclick = () => {
        second_side.style.animationPlayState = 'running'
        setTimeout(() => {
          second_side.classList.add('d-none');
          document.getElementById('category').classList.add('d-none')
          document.getElementById('profile').classList.add('d-none')
        }, 1000)

    }
    if (logged){
    logged.onclick = () => {
        second_side.style.animationPlayState = 'running'
        setTimeout(() => {
          second_side.style.animationPlayState = 'paused'
        }, 1000)
        second_side.classList.remove('d-none');
        document.getElementById('profile').classList.remove('d-none')
    }
}
    top_categories = document.querySelectorAll('#first-categories li');
    top_categories.forEach(category => {
        category.onmouseover = () => {
            fetch(`/category/${category.dataset.categoryid}`)
            .then(response => response.json())
            .then(result => {
                sub_ul = document.getElementById('fetching-sub-category');
                sub_ul.innerHTML = ''
                li = document.createElement('li')
                li.id = 'firstone'
                li.innerHTML = result.category
                sub_ul.append(li)
                result.subcategories.forEach(category => {
                    console.log(category)
                    li = document.createElement('li')
                    li.innerHTML = `<a href="/search?q=${category.text}">${category.text}</a>`
                    sub_ul.append(li)
                })
            })
        }

    })
    let mynav = document.getElementById('my-nav');
    let scroll_position = 0;
    let scroll_direction;

    window.addEventListener('scroll', function(e){
        scroll_direction = (document.body.getBoundingClientRect()).top > scroll_position ? 'up' : 'down';
        scroll_position = (document.body.getBoundingClientRect()).top;
        if (scroll_direction == 'up'){
            mynav.classList.add('sticky-top')
        }else{
            mynav.classList.remove('sticky-top')
        }
    });
})


function sidebarCC(){
    $('.ui')
    .sidebar('setting', 'transition', 'overlay')
    .sidebar('toggle');
}
