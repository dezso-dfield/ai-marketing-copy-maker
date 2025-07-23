document.addEventListener('DOMContentLoaded', () => {
    const valueDrivenForm = document.getElementById('valueDrivenForm');
    const valueDrivenOutput = document.getElementById('valueDrivenOutput');
    const valueDrivenLoading = document.getElementById('valueDrivenLoading');
    const valueDrivenSubmitButton = valueDrivenForm.querySelector('button[type="submit"]');
    const valueDrivenLanguageSelect = document.getElementById('valueDrivenLanguage');

    const pasForm = document.getElementById('pasForm');
    const pasOutput = document.getElementById('pasOutput');
    const pasLoading = document.getElementById('pasLoading');
    const pasSubmitButton = pasForm.querySelector('button[type="submit"]');
    const pasLanguageSelect = document.getElementById('pasLanguage');

    const audienceProblemsForm = document.getElementById('audienceProblemsForm');
    const audienceOutput = document.getElementById('audienceOutput');
    const audienceLoading = document.getElementById('audienceLoading');
    const audienceSubmitButton = audienceProblemsForm.querySelector('button[type="submit"]');
    const audienceLanguageSelect = document.getElementById('audienceLanguage');

    function showLoading(spinnerElement, buttonElement) {
        spinnerElement.classList.remove('hidden');
        buttonElement.disabled = true;
        buttonElement.classList.add('opacity-70', 'cursor-not-allowed');
    }

    function hideLoading(spinnerElement, buttonElement) {
        spinnerElement.classList.add('hidden');
        buttonElement.disabled = false;
        buttonElement.classList.remove('opacity-70', 'cursor-not-allowed');
    }

    valueDrivenForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        showLoading(valueDrivenLoading, valueDrivenSubmitButton);
        valueDrivenOutput.textContent = 'Generating copy...';

        const formData = new FormData(valueDrivenForm);
        const data = Object.fromEntries(formData.entries());
        data.language = valueDrivenLanguageSelect.value;

        try {
            const response = await fetch('/generate_value_driven_copy', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            valueDrivenOutput.textContent = result.copy;
        } catch (error) {
            console.error('Error:', error);
            valueDrivenOutput.textContent = `Error: ${error.message}. Please try again.`;
        } finally {
            hideLoading(valueDrivenLoading, valueDrivenSubmitButton);
        }
    });

    pasForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        showLoading(pasLoading, pasSubmitButton);
        pasOutput.textContent = 'Generating copy...';

        const formData = new FormData(pasForm);
        const data = Object.fromEntries(formData.entries());
        data.language = pasLanguageSelect.value;

        try {
            const response = await fetch('/generate_pas_copy', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            pasOutput.textContent = result.copy;
        } catch (error) {
            console.error('Error:', error);
            pasOutput.textContent = `Error: ${error.message}. Please try again.`;
        } finally {
            hideLoading(pasLoading, pasSubmitButton);
        }
    });

    audienceProblemsForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        showLoading(audienceLoading, audienceSubmitButton);
        audienceOutput.textContent = 'Finding problems for your audience...';

        const formData = new FormData(audienceProblemsForm);
        const data = Object.fromEntries(formData.entries());
        data.language = audienceLanguageSelect.value;

        try {
            const response = await fetch('/generate_audience_problems', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            audienceOutput.textContent = result.problems;
        } catch (error) {
            console.error('Error:', error);
            audienceOutput.textContent = `Error: ${error.message}. Please try again.`;
        } finally {
            hideLoading(audienceLoading, audienceSubmitButton);
        }
    });
});
