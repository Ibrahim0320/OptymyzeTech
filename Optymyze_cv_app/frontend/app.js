document.getElementById('upload-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    // Show the spinner
    const spinner = document.getElementById('spinner');
    spinner.style.display = 'block';

    // Estimate time
    const files = document.getElementById('files').files;
    const estimatedTime = Math.ceil((files.length / 10) * 5);
    document.getElementById('estimated-time').textContent = `Estimated processing time: ${estimatedTime} minute(s).`;

    const formData = new FormData();
    formData.append('job_description', document.getElementById('job_description').value);
    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
    }

    try {
        const response = await fetch('/evaluate', {
            method: 'POST',
            body: formData
        });

        // Hide the spinner once the response is received
        spinner.style.display = 'none';

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        if (result.error) {
            displayError(result.error);
        } else {
            window.location.href = `/results?zip_name=${result.zip_name}&result=${encodeURIComponent(result.result)}&chatgpt_report=${encodeURIComponent(result.chatgpt_report)}`;
        }
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        // Hide the spinner if there's an error
        spinner.style.display = 'none';
        displayError('There was a problem processing the CVs.');
    }
});

function displayError(error) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `<h2>Error:</h2><p>${error}</p>`;
}
