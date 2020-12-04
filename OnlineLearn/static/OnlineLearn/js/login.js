document.addEventListener("DOMContentLoaded", () => {
    pass_in = document.getElementById('pass-in');
    b_div = document.getElementById('t-password');
    hide_or = document.getElementById('hide-or');
    pass_in.onfocus = () => {
        b_div.classList.add('focussed')
    }
    pass_in.addEventListener('focusout',() => {
        b_div.classList.remove('focussed')
    })
    hide_or.onclick = () => {
        if (hide_or.dataset.true == 1){
            hide_or.dataset.true = 0;
            pass_in.type = 'text';
            hide_or.classList.remove('fa-eye');
            hide_or.classList.add('fa-eye-slash');
        }else{
            hide_or.dataset.true = 1;
            pass_in.type = 'password';
            hide_or.classList.remove('fa-eye-slash');
            hide_or.classList.add('fa-eye');
        }

    }
})
