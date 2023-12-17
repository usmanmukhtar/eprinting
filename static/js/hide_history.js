const submitButton = Array.from(document.querySelectorAll('a')).find(button => button.textContent === 'History');
if (submitButton) {
//     set display none to the submit button
    submitButton.style.display = 'none';
}


function debounce(func, wait) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            func(...args);
        }, wait);
    };
}


const searchInput = document.querySelector("input[name='q']");
if (searchInput) {
    searchInput.addEventListener("input", debounce(function () {
        try {
            document.forms[0].submit();
        } catch (error) {
            // Do nothing if an error occurs
        }
    }, 500));
}



