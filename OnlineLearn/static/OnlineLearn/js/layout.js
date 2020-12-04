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
    input.addEventListener("input", () => {
        next.classList.remove('d-none')
    })
    input.addEventListener('focusout', () => {
        next.classList.add('d-none')
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
    p_img.onmouseover = () => {
        p_tho.classList.remove('d-none');
        p_tho.style.animationPlayState = 'running'

    }
    p_img.onmouseout = () => {
        p_tho.classList.add('d-none');

    }
    lis.forEach(li => {
        li.onclick = () => {
            // fetch data
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

    document.querySelector('.s-first-logged').onclick = () => {
        second_side.style.animationPlayState = 'running'
        setTimeout(() => {
          second_side.style.animationPlayState = 'paused'
        }, 1000)
        second_side.classList.remove('d-none');
        document.getElementById('profile').classList.remove('d-none')
    }
})


function sidebarCC(){
    $('.ui')
    .sidebar('setting', 'transition', 'overlay')
    .sidebar('toggle');
}
