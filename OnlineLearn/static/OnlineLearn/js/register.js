document.addEventListener("DOMContentLoaded", () => {
    pass_in = document.getElementById('pass-in');
    c_pass_in = document.getElementById('c-pass-in');
    b_div = document.getElementById('t-password');
    c_b_div = document.getElementById('c-t-password');
    hide_or = document.getElementById('hide-or');
    c_hide_or = document.getElementById('c-hide-or');
    p_message = document.getElementById('p-message');
    pass_in.onfocus = () => {
        b_div.classList.add('focussed')
    }
    pass_in.addEventListener('focusout',() => {
        b_div.classList.remove('focussed')
    })
    c_pass_in.onfocus = () => {
        c_b_div.classList.add('focussed')
    }
    c_pass_in.addEventListener('focusout',() => {
        c_b_div.classList.remove('focussed')
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
    c_hide_or.onclick = () => {
        if (c_hide_or.dataset.true == 1){
            c_hide_or.dataset.true = 0;
            c_pass_in.type = 'text';
            c_hide_or.classList.remove('fa-eye');
            c_hide_or.classList.add('fa-eye-slash');
        }else{
            c_hide_or.dataset.true = 1;
            c_pass_in.type = 'password';
            c_hide_or.classList.remove('fa-eye-slash');
            c_hide_or.classList.add('fa-eye');
        }
    }
})
