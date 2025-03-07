
document.addEventListener('DOMContentLoaded', function() {
    const optionButtons = document.querySelectorAll('.option-btn');
    if (optionButtons) {
        optionButtons.forEach(button => {
            button.addEventListener('mouseenter', function() {
            });
        });
    }
    
    setupLifelines();
});

function setupLifelines() {
    // Fifty-fifty lifeline
    const fiftyFiftyBtn = document.getElementById('fifty-fifty');
    if (fiftyFiftyBtn) {
        fiftyFiftyBtn.addEventListener('click', function() {
            if (!this.disabled) {
                useLifeline('fifty_fifty');
            }
        });
    }
     
}



function useLifeline(lifeline) {
    // Get CSRF token if needed
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
    
    fetch('/use_lifeline', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        },
        body: 'lifeline=' + lifeline
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const button = document.getElementById(lifeline.replace('_', '-'));
            if (button) {
                button.disabled = true;
                button.classList.add('opacity-50', 'cursor-not-allowed');
            }
            
            if (lifeline === 'fifty_fifty') {
                handleFiftyFifty(data.result.removed_options);
            } 
        } else {
            console.error('Error using lifeline:', data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function handleFiftyFifty(removedOptions) {
    const optionButtons = document.querySelectorAll('.option-btn');
    optionButtons.forEach(button => {
        if (removedOptions.includes(button.value)) {
            button.parentElement.classList.add('hidden');
        }
    });
}


